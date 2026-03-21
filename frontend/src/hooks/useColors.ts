import { useThemeStore } from '../store/themeStore';
import { getColors, ColorScheme } from '../theme/colors';

export function useColors(): ColorScheme {
  const mode = useThemeStore((state) => state.mode);
  return getColors(mode);
}
