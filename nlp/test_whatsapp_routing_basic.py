import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import json
import logging
from typing import Dict, Any

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command

# Setup logging
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(logs_dir, exist_ok=True)

log_file = os.path.join(logs_dir, 'test_whatsapp_routing.log')

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
        import nlp.multilingual_handler
        parsed_result = nlp.multilingual_handler.parse_multilingual_command(message_text)
        logger.info(f"Parsed result: {json.dumps(parsed_result, ensure_ascii=False)}")
        
        # Store the session data for this user
        self.user_sessions[user_id] = {
            "last_intent": parsed_result["intent"],
            "language": parsed_result["language"],
            "timestamp": "2023-06-01T12:00:00Z"  # Mock timestamp
        }
        
        # Route the command to get a response
        import nlp.command_router
        response = nlp.command_router.route_command(parsed_result, user_id=user_id)
        logger.info(f"Response: {response}")
        
        # Send the response back via WhatsApp
        self.gateway.send_message(phone_number, response)
        
        return response
    
    def get_user_session(self, user_id):
        """Get the session data for a user"""
        return self.user_sessions.get(user_id, {})

class TestWhatsAppRoutingBasic(unittest.TestCase):
    
    def setUp(self):
        # Initialize the mock gateway and handler
        self.gateway = MockWhatsAppGateway()
        self.handler = WhatsAppIntegrationHandler(self.gateway)
        self.phone_number = "1234567890"
        self.user_id = f"whatsapp-{self.phone_number}"
    
    def test_english_command_routing(self):
        """Test routing of English commands through WhatsApp integration"""
        # Test cases for different intents
        test_cases = [
            {"message": "Show my inventory", "expected_intent": "get_inventory"},
            {"message": "Show low stock items", "expected_intent": "get_low_stock"},
            {"message": "Search for rice", "expected_intent": "search_product"}
        ]
        
        for test_case in test_cases:
            message = test_case["message"]
            expected_intent = test_case["expected_intent"]
            
            # Mock both parse_multilingual_command and route_command functions
            with patch("nlp.multilingual_handler.parse_multilingual_command") as mock_parse, \
                 patch("nlp.command_router.route_command") as mock_route:
                # Set up the mocks to return predefined responses
                mock_parse.return_value = {
                    "intent": expected_intent,
                    "entities": {},
                    "language": "en"
                }
                mock_route.return_value = f"Mock response for {expected_intent}"
                
                # Process the message
                response = self.handler.process_incoming_message(self.phone_number, message)
                
                # Verify the message was processed correctly
                mock_parse.assert_called_once_with(message)
                mock_route.assert_called_once()
                parsed_result = mock_route.call_args[0][0]
                self.assertEqual(parsed_result["intent"], expected_intent)
                self.assertEqual(parsed_result["language"], "en")
                
                # Verify a response was sent via WhatsApp
                last_message = self.gateway.get_last_sent_message()
                self.assertIsNotNone(last_message)
                self.assertEqual(last_message["to"], self.phone_number)
                self.assertEqual(last_message["text"], f"Mock response for {expected_intent}")
                
                # Verify user session was updated
                session = self.handler.get_user_session(self.user_id)
                self.assertEqual(session["last_intent"], expected_intent)
                self.assertEqual(session["language"], "en")
    
    def test_hindi_command_routing(self):
        """Test routing of Hindi commands through WhatsApp integration"""
        # Test cases for different intents in Hindi
        test_cases = [
            {"message": "मेरा इन्वेंटरी दिखाओ", "expected_intent": "get_inventory"},
            {"message": "कम स्टॉक वाले आइटम दिखाओ", "expected_intent": "get_low_stock"},
            {"message": "चावल सर्च करो", "expected_intent": "search_product"}
        ]
        
        for test_case in test_cases:
            message = test_case["message"]
            expected_intent = test_case["expected_intent"]
            
            # Mock both parse_multilingual_command and route_command functions
            with patch("nlp.multilingual_handler.parse_multilingual_command") as mock_parse, \
                 patch("nlp.command_router.route_command") as mock_route:
                # Set up the mocks to return predefined responses
                mock_parse.return_value = {
                    "intent": expected_intent,
                    "entities": {},
                    "language": "hi"
                }
                mock_route.return_value = f"Mock response for {expected_intent} in Hindi"
                
                # Process the message
                response = self.handler.process_incoming_message(self.phone_number, message)
                
                # Verify the message was processed correctly
                mock_parse.assert_called_once_with(message)
                mock_route.assert_called_once()
                parsed_result = mock_route.call_args[0][0]
                self.assertEqual(parsed_result["intent"], expected_intent)
                self.assertEqual(parsed_result["language"], "hi")
                
                # Verify a response was sent via WhatsApp
                last_message = self.gateway.get_last_sent_message()
                self.assertIsNotNone(last_message)
                self.assertEqual(last_message["to"], self.phone_number)
                self.assertEqual(last_message["text"], f"Mock response for {expected_intent} in Hindi")
                
                # Verify user session was updated
                session = self.handler.get_user_session(self.user_id)
                self.assertEqual(session["last_intent"], expected_intent)
                self.assertEqual(session["language"], "hi")
    
    def test_unknown_command_routing(self):
        """Test routing of unknown commands through WhatsApp integration"""
        # Test with an unknown command
        message = "Hello there"
        
        # Mock both parse_multilingual_command and route_command functions
        with patch("nlp.multilingual_handler.parse_multilingual_command") as mock_parse, \
             patch("nlp.command_router.route_command") as mock_route:
            # Set up the mocks to return predefined responses
            mock_parse.return_value = {
                "intent": "unknown",
                "entities": {},
                "language": "en"
            }
            mock_route.return_value = "I don't understand that command"
            
            # Process the message
            response = self.handler.process_incoming_message(self.phone_number, message)
            
            # Verify the message was processed correctly
            mock_parse.assert_called_once_with(message)
            mock_route.assert_called_once()
            parsed_result = mock_route.call_args[0][0]
            self.assertEqual(parsed_result["intent"], "unknown")
            
            # Verify a response was sent via WhatsApp
            last_message = self.gateway.get_last_sent_message()
            self.assertIsNotNone(last_message)
            self.assertEqual(last_message["to"], self.phone_number)
            self.assertEqual(last_message["text"], "I don't understand that command")
            
            # Verify user session was updated
            session = self.handler.get_user_session(self.user_id)
            self.assertEqual(session["last_intent"], "unknown")

if __name__ == "__main__":
    unittest.main()