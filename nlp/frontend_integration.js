/**
 * Example frontend integration for the WhatsApp Command Intent Handler
 * 
 * This file demonstrates how to connect the React frontend with the NLP backend
 * to process commands and display appropriate responses.
 */

// Example API client for the intent handler
class IntentHandlerClient {
  constructor(baseUrl = '/api') {
    this.baseUrl = baseUrl;
  }

  /**
   * Parse a command message
   * @param {string} message - The command message
   * @param {string} userId - Optional user ID for context
   * @returns {Promise<Object>} - Parsed intent and entities
   */
  async parseCommand(message, userId = null) {
    try {
      const response = await fetch(`${this.baseUrl}/parse-command`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message,
          user_id: userId,
          context: {}
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to parse command:', error);
      throw error;
    }
  }

  /**
   * Get supported intents and example commands
   * @returns {Promise<Object>} - List of supported intents
   */
  async getSupportedIntents() {
    try {
      const response = await fetch(`${this.baseUrl}/supported-intents`);
      
      if (!response.ok) {
        throw new Error(`Error: ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      console.error('Failed to get supported intents:', error);
      throw error;
    }
  }
}

/**
 * Example React hook for using the intent handler
 */
function useIntentHandler() {
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState(null);
  const client = React.useMemo(() => new IntentHandlerClient(), []);

  /**
   * Process a command message
   * @param {string} message - The command message
   * @returns {Promise<Object>} - The processed result
   */
  const processCommand = React.useCallback(async (message) => {
    setLoading(true);
    setError(null);
    
    try {
      const result = await client.parseCommand(message);
      setLoading(false);
      return result;
    } catch (err) {
      setError(err.message);
      setLoading(false);
      throw err;
    }
  }, [client]);

  return {
    processCommand,
    loading,
    error,
    client,
  };
}

/**
 * Example integration with the CommandConsole component
 */
function CommandConsoleWithNLP() {
  const [input, setInput] = React.useState('');
  const [messages, setMessages] = React.useState([]);
  const { processCommand, loading } = useIntentHandler();
  
  const handleSendMessage = async () => {
    if (!input.trim()) return;
    
    // Add user message to the chat
    const userMessage = { type: 'user', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    
    try {
      // Process the command with NLP
      const result = await processCommand(input);
      
      // Handle the intent based on the result
      let responseMessage;
      
      switch (result.intent) {
        case 'get_inventory':
          responseMessage = { 
            type: 'system', 
            text: 'Here are your products:', 
            data: { type: 'products' } 
          };
          break;
          
        case 'get_low_stock':
          responseMessage = { 
            type: 'system', 
            text: 'These items are running low on stock:', 
            data: { type: 'low_stock' } 
          };
          break;
          
        case 'get_report':
          const range = result.entities.range || 'today';
          responseMessage = { 
            type: 'system', 
            text: `Generating ${range}'s report for you:`, 
            data: { type: 'report', range } 
          };
          break;
          
        case 'add_product':
          responseMessage = { 
            type: 'system', 
            text: `Adding new product: ${result.entities.name} with price ${result.entities.price} and stock ${result.entities.stock}`, 
            data: { type: 'confirmation' } 
          };
          break;
          
        case 'edit_stock':
          responseMessage = { 
            type: 'system', 
            text: `Updating stock of ${result.entities.name} to ${result.entities.stock}`, 
            data: { type: 'confirmation' } 
          };
          break;
          
        case 'get_orders':
          responseMessage = { 
            type: 'system', 
            text: 'Here are your recent orders:', 
            data: { type: 'orders' } 
          };
          break;
          
        default:
          responseMessage = { 
            type: 'system', 
            text: "I'm not sure what you want to do. Try one of the quick commands below.", 
            data: { type: 'help' } 
          };
      }
      
      // Add system response to the chat
      setMessages(prev => [...prev, responseMessage]);
      
    } catch (error) {
      // Handle error
      setMessages(prev => [...prev, { 
        type: 'system', 
        text: 'Sorry, I encountered an error processing your command.', 
        error: true 
      }]);
    }
  };
  
  return (
    <div className="command-console">
      {/* Message display area */}
      <div className="message-container">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            {msg.text}
            {msg.data && renderMessageData(msg.data)}
          </div>
        ))}
        {loading && <div className="message system">Processing...</div>}
      </div>
      
      {/* Input area */}
      <div className="input-container">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Type a command..."
          disabled={loading}
        />
        <button onClick={handleSendMessage} disabled={loading || !input.trim()}>
          Send
        </button>
      </div>
      
      {/* Quick commands */}
      <div className="quick-commands">
        <button onClick={() => setInput('Show my products')}>Products</button>
        <button onClick={() => setInput('Show low stock items')}>Low Stock</button>
        <button onClick={() => setInput("Send today's report")}>Report</button>
      </div>
    </div>
  );
}

/**
 * Helper function to render different types of message data
 */
function renderMessageData(data) {
  switch (data.type) {
    case 'products':
      return <div className="data-table">Product table would render here</div>;
      
    case 'low_stock':
      return <div className="data-table">Low stock items would render here</div>;
      
    case 'report':
      return <div className="report">Report for {data.range} would render here</div>;
      
    case 'confirmation':
      return <div className="confirmation">✅ Action confirmed</div>;
      
    case 'orders':
      return <div className="data-table">Orders would render here</div>;
      
    case 'help':
      return (
        <div className="help">
          Try commands like:
          <ul>
            <li>"Show my products"</li>
            <li>"Send today's report"</li>
            <li>"Show low stock items"</li>
            <li>"Add new product Rice 50rs 20qty"</li>
          </ul>
        </div>
      );
      
    default:
      return null;
  }
}