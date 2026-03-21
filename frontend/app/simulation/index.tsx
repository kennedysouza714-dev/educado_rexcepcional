import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useColors } from '../../src/hooks/useColors';
import { Button } from '../../src/components/Button';
import { simulationAPI } from '../../src/services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

const MODULES = [
  { id: '1', name: 'Placas, Cores e Caminhos', emoji: '🚦', total: 371 },
  { id: '2', name: 'Escolhas e Consequências', emoji: '⚖️', total: 171 },
  { id: '3', name: 'Na Direção da Segurança', emoji: '🛡️', total: 575 },
  { id: '4', name: 'Cuidar, Agir e Preservar', emoji: '💚', total: 36 },
];

const QUESTION_OPTIONS = [10, 15, 20, 30, 40, 50];

export default function SimulationStartScreen() {
  const router = useRouter();
  const colors = useColors();
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState<'official' | 'custom'>('official');
  const [selectedModules, setSelectedModules] = useState<string[]>([]);
  const [questionCount, setQuestionCount] = useState(30);

  const toggleModule = (id: string) => {
    setSelectedModules(prev =>
      prev.includes(id) ? prev.filter(m => m !== id) : [...prev, id]
    );
  };

  const handleStart = async () => {
    setLoading(true);
    try {
      const modules = mode === 'custom' && selectedModules.length > 0 ? selectedModules : undefined;
      const count = mode === 'custom' ? questionCount : 30;
      const timeLimit = mode === 'custom' ? Math.ceil(count * 1.33) * 60 : 40 * 60;

      const questions = await simulationAPI.startNew(modules, count);
      await AsyncStorage.setItem('simulation_questions', JSON.stringify(questions));
      await AsyncStorage.setItem('simulation_start_time', Date.now().toString());
      await AsyncStorage.setItem('simulation_answers', JSON.stringify([]));
      await AsyncStorage.setItem('simulation_current_index', '0');
      await AsyncStorage.setItem('simulation_time_limit', timeLimit.toString());
      await AsyncStorage.setItem('simulation_total', count.toString());
      router.push('/simulation/question');
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Erro ao iniciar simulado';
      Alert.alert('Erro', message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <Button
            title="← Voltar"
            onPress={() => router.back()}
            variant="outline"
            size="small"
            style={styles.backButton}
          />
        </View>

        <View style={styles.info}>
          <Text style={styles.emoji}>🚗</Text>
          <Text style={[styles.title, { color: colors.text }]}>Educador Excepcional</Text>
        </View>

        {/* Mode Toggle */}
        <View style={styles.modeToggle}>
          <TouchableOpacity
            style={[styles.modeBtn, mode === 'official' && { backgroundColor: colors.primary }]}
            onPress={() => setMode('official')}
          >
            <Text style={[styles.modeBtnText, mode === 'official' && { color: '#FFFFFF' }]}>
              📋 Oficial
            </Text>
          </TouchableOpacity>
          <TouchableOpacity
            style={[styles.modeBtn, mode === 'custom' && { backgroundColor: colors.primary }]}
            onPress={() => setMode('custom')}
          >
            <Text style={[styles.modeBtnText, mode === 'custom' && { color: '#FFFFFF' }]}>
              ⚙️ Personalizado
            </Text>
          </TouchableOpacity>
        </View>

        {mode === 'official' ? (
          <View style={[styles.rules, { backgroundColor: colors.card }]}>
            <Text style={[styles.rulesTitle, { color: colors.text }]}>Simulado Oficial</Text>
            <View style={styles.ruleItem}>
              <Text style={styles.ruleIcon}>📋</Text>
              <View style={styles.ruleText}>
                <Text style={[styles.ruleTitle2, { color: colors.text }]}>30 Questões</Text>
                <Text style={[styles.ruleDesc, { color: colors.textSecondary }]}>Aleatórias de todos os módulos</Text>
              </View>
            </View>
            <View style={styles.ruleItem}>
              <Text style={styles.ruleIcon}>⏱</Text>
              <View style={styles.ruleText}>
                <Text style={[styles.ruleTitle2, { color: colors.text }]}>40 Minutos</Text>
                <Text style={[styles.ruleDesc, { color: colors.textSecondary }]}>Tempo máximo</Text>
              </View>
            </View>
            <View style={styles.ruleItem}>
              <Text style={styles.ruleIcon}>✅</Text>
              <View style={styles.ruleText}>
                <Text style={[styles.ruleTitle2, { color: colors.text }]}>70% para Aprovar</Text>
                <Text style={[styles.ruleDesc, { color: colors.textSecondary }]}>Mínimo de 21 acertos</Text>
              </View>
            </View>
          </View>
        ) : (
          <View style={[styles.customSection, { backgroundColor: colors.card }]}>
            <Text style={[styles.rulesTitle, { color: colors.text }]}>Personalizar Simulado</Text>

            {/* Module Selection */}
            <Text style={[styles.customLabel, { color: colors.textSecondary }]}>Módulos (vazio = todos)</Text>
            <View style={styles.modulesGrid}>
              {MODULES.map(mod => {
                const isSelected = selectedModules.includes(mod.id);
                return (
                  <TouchableOpacity
                    key={mod.id}
                    style={[
                      styles.moduleChip,
                      { backgroundColor: colors.gray100 },
                      isSelected && { backgroundColor: colors.primary + '20', borderColor: colors.primary },
                    ]}
                    onPress={() => toggleModule(mod.id)}
                  >
                    <Text style={styles.moduleChipEmoji}>{mod.emoji}</Text>
                    <Text style={[
                      styles.moduleChipText,
                      { color: colors.text },
                      isSelected && { color: colors.primary, fontWeight: '700' },
                    ]}>
                      M{mod.id}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>

            {/* Question Count */}
            <Text style={[styles.customLabel, { color: colors.textSecondary }]}>Quantidade de questões</Text>
            <View style={styles.countGrid}>
              {QUESTION_OPTIONS.map(count => {
                const isSelected = questionCount === count;
                return (
                  <TouchableOpacity
                    key={count}
                    style={[
                      styles.countChip,
                      { backgroundColor: colors.gray100 },
                      isSelected && { backgroundColor: colors.primary },
                    ]}
                    onPress={() => setQuestionCount(count)}
                  >
                    <Text style={[
                      styles.countChipText,
                      { color: colors.text },
                      isSelected && { color: '#FFFFFF' },
                    ]}>
                      {count}
                    </Text>
                  </TouchableOpacity>
                );
              })}
            </View>

            <View style={[styles.summaryBox, { backgroundColor: colors.gray100 }]}>
              <Text style={[styles.summaryText, { color: colors.textSecondary }]}>
                ⏱ Tempo: {Math.ceil(questionCount * 1.33)} min  •  ✅ Aprovar: {Math.ceil(questionCount * 0.7)} acertos
              </Text>
            </View>
          </View>
        )}

        <View style={styles.actions}>
          <Button
            title={mode === 'official' ? 'Iniciar Simulado Oficial' : `Iniciar (${questionCount} questões)`}
            onPress={handleStart}
            loading={loading}
            size="large"
          />
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1 },
  content: { padding: 20 },
  header: { alignItems: 'flex-start', marginBottom: 16 },
  backButton: { paddingHorizontal: 12 },
  info: { alignItems: 'center', marginBottom: 24 },
  emoji: { fontSize: 50, marginBottom: 12 },
  title: { fontSize: 26, fontWeight: 'bold' },
  modeToggle: {
    flexDirection: 'row',
    gap: 10,
    marginBottom: 20,
  },
  modeBtn: {
    flex: 1,
    paddingVertical: 14,
    borderRadius: 12,
    alignItems: 'center',
    backgroundColor: '#E5E7EB',
  },
  modeBtnText: {
    fontSize: 15,
    fontWeight: '600',
    color: '#374151',
  },
  rules: { borderRadius: 16, padding: 20, marginBottom: 24 },
  rulesTitle: { fontSize: 18, fontWeight: '600', marginBottom: 20 },
  ruleItem: { flexDirection: 'row', alignItems: 'center', marginBottom: 16 },
  ruleIcon: { fontSize: 28, marginRight: 16 },
  ruleText: { flex: 1 },
  ruleTitle2: { fontSize: 16, fontWeight: '600', marginBottom: 2 },
  ruleDesc: { fontSize: 14 },
  customSection: { borderRadius: 16, padding: 20, marginBottom: 24 },
  customLabel: { fontSize: 13, fontWeight: '600', marginBottom: 10, textTransform: 'uppercase' },
  modulesGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 20 },
  moduleChip: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 10,
    paddingHorizontal: 14,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: 'transparent',
  },
  moduleChipEmoji: { fontSize: 18, marginRight: 8 },
  moduleChipText: { fontSize: 14, fontWeight: '500' },
  countGrid: { flexDirection: 'row', flexWrap: 'wrap', gap: 10, marginBottom: 16 },
  countChip: {
    width: 56,
    height: 44,
    borderRadius: 10,
    justifyContent: 'center',
    alignItems: 'center',
  },
  countChipText: { fontSize: 16, fontWeight: '600' },
  summaryBox: { padding: 12, borderRadius: 10 },
  summaryText: { fontSize: 13, textAlign: 'center' },
  actions: { marginTop: 8 },
});
