import React, { useState, useEffect, useRef } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  Modal,
  FlatList,
  Dimensions,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors } from '../../src/theme/colors';
import { Button } from '../../src/components/Button';
import { ImagePlaceholder, detectImageType } from '../../src/components/ImagePlaceholder';
import { modulesAPI, bookmarksAPI } from '../../src/services/api';

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

const moduleTotals: Record<string, number> = {
  '1': 371,
  '2': 171,
  '3': 575,
  '4': 36,
};

const BATCH_SIZE = 50;

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
  const [loadingMore, setLoadingMore] = useState(false);
  const [loadingAnswer, setLoadingAnswer] = useState(false);
  const [showJumpModal, setShowJumpModal] = useState(false);
  const [bookmarks, setBookmarks] = useState<string[]>([]);
  const [filterMode, setFilterMode] = useState<'all' | 'bookmarked'>('all');
  const [totalLoaded, setTotalLoaded] = useState(0);
  const scrollRef = useRef<ScrollView>(null);

  useEffect(() => {
    loadInitialData();
  }, [modulo]);

  const loadInitialData = async () => {
    if (!modulo) return;
    setLoading(true);
    try {
      const [questionsData, bookmarksData] = await Promise.all([
        modulesAPI.getModuleQuestions(modulo, BATCH_SIZE, 0),
        bookmarksAPI.getBookmarks().catch(() => ({ bookmarks: [] })),
      ]);
      setQuestions(questionsData);
      setTotalLoaded(questionsData.length);
      setBookmarks(bookmarksData.bookmarks || []);
    } catch (error) {
      console.error('Error loading questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const loadMoreQuestions = async () => {
    if (!modulo || loadingMore) return;
    const total = moduleTotals[modulo] || 0;
    if (totalLoaded >= total) return;
    
    setLoadingMore(true);
    try {
      const moreQuestions = await modulesAPI.getModuleQuestions(modulo, BATCH_SIZE, totalLoaded);
      if (moreQuestions.length > 0) {
        setQuestions(prev => [...prev, ...moreQuestions]);
        setTotalLoaded(prev => prev + moreQuestions.length);
      }
    } catch (error) {
      console.error('Error loading more questions:', error);
    } finally {
      setLoadingMore(false);
    }
  };

  // Auto-load more when approaching end
  useEffect(() => {
    if (currentIndex >= questions.length - 5 && questions.length < (moduleTotals[modulo || '1'] || 0)) {
      loadMoreQuestions();
    }
  }, [currentIndex]);

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

  const goToQuestion = (index: number) => {
    setCurrentIndex(index);
    setSelectedOption(null);
    setShowAnswer(false);
    setCorrectAnswer('');
    setComment('');
    setShowJumpModal(false);
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

  const toggleBookmark = async () => {
    const questionId = questions[currentIndex]?.id;
    if (!questionId) return;
    
    try {
      const result = await bookmarksAPI.toggleBookmark(questionId);
      setBookmarks(result.bookmarks);
    } catch (error) {
      // Optimistic update - toggle locally on error
      setBookmarks(prev => 
        prev.includes(questionId) 
          ? prev.filter(id => id !== questionId)
          : [...prev, questionId]
      );
    }
  };

  const isBookmarked = (questionId: string) => bookmarks.includes(questionId);

  const filteredQuestions = filterMode === 'bookmarked' 
    ? questions.filter(q => isBookmarked(q.id))
    : questions;

  const effectiveIndex = filterMode === 'bookmarked' 
    ? Math.min(currentIndex, filteredQuestions.length - 1) 
    : currentIndex;

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary} />
          <Text style={styles.loadingText}>Carregando questões...</Text>
        </View>
      </SafeAreaView>
    );
  }

  const currentQuestion = filteredQuestions[effectiveIndex];
  const totalModuleQuestions = moduleTotals[modulo || '1'] || 0;

  if (!currentQuestion) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.emptyEmoji}>{filterMode === 'bookmarked' ? '🔖' : '📭'}</Text>
          <Text style={styles.emptyTitle}>
            {filterMode === 'bookmarked' 
              ? 'Nenhuma questão salva' 
              : 'Nenhuma questão disponível'}
          </Text>
          <Text style={styles.emptyText}>
            {filterMode === 'bookmarked' 
              ? 'Marque questões com ★ para revisar depois' 
              : 'Tente novamente mais tarde'}
          </Text>
          {filterMode === 'bookmarked' && (
            <Button
              title="Ver Todas"
              onPress={() => { setFilterMode('all'); setCurrentIndex(0); }}
              style={{ marginTop: 16 }}
            />
          )}
          <Button
            title="Voltar"
            onPress={() => router.back()}
            variant="outline"
            style={{ marginTop: 12 }}
          />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity onPress={() => router.back()} style={styles.backBtn}>
          <Text style={styles.backButton}>←</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={() => setShowJumpModal(true)} style={styles.progressBtn}>
          <Text style={styles.headerTitle}>
            {effectiveIndex + 1}/{filteredQuestions.length}
          </Text>
          <Text style={styles.jumpHint}>▼</Text>
        </TouchableOpacity>
        <TouchableOpacity onPress={toggleBookmark} style={styles.bookmarkBtn}>
          <Text style={styles.bookmarkIcon}>
            {isBookmarked(currentQuestion.id) ? '★' : '☆'}
          </Text>
        </TouchableOpacity>
      </View>

      {/* Filter Tabs */}
      <View style={styles.filterTabs}>
        <TouchableOpacity
          style={[styles.filterTab, filterMode === 'all' && styles.filterTabActive]}
          onPress={() => { setFilterMode('all'); setCurrentIndex(0); }}
        >
          <Text style={[styles.filterText, filterMode === 'all' && styles.filterTextActive]}>
            Todas ({questions.length}{totalLoaded < totalModuleQuestions ? '+' : ''})
          </Text>
        </TouchableOpacity>
        <TouchableOpacity
          style={[styles.filterTab, filterMode === 'bookmarked' && styles.filterTabActive]}
          onPress={() => { setFilterMode('bookmarked'); setCurrentIndex(0); }}
        >
          <Text style={[styles.filterText, filterMode === 'bookmarked' && styles.filterTextActive]}>
            ★ Salvas ({questions.filter(q => isBookmarked(q.id)).length})
          </Text>
        </TouchableOpacity>
      </View>

      {/* Progress Bar */}
      <View style={styles.progressBar}>
        <View 
          style={[
            styles.progressFill, 
            { width: `${((effectiveIndex + 1) / filteredQuestions.length) * 100}%` }
          ]} 
        />
      </View>

      {/* Question Content */}
      <ScrollView ref={scrollRef} style={styles.content} contentContainerStyle={styles.contentContainer}>
        <Text style={styles.moduleName}>
          Módulo {modulo} — {moduleNames[modulo || '1']}
        </Text>
        
        <View style={styles.questionCard}>
          <Text style={styles.questionNumber}>Questão {currentQuestion.numero}</Text>
          <Text style={styles.questionText}>{currentQuestion.questao}</Text>
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
          <View style={[
            styles.commentCard,
            selectedOption === correctAnswer ? styles.commentCorrect : styles.commentWrong,
          ]}>
            <Text style={styles.commentTitle}>
              {selectedOption === correctAnswer ? '✅ Correto!' : '❌ Incorreto'}
            </Text>
            <Text style={styles.commentText}>{comment}</Text>
          </View>
        )}

        {loadingMore && (
          <View style={styles.loadingMoreContainer}>
            <ActivityIndicator size="small" color={colors.primary} />
            <Text style={styles.loadingMoreText}>Carregando mais questões...</Text>
          </View>
        )}
      </ScrollView>

      {/* Footer */}
      <View style={styles.footer}>
        <View style={styles.navigationButtons}>
          <TouchableOpacity
            style={[styles.navBtn, effectiveIndex === 0 && styles.navBtnDisabled]}
            onPress={handlePrevious}
            disabled={effectiveIndex === 0}
          >
            <Text style={[styles.navBtnText, effectiveIndex === 0 && styles.navBtnTextDisabled]}>
              ← Anterior
            </Text>
          </TouchableOpacity>
          
          {!showAnswer ? (
            <TouchableOpacity
              style={[styles.checkBtn, !selectedOption && styles.checkBtnDisabled]}
              onPress={handleCheckAnswer}
              disabled={!selectedOption || loadingAnswer}
            >
              {loadingAnswer ? (
                <ActivityIndicator size="small" color={colors.white} />
              ) : (
                <Text style={styles.checkBtnText}>Verificar</Text>
              )}
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              style={styles.nextBtn}
              onPress={handleNext}
              disabled={effectiveIndex === filteredQuestions.length - 1}
            >
              <Text style={styles.nextBtnText}>Próxima →</Text>
            </TouchableOpacity>
          )}
          
          <TouchableOpacity
            style={[styles.navBtn, effectiveIndex >= filteredQuestions.length - 1 && styles.navBtnDisabled]}
            onPress={handleNext}
            disabled={effectiveIndex >= filteredQuestions.length - 1}
          >
            <Text style={[styles.navBtnText, effectiveIndex >= filteredQuestions.length - 1 && styles.navBtnTextDisabled]}>
              Próxima →
            </Text>
          </TouchableOpacity>
        </View>
      </View>

      {/* Jump-to-Question Modal */}
      <Modal visible={showJumpModal} transparent animationType="slide">
        <View style={styles.modalOverlay}>
          <View style={styles.modalContent}>
            <View style={styles.modalHeader}>
              <Text style={styles.modalTitle}>Ir para Questão</Text>
              <TouchableOpacity onPress={() => setShowJumpModal(false)}>
                <Text style={styles.modalClose}>✕</Text>
              </TouchableOpacity>
            </View>
            <FlatList
              data={filteredQuestions}
              numColumns={5}
              keyExtractor={(item) => item.id}
              contentContainerStyle={styles.gridContainer}
              renderItem={({ item, index }) => {
                const isCurrent = index === effectiveIndex;
                const isSaved = isBookmarked(item.id);
                return (
                  <TouchableOpacity
                    style={[
                      styles.gridItem,
                      isCurrent && styles.gridItemCurrent,
                      isSaved && styles.gridItemSaved,
                    ]}
                    onPress={() => goToQuestion(index)}
                  >
                    <Text style={[
                      styles.gridItemText,
                      isCurrent && styles.gridItemTextCurrent,
                    ]}>
                      {index + 1}
                    </Text>
                    {isSaved && <Text style={styles.gridItemStar}>★</Text>}
                  </TouchableOpacity>
                );
              }}
            />
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const { width } = Dimensions.get('window');

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  loadingText: {
    marginTop: 12,
    fontSize: 14,
    color: colors.textSecondary,
  },
  emptyEmoji: {
    fontSize: 60,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 14,
    color: colors.textSecondary,
    textAlign: 'center',
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 16,
    paddingVertical: 12,
  },
  backBtn: {
    padding: 8,
  },
  backButton: {
    fontSize: 22,
    color: colors.primary,
    fontWeight: '600',
  },
  progressBtn: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.gray100,
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 20,
  },
  headerTitle: {
    fontSize: 15,
    fontWeight: '600',
    color: colors.text,
  },
  jumpHint: {
    fontSize: 10,
    color: colors.textSecondary,
    marginLeft: 6,
  },
  bookmarkBtn: {
    padding: 8,
  },
  bookmarkIcon: {
    fontSize: 26,
    color: colors.secondary,
  },
  filterTabs: {
    flexDirection: 'row',
    paddingHorizontal: 16,
    marginBottom: 8,
    gap: 8,
  },
  filterTab: {
    flex: 1,
    paddingVertical: 8,
    borderRadius: 20,
    backgroundColor: colors.gray100,
    alignItems: 'center',
  },
  filterTabActive: {
    backgroundColor: colors.primary,
  },
  filterText: {
    fontSize: 13,
    fontWeight: '600',
    color: colors.textSecondary,
  },
  filterTextActive: {
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
    paddingBottom: 40,
  },
  moduleName: {
    fontSize: 13,
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
  questionNumber: {
    fontSize: 12,
    color: colors.textSecondary,
    fontWeight: '500',
    marginBottom: 8,
  },
  questionText: {
    fontSize: 17,
    color: colors.text,
    lineHeight: 26,
    marginBottom: 4,
  },
  options: {
    gap: 10,
  },
  optionButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.white,
    borderRadius: 12,
    padding: 14,
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
    borderRadius: 12,
    padding: 16,
    marginTop: 16,
  },
  commentCorrect: {
    backgroundColor: colors.success + '15',
    borderLeftWidth: 4,
    borderLeftColor: colors.success,
  },
  commentWrong: {
    backgroundColor: colors.error + '15',
    borderLeftWidth: 4,
    borderLeftColor: colors.error,
  },
  commentTitle: {
    fontSize: 15,
    fontWeight: '700',
    color: colors.text,
    marginBottom: 8,
  },
  commentText: {
    fontSize: 14,
    color: colors.text,
    lineHeight: 22,
  },
  loadingMoreContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 16,
    gap: 8,
  },
  loadingMoreText: {
    fontSize: 13,
    color: colors.textSecondary,
  },
  footer: {
    padding: 16,
    backgroundColor: colors.white,
    borderTopWidth: 1,
    borderTopColor: colors.gray200,
  },
  navigationButtons: {
    flexDirection: 'row',
    gap: 10,
    alignItems: 'center',
  },
  navBtn: {
    paddingVertical: 12,
    paddingHorizontal: 14,
    borderRadius: 10,
    borderWidth: 1.5,
    borderColor: colors.gray300,
  },
  navBtnDisabled: {
    borderColor: colors.gray200,
    opacity: 0.4,
  },
  navBtnText: {
    fontSize: 13,
    fontWeight: '600',
    color: colors.text,
  },
  navBtnTextDisabled: {
    color: colors.gray400,
  },
  checkBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 10,
    backgroundColor: colors.primary,
    alignItems: 'center',
  },
  checkBtnDisabled: {
    backgroundColor: colors.gray300,
  },
  checkBtnText: {
    fontSize: 15,
    fontWeight: '700',
    color: colors.white,
  },
  nextBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 10,
    backgroundColor: colors.success,
    alignItems: 'center',
  },
  nextBtnText: {
    fontSize: 15,
    fontWeight: '700',
    color: colors.white,
  },
  // Modal Styles
  modalOverlay: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.5)',
    justifyContent: 'flex-end',
  },
  modalContent: {
    backgroundColor: colors.white,
    borderTopLeftRadius: 20,
    borderTopRightRadius: 20,
    maxHeight: '70%',
    paddingBottom: 30,
  },
  modalHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: 20,
    borderBottomWidth: 1,
    borderBottomColor: colors.gray200,
  },
  modalTitle: {
    fontSize: 18,
    fontWeight: '700',
    color: colors.text,
  },
  modalClose: {
    fontSize: 22,
    color: colors.gray500,
    padding: 4,
  },
  gridContainer: {
    padding: 16,
  },
  gridItem: {
    width: (width - 80) / 5,
    height: 48,
    margin: 4,
    borderRadius: 10,
    backgroundColor: colors.gray100,
    justifyContent: 'center',
    alignItems: 'center',
  },
  gridItemCurrent: {
    backgroundColor: colors.primary,
  },
  gridItemSaved: {
    borderWidth: 2,
    borderColor: colors.secondary,
  },
  gridItemText: {
    fontSize: 14,
    fontWeight: '600',
    color: colors.text,
  },
  gridItemTextCurrent: {
    color: colors.white,
  },
  gridItemStar: {
    position: 'absolute',
    top: 2,
    right: 4,
    fontSize: 10,
    color: colors.secondary,
  },
});
