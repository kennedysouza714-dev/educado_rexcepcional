import React, { useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Alert,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { colors } from '../../src/theme/colors';
import { Button } from '../../src/components/Button';
import { simulationAPI } from '../../src/services/api';
import AsyncStorage from '@react-native-async-storage/async-storage';

export default function SimulationStartScreen() {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleStartSimulation = async () => {
    setLoading(true);
    try {
      const questions = await simulationAPI.startNew();
      
      // Store questions and start time
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
    <SafeAreaView style={styles.container}>
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
          <Text style={styles.title}>Simulado DETRAN</Text>
          <Text style={styles.subtitle}>Teste seus conhecimentos</Text>
        </View>

        <View style={styles.rules}>
          <Text style={styles.rulesTitle}>Regras do Simulado</Text>
          
          <View style={styles.ruleItem}>
            <Text style={styles.ruleIcon}>📋</Text>
            <View style={styles.ruleText}>
              <Text style={styles.ruleTitle}>30 Questões</Text>
              <Text style={styles.ruleDesc}>Questões aleatórias de todos os módulos</Text>
            </View>
          </View>
          
          <View style={styles.ruleItem}>
            <Text style={styles.ruleIcon}>⏱</Text>
            <View style={styles.ruleText}>
              <Text style={styles.ruleTitle}>40 Minutos</Text>
              <Text style={styles.ruleDesc}>Tempo máximo para conclusão</Text>
            </View>
          </View>
          
          <View style={styles.ruleItem}>
            <Text style={styles.ruleIcon}>✅</Text>
            <View style={styles.ruleText}>
              <Text style={styles.ruleTitle}>70% para Aprovar</Text>
              <Text style={styles.ruleDesc}>Mínimo de 21 acertos</Text>
            </View>
          </View>
          
          <View style={styles.ruleItem}>
            <Text style={styles.ruleIcon}>💡</Text>
            <View style={styles.ruleText}>
              <Text style={styles.ruleTitle}>Feedback Imediato</Text>
              <Text style={styles.ruleDesc}>Veja se acertou após cada resposta</Text>
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
    backgroundColor: colors.background,
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
    color: colors.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: colors.textSecondary,
  },
  rules: {
    backgroundColor: colors.white,
    borderRadius: 16,
    padding: 20,
    marginBottom: 32,
  },
  rulesTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
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
  ruleTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 2,
  },
  ruleDesc: {
    fontSize: 14,
    color: colors.textSecondary,
  },
  actions: {
    marginTop: 'auto',
  },
});
