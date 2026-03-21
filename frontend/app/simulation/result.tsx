import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  ActivityIndicator,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useColors } from '../../src/hooks/useColors';
import { Button } from '../../src/components/Button';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { simulationAPI } from '../../src/services/api';

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
    selected_option: string;
    correct_answer: string;
    is_correct: boolean;
    comentario: string;
    alternativas: Record<string, string>;
  }>;
}

export default function SimulationResultScreen() {
  const router = useRouter();
  const colors = useColors();
  const [result, setResult] = useState<SimulationResult | null>(null);
  const [loading, setLoading] = useState(true);
  const [showReview, setShowReview] = useState(false);

  useEffect(() => {
    submitSimulation();
  }, []);

  const submitSimulation = async () => {
    try {
      const answersJson = await AsyncStorage.getItem('simulation_answers');
      const timeTakenStr = await AsyncStorage.getItem('simulation_time_taken');
      if (!answersJson) {
        Alert.alert('Erro', 'Dados do simulado não encontrados');
        router.replace('/(tabs)/home');
        return;
      }
      const answers = JSON.parse(answersJson);
      const timeTaken = parseInt(timeTakenStr || '0', 10);
      const response = await simulationAPI.submit(answers, timeTaken);
      setResult(response);
      await AsyncStorage.multiRemove([
        'simulation_questions',
        'simulation_answers',
        'simulation_start_time',
        'simulation_current_index',
        'simulation_time_taken',
      ]);
    } catch (error: any) {
      console.error('Error submitting simulation:', error);
      Alert.alert('Erro', 'Erro ao enviar resultado do simulado');
      router.replace('/(tabs)/home');
    } finally {
      setLoading(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}m ${secs}s`;
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

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView contentContainerStyle={styles.content}>
        {!showReview ? (
          <>
            <View style={styles.resultCard}>
              <Text style={styles.resultEmoji}>
                {result.passed ? '🎉' : '💪'}
              </Text>
              <Text style={[
                styles.resultTitle,
                { color: result.passed ? colors.success : colors.error }
              ]}>
                {result.passed ? 'Aprovado!' : 'Reprovado'}
              </Text>
              <Text style={[styles.resultSubtitle, { color: colors.textSecondary }]}>
                {result.passed 
                  ? 'Parabéns! Você passou no simulado!'
                  : 'Não desista! Continue estudando!'}
              </Text>
            </View>

            <View style={[styles.statsCard, { backgroundColor: colors.card }]}>
              <View style={[styles.scoreContainer, { borderBottomColor: colors.gray200 }]}>
                <Text style={[
                  styles.scoreValue,
                  { color: result.passed ? colors.success : colors.error }
                ]}>
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
                  <Text style={[styles.statValue, { color: colors.text }]}>
                    {formatTime(result.time_taken_seconds)}
                  </Text>
                  <Text style={[styles.statLabel, { color: colors.textSecondary }]}>Tempo</Text>
                </View>
                <View style={styles.statItem}>
                  <Text style={[styles.statValue, { color: colors.text }]}>70%</Text>
                  <Text style={[styles.statLabel, { color: colors.textSecondary }]}>Mínimo</Text>
                </View>
              </View>
            </View>

            <View style={styles.actions}>
              <Button
                title="Ver Revisão"
                onPress={() => setShowReview(true)}
                variant="outline"
                size="large"
                style={styles.actionButton}
              />
              <Button
                title="Novo Simulado"
                onPress={() => router.replace('/simulation')}
                size="large"
                style={styles.actionButton}
              />
              <Button
                title="Voltar ao Início"
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
              <Text style={[styles.reviewTitle, { color: colors.text }]}>Revisão das Questões</Text>
              <Button
                title="Voltar"
                onPress={() => setShowReview(false)}
                variant="outline"
                size="small"
              />
            </View>

            {result.answers_review?.map((answer, index) => (
              <View 
                key={answer.question_id} 
                style={[
                  styles.reviewCard,
                  { backgroundColor: colors.card },
                  answer.is_correct 
                    ? { borderLeftColor: colors.success }
                    : { borderLeftColor: colors.error }
                ]}
              >
                <View style={styles.reviewCardHeader}>
                  <Text style={[styles.reviewIndex, { color: colors.textSecondary }]}>Questão {index + 1}</Text>
                  <Text style={[
                    styles.reviewStatus,
                    { color: answer.is_correct ? colors.success : colors.error }
                  ]}>
                    {answer.is_correct ? '✓ Correta' : '✗ Incorreta'}
                  </Text>
                </View>
                
                <Text style={[styles.reviewQuestion, { color: colors.text }]}>{answer.questao}</Text>
                
                <View style={styles.reviewAnswers}>
                  <Text style={[styles.reviewAnswerLabel, { color: colors.textSecondary }]}>
                    Sua resposta: <Text style={[
                      styles.reviewAnswerValue,
                      { color: answer.is_correct ? colors.success : colors.error }
                    ]}>{answer.selected_option}</Text>
                  </Text>
                  {!answer.is_correct && (
                    <Text style={[styles.reviewAnswerLabel, { color: colors.textSecondary }]}>
                      Resposta correta: <Text style={[
                        styles.reviewAnswerValue,
                        { color: colors.success }
                      ]}>{answer.correct_answer}</Text>
                    </Text>
                  )}
                </View>
                
                <View style={[styles.reviewComment, { backgroundColor: colors.gray100 }]}>
                  <Text style={[styles.reviewCommentLabel, { color: colors.textSecondary }]}>Comentário:</Text>
                  <Text style={[styles.reviewCommentText, { color: colors.text }]}>{answer.comentario}</Text>
                </View>
              </View>
            ))}

            <Button
              title="Voltar ao Início"
              onPress={() => router.replace('/(tabs)/home')}
              size="large"
              style={{ marginTop: 20 }}
            />
          </>
        )}
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
  },
  content: {
    padding: 20,
  },
  resultCard: {
    alignItems: 'center',
    marginBottom: 24,
  },
  resultEmoji: {
    fontSize: 80,
    marginBottom: 16,
  },
  resultTitle: {
    fontSize: 32,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  resultSubtitle: {
    fontSize: 16,
    textAlign: 'center',
  },
  statsCard: {
    borderRadius: 20,
    padding: 24,
    marginBottom: 24,
  },
  scoreContainer: {
    alignItems: 'center',
    marginBottom: 24,
    paddingBottom: 24,
    borderBottomWidth: 1,
  },
  scoreValue: {
    fontSize: 64,
    fontWeight: 'bold',
  },
  scoreLabel: {
    fontSize: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    justifyContent: 'space-around',
  },
  statItem: {
    alignItems: 'center',
  },
  statValue: {
    fontSize: 24,
    fontWeight: 'bold',
  },
  statLabel: {
    fontSize: 12,
    marginTop: 4,
  },
  actions: {
    gap: 12,
  },
  actionButton: {
    width: '100%',
  },
  reviewHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 20,
  },
  reviewTitle: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  reviewCard: {
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
  },
  reviewCardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  reviewIndex: {
    fontSize: 12,
    fontWeight: '600',
  },
  reviewStatus: {
    fontSize: 12,
    fontWeight: '600',
  },
  reviewQuestion: {
    fontSize: 15,
    marginBottom: 12,
    lineHeight: 22,
  },
  reviewAnswers: {
    marginBottom: 12,
  },
  reviewAnswerLabel: {
    fontSize: 14,
    marginBottom: 4,
  },
  reviewAnswerValue: {
    fontWeight: '600',
  },
  reviewComment: {
    padding: 12,
    borderRadius: 8,
  },
  reviewCommentLabel: {
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 4,
  },
  reviewCommentText: {
    fontSize: 14,
    lineHeight: 20,
  },
});
