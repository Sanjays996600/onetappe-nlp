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
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/test_whatsapp_integration.log'
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
        
        # Parse the message using the NLP system
        parsed_result = parse_multilingual_command(message_text)
        
        # Store the session data for this user
        self.user_sessions[user_id] = {
            "last_intent": parsed_result["intent"],
            "language": parsed_result["language"],
            "timestamp": "2023-06-01T12:00:00Z"  # Mock timestamp
        }
        
        # Route the command to get a response
        response = route_command(parsed_result, user_id=user_id)
        
        # Send the response back via WhatsApp
        self.gateway.send_message(phone_number, response)
        
        return response
    
    def get_user_session(self, user_id):
        """Get the session data for a user"""
        return self.user_sessions.get(user_id, {})

class TestWhatsAppIntegration(unittest.TestCase):
    
    def setUp(self):
        # Create a directory for logs if it doesn't exist
        os.makedirs('logs', exist_ok=True)
        
        # Initialize the mock gateway and handler
        self.gateway = MockWhatsAppGateway()
        self.handler = WhatsAppIntegrationHandler(self.gateway)
    
    def test_english_commands_integration(self):
        """Test processing English commands through WhatsApp integration"""
        # Test cases for different intents
        test_cases = [
            {"message": "Show my inventory", "expected_intent": "get_inventory"},
            {"message": "Show top 5 customers", "expected_intent": "get_customer_data"},
            {"message": "Show top 3 products this week", "expected_intent": "get_top_products"},
            {"message": "Show low stock items", "expected_intent": "get_low_stock"},
            {"message": "Search for rice", "expected_intent": "search_product"}
        ]
        
        for test_case in test_cases:
            message = test_case["message"]
            expected_intent = test_case["expected_intent"]
            phone_number = "1234567890"
            user_id = f"whatsapp-{phone_number}"
            
            print(f"\nTesting WhatsApp integration with message: '{message}'")
            
            # Mock the route_command function to avoid actual API calls
            with patch("nlp.command_router.route_command") as mock_route:
                # Set up the mock to return a predefined response
                mock_route.return_value = f"Mock response for {expected_intent}"
                
                # Process the message
                response = self.handler.process_incoming_message(phone_number, message)
                
                # Verify the message was processed correctly
                mock_route.assert_called_once()
                parsed_result = mock_route.call_args[0][0]
                self.assertEqual(parsed_result["intent"], expected_intent)
                self.assertEqual(parsed_result["language"], "en")
                
                # Verify a response was sent via WhatsApp
                last_message = self.gateway.get_last_sent_message()
                self.assertIsNotNone(last_message)
                self.assertEqual(last_message["to"], phone_number)
                self.assertEqual(last_message["text"], f"Mock response for {expected_intent}")
                
                # Verify user session was updated
                session = self.handler.get_user_session(user_id)
                self.assertEqual(session["last_intent"], expected_intent)
                self.assertEqual(session["language"], "en")
    
    def test_hindi_commands_integration(self):
        """Test processing Hindi commands through WhatsApp integration"""
        # Test cases for different intents in Hindi
        test_cases = [
            {"message": "मेरा इन्वेंटरी दिखाओ", "expected_intent": "get_inventory"},
            {"message": "टॉप 5 ग्राहक दिखाओ", "expected_intent": "get_customer_data"},
            {"message": "इस हफ्ते के टॉप 3 प्रोडक्ट्स बताओ", "expected_intent": "get_top_products"},
            {"message": "कम स्टॉक वाले आइटम दिखाओ", "expected_intent": "get_low_stock"},
            {"message": "चावल सर्च करो", "expected_intent": "search_product"}
        ]
        
        for test_case in test_cases:
            message = test_case["message"]
            expected_intent = test_case["expected_intent"]
            phone_number = "1234567890"
            user_id = f"whatsapp-{phone_number}"
            
            print(f"\nTesting Hindi WhatsApp integration with message: '{message}'")
            
            # Mock the route_command function to avoid actual API calls
            with patch("nlp.command_router.route_command") as mock_route:
                # Set up the mock to return a predefined response
                mock_route.return_value = f"Mock response for {expected_intent} in Hindi"
                
                # Process the message
                response = self.handler.process_incoming_message(phone_number, message)
                
                # Verify the message was processed correctly
                mock_route.assert_called_once()
                parsed_result = mock_route.call_args[0][0]
                self.assertEqual(parsed_result["intent"], expected_intent)
                self.assertEqual(parsed_result["language"], "hi")
                
                # Verify a response was sent via WhatsApp
                last_message = self.gateway.get_last_sent_message()
                self.assertIsNotNone(last_message)
                self.assertEqual(last_message["to"], phone_number)
                self.assertEqual(last_message["text"], f"Mock response for {expected_intent} in Hindi")
                
                # Verify user session was updated
                session = self.handler.get_user_session(user_id)
                self.assertEqual(session["last_intent"], expected_intent)
                self.assertEqual(session["language"], "hi")
    
    def test_unicode_handling_integration(self):
        """Test handling of Unicode characters in WhatsApp integration"""
        # Test with a complex Hindi message containing various Unicode characters
        message = "मेरे टॉप १० ग्राहकों की जानकारी दिखाओ जो इस महीने सबसे ज़्यादा खरीदारी कर रहे हैं।"
        phone_number = "1234567890"
        
        # Mock the route_command function
        with patch("nlp.command_router.route_command") as mock_route:
            mock_route.return_value = "Unicode response: हिंदी में जवाब"
            
            # Process the message
            response = self.handler.process_incoming_message(phone_number, message)
            
            # Verify the message was processed correctly
            mock_route.assert_called_once()
            parsed_result = mock_route.call_args[0][0]
            self.assertEqual(parsed_result["language"], "hi")
            
            # Verify the Unicode response was sent correctly
            last_message = self.gateway.get_last_sent_message()
            self.assertEqual(last_message["text"], "Unicode response: हिंदी में जवाब")
    
    def test_error_handling_integration(self):
        """Test error handling in WhatsApp integration"""
        # Test with an invalid command
        message = "This is not a valid command"
        phone_number = "1234567890"
        
        # Mock the route_command function to return an unknown intent response
        with patch("nlp.multilingual_handler.parse_multilingual_command") as mock_parse:
            mock_parse.return_value = {"intent": "unknown", "language": "en", "entities": {}}
            
            with patch("nlp.command_router.route_command") as mock_route:
                mock_route.return_value = "Sorry, I couldn't understand that command."
                
                # Process the message
                response = self.handler.process_incoming_message(phone_number, message)
                
                # Verify the error response was sent
                last_message = self.gateway.get_last_sent_message()
                self.assertEqual(last_message["text"], "Sorry, I couldn't understand that command.")
    
    def test_message_encoding_decoding(self):
        """Test message encoding and decoding in WhatsApp integration"""
        # Test with special characters and emojis
        messages = [
            "Show my inventory 📦",
            "टॉप 5 ग्राहक दिखाओ 👨‍👩‍👧‍👦",
            "Search for Dal (दाल) 🍲"
        ]
        
        for message in messages:
            phone_number = "1234567890"
            
            # Mock the route_command function
            with patch("nlp.command_router.route_command") as mock_route:
                mock_route.return_value = f"Response: {message}"
                
                # Process the message
                response = self.handler.process_incoming_message(phone_number, message)
                
                # Verify the response contains the original special characters
                last_message = self.gateway.get_last_sent_message()
                self.assertEqual(last_message["text"], f"Response: {message}")
    
    def test_conversation_flow(self):
        """Test conversation flow with multiple messages"""
        phone_number = "1234567890"
        user_id = f"whatsapp-{phone_number}"
        
        # First message
        with patch("nlp.command_router.route_command") as mock_route:
            mock_route.return_value = "Here's your inventory"
            self.handler.process_incoming_message(phone_number, "Show my inventory")
        
        # Verify session was updated
        session = self.handler.get_user_session(user_id)
        self.assertEqual(session["last_intent"], "get_inventory")
        
        # Second message
        with patch("nlp.command_router.route_command") as mock_route:
            mock_route.return_value = "Here are your top customers"
            self.handler.process_incoming_message(phone_number, "Show top customers")
        
        # Verify session was updated again
        session = self.handler.get_user_session(user_id)
        self.assertEqual(session["last_intent"], "get_customer_data")
        
        # Verify message history in gateway
        self.assertEqual(len(self.gateway.sent_messages), 2)
        self.assertEqual(self.gateway.sent_messages[0]["text"], "Here's your inventory")
        self.assertEqual(self.gateway.sent_messages[1]["text"], "Here are your top customers")

if __name__ == "__main__":
    unittest.main()