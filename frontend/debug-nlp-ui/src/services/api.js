import axios from 'axios';
import { API_BASE_URL, API_ENDPOINTS } from '../utils/constants';

const api = {
  processCommand: async (message, languagePreference = null) => {
    try {
      const response = await axios.post(`${API_BASE_URL}${API_ENDPOINTS.PROCESS}`, {
        message,
        language_preference: languagePreference
      });
      return response.data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  },
  
  checkHealth: async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}${API_ENDPOINTS.HEALTH}`);
      return response.data;
    } catch (error) {
      console.error('Health check failed:', error);
      throw error;
    }
  }
};

export default api;