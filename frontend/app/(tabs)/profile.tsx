import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Switch,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useColors } from '../../src/hooks/useColors';
import { useThemeStore } from '../../src/store/themeStore';
import { Button } from '../../src/components/Button';
import { useAuthStore } from '../../src/store/authStore';

export default function ProfileScreen() {
  const router = useRouter();
  const colors = useColors();
  const { user, logout } = useAuthStore();
  const { mode, toggleTheme } = useThemeStore();

  const handleLogout = () => {
    Alert.alert(
      'Sair',
      'Deseja realmente sair da sua conta?',
      [
        { text: 'Cancelar', style: 'cancel' },
        {
          text: 'Sair',
          style: 'destructive',
          onPress: async () => {
            await logout();
            router.replace('/');
          },
        },
      ]
    );
  };

  return (
    <SafeAreaView style={[styles.container, { backgroundColor: colors.background }]}>
      <ScrollView contentContainerStyle={styles.content}>
        <View style={styles.header}>
          <View style={[styles.avatar, { backgroundColor: colors.primary }]}>
            <Text style={styles.avatarText}>
              {user?.name?.charAt(0).toUpperCase() || 'U'}
            </Text>
          </View>
          <Text style={[styles.name, { color: colors.text }]}>{user?.name}</Text>
          <Text style={[styles.email, { color: colors.textSecondary }]}>{user?.email}</Text>
        </View>

        <View style={[styles.section, { backgroundColor: colors.card }]}>
          <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>Configurações</Text>
          
          <View style={[styles.menuItem, { borderBottomColor: colors.gray100 }]}>
            <Text style={styles.menuIcon}>🔔</Text>
            <Text style={[styles.menuText, { color: colors.text }]}>Notificações</Text>
            <Text style={[styles.menuArrow, { color: colors.gray400 }]}>›</Text>
          </View>
          
          <View style={[styles.menuItem, { borderBottomColor: colors.gray100 }]}>
            <Text style={styles.menuIcon}>{mode === 'dark' ? '☀️' : '🌙'}</Text>
            <Text style={[styles.menuText, { color: colors.text }]}>Tema Escuro</Text>
            <Switch
              value={mode === 'dark'}
              onValueChange={toggleTheme}
              trackColor={{ false: colors.gray300, true: colors.primary + '80' }}
              thumbColor={mode === 'dark' ? colors.primary : colors.gray400}
            />
          </View>
          
          <View style={[styles.menuItem, { borderBottomColor: colors.gray100 }]}>
            <Text style={styles.menuIcon}>❓</Text>
            <Text style={[styles.menuText, { color: colors.text }]}>Ajuda</Text>
            <Text style={[styles.menuArrow, { color: colors.gray400 }]}>›</Text>
          </View>
        </View>

        <View style={[styles.section, { backgroundColor: colors.card }]}>
          <Text style={[styles.sectionTitle, { color: colors.textSecondary }]}>Sobre</Text>
          
          <View style={[styles.menuItem, { borderBottomColor: colors.gray100 }]}>
            <Text style={styles.menuIcon}>ℹ️</Text>
            <Text style={[styles.menuText, { color: colors.text }]}>Versão do App</Text>
            <Text style={[styles.menuValue, { color: colors.textSecondary }]}>1.0.0</Text>
          </View>
          
          <View style={[styles.menuItem, { borderBottomColor: colors.gray100 }]}>
            <Text style={styles.menuIcon}>📄</Text>
            <Text style={[styles.menuText, { color: colors.text }]}>Termos de Uso</Text>
            <Text style={[styles.menuArrow, { color: colors.gray400 }]}>›</Text>
          </View>
          
          <View style={[styles.menuItem, { borderBottomColor: colors.gray100 }]}>
            <Text style={styles.menuIcon}>🔒</Text>
            <Text style={[styles.menuText, { color: colors.text }]}>Política de Privacidade</Text>
            <Text style={[styles.menuArrow, { color: colors.gray400 }]}>›</Text>
          </View>
        </View>

        <View style={styles.logoutSection}>
          <Button
            title="Sair da Conta"
            onPress={handleLogout}
            variant="danger"
            size="large"
          />
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
    alignItems: 'center',
    marginBottom: 32,
  },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 16,
  },
  avatarText: {
    fontSize: 32,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  name: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 4,
  },
  email: {
    fontSize: 14,
  },
  section: {
    borderRadius: 16,
    padding: 16,
    marginBottom: 24,
  },
  sectionTitle: {
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'uppercase',
    marginBottom: 16,
  },
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
  },
  menuIcon: {
    fontSize: 20,
    marginRight: 16,
  },
  menuText: {
    flex: 1,
    fontSize: 16,
  },
  menuArrow: {
    fontSize: 20,
  },
  menuValue: {
    fontSize: 14,
  },
  logoutSection: {
    marginTop: 8,
  },
});
