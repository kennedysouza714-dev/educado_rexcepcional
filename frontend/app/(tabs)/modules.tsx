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
import { modulesAPI } from '../../src/services/api';

interface Module {
  modulo: string;
  name: string;
  difficulty: string;
  total_questions: number;
}

const difficultyColors: Record<string, string> = {
  'fácil': colors.success,
  'intermediário': colors.warning,
  'difícil': colors.error,
};

const moduleEmojis: Record<string, string> = {
  '1': '🚦',
  '2': '⚖️',
  '3': '🛡️',
  '4': '💚',
};

export default function ModulesScreen() {
  const router = useRouter();
  const [modules, setModules] = useState<Module[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadModules();
  }, []);

  const loadModules = async () => {
    try {
      const data = await modulesAPI.getModules();
      setModules(data);
    } catch (error) {
      console.error('Error loading modules:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>Módulos de Estudo</Text>
        <Text style={styles.subtitle}>Escolha um módulo para estudar</Text>
      </View>

      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={colors.primary} />
        </View>
      ) : (
        <ScrollView contentContainerStyle={styles.content}>
          {modules.map((module) => (
            <TouchableOpacity
              key={module.modulo}
              style={styles.moduleCard}
              onPress={() => router.push(`/study/${module.modulo}`)}
            >
              <View style={styles.moduleHeader}>
                <Text style={styles.moduleEmoji}>{moduleEmojis[module.modulo]}</Text>
                <View style={styles.moduleInfo}>
                  <Text style={styles.moduleName}>Módulo {module.modulo}</Text>
                  <Text style={styles.moduleTitle}>{module.name}</Text>
                </View>
              </View>
              
              <View style={styles.moduleFooter}>
                <View style={[
                  styles.difficultyBadge,
                  { backgroundColor: difficultyColors[module.difficulty] + '20' }
                ]}>
                  <Text style={[
                    styles.difficultyText,
                    { color: difficultyColors[module.difficulty] }
                  ]}>
                    {module.difficulty}
                  </Text>
                </View>
                <Text style={styles.questionsCount}>
                  {module.total_questions} questões
                </Text>
              </View>
            </TouchableOpacity>
          ))}
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background,
  },
  header: {
    padding: 20,
    paddingBottom: 10,
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
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    padding: 20,
    paddingTop: 10,
  },
  moduleCard: {
    backgroundColor: colors.white,
    borderRadius: 16,
    padding: 20,
    marginBottom: 16,
  },
  moduleHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  moduleEmoji: {
    fontSize: 40,
    marginRight: 16,
  },
  moduleInfo: {
    flex: 1,
  },
  moduleName: {
    fontSize: 14,
    color: colors.textSecondary,
    marginBottom: 2,
  },
  moduleTitle: {
    fontSize: 18,
    fontWeight: '600',
    color: colors.text,
  },
  moduleFooter: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
  },
  difficultyBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 20,
  },
  difficultyText: {
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'capitalize',
  },
  questionsCount: {
    fontSize: 14,
    color: colors.textSecondary,
  },
});
