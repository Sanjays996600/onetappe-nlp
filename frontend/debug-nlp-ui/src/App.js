import React, { useState, useEffect, useRef } from 'react';
import NLPForm from './components/NLPForm';
import WhatsAppPreview from './components/WhatsAppPreview';
import ResultDisplay from './components/ResultDisplay';
import ErrorDisplay from './components/ErrorDisplay';
import ExampleResponse from './components/ExampleResponse';
import TestCommands from './components/TestCommands';
import Footer from './components/Footer';
import api from './services/api';
import { API_STATUS, UI_TEXT, API_BASE_URL } from './utils/constants';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [apiStatus, setApiStatus] = useState(API_STATUS.CHECKING);
  const [userMessage, setUserMessage] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [result, setResult] = useState(null);
  const [selectedCommand, setSelectedCommand] = useState('');
  
  // Reference to the NLPForm component
  const nlpFormRef = useRef(null);

  // Function to check API health
  const checkApiHealth = async () => {
    try {
      await api.checkHealth();
      setApiStatus(API_STATUS.ONLINE);
      setError(null);
    } catch (error) {
      setApiStatus(API_STATUS.OFFLINE);
      setError(`NLP API is not available. Please make sure the API is running at ${API_BASE_URL}`);
    }
  };

  // Check API health on component mount
  useEffect(() => {
    checkApiHealth();
  }, []);

  const handleSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    setUserMessage(formData.message);
    setBotResponse('');
    setResult(null);

    try {
      // Only pass language preference if not set to auto
      const languagePreference = formData.languageSelection !== 'auto' ? formData.languageSelection : null;
      
      const response = await api.processCommand(formData.message, languagePreference);
      
      setResult({
        language: response.detected_language || 'unknown',
        intent: response.intent || 'unknown',
        entities: response.entities || {},
        confidence: response.confidence || 0,
        rule_based_intent: response.rule_based_intent || 'unknown',
        ml_intent: response.ml_intent || 'unknown',
        rule_based_confidence: response.rule_based_confidence || 0,
        ml_confidence: response.ml_confidence || 0
      });
      
      setBotResponse(response.response || 'No response generated');
    } catch (error) {
      console.error('Error processing command:', error);
      setError(
        error.response?.data?.error ||
        'Failed to process your command. Please check the API connection.'
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 py-8 px-4">
      <div className="max-w-6xl mx-auto">
        <header className="mb-8 text-center">
          <h1 className="text-3xl font-bold text-gray-800">{UI_TEXT.APP_TITLE}</h1>
          <p className="text-gray-600 mt-2">
            {UI_TEXT.APP_SUBTITLE}
            <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
              apiStatus === API_STATUS.ONLINE ? 'bg-green-100 text-green-800' :
              apiStatus === API_STATUS.OFFLINE ? 'bg-red-100 text-red-800' : 'bg-yellow-100 text-yellow-800'
            }`}>
              API {apiStatus}
            </span>
          </p>
        </header>

        <ErrorDisplay 
          error={error} 
          onRetry={() => {
            setApiStatus('checking');
            setError(null);
            checkApiHealth();
          }} 
        />

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <NLPForm 
              onSubmit={handleSubmit} 
              isLoading={loading} 
              initialMessage={selectedCommand}
              ref={nlpFormRef}
            />
            {result && <ResultDisplay result={result} />}
            {!result && (
              <TestCommands 
                onSelectCommand={(command) => {
                  setSelectedCommand(command);
                  // If we have a ref to the form, we can update its message directly
                  if (nlpFormRef.current && typeof nlpFormRef.current.setMessage === 'function') {
                    nlpFormRef.current.setMessage(command);
                  }
                }} 
              />
            )}
          </div>
          
          <div>
            <WhatsAppPreview userMessage={userMessage} botResponse={botResponse} />
            {!result && <ExampleResponse />}
          </div>
        </div>
        
        <Footer />
      </div>
    </div>
  );
}

export default App;