import React from 'react';
import { API_BASE_URL, API_ENDPOINTS, UI_TEXT } from '../utils/constants';

const Footer = () => {
  return (
    <footer className="mt-12 py-6 border-t border-gray-200">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex flex-col md:flex-row justify-between items-center">
          <div className="mb-4 md:mb-0">
            <p className="text-gray-600 text-sm">
              {UI_TEXT.APP_TITLE} - For testing multilingual WhatsApp commands
            </p>
          </div>
          <div className="flex space-x-4">
            <button 
              type="button"
              onClick={() => window.open(`${API_BASE_URL}${API_ENDPOINTS.HEALTH}`, '_blank')}
              className="text-blue-600 hover:text-blue-800 text-sm bg-transparent border-none p-0 cursor-pointer"
            >
              Check API Status
            </button>
            <span className="text-gray-400">|</span>
            <button 
              type="button"
              onClick={() => window.location.reload()}
              className="text-blue-600 hover:text-blue-800 text-sm bg-transparent border-none p-0 cursor-pointer"
            >
              Reset UI
            </button>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;