import React, { useState, useEffect, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  TouchableOpacity,
  ScrollView,
  Alert,
  BackHandler,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors } from '../../src/theme/colors';
import { Button } from '../../src/components/Button';
import AsyncStorage from '@react-native-async-storage/async-storage';

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

interface Answer {
  question_id: string;
  selected_option: string;
}

const SIMULATION_TIME = 40 * 60; // 40 minutes in seconds

export default function SimulationQuestionScreen() {
  const router = useRouter();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [timeLeft, setTimeLeft] = useState(SIMULATION_TIME);
  const [startTime, setStartTime] = useState(0);

  useEffect(() => {
    loadSimulationData();
    
    // Handle back button
    const backHandler = BackHandler.addEventListener('hardwareBackPress', () => {
      handleQuit();
      return true;
    });
    
    return () => backHandler.remove();
  }, []);

  // Timer
  useEffect(() => {
    if (timeLeft <= 0) {
      handleTimeUp();
      return;
    }
    
    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);
    
    return () => clearInterval(timer);
  }, [timeLeft]);

  const loadSimulationData = async () => {
    try {
      const questionsJson = await AsyncStorage.getItem('simulation_questions');
      const answersJson = await AsyncStorage.getItem('simulation_answers');
      const indexStr = await AsyncStorage.getItem('simulation_current_index');
      const startTimeStr = await AsyncStorage.getItem('simulation_start_time');
      
      if (questionsJson) {
        setQuestions(JSON.parse(questionsJson));
      }
      if (answersJson) {
        setAnswers(JSON.parse(answersJson));
      }
      if (indexStr) {
        setCurrentIndex(parseInt(indexStr, 10));
      }
      if (startTimeStr) {
        const start = parseInt(startTimeStr, 10);
        setStartTime(start);
        const elapsed = Math.floor((Date.now() - start) / 1000);
        setTimeLeft(Math.max(0, SIMULATION_TIME - elapsed));
      }
    } catch (error) {
      console.error('Error loading simulation data:', error);
    }
  };

  const handleTimeUp = () => {
    Alert.alert(
      'Tempo Esgotado!',
      'O tempo do simulado acabou. Suas respostas serão enviadas.',
      [{ text: 'OK', onPress: finishSimulation }]
    );
  };

  const handleQuit = () => {
    Alert.alert(
      'Sair do Simulado',
      'Tem certeza que deseja sair? Seu progresso será perdido.',
      [
        { text: 'Continuar', style: 'cancel' },
        { text: 'Sair', style: 'destructive', onPress: () => router.replace('/(tabs)/home') },
      ]
    );
  };

  const handleSelectOption = (option: string) => {
    if (showFeedback) return;
    setSelectedOption(option);
  };

  const handleConfirm = async () => {
    if (!selectedOption) return;
    
    const newAnswer: Answer = {
      question_id: questions[currentIndex].id,
      selected_option: selectedOption,
    };
    
    const newAnswers = [...answers];
    // Check if already answered
    const existingIndex = newAnswers.findIndex(a => a.question_id === newAnswer.question_id);
    if (existingIndex >= 0) {
      newAnswers[existingIndex] = newAnswer;
    } else {
      newAnswers.push(newAnswer);
    }
    
    setAnswers(newAnswers);
    await AsyncStorage.setItem('simulation_answers', JSON.stringify(newAnswers));
    
    setShowFeedback(true);
  };

  const handleNext = async () => {
    setShowFeedback(false);
    setSelectedOption(null);
    
    if (currentIndex < questions.length - 1) {
      const newIndex = currentIndex + 1;
      setCurrentIndex(newIndex);
      await AsyncStorage.setItem('simulation_current_index', newIndex.toString());
    } else {
      // Last question - finish simulation
      finishSimulation();
    }
  };

  const finishSimulation = async () => {
    const timeTaken = SIMULATION_TIME - timeLeft;
    await AsyncStorage.setItem('simulation_time_taken', timeTaken.toString());
    router.replace('/simulation/result');
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  const currentQuestion = questions[currentIndex];

  if (!currentQuestion) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text>Carregando...</Text>
        </View>
      </SafeAreaView>
    );
  }

  const isTimeWarning = timeLeft < 300; // Less than 5 minutes

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity onPress={handleQuit}>
          <Text style={styles.quitButton}>✕</Text>
        </TouchableOpacity>
        <View style={styles.progress}>
          <Text style={styles.progressText}>
            {currentIndex + 1}/{questions.length}
          </Text>
        </View>
        <View style={[styles.timer, isTimeWarning && styles.timerWarning]}>
          <Text style={[styles.timerText, isTimeWarning && styles.timerTextWarning]}>
            ⏱ {formatTime(timeLeft)}
          </Text>
        </View>
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
        <View style={styles.questionCard}>
          <Text style={styles.moduleTag}>Módulo {currentQuestion.modulo}</Text>
          <Text style={styles.questionText}>{currentQuestion.questao}</Text>
        </View>

        <View style={styles.options}>
          {(['A', 'B', 'C', 'D'] as const).map((option) => {
            const isSelected = selectedOption === option;
            
            return (
              <TouchableOpacity
                key={option}
                style={[
                  styles.optionButton,
                  isSelected && styles.optionSelected,
                  showFeedback && isSelected && styles.optionAnswered,
                ]}
                onPress={() => handleSelectOption(option)}
                disabled={showFeedback}
              >
                <View style={[
                  styles.optionLabel,
                  isSelected && styles.optionLabelSelected,
                ]}>
                  <Text style={[
                    styles.optionLabelText,
                    isSelected && styles.optionLabelTextSelected,
                  ]}>
                    {option}
                  </Text>
                </View>
                <Text style={[
                  styles.optionText,
                  isSelected && styles.optionTextSelected,
                ]}>
                  {currentQuestion.alternativas[option]}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>

      <View style={styles.footer}>
        {!showFeedback ? (
          <Button
            title="Confirmar Resposta"
            onPress={handleConfirm}
            disabled={!selectedOption}
            size="large"
          />
        ) : (
          <Button
            title={currentIndex < questions.length - 1 ? "Próxima Questão" : "Ver Resultado"}
            onPress={handleNext}
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
  quitButton: {
    fontSize: 24,
    color: colors.gray500,
  },
  progress: {
    backgroundColor: colors.gray100,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  progressText: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.text,
  },
  timer: {
    backgroundColor: colors.primary,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  timerWarning: {
    backgroundColor: colors.error,
  },
  timerText: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.white,
  },
  timerTextWarning: {
    color: colors.white,
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
  questionCard: {
    backgroundColor: colors.white,
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
  },
  moduleTag: {
    fontSize: 12,
    color: colors.primary,
    fontWeight: '600',
    marginBottom: 12,
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
  optionAnswered: {
    borderColor: colors.primaryLight,
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
  optionTextSelected: {
    fontWeight: '500',
  },
  footer: {
    padding: 20,
    backgroundColor: colors.white,
    borderTopWidth: 1,
    borderTopColor: colors.gray200,
  },
});
