import React, { useState } from 'react';
import { UI_TEXT } from '../utils/constants';

const TestCommands = ({ onSelectCommand }) => {
  const [isOpen, setIsOpen] = useState(false);
  
  const commandCategories = [
    {
      name: 'Inventory Queries',
      commands: [
        { text: 'Show my inventory', language: 'English' },
        { text: 'मेरा स्टॉक दिखाओ', language: 'Hindi' },
        { text: 'Stock dikhao', language: 'Hinglish' },
        { text: 'Show low stock items', language: 'English' },
      ]
    },
    {
      name: 'Order Queries',
      commands: [
        { text: 'Show my orders', language: 'English' },
        { text: 'मेरे ऑर्डर दिखाओ', language: 'Hindi' },
        { text: 'Last 5 orders dikhao', language: 'Hinglish' },
        { text: 'Show pending orders', language: 'English' },
      ]
    },
    {
      name: 'Inventory Updates',
      commands: [
        { text: 'Add 10 units of product ABC123', language: 'English' },
        { text: 'प्रोडक्ट XYZ789 में 5 यूनिट जोड़ें', language: 'Hindi' },
        { text: 'Update stock of DEF456 to 20 units', language: 'English' },
      ]
    },
    {
      name: 'Reports',
      commands: [
        { text: 'Show sales report', language: 'English' },
        { text: 'पिछले महीने का रिपोर्ट दिखाओ', language: 'Hindi' },
        { text: 'Top products report dikhao', language: 'Hinglish' },
      ]
    }
  ];
  
  return (
    <div className="mt-6 bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <div className="flex justify-between items-center cursor-pointer" onClick={() => setIsOpen(!isOpen)}>
        <h2 className="text-xl font-semibold">{UI_TEXT.TEST_COMMANDS_TITLE}</h2>
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
        <div className="mt-4 space-y-6">
          <p className="text-sm text-gray-600">Click on any command to use it in the form above.</p>
          
          {commandCategories.map((category, index) => (
            <div key={index} className="space-y-2">
              <h3 className="text-md font-medium text-gray-700">{category.name}</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                {category.commands.map((command, cmdIndex) => (
                  <button
                    key={cmdIndex}
                    onClick={() => onSelectCommand(command.text)}
                    className="text-left p-2 border border-gray-200 rounded hover:bg-blue-50 hover:border-blue-300 transition-colors"
                  >
                    <div className="text-sm">{command.text}</div>
                    <div className="text-xs text-gray-500">{command.language}</div>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default TestCommands;