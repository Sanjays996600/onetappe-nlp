import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import LoadingSpinner from './LoadingSpinner';
import { LANGUAGE_OPTIONS, UI_TEXT } from '../utils/constants';

const NLPForm = forwardRef(({ onSubmit, isLoading, initialMessage = '' }, ref) => {
  const [message, setMessage] = useState(initialMessage);
  const [languageSelection, setLanguageSelection] = useState('auto');
  
  // Expose setMessage function to parent component via ref
  useImperativeHandle(ref, () => ({
    setMessage
  }));
  
  // Update message when initialMessage prop changes
  useEffect(() => {
    if (initialMessage) {
      setMessage(initialMessage);
    }
  }, [initialMessage]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim()) return;
    
    onSubmit({
      message,
      languageSelection
    });
  };

  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-xl font-semibold mb-4">{UI_TEXT.FORM_TITLE}</h2>
      
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-1">
            Enter WhatsApp Command
          </label>
          <textarea
            id="message"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            rows="3"
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            placeholder="Type your command here (e.g., 'Show inventory', 'मेरा स्टॉक दिखाओ')"
            required
          />
        </div>
        
        <div className="mb-4">
          <label htmlFor="languageSelection" className="block text-sm font-medium text-gray-700 mb-1">
            Language Selection
          </label>
          <select
            id="languageSelection"
            className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
            value={languageSelection}
            onChange={(e) => setLanguageSelection(e.target.value)}
          >
            {LANGUAGE_OPTIONS.map(option => (
              <option key={option.value} value={option.value}>{option.label}</option>
            ))}
          </select>
        </div>
        
        <button
          type="submit"
          className={`w-full py-2 px-4 rounded-md text-white font-medium flex justify-center items-center ${isLoading ? 'bg-blue-400 cursor-not-allowed' : 'bg-blue-600 hover:bg-blue-700'}`}
          disabled={isLoading}
        >
          {isLoading ? (
            <>
              <LoadingSpinner size="sm" color="white" />
              <span className="ml-2">Processing...</span>
            </>
          ) : 'Submit'}
        </button>
      </form>
    </div>
  );
});

export default NLPForm;
