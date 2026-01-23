import React from 'react';
import { Tabs } from 'expo-router';
import { View, Text, StyleSheet, Platform } from 'react-native';
import { colors } from '../../src/theme/colors';

interface TabIconProps {
  name: string;
  emoji: string;
  color: string;
  focused: boolean;
}

function TabIcon({ name, emoji, color, focused }: TabIconProps) {
  return (
    <View style={styles.tabIcon}>
      <Text style={[styles.emoji, { opacity: focused ? 1 : 0.6 }]}>{emoji}</Text>
      <Text style={[styles.tabLabel, { color }]}>{name}</Text>
    </View>
  );
}

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        headerShown: false,
        tabBarStyle: styles.tabBar,
        tabBarActiveTintColor: colors.primary,
        tabBarInactiveTintColor: colors.gray400,
      }}
    >
      <Tabs.Screen
        name="home"
        options={{
          title: 'Início',
          tabBarIcon: ({ color, focused }) => (
            <TabIcon name="Início" emoji="🏠" color={color} focused={focused} />
          ),
          tabBarLabel: () => null,
        }}
      />
      <Tabs.Screen
        name="modules"
        options={{
          title: 'Módulos',
          tabBarIcon: ({ color, focused }) => (
            <TabIcon name="Módulos" emoji="📚" color={color} focused={focused} />
          ),
          tabBarLabel: () => null,
        }}
      />
      <Tabs.Screen
        name="history"
        options={{
          title: 'Histórico',
          tabBarIcon: ({ color, focused }) => (
            <TabIcon name="Histórico" emoji="📊" color={color} focused={focused} />
          ),
          tabBarLabel: () => null,
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Perfil',
          tabBarIcon: ({ color, focused }) => (
            <TabIcon name="Perfil" emoji="👤" color={color} focused={focused} />
          ),
          tabBarLabel: () => null,
        }}
      />
    </Tabs>
  );
}

const styles = StyleSheet.create({
  tabBar: {
    backgroundColor: colors.white,
    borderTopColor: colors.gray200,
    borderTopWidth: 1,
    height: Platform.OS === 'ios' ? 85 : 70,
    paddingTop: 8,
    paddingBottom: Platform.OS === 'ios' ? 25 : 10,
  },
  tabIcon: {
    alignItems: 'center',
    justifyContent: 'center',
  },
  emoji: {
    fontSize: 24,
    marginBottom: 4,
  },
  tabLabel: {
    fontSize: 12,
    fontWeight: '500',
  },
});
