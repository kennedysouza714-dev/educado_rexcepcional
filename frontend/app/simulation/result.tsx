import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
  Share,
  Platform,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useColors } from '../../src/hooks/useColors';
import { Button } from '../../src/components/Button';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { simulationAPI } from '../../src/services/api';
import Animated, { useSharedValue, useAnimatedStyle, withTiming, withDelay, withSpring } from 'react-native-reanimated';

interface SimulationResult {
  id: string;
  score: number;
  correct_answers: number;
  total_questions: number;
  passed: boolean;
  time_taken_seconds: number;
  answers_review?: Array<{
    question_id: string;
    questao: string;
    modulo: string;
    selected_option: string;
    correct_answer: string;
    is_correct: boolean;
    comentario: string;
    alternativas: Record<string, string>;
  }>;
}

const moduleNames: Record<string, string> = {
  '1': 'Placas', '2': 'Escolhas', '3': 'Segurança', '4': 'Preservar',
};

export default function SimulationResultScreen() {
  const router = useRouter();
  const colors = useColors();
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [showReview, setShowReview] = useState(false);

  // Animations
  const scoreScale = useSharedValue(0);
  const statsOpacity = useSharedValue(0);
  const chartOpacity = useSharedValue(0);

  const scoreAnimStyle = useAnimatedStyle(() => ({
    transform: [{ scale: scoreScale.value }],
  }));
  const statsAnimStyle = useAnimatedStyle(() => ({
    opacity: statsOpacity.value,
    transform: [{ translateY: (1 - statsOpacity.value) * 20 }],
  }));
  const chartAnimStyle = useAnimatedStyle(() => ({
    opacity: chartOpacity.value,
  }));

  useEffect(() => {
    submitSimulation();
  }, []);

  const startAnimations = () => {
    scoreScale.value = withSpring(1, { damping: 8 });
    statsOpacity.value = withDelay(300, withTiming(1, { duration: 500 }));
    chartOpacity.value = withDelay(600, withTiming(1, { duration: 500 }));
  };

  const submitSimulation = async () => {
    try {
      const answersJson = await AsyncStorage.getItem('simulation_answers');
      const timeTakenStr = await AsyncStorage.getItem('simulation_time_taken');
      if (!answersJson) {
        Alert.alert('Erro', 'Dados não encontrados');
        router.replace('/(tabs)/home');
        return;
      }
      const answers = JSON.parse(answersJson);
      const timeTaken = parseInt(timeTakenStr || '0', 10);
      const response = await simulationAPI.submit(answers, timeTaken);
      setResult(response);
      await AsyncStorage.multiRemove([
        'simulation_questions', 'simulation_answers', 'simulation_start_time',
        'simulation_current_index', 'simulation_time_taken', 'simulation_time_limit',
        'simulation_total',
      ]);
      startAnimations();
    } catch (error: any) {
      console.error('Error submitting:', error);
      Alert.alert('Erro', 'Erro ao enviar resultado');
      router.replace('/(tabs)/home');
    } finally {
      setLoading(false);
    }
  };

  const handleShare = async () => {
    if (!result) return;
    const message = `🚗 Educador Excepcional\n\n${result.passed ? '✅ APROVADO!' : '❌ Reprovado'}\n📊 Nota: ${result.score.toFixed(0)}%\n✏️ Acertos: ${result.correct_answers}/${result.total_questions}\n⏱ Tempo: ${formatTime(result.time_taken_seconds)}\n\nEstude com o Educador Excepcional!`;
    try {
      await Share.share({ message });
    } catch (e) {
      console.error('Share error:', e);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
  };

  // Calculate module-level stats from answers_review
  const getModuleBreakdown = () => {
    if (!result?.answers_review) return {};
    const breakdown: Record<string, { correct: number; total: number }> = {};
    for (const answer of result.answers_review) {
      const mod = answer.modulo || '?';
      if (!breakdown[mod]) breakdown[mod] = { correct: 0, total: 0 };
      breakdown[mod].total++;
      if (answer.is_correct) breakdown[mod].correct++;
    }
    return breakdown;
  };

  if (loading) {
    return (
      <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={[styles.loadingText, { color: colors.textSecondary }]}>Calculando resultado...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!result) return null;

  const moduleBreakdown = getModuleBreakdown();

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView contentContainerStyle={styles.content}>
        {!showReview ? (
          <>
            {/* Score */}
            <Animated.View style={[styles.resultCard, scoreAnimStyle]}>
              <Text style={styles.resultEmoji}>{result.passed ? '🎉' : '💪'}</Text>
              <Text style={[styles.resultTitle, { color: result.passed ? colors.success : colors.error }]}>
                {result.passed ? 'Aprovado!' : 'Reprovado'}
              </Text>
              <Text style={[styles.resultSubtitle, { color: colors.textSecondary }]}>
                {result.passed ? 'Parabéns! Você passou!' : 'Continue estudando!'}
              </Text>
            </Animated.View>

            {/* Stats */}
            <Animated.View style={[styles.statsCard, { backgroundColor: colors.card }, statsAnimStyle]}>
              <View style={[styles.scoreContainer, { borderBottomColor: colors.gray200 }]}>
                <Text style={[styles.scoreValue, { color: result.passed ? colors.success : colors.error }]}>
                  {result.score.toFixed(0)}%
                </Text>
                <Text style={[styles.scoreLabel, { color: colors.textSecondary }]}>Pontuação</Text>
              </View>
              <View style={styles.statsGrid}>
                <View style={styles.statItem}>
                  <Text style={[styles.statValue, { color: colors.text }]}>
                    {result.correct_answers}/{result.total_questions}
                  </Text>
                  <Text style={[styles.statLabel, { color: colors.textSecondary }]}>Acertos</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={[styles.statValue, { color: colors.text }]}>{formatTime(result.time_taken_seconds)}</Text>
                  <Text style={[styles.statLabel, { color: colors.textSecondary }]}>Tempo</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={[styles.statValue, { color: colors.text }]}>70%</Text>
                  <Text style={[styles.statLabel, { color: colors.textSecondary }]}>Mínimo</Text>
                </View>
              </View>
            </Animated.View>

            {/* Module Breakdown Chart (Melhoria 7) */}
            <Animated.View style={[styles.chartCard, { backgroundColor: colors.card }, chartAnimStyle]}>
              <Text style={[styles.chartTitle, { color: colors.text }]}>Desempenho por Módulo</Text>
              {Object.entries(moduleBreakdown).sort(([a], [b]) => a.localeCompare(b)).map(([mod, data]) => {
                const pct = data.total > 0 ? Math.round((data.correct / data.total) * 100) : 0;
                const barColor = pct >= 70 ? colors.success : pct >= 50 ? colors.warning : colors.error;
                return (
                  <View key={mod} style={styles.chartRow}>
                    <Text style={[styles.chartLabel, { color: colors.text }]}>
                      M{mod}
                    </Text>
                    <View style={[styles.chartBarBg, { backgroundColor: colors.gray200 }]}>
                      <View style={[styles.chartBarFill, { width: `${pct}%`, backgroundColor: barColor }]} />
                    </View>
                    <Text style={[styles.chartValue, { color: barColor }]}>
                      {data.correct}/{data.total}
                    </Text>
                  </View>
                );
              })}
            </Animated.View>

            {/* Actions */}
            <View style={styles.actions}>
              <Button
                title="📤 Compartilhar Resultado"
                onPress={handleShare}
                variant="outline"
                size="large"
                style={styles.actionButton}
              />
              <Button
                title="📝 Ver Revisão"
                onPress={() => setShowReview(true)}
                variant="outline"
                size="large"
                style={styles.actionButton}
              />
              <Button
                title="🔄 Novo Simulado"
                onPress={() => router.replace('/simulation')}
                size="large"
                style={styles.actionButton}
              />
              <Button
                title="🏠 Voltar ao Início"
                onPress={() => router.replace('/(tabs)/home')}
                variant="secondary"
                size="large"
                style={styles.actionButton}
              />
            </View>
          </>
        ) : (
          <>
            <View style={styles.reviewHeader}>
              <Text style={[styles.reviewTitle, { color: colors.text }]}>Revisão</Text>
              <Button title="Voltar" onPress={() => setShowReview(false)} variant="outline" size="small" />
            </View>
            {result.answers_review?.map((answer, index) => (
              <View key={answer.question_id} style={[
                styles.reviewCard, { backgroundColor: colors.card },
                { borderLeftColor: answer.is_correct ? colors.success : colors.error },
              ]}>
                <View style={styles.reviewCardHeader}>
                  <Text style={[styles.reviewIndex, { color: colors.textSecondary }]}>Q{index + 1} • M{answer.modulo}</Text>
                  <Text style={[styles.reviewStatus, { color: answer.is_correct ? colors.success : colors.error }]}>
                    {answer.is_correct ? '✓' : '✗'}
                  </Text>
                </View>
                <Text style={[styles.reviewQuestion, { color: colors.text }]}>{answer.questao}</Text>
                <View style={styles.reviewAnswers}>
                  <Text style={[styles.reviewAnswerLabel, { color: colors.textSecondary }]}>
                    Sua: <Text style={{ color: answer.is_correct ? colors.success : colors.error, fontWeight: '600' }}>{answer.selected_option} - {answer.alternativas[answer.selected_option]}</Text>
                  </Text>
                  {!answer.is_correct && (
                    <Text style={[styles.reviewAnswerLabel, { color: colors.textSecondary }]}>
                      Correta: <Text style={{ color: colors.success, fontWeight: '600' }}>{answer.correct_answer} - {answer.alternativas[answer.correct_answer]}</Text>
                    </Text>
                  )}
                </View>
                <View style={[styles.reviewComment, { backgroundColor: colors.gray100 }]}>
                  <Text style={[styles.reviewCommentText, { color: colors.text }]}>{answer.comentario}</Text>
                </View>
              </View>
            ))}
            <Button title="🏠 Voltar ao Início" onPress={() => router.replace('/(tabs)/home')} size="large" style={{ marginTop: 20 }} />
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  loadingText: { marginTop: 16, fontSize: 16 },
  content: { padding: 20 },
  resultCard: { alignItems: 'center', marginBottom: 24 },
  resultEmoji: { fontSize: 80, marginBottom: 16 },
  resultTitle: { fontSize: 32, fontWeight: 'bold', marginBottom: 8 },
  resultSubtitle: { fontSize: 16, textAlign: 'center' },
  statsCard: { borderRadius: 20, padding: 24, marginBottom: 20 },
  scoreContainer: { alignItems: 'center', marginBottom: 24, paddingBottom: 24, borderBottomWidth: 1 },
  scoreValue: { fontSize: 64, fontWeight: 'bold' },
  scoreLabel: { fontSize: 16 },
  statsGrid: { flexDirection: 'row', justifyContent: 'space-around' },
  statItem: { alignItems: 'center' },
  statValue: { fontSize: 24, fontWeight: 'bold' },
  statLabel: { fontSize: 12, marginTop: 4 },
  // Chart (Melhoria 7)
  chartCard: { borderRadius: 16, padding: 20, marginBottom: 20 },
  chartTitle: { fontSize: 16, fontWeight: '700', marginBottom: 16 },
  chartRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 12 },
  chartLabel: { width: 32, fontSize: 13, fontWeight: '600' },
  chartBarBg: { flex: 1, height: 12, borderRadius: 6, marginHorizontal: 10 },
  chartBarFill: { height: '100%', borderRadius: 6 },
  chartValue: { width: 40, fontSize: 12, fontWeight: '600', textAlign: 'right' },
  // Actions
  actions: { gap: 12 },
  actionButton: { width: '100%' },
  // Review
  reviewHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 },
  reviewTitle: { fontSize: 20, fontWeight: 'bold' },
  reviewCard: { borderRadius: 16, padding: 16, marginBottom: 12, borderLeftWidth: 4 },
  reviewCardHeader: { flexDirection: 'row', justifyContent: 'space-between', marginBottom: 10 },
  reviewIndex: { fontSize: 12, fontWeight: '600' },
  reviewStatus: { fontSize: 16, fontWeight: '700' },
  reviewQuestion: { fontSize: 15, marginBottom: 12, lineHeight: 22 },
  reviewAnswers: { marginBottom: 10 },
  reviewAnswerLabel: { fontSize: 13, marginBottom: 4, lineHeight: 20 },
  reviewComment: { padding: 12, borderRadius: 8 },
  reviewCommentText: { fontSize: 13, lineHeight: 20 },
});
