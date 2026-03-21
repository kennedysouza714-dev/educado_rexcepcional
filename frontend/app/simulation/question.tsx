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
import { useColors } from '../../src/hooks/useColors';
import { Button } from '../../src/components/Button';
import { ImagePlaceholder, detectImageType } from '../../src/components/ImagePlaceholder';
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

const SIMULATION_TIME = 40 * 60;

export default function SimulationQuestionScreen() {
  const router = useRouter();
  const colors = useColors();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const [selectedOption, setSelectedOption] = useState<string | null>(null);
  const [showFeedback, setShowFeedback] = useState(false);
  const [timeLeft, setTimeLeft] = useState(SIMULATION_TIME);
  const [startTime, setStartTime] = useState(0);

  useEffect(() => {
    loadSimulationData();
    const backHandler = BackHandler.addEventListener('hardwareBackPress', () => {
      handleQuit();
      return true;
    });
    return () => backHandler.remove();
  }, []);

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
      if (questionsJson) setQuestions(JSON.parse(questionsJson));
      if (answersJson) setAnswers(JSON.parse(answersJson));
      if (indexStr) setCurrentIndex(parseInt(indexStr, 10));
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
      <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.loadingContainer}>
          <Text style={{ color: colors.text }}>Carregando...</Text>
        </View>
      </SafeAreaView>
    );
  }

  const isTimeWarning = timeLeft < 300;

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={styles.header}>
        <TouchableOpacity onPress={handleQuit}>
          <Text style={[styles.quitButton, { color: colors.gray500 }]}>✕</Text>
        </TouchableOpacity>
        <View style={[styles.progress, { backgroundColor: colors.gray100 }]}>
          <Text style={[styles.progressText, { color: colors.text }]}>
            {currentIndex + 1}/{questions.length}
          </Text>
        </View>
        <View style={[styles.timer, { backgroundColor: isTimeWarning ? colors.error : colors.primary }]}>
          <Text style={styles.timerText}>
            ⏱ {formatTime(timeLeft)}
          </Text>
        </View>
      </View>

      <View style={[styles.progressBar, { backgroundColor: colors.gray200 }]}>
        <View 
          style={[
            styles.progressFill, 
            { width: `${((currentIndex + 1) / questions.length) * 100}%`, backgroundColor: colors.primary }
          ]} 
        />
      </View>

      <ScrollView style={styles.content} contentContainerStyle={styles.contentContainer}>
        <View style={[styles.questionCard, { backgroundColor: colors.card }]}>
          <Text style={[styles.moduleTag, { color: colors.primary }]}>Módulo {currentQuestion.modulo}</Text>
          <Text style={[styles.questionText, { color: colors.text }]}>{currentQuestion.questao}</Text>
          {(() => {
            const imageType = detectImageType(currentQuestion.questao);
            return imageType ? <ImagePlaceholder type={imageType} size="medium" /> : null;
          })()}
        </View>

        <View style={styles.options}>
          {(['A', 'B', 'C', 'D'] as const).map((option) => {
            const isSelected = selectedOption === option;
            return (
              <TouchableOpacity
                key={option}
                style={[
                  styles.optionButton,
                  { backgroundColor: colors.card },
                  isSelected && { borderColor: colors.primary, backgroundColor: colors.primary + '10' },
                  showFeedback && isSelected && { borderColor: colors.primaryLight },
                ]}
                onPress={() => handleSelectOption(option)}
                disabled={showFeedback}
              >
                <View style={[
                  styles.optionLabel,
                  { backgroundColor: colors.gray100 },
                  isSelected && { backgroundColor: colors.primary },
                ]}>
                  <Text style={[
                    styles.optionLabelText,
                    { color: colors.text },
                    isSelected && { color: '#FFFFFF' },
                  ]}>
                    {option}
                  </Text>
                </View>
                <Text style={[
                  styles.optionText,
                  { color: colors.text },
                  isSelected && { fontWeight: '500' },
                ]}>
                  {currentQuestion.alternativas[option]}
                </Text>
              </TouchableOpacity>
            );
          })}
        </View>
      </ScrollView>

      <View style={[styles.footer, { backgroundColor: colors.card, borderTopColor: colors.gray200 }]}>
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
  },
  progress: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  progressText: {
    fontSize: 14,
    fontWeight: '600',
  },
  timer: {
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  timerText: {
    fontSize: 14,
    fontWeight: '600',
    color: '#FFFFFF',
  },
  progressBar: {
    height: 4,
  },
  progressFill: {
    height: '100%',
  },
  content: {
    flex: 1,
  },
  contentContainer: {
    padding: 20,
  },
  questionCard: {
    borderRadius: 16,
    padding: 20,
    marginBottom: 20,
  },
  moduleTag: {
    fontSize: 12,
    fontWeight: '600',
    marginBottom: 12,
  },
  questionText: {
    fontSize: 18,
    lineHeight: 26,
  },
  options: {
    gap: 12,
  },
  optionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    borderRadius: 12,
    padding: 16,
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
  footer: {
    padding: 20,
    borderTopWidth: 1,
  },
});
