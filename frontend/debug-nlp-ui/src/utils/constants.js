/**
 * Application-wide constants
 */

// API endpoints
export const API_BASE_URL = 'http://localhost:5000';
export const API_ENDPOINTS = {
  PROCESS: '/api/process',
  HEALTH: '/api/health'
};

// Language options
export const LANGUAGE_OPTIONS = [
  { value: 'auto', label: 'Auto Detect' },
  { value: 'en', label: 'English' },
  { value: 'hi', label: 'Hindi' },
  { value: 'mixed', label: 'Mixed (Hinglish)' }
];

// Status indicators
export const API_STATUS = {
  CHECKING: 'checking',
  ONLINE: 'online',
  OFFLINE: 'offline'
};

// UI text
export const UI_TEXT = {
  APP_TITLE: 'OneTappe NLP Debug UI',
  APP_SUBTITLE: 'Test multilingual WhatsApp commands with the NLP API',
  FORM_TITLE: 'WhatsApp Command Input',
  PREVIEW_TITLE: 'WhatsApp Preview',
  RESULTS_TITLE: 'NLP Analysis Results',
  EXAMPLES_TITLE: 'API Format Example',
  TEST_COMMANDS_TITLE: 'Test Commands'
};