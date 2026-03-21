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
import { useColors } from '../../src/hooks/useColors';
import { Button } from '../../src/components/Button';
import { useAuthStore } from '../../src/store/authStore';
import { historyAPI } from '../../src/services/api';

export default function HomeScreen() {
  const router = useRouter();
  const colors = useColors();
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
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <Text style={[styles.greeting, { color: colors.text }]}>
            Olá, {user?.name?.split(' ')[0]}! 👋
          </Text>
          <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
            Pronto para estudar hoje?
          </Text>
        </View>

        <View style={[styles.simulationCard, { backgroundColor: colors.primary }]}>
          <Text style={styles.cardTitle}>🚗 Simulado DETRAN</Text>
          <Text style={styles.cardDescription}>
            30 questões em 40 minutos{"\n"}
            Aprovação: 70% (21 acertos)
          </Text>
          <Button
            title="Iniciar Simulado"
            onPress={() => router.push('/simulation')}
            size="large"
            style={{ backgroundColor: '#FFFFFF' }}
            textStyle={{ color: colors.primary }}
          />
        </View>

        <View style={styles.statsSection}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>Seu Desempenho</Text>
          
          {loading ? (
            <ActivityIndicator color={colors.primary} />
          ) : stats ? (
            <View style={styles.statsGrid}>
              <View style={[styles.statCard, { backgroundColor: colors.card }]}>
                <Text style={[styles.statValue, { color: colors.primary }]}>
                  {stats.total_simulations}
                </Text>
                <Text style={[styles.statLabel, { color: colors.textSecondary }]}>Simulados</Text>
              </View>
              <View style={[styles.statCard, { backgroundColor: colors.card }]}>
                <Text style={[styles.statValue, { color: colors.primary }]}>
                  {stats.passed_simulations}
                </Text>
                <Text style={[styles.statLabel, { color: colors.textSecondary }]}>Aprovações</Text>
              </View>
              <View style={[styles.statCard, { backgroundColor: colors.card }]}>
                <Text style={[styles.statValue, { color: colors.success }]}>
                  {stats.pass_rate}%
                </Text>
                <Text style={[styles.statLabel, { color: colors.textSecondary }]}>Taxa</Text>
              </View>
              <View style={[styles.statCard, { backgroundColor: colors.card }]}>
                <Text style={[styles.statValue, { color: colors.primary }]}>
                  {stats.best_score?.toFixed(0) || 0}%
                </Text>
                <Text style={[styles.statLabel, { color: colors.textSecondary }]}>Melhor</Text>
              </View>
            </View>
          ) : (
            <Text style={[styles.noStats, { color: colors.textSecondary }]}>
              Faça seu primeiro simulado!
            </Text>
          )}
        </View>

        <View style={styles.modulesSection}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>Estudar por Módulo</Text>
          <TouchableOpacity
            style={[styles.moduleButton, { backgroundColor: colors.card }]}
            onPress={() => router.push('/(tabs)/modules')}
          >
            <Text style={styles.moduleEmoji}>📚</Text>
            <View style={styles.moduleInfo}>
              <Text style={[styles.moduleTitle, { color: colors.text }]}>4 Módulos Disponíveis</Text>
              <Text style={[styles.moduleSubtitle, { color: colors.textSecondary }]}>
                1153 questões para estudar
              </Text>
            </View>
            <Text style={[styles.moduleArrow, { color: colors.primary }]}>→</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
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
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
  },
  simulationCard: {
    borderRadius: 20,
    padding: 24,
    marginBottom: 24,
  },
  cardTitle: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#FFFFFF',
    marginBottom: 8,
  },
  cardDescription: {
    fontSize: 14,
    color: '#E5E7EB',
    marginBottom: 20,
    lineHeight: 22,
  },
  statsSection: {
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 18,
    fontWeight: '600',
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
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
  },
  statValue: {
    fontSize: 28,
    fontWeight: 'bold',
  },
  statLabel: {
    fontSize: 12,
    marginTop: 4,
  },
  noStats: {
    textAlign: 'center',
    padding: 20,
  },
  modulesSection: {
    marginBottom: 24,
  },
  moduleButton: {
    flexDirection: 'row',
    alignItems: 'center',
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
  },
  moduleSubtitle: {
    fontSize: 14,
  },
  moduleArrow: {
    fontSize: 20,
  },
});
