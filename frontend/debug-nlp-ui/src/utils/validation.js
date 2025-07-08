/**
 * Form validation utilities
 */

/**
 * Validates if a string is not empty
 * @param {string} value - The string to validate
 * @returns {boolean} True if the string is not empty
 */
export const isNotEmpty = (value) => {
  return typeof value === 'string' && value.trim().length > 0;
};

/**
 * Validates if a string is within a specified length range
 * @param {string} value - The string to validate
 * @param {number} min - Minimum length (inclusive)
 * @param {number} max - Maximum length (inclusive)
 * @returns {boolean} True if the string length is within range
 */
export const isWithinLength = (value, min, max) => {
  if (typeof value !== 'string') return false;
  const length = value.trim().length;
  return length >= min && length <= max;
};

/**
 * Validates if a value is one of the allowed options
 * @param {any} value - The value to validate
 * @param {Array} options - Array of allowed options
 * @returns {boolean} True if the value is in the options array
 */
export const isValidOption = (value, options) => {
  return options.includes(value);
};

/**
 * Validates a WhatsApp command
 * @param {string} command - The command to validate
 * @returns {Object} Validation result with isValid and errorMessage
 */
export const validateCommand = (command) => {
  if (!isNotEmpty(command)) {
    return {
      isValid: false,
      errorMessage: 'Command cannot be empty'
    };
  }
  
  if (!isWithinLength(command, 1, 500)) {
    return {
      isValid: false,
      errorMessage: 'Command must be between 1 and 500 characters'
    };
  }
  
  return {
    isValid: true,
    errorMessage: ''
  };
};

/**
 * Validates language selection
 * @param {string} language - The selected language code
 * @param {Array} availableLanguages - Array of available language codes
 * @returns {Object} Validation result with isValid and errorMessage
 */
export const validateLanguage = (language, availableLanguages) => {
  if (!isValidOption(language, availableLanguages)) {
    return {
      isValid: false,
      errorMessage: 'Please select a valid language'
    };
  }
  
  return {
    isValid: true,
    errorMessage: ''
  };
};

/**
 * Validates the entire NLP form
 * @param {Object} formData - The form data to validate
 * @param {string} formData.command - The command to validate
 * @param {string} formData.language - The selected language
 * @param {Array} availableLanguages - Array of available language codes
 * @returns {Object} Validation result with isValid, errors and a summary message
 */
export const validateNLPForm = (formData, availableLanguages) => {
  const { command, language } = formData;
  
  const commandValidation = validateCommand(command);
  const languageValidation = validateLanguage(language, availableLanguages);
  
  const isValid = commandValidation.isValid && languageValidation.isValid;
  
  const errors = {
    command: commandValidation.errorMessage,
    language: languageValidation.errorMessage
  };
  
  let errorSummary = '';
  if (!isValid) {
    const errorMessages = [];
    if (!commandValidation.isValid) errorMessages.push(commandValidation.errorMessage);
    if (!languageValidation.isValid) errorMessages.push(languageValidation.errorMessage);
    errorSummary = errorMessages.join('. ');
  }
  
  return {
    isValid,
    errors,
    errorSummary
  };
};