import React from 'react';
import { UI_TEXT } from '../utils/constants';
import { COLORS } from '../utils/theme';

const WhatsAppPreview = ({ userMessage, botResponse }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-xl font-semibold mb-4">{UI_TEXT.PREVIEW_TITLE}</h2>
      <div className="bg-[#e5ddd5] p-4 rounded-lg shadow-sm border border-gray-200 h-full min-h-[400px] flex flex-col" style={{ backgroundColor: COLORS.whatsapp.background }}>
        <div className="text-white p-3 rounded-t-lg flex items-center" style={{ backgroundColor: COLORS.whatsapp.header }}>
          <div className="w-8 h-8 bg-gray-300 rounded-full mr-3"></div>
          <div>
            <h3 className="font-semibold">OneTappe Bot</h3>
            <p className="text-xs opacity-80">Online</p>
          </div>
        </div>
      
      <div className="flex-1 overflow-y-auto py-4 space-y-4">
        {userMessage && (
          <div className="flex justify-end">
            <div className="p-3 rounded-lg max-w-[80%] shadow-sm" style={{ backgroundColor: COLORS.whatsapp.userMessage }}>
              <p className="text-sm">{userMessage}</p>
              <p className="text-right text-xs text-gray-500 mt-1">{new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
            </div>
          </div>
        )}
        
        {botResponse && (
          <div className="flex justify-start">
            <div className="p-3 rounded-lg max-w-[80%] shadow-sm" style={{ backgroundColor: COLORS.whatsapp.botMessage }}>
              <p className="text-sm">{botResponse}</p>
              <p className="text-right text-xs text-gray-500 mt-1">{new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</p>
            </div>
          </div>
        )}
      </div>
      
      <div className="bg-white p-2 rounded-lg flex items-center mt-2">
        <input 
          type="text" 
          className="flex-1 border-0 focus:ring-0 outline-none text-sm" 
          placeholder="Type a message" 
          disabled 
        />
        <button className="text-white rounded-full p-2 ml-2" style={{ backgroundColor: COLORS.whatsapp.header }} disabled>
          <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 0l-3 3a1 1 0 001.414 1.414L9 9.414V13a1 1 0 102 0V9.414l1.293 1.293a1 1 0 001.414-1.414z" clipRule="evenodd" />
          </svg>
        </button>
      </div>
    </div>
    </div>
  );
};

export default WhatsAppPreview;