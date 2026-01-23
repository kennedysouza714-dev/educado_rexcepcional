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
import { colors } from '../../src/theme/colors';
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
      
      // Clear simulation data
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
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={styles.loadingText}>Calculando resultado...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (!result) {
    return null;
  }

  return (
    <SafeAreaView style={styles.container}>
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
              <Text style={styles.resultSubtitle}>
                {result.passed 
                  ? 'Parabéns! Você passou no simulado!'
                  : 'Não desista! Continue estudando!'}
              </Text>
            </View>

            <View style={styles.statsCard}>
              <View style={styles.scoreContainer}>
                <Text style={[
                  styles.scoreValue,
                  { color: result.passed ? colors.success : colors.error }
                ]}>
                  {result.score.toFixed(0)}%
                </Text>
                <Text style={styles.scoreLabel}>Pontuação</Text>
              </View>

              <View style={styles.statsGrid}>
                <View style={styles.statItem}>
                  <Text style={styles.statValue}>
                    {result.correct_answers}/{result.total_questions}
                  </Text>
                  <Text style={styles.statLabel}>Acertos</Text>
                </View>
                
                <View style={styles.statItem}>
                  <Text style={styles.statValue}>
                    {formatTime(result.time_taken_seconds)}
                  </Text>
                  <Text style={styles.statLabel}>Tempo</Text>
                </View>
                
                <View style={styles.statItem}>
                  <Text style={styles.statValue}>70%</Text>
                  <Text style={styles.statLabel}>Mínimo</Text>
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
              <Text style={styles.reviewTitle}>Revisão das Questões</Text>
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
                  answer.is_correct ? styles.reviewCorrect : styles.reviewIncorrect
                ]}
              >
                <View style={styles.reviewCardHeader}>
                  <Text style={styles.reviewIndex}>Questão {index + 1}</Text>
                  <Text style={[
                    styles.reviewStatus,
                    { color: answer.is_correct ? colors.success : colors.error }
                  ]}>
                    {answer.is_correct ? '✓ Correta' : '✗ Incorreta'}
                  </Text>
                </View>
                
                <Text style={styles.reviewQuestion}>{answer.questao}</Text>
                
                <View style={styles.reviewAnswers}>
                  <Text style={styles.reviewAnswerLabel}>
                    Sua resposta: <Text style={[
                      styles.reviewAnswerValue,
                      { color: answer.is_correct ? colors.success : colors.error }
                    ]}>{answer.selected_option}</Text>
                  </Text>
                  {!answer.is_correct && (
                    <Text style={styles.reviewAnswerLabel}>
                      Resposta correta: <Text style={[
                        styles.reviewAnswerValue,
                        { color: colors.success }
                      ]}>{answer.correct_answer}</Text>
                    </Text>
                  )}
                </View>
                
                <View style={styles.reviewComment}>
                  <Text style={styles.reviewCommentLabel}>Comentário:</Text>
                  <Text style={styles.reviewCommentText}>{answer.comentario}</Text>
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
    backgroundColor: colors.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  loadingText: {
    marginTop: 16,
    fontSize: 16,
    color: colors.textSecondary,
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
    color: colors.textSecondary,
    textAlign: 'center',
  },
  statsCard: {
    backgroundColor: colors.white,
    borderRadius: 20,
    padding: 24,
    marginBottom: 24,
  },
  scoreContainer: {
    alignItems: 'center',
    marginBottom: 24,
    paddingBottom: 24,
    borderBottomWidth: 1,
    borderBottomColor: colors.gray100,
  },
  scoreValue: {
    fontSize: 64,
    fontWeight: 'bold',
  },
  scoreLabel: {
    fontSize: 16,
    color: colors.textSecondary,
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
    color: colors.text,
  },
  statLabel: {
    fontSize: 12,
    color: colors.textSecondary,
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
    color: colors.text,
  },
  reviewCard: {
    backgroundColor: colors.white,
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
    borderLeftWidth: 4,
  },
  reviewCorrect: {
    borderLeftColor: colors.success,
  },
  reviewIncorrect: {
    borderLeftColor: colors.error,
  },
  reviewCardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 12,
  },
  reviewIndex: {
    fontSize: 12,
    fontWeight: '600',
    color: colors.textSecondary,
  },
  reviewStatus: {
    fontSize: 12,
    fontWeight: '600',
  },
  reviewQuestion: {
    fontSize: 15,
    color: colors.text,
    marginBottom: 12,
    lineHeight: 22,
  },
  reviewAnswers: {
    marginBottom: 12,
  },
  reviewAnswerLabel: {
    fontSize: 14,
    color: colors.textSecondary,
    marginBottom: 4,
  },
  reviewAnswerValue: {
    fontWeight: '600',
  },
  reviewComment: {
    backgroundColor: colors.gray50,
    padding: 12,
    borderRadius: 8,
  },
  reviewCommentLabel: {
    fontSize: 12,
    fontWeight: '600',
    color: colors.textSecondary,
    marginBottom: 4,
  },
  reviewCommentText: {
    fontSize: 14,
    color: colors.text,
    lineHeight: 20,
  },
});
