import React, { useState } from 'react';
import { UI_TEXT, API_BASE_URL, API_ENDPOINTS } from '../utils/constants';

const ExampleResponse = () => {
  const [isOpen, setIsOpen] = useState(false);
  
  const exampleRequest = {
    message: "Show my inventory",
    language_preference: null // Auto-detect
  };
  
  const exampleResponse = {
    detected_language: "en",
    intent: "inventory_query",
    entities: {
      product_id: null,
      quantity: null,
      date_range: null
    },
    confidence: 0.95,
    rule_based_intent: "inventory_query",
    ml_intent: "inventory_query",
    rule_based_confidence: 0.9,
    ml_confidence: 0.98,
    response: "Here is your current inventory: Product A: 25 units, Product B: 10 units, Product C: 15 units."
  };
  
  return (
    <div className="mt-6 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <div className="flex justify-between items-center cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
        <h2 className="text-xl font-semibold">{UI_TEXT.EXAMPLES_TITLE}</h2>
        <button className="text-blue-600 hover:text-blue-800">
          {isOpen ? (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M14.707 12.707a1 1 0 01-1.414 0L10 9.414l-3.293 3.293a1 1 0 01-1.414-1.414l4-4a1 1 0 011.414 0l4 4a1 1 0 010 1.414z" clipRule="evenodd" />
            </svg>
          ) : (
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          )}
        </button>
      </div>
      
      {isOpen && (
        <div className="mt-4 space-y-4">
          <div>
            <h3 className="text-md font-medium text-gray-700 mb-2">Example Request:</h3>
            <pre className="bg-gray-50 p-3 rounded overflow-x-auto text-sm">
              {JSON.stringify(exampleRequest, null, 2)}
            </pre>
          </div>
          
          <div>
            <h3 className="text-md font-medium text-gray-700 mb-2">Example Response:</h3>
            <pre className="bg-gray-50 p-3 rounded overflow-x-auto text-sm">
              {JSON.stringify(exampleResponse, null, 2)}
            </pre>
          </div>
          
          <div className="text-sm text-gray-600">
            <p>The API endpoint is available at: <code className="bg-gray-100 px-1 py-0.5 rounded">{API_BASE_URL}{API_ENDPOINTS.PROCESS}</code></p>
            <p className="mt-1">Health check endpoint: <code className="bg-gray-100 px-1 py-0.5 rounded">{API_BASE_URL}{API_ENDPOINTS.HEALTH}</code></p>
          </div>
        </div>
      )}
    </div>
  );
};

export default ExampleResponse;