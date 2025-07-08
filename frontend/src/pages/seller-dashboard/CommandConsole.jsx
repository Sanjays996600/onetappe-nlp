import React, { useState, useRef, useEffect } from 'react';
import Sidebar from './Sidebar';
import Header from './Header';

const CommandConsole = () => {
  const [input, setInput] = useState('');
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const messagesEndRef = useRef(null);

  // Sample product data (simulating database)
  const dummyProducts = [
    { id: 1, name: 'Organic Rice', price: 120, stock: 50 },
    { id: 2, name: 'Wheat Flour', price: 45, stock: 30 },
    { id: 3, name: 'Spice Mix', price: 85, stock: 15 },
    { id: 4, name: 'Cooking Oil', price: 110, stock: 25 },
  ];

  // Sample low stock items
  const lowStockItems = dummyProducts.filter(product => product.stock < 20);

  // Sample report data
  const todayReport = {
    date: new Date().toLocaleDateString(),
    totalSales: 4250,
    orderCount: 12,
    topProduct: 'Organic Rice'
  };

  // Auto-scroll to bottom when messages update
  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  const processCommand = (command) => {
    // Add user message
    setMessages(prev => [...prev, { type: 'user', text: command }]);
    
    setIsProcessing(true);
    
    // Simulate processing delay
    setTimeout(() => {
      let response;
      
      // Process commands
      if (command.toLowerCase().includes('show my products')) {
        response = {
          type: 'system',
          text: 'Here are your products:',
          data: dummyProducts
        };
      } else if (command.toLowerCase().includes('send today\'s report')) {
        response = {
          type: 'system',
          text: 'Here is your sales report for today:',
          report: todayReport
        };
      } else if (command.toLowerCase().includes('show low stock')) {
        response = {
          type: 'system',
          text: 'These items are running low on stock:',
          data: lowStockItems
        };
      } else {
        response = {
          type: 'system',
          text: 'Sorry, I don\'t understand that command. Try "show my products", "send today\'s report", or "show low stock items"'
        };
      }
      
      setMessages(prev => [...prev, response]);
      setIsProcessing(false);
    }, 1000);
    
    setInput('');
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (input.trim() && !isProcessing) {
      processCommand(input.trim());
    }
  };

  const handleQuickCommand = (command) => {
    if (!isProcessing) {
      setInput(command);
      processCommand(command);
    }
  };

  // Render different message types
  const renderMessage = (message, index) => {
    if (message.type === 'user') {
      return (
        <div key={index} className="flex justify-end mb-4">
          <div className="bg-teal-600 text-white rounded-lg py-2 px-4 max-w-[80%]">
            {message.text}
          </div>
        </div>
      );
    } else {
      // System message
      return (
        <div key={index} className="flex justify-start mb-4">
          <div className="bg-gray-200 rounded-lg py-2 px-4 max-w-[80%]">
            <p>{message.text}</p>
            
            {/* Product list */}
            {message.data && (
              <div className="mt-2">
                <table className="min-w-full bg-white border border-gray-300 rounded-md overflow-hidden">
                  <thead className="bg-gray-100">
                    <tr>
                      <th className="py-2 px-3 text-left text-xs font-medium text-gray-600">Name</th>
                      <th className="py-2 px-3 text-left text-xs font-medium text-gray-600">Price</th>
                      <th className="py-2 px-3 text-left text-xs font-medium text-gray-600">Stock</th>
                    </tr>
                  </thead>
                  <tbody>
                    {message.data.map(product => (
                      <tr key={product.id} className="border-t border-gray-300">
                        <td className="py-2 px-3 text-sm">{product.name}</td>
                        <td className="py-2 px-3 text-sm">₹{product.price}</td>
                        <td className="py-2 px-3 text-sm">
                          <span className={product.stock < 20 ? 'text-red-600 font-medium' : ''}>
                            {product.stock}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
            
            {/* Report */}
            {message.report && (
              <div className="mt-2 bg-white p-3 border border-gray-300 rounded-md">
                <h4 className="font-medium text-gray-800">Sales Report: {message.report.date}</h4>
                <div className="grid grid-cols-2 gap-2 mt-2">
                  <div>
                    <p className="text-sm text-gray-600">Total Sales</p>
                    <p className="font-medium">₹{message.report.totalSales}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Orders</p>
                    <p className="font-medium">{message.report.orderCount}</p>
                  </div>
                  <div>
                    <p className="text-sm text-gray-600">Top Product</p>
                    <p className="font-medium">{message.report.topProduct}</p>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      );
    }
  };

  return (
    <div className="flex h-screen bg-gray-100">
      <Sidebar />
      <div className="flex-1 flex flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-100 p-6">
          <div className="max-w-3xl mx-auto bg-white rounded-lg shadow-md flex flex-col h-[calc(100vh-10rem)]">
            <div className="p-4 border-b border-gray-200">
              <h2 className="text-xl font-semibold text-gray-800">WhatsApp Command Console</h2>
              <p className="text-sm text-gray-600">Test your WhatsApp commands here</p>
            </div>
            
            {/* Quick commands */}
            <div className="p-3 bg-gray-50 border-b border-gray-200 flex flex-wrap gap-2">
              <button 
                onClick={() => handleQuickCommand('show my products')}
                disabled={isProcessing}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 text-sm py-1 px-3 rounded-full transition-colors"
              >
                show my products
              </button>
              <button 
                onClick={() => handleQuickCommand('send today\'s report')}
                disabled={isProcessing}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 text-sm py-1 px-3 rounded-full transition-colors"
              >
                send today's report
              </button>
              <button 
                onClick={() => handleQuickCommand('show low stock items')}
                disabled={isProcessing}
                className="bg-gray-200 hover:bg-gray-300 text-gray-800 text-sm py-1 px-3 rounded-full transition-colors"
              >
                show low stock items
              </button>
            </div>
            
            {/* Messages area */}
            <div className="flex-1 p-4 overflow-y-auto">
              {messages.length === 0 ? (
                <div className="h-full flex items-center justify-center text-gray-500">
                  <p>Send a command to get started</p>
                </div>
              ) : (
                messages.map((message, index) => renderMessage(message, index))
              )}
              <div ref={messagesEndRef} />
            </div>
            
            {/* Input area */}
            <div className="p-4 border-t border-gray-200">
              <form onSubmit={handleSubmit} className="flex">
                <input
                  type="text"
                  value={input}
                  onChange={handleInputChange}
                  placeholder="Type a command..."
                  className="flex-1 border border-gray-300 rounded-l-md py-2 px-4 focus:outline-none focus:ring-2 focus:ring-teal-500 focus:border-transparent"
                  disabled={isProcessing}
                />
                <button
                  type="submit"
                  disabled={!input.trim() || isProcessing}
                  className={`bg-teal-600 hover:bg-teal-700 text-white px-4 rounded-r-md transition-colors ${(!input.trim() || isProcessing) ? 'opacity-50 cursor-not-allowed' : ''}`}
                >
                  {isProcessing ? (
                    <span className="flex items-center">
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Processing
                    </span>
                  ) : 'Send'}
                </button>
              </form>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
};

export default CommandConsole;