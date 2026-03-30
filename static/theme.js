/**
 * Theme Management - Dark Mode Toggle
 * This script handles dark mode switching between system preference,
 * light mode, and dark mode.
 */

class ThemeManager {
  constructor() {
    this.STORAGE_KEY = 'theme-preference';
    this.THEME_ATTR = 'data-theme';
    this.DARK_MODE_CLASS = 'dark-mode';
    
    this.init();
  }

  /**
   * Initialize the theme manager
   */
  init() {
    this.applyTheme(this.getThemePreference());
    this.setupListeners();
  }

  /**
   * Get the user's theme preference
   * Priority: localStorage > system preference > 'light'
   */
  getThemePreference() {
    const stored = localStorage.getItem(this.STORAGE_KEY);
    if (stored) {
      return stored;
    }

    // Check system preference for dark mode
    if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
      return 'dark';
    }

    return 'light';
  }

  /**
   * Apply theme to the document with proper cleanup
   */
  applyTheme(theme) {
    const html = document.documentElement;
    const body = document.body;

    // Remove data-theme attribute first
    html.removeAttribute(this.THEME_ATTR);

    // Apply new theme
    if (theme === 'dark') {
      html.setAttribute(this.THEME_ATTR, 'dark');
    }

    // Store preference
    localStorage.setItem(this.STORAGE_KEY, theme);
    
    // Force paint
    void body.offsetHeight;
    
    // Trigger custom event for other scripts
    document.dispatchEvent(new CustomEvent('themechange', { detail: { theme } }));
  }

  /**
   * Toggle between light and dark modes
   */
  toggle() {
    const current = this.getThemePreference();
    const next = current === 'dark' ? 'light' : 'dark';
    this.applyTheme(next);
  }

  /**
   * Set specific theme
   */
  setTheme(theme) {
    if (['light', 'dark'].includes(theme)) {
      this.applyTheme(theme);
    }
  }

  /**
   * Setup system preference listener
   */
  setupListeners() {
    if (!window.matchMedia) return;

    // Listen for system preference changes
    const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
    darkModeQuery.addEventListener('change', (e) => {
      // Only apply if user hasn't set a preference
      if (!localStorage.getItem(this.STORAGE_KEY)) {
        this.applyTheme(e.matches ? 'dark' : 'light');
      }
    });
  }

  /**
   * Get current theme
   */
  getCurrentTheme() {
    return localStorage.getItem(this.STORAGE_KEY) || 'light';
  }
}

// Initialize theme manager when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    window.themeManager = new ThemeManager();
  });
} else {
  window.themeManager = new ThemeManager();
}

/**
 * Helper functions for easy access
 */
window.toggleDarkMode = () => {
  if (window.themeManager) {
    window.themeManager.toggle();
  }
};

window.setTheme = (theme) => {
  if (window.themeManager) {
    window.themeManager.setTheme(theme);
  }
};

window.getTheme = () => {
  if (window.themeManager) {
    return window.themeManager.getCurrentTheme();
  }
  return 'light';
};
