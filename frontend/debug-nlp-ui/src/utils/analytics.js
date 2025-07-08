/**
 * Analytics utilities for tracking user interactions
 * 
 * This module provides functions to track various events in the application.
 * It's designed to be easily integrated with different analytics providers.
 */

// Default configuration
const defaultConfig = {
  enabled: process.env.NODE_ENV === 'production', // Only enable in production by default
  debug: process.env.NODE_ENV === 'development', // Debug mode in development
  anonymizeIp: true // Anonymize IP addresses by default
};

// Current configuration
let config = { ...defaultConfig };

/**
 * Configure analytics settings
 * @param {Object} options - Configuration options
 */
export const configureAnalytics = (options = {}) => {
  config = { ...config, ...options };
};

/**
 * Track a page view
 * @param {string} pageName - Name of the page
 * @param {Object} properties - Additional properties
 */
export const trackPageView = (pageName, properties = {}) => {
  if (!config.enabled) return;
  
  if (config.debug) {
    console.log('[Analytics] Page View:', pageName, properties);
  }
  
  // Implementation would connect to actual analytics service
  // Example: Google Analytics, Mixpanel, etc.
};

/**
 * Track a user event
 * @param {string} category - Event category
 * @param {string} action - Event action
 * @param {string} label - Event label
 * @param {Object} properties - Additional properties
 */
export const trackEvent = (category, action, label = '', properties = {}) => {
  if (!config.enabled) return;
  
  if (config.debug) {
    console.log('[Analytics] Event:', { category, action, label, ...properties });
  }
  
  // Implementation would connect to actual analytics service
};

/**
 * Track an API call
 * @param {string} endpoint - API endpoint
 * @param {string} method - HTTP method
 * @param {number} status - HTTP status code
 * @param {number} duration - Call duration in ms
 */
export const trackApiCall = (endpoint, method = 'GET', status = 200, duration = 0) => {
  if (!config.enabled) return;
  
  trackEvent('API', method, endpoint, { status, duration });
};

/**
 * Track a form submission
 * @param {string} formName - Name of the form
 * @param {Object} formData - Form data (sensitive data should be excluded)
 * @param {boolean} success - Whether submission was successful
 */
export const trackFormSubmission = (formName, formData = {}, success = true) => {
  if (!config.enabled) return;
  
  // Remove any sensitive data
  const safeData = { ...formData };
  delete safeData.password;
  delete safeData.token;
  
  trackEvent('Form', success ? 'Submit Success' : 'Submit Error', formName, safeData);
};

/**
 * Track an error
 * @param {string} errorType - Type of error
 * @param {string} errorMessage - Error message
 * @param {Object} errorDetails - Additional error details
 */
export const trackError = (errorType, errorMessage, errorDetails = {}) => {
  if (!config.enabled) return;
  
  trackEvent('Error', errorType, errorMessage, errorDetails);
};

/**
 * Track NLP command submission
 * @param {string} command - The command text
 * @param {string} language - The language code
 * @param {boolean} success - Whether processing was successful
 */
export const trackNlpCommand = (command, language, success = true) => {
  if (!config.enabled) return;
  
  // Don't log the full command for privacy, just length and first few chars
  const commandInfo = {
    length: command.length,
    preview: command.substring(0, 10) + (command.length > 10 ? '...' : ''),
    language,
    success
  };
  
  trackEvent('NLP', 'Command', success ? 'Success' : 'Error', commandInfo);
};

/**
 * Track feature usage
 * @param {string} featureName - Name of the feature
 * @param {Object} properties - Additional properties
 */
export const trackFeatureUsage = (featureName, properties = {}) => {
  if (!config.enabled) return;
  
  trackEvent('Feature', 'Use', featureName, properties);
};

/**
 * Analytics hook for React components
 * @returns {Object} Analytics tracking functions
 */
export const useAnalytics = () => {
  return {
    trackPageView,
    trackEvent,
    trackApiCall,
    trackFormSubmission,
    trackError,
    trackNlpCommand,
    trackFeatureUsage
  };
};