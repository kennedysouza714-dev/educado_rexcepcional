import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useColors } from '../../src/hooks/useColors';
import { Button } from '../../src/components/Button';
import { simulationAPI } from '../../src/services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SimulationStartScreen() {
  const router = useRouter();
  const colors = useColors();
  const [loading, setLoading] = useState(false);

  const handleStartSimulation = async () => {
    setLoading(true);
    try {
      const questions = await simulationAPI.startNew();
      await AsyncStorage.setItem('simulation_questions', JSON.stringify(questions));
      await AsyncStorage.setItem('simulation_start_time', Date.now().toString());
      await AsyncStorage.setItem('simulation_answers', JSON.stringify([]));
      await AsyncStorage.setItem('simulation_current_index', '0');
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
      <View style={styles.content}>
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
          <Text style={[styles.title, { color: colors.text }]}>Simulado DETRAN</Text>
          <Text style={[styles.subtitle, { color: colors.textSecondary }]}>Teste seus conhecimentos</Text>
        </View>

        <View style={[styles.rules, { backgroundColor: colors.card }]}>
          <Text style={[styles.rulesTitle, { color: colors.text }]}>Regras do Simulado</Text>
          
          <View style={styles.ruleItem}>
            <Text style={styles.ruleIcon}>📋</Text>
            <View style={styles.ruleText}>
              <Text style={[styles.ruleTitle2, { color: colors.text }]}>30 Questões</Text>
              <Text style={[styles.ruleDesc, { color: colors.textSecondary }]}>Questões aleatórias de todos os módulos</Text>
            </View>
          </View>
          
          <View style={styles.ruleItem}>
            <Text style={styles.ruleIcon}>⏱</Text>
            <View style={styles.ruleText}>
              <Text style={[styles.ruleTitle2, { color: colors.text }]}>40 Minutos</Text>
              <Text style={[styles.ruleDesc, { color: colors.textSecondary }]}>Tempo máximo para conclusão</Text>
            </View>
          </View>
          
          <View style={styles.ruleItem}>
            <Text style={styles.ruleIcon}>✅</Text>
            <View style={styles.ruleText}>
              <Text style={[styles.ruleTitle2, { color: colors.text }]}>70% para Aprovar</Text>
              <Text style={[styles.ruleDesc, { color: colors.textSecondary }]}>Mínimo de 21 acertos</Text>
            </View>
          </View>
          
          <View style={styles.ruleItem}>
            <Text style={styles.ruleIcon}>💡</Text>
            <View style={styles.ruleText}>
              <Text style={[styles.ruleTitle2, { color: colors.text }]}>Feedback Imediato</Text>
              <Text style={[styles.ruleDesc, { color: colors.textSecondary }]}>Veja se acertou após cada resposta</Text>
            </View>
          </View>
        </View>

        <View style={styles.actions}>
          <Button
            title="Iniciar Simulado"
            onPress={handleStartSimulation}
            loading={loading}
            size="large"
          />
        </View>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    padding: 20,
  },
  header: {
    alignItems: 'flex-start',
    marginBottom: 20,
  },
  backButton: {
    paddingHorizontal: 12,
  },
  info: {
    alignItems: 'center',
    marginBottom: 32,
  },
  emoji: {
    fontSize: 60,
    marginBottom: 16,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
  },
  rules: {
    borderRadius: 16,
    padding: 20,
    marginBottom: 32,
  },
  rulesTitle: {
    fontSize: 18,
    fontWeight: '600',
    marginBottom: 20,
  },
  ruleItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  ruleIcon: {
    fontSize: 28,
    marginRight: 16,
  },
  ruleText: {
    flex: 1,
  },
  ruleTitle2: {
    fontSize: 16,
    fontWeight: '600',
    marginBottom: 2,
  },
  ruleDesc: {
    fontSize: 14,
  },
  actions: {
    marginTop: 'auto',
  },
});
