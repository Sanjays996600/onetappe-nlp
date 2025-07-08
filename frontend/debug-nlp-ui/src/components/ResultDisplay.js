import React from 'react';
import { UI_TEXT } from '../utils/constants';

const ResultDisplay = ({ result }) => {
  const {
    language,
    intent,
    entities,
    confidence,
    rule_based_intent,
    ml_intent,
    rule_based_confidence,
    ml_confidence
  } = result;

  // Format entities for display
  const formatEntities = (entities) => {
    if (!entities || Object.keys(entities).length === 0) {
      return 'None';
    }
    
    return (
      <div className="space-y-1">
        {Object.entries(entities).map(([key, value]) => (
          <div key={key} className="flex">
            <span className="font-medium mr-2">{key}:</span>
            <span>{typeof value === 'object' ? JSON.stringify(value) : value.toString()}</span>
          </div>
        ))}
      </div>
    );
  };

  return (
    <div className="mt-6 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-xl font-semibold mb-4">{UI_TEXT.RESULTS_TITLE}</h2>
      
      <div className="space-y-4">
        <div>
          <h3 className="text-md font-medium text-gray-700">Detected Language</h3>
          <div className="mt-1 p-2 bg-gray-50 rounded">
            <span className="font-mono">{language}</span>
            {language === 'en' && <span className="ml-2 text-gray-500">(English)</span>}
            {language === 'hi' && <span className="ml-2 text-gray-500">(Hindi)</span>}
            {language === 'mixed' && <span className="ml-2 text-gray-500">(Hinglish)</span>}
          </div>
        </div>
        
        <div>
          <h3 className="text-md font-medium text-gray-700">Predicted Intent</h3>
          <div className="mt-1 p-2 bg-gray-50 rounded">
            <div className="flex items-center">
              <span className="font-mono">{intent}</span>
              <span className="ml-2 text-sm bg-blue-100 text-blue-800 py-0.5 px-2 rounded">
                {(confidence * 100).toFixed(1)}% confidence
              </span>
            </div>
            
            <div className="mt-2 text-sm text-gray-500">
              <div>Rule-based: {rule_based_intent} ({(rule_based_confidence * 100).toFixed(1)}%)</div>
              <div>ML-based: {ml_intent} ({(ml_confidence * 100).toFixed(1)}%)</div>
            </div>
          </div>
        </div>
        
        <div>
          <h3 className="text-md font-medium text-gray-700">Extracted Entities</h3>
          <div className="mt-1 p-2 bg-gray-50 rounded">
            {formatEntities(entities)}
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultDisplay;