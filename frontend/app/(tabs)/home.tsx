import React, { useEffect, useState } from 'react';
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
import { colors } from '../../src/theme/colors';
import { Button } from '../../src/components/Button';
import { useAuthStore } from '../../src/store/authStore';
import { historyAPI } from '../../src/services/api';

export default function HomeScreen() {
  const router = useRouter();
  const { user } = useAuthStore();
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await historyAPI.getStats();
      setStats(data);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <Text style={styles.greeting}>Olá, {user?.name?.split(' ')[0]}! 👋</Text>
          <Text style={styles.subtitle}>Pronto para estudar hoje?</Text>
        </View>

        <View style={styles.simulationCard}>
          <Text style={styles.cardTitle}>🚗 Simulado DETRAN</Text>
          <Text style={styles.cardDescription}>
            30 questões em 40 minutos{"\n"}
            Aprovação: 70% (21 acertos)
          </Text>
          <Button
            title="Iniciar Simulado"
            onPress={() => router.push('/simulation')}
            size="large"
            style={styles.startButton}
          />
        </View>

        <View style={styles.statsSection}>
          <Text style={styles.sectionTitle}>Seu Desempenho</Text>
          
          {loading ? (
            <ActivityIndicator color={colors.primary} />
          ) : stats ? (
            <View style={styles.statsGrid}>
              <View style={styles.statCard}>
                <Text style={styles.statValue}>{stats.total_simulations}</Text>
                <Text style={styles.statLabel}>Simulados</Text>
              </View>
              <View style={styles.statCard}>
                <Text style={styles.statValue}>{stats.passed_simulations}</Text>
                <Text style={styles.statLabel}>Aprovações</Text>
              </View>
              <View style={styles.statCard}>
                <Text style={[styles.statValue, { color: colors.success }]}>
                  {stats.pass_rate}%
                </Text>
                <Text style={styles.statLabel}>Taxa</Text>
              </View>
              <View style={styles.statCard}>
                <Text style={styles.statValue}>{stats.best_score?.toFixed(0) || 0}%</Text>
                <Text style={styles.statLabel}>Melhor</Text>
              </View>
            </View>
          ) : (
            <Text style={styles.noStats}>Faça seu primeiro simulado!</Text>
          )}
        </View>

        <View style={styles.modulesSection}>
          <Text style={styles.sectionTitle}>Estudar por Módulo</Text>
          <TouchableOpacity
            style={styles.moduleButton}
            onPress={() => router.push('/(tabs)/modules')}
          >
            <Text style={styles.moduleEmoji}>📚</Text>
            <View style={styles.moduleInfo}>
              <Text style={styles.moduleTitle}>4 Módulos Disponíveis</Text>
              <Text style={styles.moduleSubtitle}>45+ questões para estudar</Text>
            </View>
            <Text style={styles.moduleArrow}>→</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  content: {
    padding: 20,
  },
  header: {
    marginBottom: 24,
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.text,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
    color: colors.textSecondary,
  },
  simulationCard: {
    backgroundColor: colors.primary,
    borderRadius: 20,
    padding: 24,
    marginBottom: 24,
  },
  cardTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: colors.white,
    marginBottom: 8,
  },
  cardDescription: {
    fontSize: 14,
    color: colors.gray200,
    marginBottom: 20,
    lineHeight: 22,
  },
  startButton: {
    backgroundColor: colors.white,
  },
  statsSection: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
    marginBottom: 16,
  },
  statsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: 12,
  },
  statCard: {
    flex: 1,
    minWidth: '45%',
    backgroundColor: colors.white,
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: colors.primary,
  },
  statLabel: {
    fontSize: 12,
    color: colors.textSecondary,
    marginTop: 4,
  },
  noStats: {
    textAlign: 'center',
    color: colors.textSecondary,
    padding: 20,
  },
  modulesSection: {
    marginBottom: 24,
  },
  moduleButton: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: colors.white,
    borderRadius: 16,
    padding: 16,
  },
  moduleEmoji: {
    fontSize: 32,
    marginRight: 16,
  },
  moduleInfo: {
    flex: 1,
  },
  moduleTitle: {
    fontSize: 16,
    fontWeight: '600',
    color: colors.text,
  },
  moduleSubtitle: {
    fontSize: 14,
    color: colors.textSecondary,
  },
  moduleArrow: {
    fontSize: 20,
    color: colors.primary,
  },
});
