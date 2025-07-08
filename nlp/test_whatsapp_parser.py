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
    filename='logs/test_whatsapp_parser.log'
)
logger = logging.getLogger(__name__)

# Mock WhatsApp API Gateway class
class MockWhatsAppGateway:
    def __init__(self):
        self.sent_messages = []
    
    def send_message(self, phone_number, message):
        self.sent_messages.append({"phone": phone_number, "message": message})
        return {"status": "success", "message_id": "mock-id-123"}
    
    def get_last_message(self):
        return self.sent_messages[-1] if self.sent_messages else None

# WhatsApp Parser class (to be implemented in the actual system)
class WhatsAppParser:
    def __init__(self, gateway):
        self.gateway = gateway
    
    def process_incoming_message(self, phone_number, message_text, user_id=None):
        """Process an incoming WhatsApp message and send a response"""
        # Parse the message using the NLP system
        parsed_result = parse_multilingual_command(message_text)
        
        # Log raw vs normalized text
        logger.info(f"Raw text: {parsed_result.get('raw_text', message_text)}")
        logger.info(f"Normalized text: {parsed_result.get('normalized_text', message_text)}")
        
        # Route the command to get a response
        response = route_command(parsed_result, user_id=user_id)
        
        # Send the response back via WhatsApp
        self.gateway.send_message(phone_number, response)
        
        return response

class TestWhatsAppParser(unittest.TestCase):
    
    def setUp(self):
        self.gateway = MockWhatsAppGateway()
        self.parser = WhatsAppParser(self.gateway)
    
    def test_english_commands(self):
        """Test processing English commands through WhatsApp parser"""
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
            
            print(f"\nTesting WhatsApp message: '{message}'")
            
            # Mock the route_command function to avoid actual API calls
            with patch("nlp.command_router.route_command") as mock_route:
                # Set up the mock to return a predefined response
                mock_route.return_value = f"Mock response for {expected_intent}"
                
                # Process the message
                response = self.parser.process_incoming_message("1234567890", message, user_id="test_user")
                
                # Verify the message was parsed correctly
                mock_route.assert_called_once()
                parsed_result = mock_route.call_args[0][0]
                self.assertEqual(parsed_result["intent"], expected_intent)
                self.assertEqual(parsed_result["language"], "en")
                self.assertEqual(parsed_result["raw_text"], message)
                self.assertIsNotNone(parsed_result["normalized_text"])
                
                # Verify a response was sent via WhatsApp
                last_message = self.gateway.get_last_message()
                self.assertIsNotNone(last_message)
                self.assertEqual(last_message["phone"], "1234567890")
                self.assertEqual(last_message["message"], f"Mock response for {expected_intent}")
    
    def test_hindi_commands(self):
        """Test processing Hindi commands through WhatsApp parser"""
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
            
            print(f"\nTesting Hindi WhatsApp message: '{message}'")
            
            # Mock the route_command function to avoid actual API calls
            with patch("nlp.command_router.route_command") as mock_route:
                # Set up the mock to return a predefined response
                mock_route.return_value = f"Mock response for {expected_intent} in Hindi"
                
                # Process the message
                response = self.parser.process_incoming_message("1234567890", message, user_id="test_user")
                
                # Verify the message was parsed correctly
                mock_route.assert_called_once()
                parsed_result = mock_route.call_args[0][0]
                self.assertEqual(parsed_result["intent"], expected_intent)
                self.assertEqual(parsed_result["language"], "hi")
                self.assertEqual(parsed_result["raw_text"], message)
                self.assertIsNotNone(parsed_result["normalized_text"])
                
                # Verify a response was sent via WhatsApp
                last_message = self.gateway.get_last_message()
                self.assertIsNotNone(last_message)
                self.assertEqual(last_message["phone"], "1234567890")
                self.assertEqual(last_message["message"], f"Mock response for {expected_intent} in Hindi")
    
    def test_unicode_handling(self):
        """Test handling of Unicode characters in WhatsApp messages"""
        # Test with a complex Hindi message containing various Unicode characters
        message = "मेरे टॉप १० ग्राहकों की जानकारी दिखाओ जो इस महीने सबसे ज़्यादा खरीदारी कर रहे हैं।"
        
        # Mock the route_command function
        with patch("nlp.command_router.route_command") as mock_route:
            mock_route.return_value = "Unicode response: हिंदी में जवाब"
            
            # Process the message
            response = self.parser.process_incoming_message("1234567890", message, user_id="test_user")
            
            # Verify the message was processed correctly
            mock_route.assert_called_once()
            parsed_result = mock_route.call_args[0][0]
            self.assertEqual(parsed_result["language"], "hi")
            self.assertEqual(parsed_result["raw_text"], message)
            self.assertIsNotNone(parsed_result["normalized_text"])
            
            # Verify the Unicode response was sent correctly
            last_message = self.gateway.get_last_message()
            self.assertEqual(last_message["message"], "Unicode response: हिंदी में जवाब")
    
    def test_error_handling(self):
        """Test error handling in WhatsApp parser"""
        # Test with an invalid command
        message = "This is not a valid command"
        
        # Mock the route_command function to return an unknown intent response
        with patch("nlp.multilingual_handler.parse_multilingual_command") as mock_parse:
            mock_parse.return_value = {
                "intent": "unknown", 
                "language": "en", 
                "entities": {},
                "raw_text": message,
                "normalized_text": message.lower().strip()
            }
            
            with patch("nlp.command_router.route_command") as mock_route:
                mock_route.return_value = "Sorry, I couldn't understand that command."
                
                # Process the message
                response = self.parser.process_incoming_message("1234567890", message, user_id="test_user")
                
                # Verify the error response was sent
                last_message = self.gateway.get_last_message()
                self.assertEqual(last_message["message"], "Sorry, I couldn't understand that command.")

if __name__ == "__main__":
    unittest.main()