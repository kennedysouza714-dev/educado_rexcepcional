import React, { useEffect, useState, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  ActivityIndicator,
  RefreshControl,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useColors } from '../../src/hooks/useColors';
import { historyAPI } from '../../src/services/api';

interface HistoryItem {
  id: string;
  score: number;
  passed: boolean;
  time_taken_seconds: number;
  created_at: string;
}

export default function HistoryScreen() {
  const colors = useColors();
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const loadHistory = useCallback(async () => {
    try {
      const data = await historyAPI.getHistory();
      setHistory(data);
    } catch (error) {
      console.error('Error loading history:', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    loadHistory();
  }, [loadHistory]);

  const onRefresh = () => {
    setRefreshing(true);
    loadHistory();
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const renderItem = ({ item, index }: { item: HistoryItem; index: number }) => (
    <View style={[styles.historyCard, { backgroundColor: colors.card }]}>
      <View style={styles.cardHeader}>
        <View style={[styles.cardIndex, { backgroundColor: colors.gray100 }]}>
          <Text style={[styles.indexText, { color: colors.textSecondary }]}>
            #{history.length - index}
          </Text>
        </View>
        <View style={[
          styles.statusBadge,
          item.passed 
            ? { backgroundColor: colors.success + '20' }
            : { backgroundColor: colors.error + '20' }
        ]}>
          <Text style={{ 
            fontSize: 12, 
            fontWeight: '600', 
            color: item.passed ? colors.success : colors.error 
          }}>
            {item.passed ? 'Aprovado' : 'Reprovado'}
          </Text>
        </View>
      </View>
      
      <View style={styles.cardBody}>
        <View style={styles.scoreContainer}>
          <Text style={[
            styles.scoreValue,
            { color: item.passed ? colors.success : colors.error }
          ]}>
            {item.score.toFixed(0)}%
          </Text>
          <Text style={[styles.scoreLabel, { color: colors.textSecondary }]}>
            {Math.round(item.score * 30 / 100)}/30 acertos
          </Text>
        </View>
        
        <View style={styles.detailsContainer}>
          <Text style={[styles.detailText, { color: colors.textSecondary }]}>
            ⏱ {formatTime(item.time_taken_seconds)}
          </Text>
          <Text style={[styles.detailText, { color: colors.textSecondary }]}>
            📅 {formatDate(item.created_at)}
          </Text>
        </View>
      </View>
    </View>
  );

  if (loading) {
    return (
      <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary} />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <View style={styles.header}>
        <Text style={[styles.title, { color: colors.text }]}>Histórico</Text>
        <Text style={[styles.subtitle, { color: colors.textSecondary }]}>
          Seus simulados anteriores
        </Text>
      </View>

      {history.length === 0 ? (
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyEmoji}>📊</Text>
          <Text style={[styles.emptyTitle, { color: colors.text }]}>Nenhum simulado ainda</Text>
          <Text style={[styles.emptyText, { color: colors.textSecondary }]}>
            Faça seu primeiro simulado para ver seu histórico aqui!
          </Text>
        </View>
      ) : (
        <FlatList
          data={history}
          renderItem={renderItem}
          keyExtractor={(item) => item.id}
          contentContainerStyle={styles.listContent}
          refreshControl={
            <RefreshControl
              refreshing={refreshing}
              onRefresh={onRefresh}
              tintColor={colors.primary}
            />
          }
        />
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  header: {
    padding: 20,
    paddingBottom: 10,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 16,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  listContent: {
    padding: 20,
    paddingTop: 10,
  },
  historyCard: {
    borderRadius: 16,
    padding: 16,
    marginBottom: 12,
  },
  cardHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  cardIndex: {
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderRadius: 8,
  },
  indexText: {
    fontSize: 12,
    fontWeight: '600',
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  cardBody: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  scoreContainer: {
    alignItems: 'flex-start',
  },
  scoreValue: {
    fontSize: 32,
    fontWeight: 'bold',
  },
  scoreLabel: {
    fontSize: 12,
  },
  detailsContainer: {
    alignItems: 'flex-end',
  },
  detailText: {
    fontSize: 12,
    marginBottom: 4,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 40,
  },
  emptyEmoji: {
    fontSize: 60,
    marginBottom: 16,
  },
  emptyTitle: {
    fontSize: 20,
    fontWeight: '600',
    marginBottom: 8,
  },
  emptyText: {
    fontSize: 14,
    textAlign: 'center',
  },
});
