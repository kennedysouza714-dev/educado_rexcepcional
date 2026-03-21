import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

type ThemeMode = 'light' | 'dark';

interface ThemeStore {
  mode: ThemeMode;
  isLoaded: boolean;
  toggleTheme: () => void;
  loadTheme: () => Promise<void>;
}

export const useThemeStore = create<ThemeStore>((set, get) => ({
  mode: 'light',
  isLoaded: false,
  
  toggleTheme: async () => {
    const newMode = get().mode === 'light' ? 'dark' : 'light';
    set({ mode: newMode });
    await AsyncStorage.setItem('theme_mode', newMode);
  },
  
  loadTheme: async () => {
    try {
      const saved = await AsyncStorage.getItem('theme_mode');
      if (saved === 'light' || saved === 'dark') {
        set({ mode: saved, isLoaded: true });
      } else {
        set({ isLoaded: true });
      }
    } catch {
      set({ isLoaded: true });
    }
  },
}));
