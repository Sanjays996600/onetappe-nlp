/**
 * Application theme constants
 */

// Color palette
export const COLORS = {
  // Primary colors
  primary: {
    light: '#93c5fd', // blue-300
    main: '#3b82f6',  // blue-500
    dark: '#1d4ed8',  // blue-700
    contrastText: '#ffffff'
  },
  
  // Secondary colors
  secondary: {
    light: '#e5e7eb', // gray-200
    main: '#9ca3af',  // gray-400
    dark: '#4b5563',  // gray-600
    contrastText: '#ffffff'
  },
  
  // Status colors
  status: {
    success: {
      light: '#d1fae5', // green-100
      main: '#10b981',  // green-500
      dark: '#065f46',  // green-800
      contrastText: '#ffffff'
    },
    warning: {
      light: '#fef3c7', // yellow-100
      main: '#f59e0b',  // yellow-500
      dark: '#92400e',  // yellow-800
      contrastText: '#ffffff'
    },
    error: {
      light: '#fee2e2', // red-100
      main: '#ef4444',  // red-500
      dark: '#b91c1c',  // red-700
      contrastText: '#ffffff'
    },
    info: {
      light: '#dbeafe', // blue-100
      main: '#3b82f6',  // blue-500
      dark: '#1e40af',  // blue-800
      contrastText: '#ffffff'
    }
  },
  
  // WhatsApp specific colors
  whatsapp: {
    header: '#075e54',
    background: '#e5ddd5',
    userMessage: '#dcf8c6',
    botMessage: '#ffffff'
  },
  
  // Text colors
  text: {
    primary: '#1f2937',   // gray-800
    secondary: '#6b7280', // gray-500
    disabled: '#9ca3af',  // gray-400
    hint: '#9ca3af'       // gray-400
  },
  
  // Background colors
  background: {
    default: '#f3f4f6',  // gray-100
    paper: '#ffffff',
    card: '#ffffff'
  },
  
  // Border colors
  border: {
    light: '#e5e7eb',  // gray-200
    main: '#d1d5db',   // gray-300
    dark: '#9ca3af'    // gray-400
  }
};

// Spacing
export const SPACING = {
  xs: '0.25rem',  // 4px
  sm: '0.5rem',   // 8px
  md: '1rem',     // 16px
  lg: '1.5rem',   // 24px
  xl: '2rem',     // 32px
  xxl: '3rem'     // 48px
};

// Typography
export const TYPOGRAPHY = {
  fontFamily: {
    sans: ['Inter', 'ui-sans-serif', 'system-ui', 'sans-serif'],
    mono: ['Menlo', 'Monaco', 'Consolas', 'monospace']
  },
  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '1.875rem' // 30px
  },
  fontWeight: {
    normal: '400',
    medium: '500',
    semibold: '600',
    bold: '700'
  }
};

// Border radius
export const BORDER_RADIUS = {
  sm: '0.125rem',  // 2px
  md: '0.25rem',   // 4px
  lg: '0.5rem',    // 8px
  xl: '0.75rem',   // 12px
  full: '9999px'   // Fully rounded
};

// Shadows
export const SHADOWS = {
  sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
  md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
  lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
  xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
};