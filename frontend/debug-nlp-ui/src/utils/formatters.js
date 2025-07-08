/**
 * Utility functions for formatting data
 */

/**
 * Formats a confidence score as a percentage
 * @param {number} score - Confidence score (0-1)
 * @param {number} decimals - Number of decimal places
 * @returns {string} Formatted percentage string
 */
export const formatConfidence = (score, decimals = 1) => {
  if (typeof score !== 'number' || isNaN(score)) {
    return 'N/A';
  }
  
  // Ensure score is between 0 and 1
  const normalizedScore = Math.max(0, Math.min(1, score));
  
  // Convert to percentage and format
  return `${(normalizedScore * 100).toFixed(decimals)}%`;
};

/**
 * Formats a timestamp to a readable date/time string
 * @param {string|number|Date} timestamp - Timestamp to format
 * @param {Object} options - Intl.DateTimeFormat options
 * @returns {string} Formatted date/time string
 */
export const formatTimestamp = (timestamp, options = {}) => {
  if (!timestamp) return 'N/A';
  
  try {
    const date = new Date(timestamp);
    
    // Default options
    const defaultOptions = {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    };
    
    // Merge with user options
    const mergedOptions = { ...defaultOptions, ...options };
    
    return new Intl.DateTimeFormat('en-US', mergedOptions).format(date);
  } catch (error) {
    console.error('Error formatting timestamp:', error);
    return 'Invalid Date';
  }
};

/**
 * Formats an API response for display
 * @param {Object} response - API response object
 * @returns {Object} Formatted response for UI display
 */
export const formatApiResponse = (response) => {
  if (!response) return null;
  
  try {
    const { detected_language, intent, entities, confidence, timestamp } = response;
    
    return {
      language: detected_language || 'Unknown',
      intent: intent || 'Unknown',
      confidence: formatConfidence(confidence),
      entities: entities || [],
      timestamp: formatTimestamp(timestamp || new Date())
    };
  } catch (error) {
    console.error('Error formatting API response:', error);
    return null;
  }
};

/**
 * Formats entity values for display
 * @param {Object} entity - Entity object from API
 * @returns {string} Formatted entity value
 */
export const formatEntityValue = (entity) => {
  if (!entity) return '';
  
  // Handle different entity value types
  if (typeof entity.value === 'object' && entity.value !== null) {
    // For complex entity values (objects)
    return JSON.stringify(entity.value);
  } else if (Array.isArray(entity.value)) {
    // For array values
    return entity.value.join(', ');
  } else {
    // For simple values
    return String(entity.value || '');
  }
};

/**
 * Truncates text to a maximum length with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length
 * @returns {string} Truncated text
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text || typeof text !== 'string') return '';
  
  if (text.length <= maxLength) return text;
  
  return `${text.substring(0, maxLength)}...`;
};

/**
 * Formats an error message for display
 * @param {Error|Object|string} error - Error object or message
 * @returns {string} Formatted error message
 */
export const formatErrorMessage = (error) => {
  if (!error) return 'An unknown error occurred';
  
  // If error is a string, return it directly
  if (typeof error === 'string') return error;
  
  // If error is an Error object or has a message property
  if (error.message) return error.message;
  
  // If error is an API response with error details
  if (error.error) return error.error;
  
  // If error is an object, stringify it
  if (typeof error === 'object') {
    try {
      return JSON.stringify(error);
    } catch (e) {
      return 'An error occurred';
    }
  }
  
  return 'An unknown error occurred';
};