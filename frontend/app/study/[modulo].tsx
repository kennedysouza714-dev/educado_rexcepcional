import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors } from '../../src/theme/colors';
import { Button } from '../../src/components/Button';
import { modulesAPI } from '../../src/services/api';

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

const moduleNames: Record<string, string> = {
  '1': 'Placas, Cores e Caminhos',
  '2': 'Escolhas e Consequências',
  '3': 'Na Direção da Segurança',
  '4': 'Cuidar, Agir e Preservar',
};

export default function StudyModuleScreen() {
  const router = useRouter();
  const { modulo } = useLocalSearchParams<{ modulo: string }>();
  
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [showAnswer, setShowAnswer] = useState(false);
  const [correctAnswer, setCorrectAnswer] = useState<string>('');
  const [comment, setComment] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [loadingAnswer, setLoadingAnswer] = useState(false);

  useEffect(() => {
    loadQuestions();
  }, [modulo]);

  const loadQuestions = async () => {
    if (!modulo) return;
    try {
      const data = await modulesAPI.getModuleQuestions(modulo, 100, 0);
      setQuestions(data);
    } catch (error) {
      console.error('Error loading questions:', error);
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
        modulo || '',
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

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
      setSelectedOption(null);
      setShowAnswer(false);
      setCorrectAnswer('');
      setComment('');
    }
  };

  const handlePrevious = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
      setSelectedOption(null);
      setShowAnswer(false);
      setCorrectAnswer('');
      setComment('');
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary} />
        </View>
      </SafeAreaView>
    );
  }

  const currentQuestion = questions[currentIndex];

  if (!currentQuestion) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text>Nenhuma questão disponível</Text>
          <Button
            title="Voltar"
            onPress={() => router.back()}
            style={{ marginTop: 20 }}
          />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()}>
          <Text style={styles.backButton}>← Voltar</Text>
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Módulo {modulo}</Text>
        <Text style={styles.progress}>{currentIndex + 1}/{questions.length}</Text>
      </View>

      <View style={styles.progressBar}>
        <View 
          style={[
            styles.progressFill, 
            { width: `${((currentIndex + 1) / questions.length) * 100}%` }
          ]} 
        />
      </View>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
        <Text style={styles.moduleName}>{moduleNames[modulo || '1']}</Text>
        
        <View style={styles.questionCard}>
          <Text style={styles.questionText}>{currentQuestion.questao}</Text>
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
                  isSelected && !showAnswer && styles.optionSelected,
                  isCorrect && styles.optionCorrect,
                  isWrong && styles.optionWrong,
                ]}
                onPress={() => handleSelectOption(option)}
                disabled={showAnswer}
              >
                <View style={[
                  styles.optionLabel,
                  isSelected && !showAnswer && styles.optionLabelSelected,
                  isCorrect && styles.optionLabelCorrect,
                  isWrong && styles.optionLabelWrong,
                ]}>
                  <Text style={[
                    styles.optionLabelText,
                    (isSelected || isCorrect || isWrong) && styles.optionLabelTextSelected,
                  ]}>
                    {option}
                  </Text>
                </View>
                <Text style={styles.optionText}>
                  {currentQuestion.alternativas[option]}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>

        {showAnswer && (
          <View style={styles.commentCard}>
            <Text style={styles.commentTitle}>💡 Comentário</Text>
            <Text style={styles.commentText}>{comment}</Text>
          </View>
        )}
      </ScrollView>

      <View style={styles.footer}>
        <View style={styles.navigationButtons}>
          <Button
            title="Anterior"
            onPress={handlePrevious}
            variant="outline"
            disabled={currentIndex === 0}
            style={styles.navButton}
          />
          <Button
            title="Próxima"
            onPress={handleNext}
            variant="outline"
            disabled={currentIndex === questions.length - 1}
            style={styles.navButton}
          />
        </View>
        
        {!showAnswer && (
          <Button
            title="Verificar Resposta"
            onPress={handleCheckAnswer}
            disabled={!selectedOption}
            loading={loadingAnswer}
            size="large"
          />
        )}
      </View>
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
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
  },
  backButton: {
    fontSize: 16,
    color: colors.primary,
    fontWeight: '500',
  },
  headerTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
  },
  progress: {
    fontSize: 14,
    color: colors.textSecondary,
  },
  progressBar: {
    height: 4,
    backgroundColor: colors.gray200,
  },
  progressFill: {
    height: '100%',
    backgroundColor: colors.primary,
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
  },
  moduleName: {
    fontSize: 14,
    color: colors.primary,
    fontWeight: '600',
    marginBottom: 12,
  },
  questionCard: {
    backgroundColor: colors.white,
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
  },
  questionText: {
    fontSize: 18,
    color: colors.text,
    lineHeight: 26,
  },
  options: {
    gap: 12,
  },
  optionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.white,
    borderRadius: 12,
    padding: 16,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  optionSelected: {
    borderColor: colors.primary,
    backgroundColor: colors.primary + '10',
  },
  optionCorrect: {
    borderColor: colors.success,
    backgroundColor: colors.success + '10',
  },
  optionWrong: {
    borderColor: colors.error,
    backgroundColor: colors.error + '10',
  },
  optionLabel: {
    width: 32,
    height: 32,
    borderRadius: 16,
    backgroundColor: colors.gray100,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  optionLabelSelected: {
    backgroundColor: colors.primary,
  },
  optionLabelCorrect: {
    backgroundColor: colors.success,
  },
  optionLabelWrong: {
    backgroundColor: colors.error,
  },
  optionLabelText: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.text,
  },
  optionLabelTextSelected: {
    color: colors.white,
  },
  optionText: {
    flex: 1,
    fontSize: 15,
    color: colors.text,
  },
  commentCard: {
    backgroundColor: colors.primaryLight + '20',
    borderRadius: 12,
    padding: 16,
    marginTop: 20,
  },
  commentTitle: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.primary,
    marginBottom: 8,
  },
  commentText: {
    fontSize: 14,
    color: colors.text,
    lineHeight: 22,
  },
  footer: {
    padding: 20,
    backgroundColor: colors.white,
    borderTopWidth: 1,
    borderTopColor: colors.gray200,
    gap: 12,
  },
  navigationButtons: {
    flexDirection: 'row',
    gap: 12,
  },
  navButton: {
    flex: 1,
  },
});
