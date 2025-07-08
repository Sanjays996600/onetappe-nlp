import sys
import os
import unittest
from unittest.mock import patch, MagicMock, call
import json
import logging
from typing import Dict, Any
import time

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(logs_dir, exist_ok=True)

log_file = os.path.join(logs_dir, 'test_command_response_loop.log')

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Mock WhatsApp Gateway class
class MockWhatsAppGateway:
    def __init__(self):
        self.sent_messages = []
        self.message_history = []
    
    def send_message(self, phone_number, message_text):
        """Send a message to a WhatsApp number"""
        message = {
            "to": phone_number,
            "text": message_text,
            "timestamp": "2023-06-01T12:00:00Z"  # Mock timestamp
        }
        self.sent_messages.append(message)
        return {"status": "success", "message_id": f"mock-id-{len(self.sent_messages)}"}
    
    def receive_message(self, phone_number, message_text):
        """Simulate receiving a message from a WhatsApp number"""
        message = {
            "from": phone_number,
            "text": message_text,
            "timestamp": "2023-06-01T12:00:00Z"  # Mock timestamp
        }
        self.message_history.append(message)
        return message
    
    def get_last_sent_message(self):
        """Get the last message sent through the gateway"""
        return self.sent_messages[-1] if self.sent_messages else None

# WhatsApp Integration Handler class
class WhatsAppIntegrationHandler:
    def __init__(self, gateway):
        self.gateway = gateway
        self.user_sessions = {}  # Store user session data
    
    def process_incoming_message(self, phone_number, message_text, user_id=None):
        """Process an incoming WhatsApp message and send a response"""
        # If no user_id provided, use phone number as identifier
        if not user_id:
            user_id = f"whatsapp-{phone_number}"
        
        logger.info(f"Processing message from {phone_number}: '{message_text}'")
        
        # Parse the message using the NLP system
        from nlp.multilingual_handler import parse_multilingual_command
        parsed_result = parse_multilingual_command(message_text)
        logger.info(f"Parsed result: {json.dumps(parsed_result, ensure_ascii=False)}")
        
        # Store the session data for this user
        self.user_sessions[user_id] = {
            "last_intent": parsed_result["intent"],
            "language": parsed_result["language"],
            "timestamp": "2023-06-01T12:00:00Z"  # Mock timestamp
        }
        
        # Route the command to get a response
        from nlp.command_router import route_command
        response = route_command(parsed_result, user_id=user_id)
        logger.info(f"Response: {response}")
        
        # Send the response back via WhatsApp
        self.gateway.send_message(phone_number, response)
        
        return response
    
    def get_user_session(self, user_id):
        """Get the session data for a user"""
        return self.user_sessions.get(user_id, {})

# Command Response Loop class
class CommandResponseLoop:
    def __init__(self, handler):
        self.handler = handler
        self.running = False
        self.message_queue = []
    
    def add_message_to_queue(self, phone_number, message_text):
        """Add a message to the processing queue"""
        self.message_queue.append({"phone_number": phone_number, "message_text": message_text})
    
    def start(self):
        """Start the command response loop"""
        self.running = True
        logger.info("Command response loop started")
        
        while self.running and self.message_queue:
            # Process the next message in the queue
            message = self.message_queue.pop(0)
            phone_number = message["phone_number"]
            message_text = message["message_text"]
            
            try:
                # Process the message
                self.handler.process_incoming_message(phone_number, message_text)
                logger.info(f"Processed message from {phone_number}: '{message_text}'")
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
            
            # Simulate a small delay between processing messages
            time.sleep(0.1)
    
    def stop(self):
        """Stop the command response loop"""
        self.running = False
        logger.info("Command response loop stopped")

class TestCommandResponseLoop(unittest.TestCase):
    
    def setUp(self):
        # Initialize the mock gateway and handler
        self.gateway = MockWhatsAppGateway()
        self.handler = WhatsAppIntegrationHandler(self.gateway)
        self.loop = CommandResponseLoop(self.handler)
        self.phone_number = "1234567890"
        self.user_id = f"whatsapp-{self.phone_number}"
    
    @patch("nlp.multilingual_handler.parse_multilingual_command")
    @patch("nlp.command_router.route_command")
    def test_single_message_processing(self, mock_route_command, mock_parse_command):
        """Test processing of a single message through the command response loop"""
        # Set up the mocks
        mock_parse_command.return_value = {
            "intent": "get_inventory",
            "entities": {},
            "language": "en"
        }
        mock_route_command.return_value = "Here is your inventory: Item 1, Item 2, Item 3"
        
        # Add a message to the queue
        message = "Show my inventory"
        self.loop.add_message_to_queue(self.phone_number, message)
        
        # Start the loop
        self.loop.start()
        
        # Verify the message was processed correctly
        mock_parse_command.assert_called_once_with(message)
        mock_route_command.assert_called_once()
        
        # Verify a response was sent via WhatsApp
        last_message = self.gateway.get_last_sent_message()
        self.assertIsNotNone(last_message)
        self.assertEqual(last_message["to"], self.phone_number)
        self.assertEqual(last_message["text"], "Here is your inventory: Item 1, Item 2, Item 3")
        
        # Verify user session was updated
        session = self.handler.get_user_session(self.user_id)
        self.assertEqual(session["last_intent"], "get_inventory")
        self.assertEqual(session["language"], "en")
    
    @patch("nlp.multilingual_handler.parse_multilingual_command")
    @patch("nlp.command_router.route_command")
    def test_multiple_message_processing(self, mock_route_command, mock_parse_command):
        """Test processing of multiple messages through the command response loop"""
        # Set up the mocks to return different values for different calls
        mock_parse_command.side_effect = [
            {"intent": "get_inventory", "entities": {}, "language": "en"},
            {"intent": "get_low_stock", "entities": {}, "language": "en"},
            {"intent": "search_product", "entities": {"product_name": "rice"}, "language": "en"}
        ]
        mock_route_command.side_effect = [
            "Here is your inventory: Item 1, Item 2, Item 3",
            "Low stock items: Item 2",
            "Rice is in stock: 50 units"
        ]
        
        # Add multiple messages to the queue
        messages = [
            "Show my inventory",
            "Show low stock items",
            "Search for rice"
        ]
        for message in messages:
            self.loop.add_message_to_queue(self.phone_number, message)
        
        # Start the loop
        self.loop.start()
        
        # Verify the messages were processed correctly
        self.assertEqual(mock_parse_command.call_count, 3)
        mock_parse_command.assert_has_calls([
            call("Show my inventory"),
            call("Show low stock items"),
            call("Search for rice")
        ])
        
        self.assertEqual(mock_route_command.call_count, 3)
        
        # Verify responses were sent via WhatsApp
        self.assertEqual(len(self.gateway.sent_messages), 3)
        self.assertEqual(self.gateway.sent_messages[0]["to"], self.phone_number)
        self.assertEqual(self.gateway.sent_messages[0]["text"], "Here is your inventory: Item 1, Item 2, Item 3")
        self.assertEqual(self.gateway.sent_messages[1]["to"], self.phone_number)
        self.assertEqual(self.gateway.sent_messages[1]["text"], "Low stock items: Item 2")
        self.assertEqual(self.gateway.sent_messages[2]["to"], self.phone_number)
        self.assertEqual(self.gateway.sent_messages[2]["text"], "Rice is in stock: 50 units")
        
        # Verify user session was updated with the last intent
        session = self.handler.get_user_session(self.user_id)
        self.assertEqual(session["last_intent"], "search_product")
        self.assertEqual(session["language"], "en")
    
    @patch("nlp.multilingual_handler.parse_multilingual_command")
    @patch("nlp.command_router.route_command")
    def test_error_handling_in_loop(self, mock_route_command, mock_parse_command):
        """Test handling of errors during message processing in the loop"""
        # Set up the mocks to raise an exception for the second message
        mock_parse_command.side_effect = [
            {"intent": "get_inventory", "entities": {}, "language": "en"},
            Exception("Test error"),
            {"intent": "search_product", "entities": {"product_name": "rice"}, "language": "en"}
        ]
        mock_route_command.side_effect = [
            "Here is your inventory: Item 1, Item 2, Item 3",
            "Rice is in stock: 50 units"
        ]
        
        # Add multiple messages to the queue
        messages = [
            "Show my inventory",
            "Invalid command",
            "Search for rice"
        ]
        for message in messages:
            self.loop.add_message_to_queue(self.phone_number, message)
        
        # Start the loop
        self.loop.start()
        
        # Verify the messages were processed correctly
        self.assertEqual(mock_parse_command.call_count, 3)
        
        # Verify responses were sent via WhatsApp for the successful messages
        self.assertEqual(len(self.gateway.sent_messages), 2)
        self.assertEqual(self.gateway.sent_messages[0]["to"], self.phone_number)
        self.assertEqual(self.gateway.sent_messages[0]["text"], "Here is your inventory: Item 1, Item 2, Item 3")
        self.assertEqual(self.gateway.sent_messages[1]["to"], self.phone_number)
        self.assertEqual(self.gateway.sent_messages[1]["text"], "Rice is in stock: 50 units")
        
        # Verify user session was updated with the last successful intent
        session = self.handler.get_user_session(self.user_id)
        self.assertEqual(session["last_intent"], "search_product")
        self.assertEqual(session["language"], "en")
    
    @patch("nlp.multilingual_handler.parse_multilingual_command")
    @patch("nlp.command_router.route_command")
    def test_multilingual_message_processing(self, mock_route_command, mock_parse_command):
        """Test processing of multilingual messages through the command response loop"""
        # Set up the mocks to return different values for different calls
        mock_parse_command.side_effect = [
            {"intent": "get_inventory", "entities": {}, "language": "en"},
            {"intent": "get_inventory", "entities": {}, "language": "hi"}
        ]
        mock_route_command.side_effect = [
            "Here is your inventory: Item 1, Item 2, Item 3",
            "आपका इन्वेंटरी: आइटम 1, आइटम 2, आइटम 3"
        ]
        
        # Add multilingual messages to the queue
        messages = [
            "Show my inventory",  # English
            "मेरा इन्वेंटरी दिखाओ"  # Hindi
        ]
        for message in messages:
            self.loop.add_message_to_queue(self.phone_number, message)
        
        # Start the loop
        self.loop.start()
        
        # Verify the messages were processed correctly
        self.assertEqual(mock_parse_command.call_count, 2)
        mock_parse_command.assert_has_calls([
            call("Show my inventory"),
            call("मेरा इन्वेंटरी दिखाओ")
        ])
        
        self.assertEqual(mock_route_command.call_count, 2)
        
        # Verify responses were sent via WhatsApp
        self.assertEqual(len(self.gateway.sent_messages), 2)
        self.assertEqual(self.gateway.sent_messages[0]["to"], self.phone_number)
        self.assertEqual(self.gateway.sent_messages[0]["text"], "Here is your inventory: Item 1, Item 2, Item 3")
        self.assertEqual(self.gateway.sent_messages[1]["to"], self.phone_number)
        self.assertEqual(self.gateway.sent_messages[1]["text"], "आपका इन्वेंटरी: आइटम 1, आइटम 2, आइटम 3")
        
        # Verify user session was updated with the last intent and language
        session = self.handler.get_user_session(self.user_id)
        self.assertEqual(session["last_intent"], "get_inventory")
        self.assertEqual(session["language"], "hi")

if __name__ == "__main__":
    unittest.main()