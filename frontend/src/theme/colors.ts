export const lightColors = {
  // Primary colors
  primary: '#1E3A8A',
  primaryLight: '#3B82F6',
  primaryDark: '#1E40AF',
  
  // Secondary colors
  secondary: '#F59E0B',
  secondaryLight: '#FCD34D',
  secondaryDark: '#D97706',
  
  // Status colors
  success: '#10B981',
  successLight: '#34D399',
  error: '#EF4444',
  errorLight: '#F87171',
  warning: '#F59E0B',
  warningLight: '#FBBF24',
  
  // Neutral colors
  white: '#FFFFFF',
  black: '#000000',
  gray50: '#F9FAFB',
  gray100: '#F3F4F6',
  gray200: '#E5E7EB',
  gray300: '#D1D5DB',
  gray400: '#9CA3AF',
  gray500: '#6B7280',
  gray600: '#4B5563',
  gray700: '#374151',
  gray800: '#1F2937',
  gray900: '#111827',
  
  // Background colors
  background: '#F3F4F6',
  card: '#FFFFFF',
  
  // Text colors
  text: '#1F2937',
  textSecondary: '#6B7280',
  textLight: '#9CA3AF',
};

export const darkColors = {
  // Primary colors
  primary: '#3B82F6',
  primaryLight: '#60A5FA',
  primaryDark: '#2563EB',
  
  // Secondary colors
  secondary: '#F59E0B',
  secondaryLight: '#FCD34D',
  secondaryDark: '#D97706',
  
  // Status colors
  success: '#34D399',
  successLight: '#6EE7B7',
  error: '#F87171',
  errorLight: '#FCA5A5',
  warning: '#FBBF24',
  warningLight: '#FDE68A',
  
  // Neutral colors
  white: '#1F2937',
  black: '#FFFFFF',
  gray50: '#111827',
  gray100: '#1F2937',
  gray200: '#374151',
  gray300: '#4B5563',
  gray400: '#6B7280',
  gray500: '#9CA3AF',
  gray600: '#D1D5DB',
  gray700: '#E5E7EB',
  gray800: '#F3F4F6',
  gray900: '#F9FAFB',
  
  // Background colors
  background: '#111827',
  card: '#1F2937',
  
  // Text colors
  text: '#F3F4F6',
  textSecondary: '#9CA3AF',
  textLight: '#6B7280',
};

export type ColorScheme = typeof lightColors;

// Default export for backwards compatibility - always light
export const colors = lightColors;

// Helper to get colors by mode
export function getColors(mode: 'light' | 'dark'): ColorScheme {
  return mode === 'dark' ? darkColors : lightColors;
}
