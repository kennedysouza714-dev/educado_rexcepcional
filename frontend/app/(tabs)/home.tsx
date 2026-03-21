import React, { useEffect, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useColors } from '../../src/hooks/useColors';
import { Button } from '../../src/components/Button';
import { useAuthStore } from '../../src/store/authStore';
import { historyAPI, missedAPI } from '../../src/services/api';

const moduleNames: Record<string, string> = {
  '1': 'Placas',
  '2': 'Escolhas',
  '3': 'Segurança',
  '4': 'Preservar',
};

export default function HomeScreen() {
  const router = useRouter();
  const colors = useColors();
  const { user } = useAuthStore();
  const [stats, setStats] = useState<any>(null);
  const [moduleStats, setModuleStats] = useState<any>(null);
  const [missedCount, setMissedCount] = useState(0);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsData, missedData, moduleData] = await Promise.all([
        historyAPI.getStats(),
        missedAPI.getMissedQuestions().catch(() => ({ total_missed: 0 })),
        missedAPI.getStatsByModule().catch(() => null),
      ]);
      setStats(statsData);
      setMissedCount(missedData.total_missed || 0);
      setModuleStats(moduleData);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  const onRefresh = () => {
    setRefreshing(true);
    loadData().then(() => setRefreshing(false));
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView 
        contentContainerStyle={styles.content}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.primary} />
        }
      >
        <View style={styles.header}>
          <Text style={[styles.greeting, { color: colors.text }]}>
            Olá, {user?.name?.split(' ')[0]}! 👋
          </Text>
          <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
            Pronto para estudar hoje?
          </Text>
        </View>

        {/* Simulation Card */}
        <View style={[styles.simulationCard, { backgroundColor: colors.primary }]}>
          <Text style={styles.cardTitle}>🚗 Educador Excepcional</Text>
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

        {/* Quick Actions */}
        <View style={styles.quickActions}>
          <TouchableOpacity
            style={[styles.quickAction, { backgroundColor: colors.error + '15' }]}
            onPress={() => router.push('/review')}
          >
            <Text style={styles.quickActionEmoji}>❌</Text>
            <Text style={[styles.quickActionTitle, { color: colors.error }]}>Revisar Erros</Text>
            <Text style={[styles.quickActionCount, { color: colors.textSecondary }]}>
              {missedCount} questão{missedCount !== 1 ? 'ões' : ''}
            </Text>
          </TouchableOpacity>
          
          <TouchableOpacity
            style={[styles.quickAction, { backgroundColor: colors.primary + '15' }]}
            onPress={() => router.push('/(tabs)/modules')}
          >
            <Text style={styles.quickActionEmoji}>📚</Text>
            <Text style={[styles.quickActionTitle, { color: colors.primary }]}>Estudar</Text>
            <Text style={[styles.quickActionCount, { color: colors.textSecondary }]}>
              1153 questões
            </Text>
          </TouchableOpacity>
        </View>

        {/* Stats Section */}
        <View style={styles.statsSection}>
          <Text style={[styles.sectionTitle, { color: colors.text }]}>Seu Desempenho</Text>
          
          {loading ? (
            <ActivityIndicator color={colors.primary} />
          ) : stats && stats.total_simulations > 0 ? (
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
            <View style={[styles.emptyStats, { backgroundColor: colors.card }]}>
              <Text style={[styles.noStats, { color: colors.textSecondary }]}>
                Faça seu primeiro simulado! 🚀
              </Text>
            </View>
          )}
        </View>

        {/* Module Stats */}
        {moduleStats && Object.values(moduleStats).some((m: any) => m.total > 0) && (
          <View style={styles.moduleStatsSection}>
            <Text style={[styles.sectionTitle, { color: colors.text }]}>
              Desempenho por Módulo
            </Text>
            <View style={styles.moduleStatsGrid}>
              {['1', '2', '3', '4'].map((mod) => {
                const modStat = moduleStats[mod] || { total: 0, correct: 0, accuracy: 0 };
                if (modStat.total === 0) return null;
                const barColor = modStat.accuracy >= 70 ? colors.success 
                  : modStat.accuracy >= 50 ? colors.warning : colors.error;
                return (
                  <View key={mod} style={[styles.moduleStatCard, { backgroundColor: colors.card }]}>
                    <View style={styles.moduleStatHeader}>
                      <Text style={[styles.moduleStatName, { color: colors.text }]}>
                        M{mod}
                      </Text>
                      <Text style={[styles.moduleStatPct, { color: barColor }]}>
                        {modStat.accuracy}%
                      </Text>
                    </View>
                    <View style={[styles.moduleStatBar, { backgroundColor: colors.gray200 }]}>
                      <View style={[
                        styles.moduleStatBarFill,
                        { width: `${modStat.accuracy}%`, backgroundColor: barColor }
                      ]} />
                    </View>
                    <Text style={[styles.moduleStatDetail, { color: colors.textSecondary }]}>
                      {modStat.correct}/{modStat.total} acertos
                    </Text>
                  </View>
                );
              })}
            </View>
          </View>
        )}
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
    marginBottom: 20,
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
  quickActions: {
    flexDirection: 'row',
    gap: 12,
    marginBottom: 24,
  },
  quickAction: {
    flex: 1,
    borderRadius: 16,
    padding: 16,
    alignItems: 'center',
  },
  quickActionEmoji: {
    fontSize: 28,
    marginBottom: 8,
  },
  quickActionTitle: {
    fontSize: 14,
    fontWeight: '700',
    marginBottom: 2,
  },
  quickActionCount: {
    fontSize: 12,
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
  emptyStats: {
    borderRadius: 16,
    padding: 24,
    alignItems: 'center',
  },
  noStats: {
    textAlign: 'center',
    fontSize: 15,
  },
  moduleStatsSection: {
    marginBottom: 24,
  },
  moduleStatsGrid: {
    gap: 10,
  },
  moduleStatCard: {
    borderRadius: 12,
    padding: 14,
  },
  moduleStatHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  moduleStatName: {
    fontSize: 14,
    fontWeight: '600',
  },
  moduleStatPct: {
    fontSize: 16,
    fontWeight: '700',
  },
  moduleStatBar: {
    height: 6,
    borderRadius: 3,
    marginBottom: 6,
  },
  moduleStatBarFill: {
    height: '100%',
    borderRadius: 3,
  },
  moduleStatDetail: {
    fontSize: 12,
  },
});
