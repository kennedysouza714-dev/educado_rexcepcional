import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useColors } from '../../src/hooks/useColors';
import { Button } from '../../src/components/Button';
import { ImagePlaceholder, detectImageType } from '../../src/components/ImagePlaceholder';
import { missedAPI, modulesAPI } from '../../src/services/api';

interface Question {
  id: string;
  modulo: string;
  numero: string;
  questao: string;
  alternativas: {
    A: string;
    B: string;
    C: string;
    D: string;
  };
}

export default function ReviewScreen() {
  const router = useRouter();
  const colors = useColors();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [correctAnswer, setCorrectAnswer] = useState('');
  const [comment, setComment] = useState('');
  const [loading, setLoading] = useState(true);
  const [loadingAnswer, setLoadingAnswer] = useState(false);
  const scrollRef = useRef<ScrollView>(null);

  useEffect(() => {
    loadMissedQuestions();
  }, []);

  const loadMissedQuestions = async () => {
    try {
      const data = await missedAPI.getMissedQuestions();
      setQuestions(data.questions || []);
    } catch (error) {
      console.error('Error loading missed questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSelectOption = (option: string) => {
    if (showAnswer) return;
    setSelectedOption(option);
  };

  const handleCheckAnswer = async () => {
    if (!selectedOption || !questions[currentIndex]) return;
    setLoadingAnswer(true);
    try {
      const data = await modulesAPI.getQuestionWithAnswer(
        questions[currentIndex].modulo,
        questions[currentIndex].id
      );
      setCorrectAnswer(data.correct_answer);
      setComment(data.comment);
      setShowAnswer(true);
    } catch (error) {
      console.error('Error getting answer:', error);
    } finally {
      setLoadingAnswer(false);
    }
  };

  const goToQuestion = (index: number) => {
    setCurrentIndex(index);
    setSelectedOption(null);
    setShowAnswer(false);
    setCorrectAnswer('');
    setComment('');
    scrollRef.current?.scrollTo({ y: 0, animated: false });
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      goToQuestion(currentIndex + 1);
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      goToQuestion(currentIndex - 1);
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={[styles.loadingText, { color: colors.textSecondary }]}>Carregando questões...</Text>
        </View>
      </SafeAreaView>
    );
  }

  if (questions.length === 0) {
    return (
      <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.header}>
          <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
            <Text style={[styles.backText, { color: colors.primary }]}>← Voltar</Text>
          </TouchableOpacity>
        </View>
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyEmoji}>🎉</Text>
          <Text style={[styles.emptyTitle, { color: colors.text }]}>Parabéns!</Text>
          <Text style={[styles.emptyText, { color: colors.textSecondary }]}>
            Você não tem questões erradas para revisar.{'\n'}
            Continue fazendo simulados para praticar!
          </Text>
          <Button
            title="Voltar ao Início"
            onPress={() => router.back()}
            style={{ marginTop: 24 }}
          />
        </View>
      </SafeAreaView>
    );
  }

  const currentQuestion = questions[currentIndex];

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Text style={[styles.backText, { color: colors.primary }]}>← Voltar</Text>
        </TouchableOpacity>
        <View style={[styles.badge, { backgroundColor: colors.error + '20' }]}>
          <Text style={[styles.badgeText, { color: colors.error }]}>
            {questions.length} errada{questions.length !== 1 ? 's' : ''}
          </Text>
        </View>
      </View>

      <Text style={[styles.screenTitle, { color: colors.text }]}>Revisão de Erros</Text>
      
      {/* Progress */}
      <View style={[styles.progressBar, { backgroundColor: colors.gray200 }]}>
        <View 
          style={[
            styles.progressFill, 
            { width: `${((currentIndex + 1) / questions.length) * 100}%`, backgroundColor: colors.error }
          ]} 
        />
      </View>
      <Text style={[styles.progressText, { color: colors.textSecondary }]}>
        {currentIndex + 1} de {questions.length}
      </Text>

      {/* Content */}
      <ScrollView ref={scrollRef} style={styles.content} contentContainerStyle={styles.contentContainer}>
        <View style={[styles.questionCard, { backgroundColor: colors.card }]}>
          <Text style={[styles.moduleBadge, { color: colors.primary }]}>
            Módulo {currentQuestion.modulo} • Questão {currentQuestion.numero}
          </Text>
          <Text style={[styles.questionText, { color: colors.text }]}>{currentQuestion.questao}</Text>
          {(() => {
            const imageType = detectImageType(currentQuestion.questao);
            return imageType ? <ImagePlaceholder type={imageType} size="medium" /> : null;
          })()}
        </View>

        <View style={styles.options}>
          {(['A', 'B', 'C', 'D'] as const).map((option) => {
            const isSelected = selectedOption === option;
            const isCorrect = showAnswer && option === correctAnswer;
            const isWrong = showAnswer && isSelected && option !== correctAnswer;
            
            return (
              <TouchableOpacity
                key={option}
                style={[
                  styles.optionButton,
                  { backgroundColor: colors.card },
                  isSelected && !showAnswer && { borderColor: colors.primary, backgroundColor: colors.primary + '10' },
                  isCorrect && { borderColor: colors.success, backgroundColor: colors.success + '10' },
                  isWrong && { borderColor: colors.error, backgroundColor: colors.error + '10' },
                ]}
                onPress={() => handleSelectOption(option)}
                disabled={showAnswer}
              >
                <View style={[
                  styles.optionLabel,
                  { backgroundColor: colors.gray100 },
                  isSelected && !showAnswer && { backgroundColor: colors.primary },
                  isCorrect && { backgroundColor: colors.success },
                  isWrong && { backgroundColor: colors.error },
                ]}>
                  <Text style={[
                    styles.optionLabelText,
                    { color: colors.text },
                    (isSelected || isCorrect || isWrong) && { color: '#FFFFFF' },
                  ]}>
                    {option}
                  </Text>
                </View>
                <Text style={[styles.optionText, { color: colors.text }]}>
                  {currentQuestion.alternativas[option]}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>

        {showAnswer && (
          <View style={[
            styles.commentCard,
            selectedOption === correctAnswer 
              ? { backgroundColor: colors.success + '15', borderLeftColor: colors.success }
              : { backgroundColor: colors.error + '15', borderLeftColor: colors.error },
          ]}>
            <Text style={[styles.commentTitle, { color: colors.text }]}>
              {selectedOption === correctAnswer ? '✅ Correto desta vez!' : '❌ Ainda incorreto'}
            </Text>
            <Text style={[styles.commentText, { color: colors.text }]}>{comment}</Text>
          </View>
        )}
      </ScrollView>

      {/* Footer */}
      <View style={[styles.footer, { backgroundColor: colors.card, borderTopColor: colors.gray200 }]}>
        <View style={styles.navigationButtons}>
          <TouchableOpacity
            style={[styles.navBtn, { borderColor: colors.gray300 }, currentIndex === 0 && styles.navBtnDisabled]}
            onPress={handlePrevious}
            disabled={currentIndex === 0}
          >
            <Text style={[styles.navBtnText, { color: colors.text }, currentIndex === 0 && { color: colors.gray400 }]}>
              ←
            </Text>
          </TouchableOpacity>
          
          {!showAnswer ? (
            <TouchableOpacity
              style={[styles.checkBtn, { backgroundColor: colors.primary }, !selectedOption && { backgroundColor: colors.gray300 }]}
              onPress={handleCheckAnswer}
              disabled={!selectedOption || loadingAnswer}
            >
              {loadingAnswer ? (
                <ActivityIndicator size="small" color="#FFFFFF" />
              ) : (
                <Text style={styles.checkBtnText}>Verificar</Text>
              )}
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              style={[styles.checkBtn, { backgroundColor: colors.success }]}
              onPress={handleNext}
              disabled={currentIndex >= questions.length - 1}
            >
              <Text style={styles.checkBtnText}>Próxima →</Text>
            </TouchableOpacity>
          )}
          
          <TouchableOpacity
            style={[styles.navBtn, { borderColor: colors.gray300 }, currentIndex >= questions.length - 1 && styles.navBtnDisabled]}
            onPress={handleNext}
            disabled={currentIndex >= questions.length - 1}
          >
            <Text style={[styles.navBtnText, { color: colors.text }, currentIndex >= questions.length - 1 && { color: colors.gray400 }]}>
              →
            </Text>
          </TouchableOpacity>
        </View>
      </View>
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
    marginTop: 12,
    fontSize: 14,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  backBtn: {
    padding: 4,
  },
  backText: {
    fontSize: 16,
    fontWeight: '600',
  },
  badge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  badgeText: {
    fontSize: 13,
    fontWeight: '600',
  },
  screenTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    paddingHorizontal: 20,
    marginBottom: 12,
  },
  progressBar: {
    height: 4,
    marginHorizontal: 20,
    borderRadius: 2,
  },
  progressFill: {
    height: '100%',
    borderRadius: 2,
  },
  progressText: {
    fontSize: 12,
    textAlign: 'center',
    marginTop: 6,
    marginBottom: 8,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  emptyEmoji: {
    fontSize: 60,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 15,
    textAlign: 'center',
    lineHeight: 24,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
    paddingBottom: 40,
  },
  questionCard: {
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
  },
  moduleBadge: {
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 10,
  },
  questionText: {
    fontSize: 17,
    lineHeight: 26,
    marginBottom: 4,
  },
  options: {
    gap: 10,
  },
  optionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 12,
    padding: 14,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  optionLabel: {
    width: 32,
    height: 32,
    borderRadius: 16,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  optionLabelText: {
    fontSize: 14,
    fontWeight: '600',
  },
  optionText: {
    flex: 1,
    fontSize: 15,
  },
  commentCard: {
    borderRadius: 12,
    padding: 16,
    marginTop: 16,
    borderLeftWidth: 4,
  },
  commentTitle: {
    fontSize: 15,
    fontWeight: '700',
    marginBottom: 8,
  },
  commentText: {
    fontSize: 14,
    lineHeight: 22,
  },
  footer: {
    padding: 16,
    borderTopWidth: 1,
  },
  navigationButtons: {
    flexDirection: 'row',
    gap: 10,
    alignItems: 'center',
  },
  navBtn: {
    width: 48,
    height: 48,
    borderRadius: 12,
    borderWidth: 1.5,
    justifyContent: 'center',
    alignItems: 'center',
  },
  navBtnDisabled: {
    opacity: 0.3,
  },
  navBtnText: {
    fontSize: 18,
    fontWeight: '600',
  },
  checkBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  checkBtnText: {
    fontSize: 15,
    fontWeight: '700',
    color: '#FFFFFF',
  },
});
