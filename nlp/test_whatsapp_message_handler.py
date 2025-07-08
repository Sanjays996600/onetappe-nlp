import sys
import os
import unittest
from unittest.mock import patch, MagicMock, call
import json
import logging
from typing import Dict, Any

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Setup logging
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
os.makedirs(logs_dir, exist_ok=True)

log_file = os.path.join(logs_dir, 'test_whatsapp_message_handler.log')

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
    
    def handle_webhook_payload(self, payload):
        """Handle a webhook payload from WhatsApp"""
        try:
            # Extract the message data from the payload
            message_data = payload.get("entry", [])[0].get("changes", [])[0].get("value", {})
            messages = message_data.get("messages", [])
            
            if not messages:
                logger.warning("No messages found in webhook payload")
                return {"status": "error", "message": "No messages found"}
            
            # Process each message in the payload
            responses = []
            for message in messages:
                phone_number = message.get("from")
                message_text = message.get("text", {}).get("body", "")
                
                if not phone_number or not message_text:
                    logger.warning("Invalid message format in webhook payload")
                    continue
                
                # Process the message
                response = self.process_incoming_message(phone_number, message_text)
                responses.append({"to": phone_number, "response": response})
            
            return {"status": "success", "responses": responses}
        
        except Exception as e:
            logger.error(f"Error processing webhook payload: {str(e)}")
            return {"status": "error", "message": str(e)}

class TestWhatsAppMessageHandler(unittest.TestCase):
    
    def setUp(self):
        # Initialize the mock gateway and handler
        self.gateway = MockWhatsAppGateway()
        self.handler = WhatsAppIntegrationHandler(self.gateway)
        self.phone_number = "1234567890"
        self.user_id = f"whatsapp-{self.phone_number}"
    
    @patch("nlp.multilingual_handler.parse_multilingual_command")
    @patch("nlp.command_router.route_command")
    def test_process_incoming_message(self, mock_route_command, mock_parse_command):
        """Test processing of incoming WhatsApp messages"""
        # Set up the mocks
        mock_parse_command.return_value = {
            "intent": "get_inventory",
            "entities": {},
            "language": "en"
        }
        mock_route_command.return_value = "Here is your inventory: Item 1, Item 2, Item 3"
        
        # Process a message
        message = "Show my inventory"
        response = self.handler.process_incoming_message(self.phone_number, message)
        
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
    def test_handle_webhook_payload(self, mock_route_command, mock_parse_command):
        """Test handling of webhook payloads from WhatsApp"""
        # Set up the mocks
        mock_parse_command.return_value = {
            "intent": "get_inventory",
            "entities": {},
            "language": "en"
        }
        mock_route_command.return_value = "Here is your inventory: Item 1, Item 2, Item 3"
        
        # Create a mock webhook payload
        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "123456789",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "9876543210",
                                    "phone_number_id": "987654321098765"
                                },
                                "contacts": [
                                    {
                                        "profile": {
                                            "name": "Test User"
                                        },
                                        "wa_id": "1234567890"
                                    }
                                ],
                                "messages": [
                                    {
                                        "from": "1234567890",
                                        "id": "wamid.abcdefghijklmnopqrstuvwxyz",
                                        "timestamp": "1623456789",
                                        "text": {
                                            "body": "Show my inventory"
                                        },
                                        "type": "text"
                                    }
                                ]
                            },
                            "field": "messages"
                        }
                    ]
                }
            ]
        }
        
        # Process the webhook payload
        result = self.handler.handle_webhook_payload(payload)
        
        # Verify the payload was processed correctly
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["responses"]), 1)
        self.assertEqual(result["responses"][0]["to"], "1234567890")
        self.assertEqual(result["responses"][0]["response"], "Here is your inventory: Item 1, Item 2, Item 3")
        
        # Verify the message was parsed and routed
        mock_parse_command.assert_called_once_with("Show my inventory")
        mock_route_command.assert_called_once()
        
        # Verify a response was sent via WhatsApp
        last_message = self.gateway.get_last_sent_message()
        self.assertIsNotNone(last_message)
        self.assertEqual(last_message["to"], "1234567890")
        self.assertEqual(last_message["text"], "Here is your inventory: Item 1, Item 2, Item 3")
    
    @patch("nlp.multilingual_handler.parse_multilingual_command")
    @patch("nlp.command_router.route_command")
    def test_multiple_messages_in_webhook(self, mock_route_command, mock_parse_command):
        """Test handling of multiple messages in a webhook payload"""
        # Set up the mocks to return different values for different calls
        mock_parse_command.side_effect = [
            {"intent": "get_inventory", "entities": {}, "language": "en"},
            {"intent": "get_low_stock", "entities": {}, "language": "en"}
        ]
        mock_route_command.side_effect = [
            "Here is your inventory: Item 1, Item 2, Item 3",
            "Low stock items: Item 2"
        ]
        
        # Create a mock webhook payload with multiple messages
        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "123456789",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "9876543210",
                                    "phone_number_id": "987654321098765"
                                },
                                "contacts": [
                                    {
                                        "profile": {
                                            "name": "Test User"
                                        },
                                        "wa_id": "1234567890"
                                    }
                                ],
                                "messages": [
                                    {
                                        "from": "1234567890",
                                        "id": "wamid.abcdefghijklmnopqrstuvwxyz1",
                                        "timestamp": "1623456789",
                                        "text": {
                                            "body": "Show my inventory"
                                        },
                                        "type": "text"
                                    },
                                    {
                                        "from": "1234567890",
                                        "id": "wamid.abcdefghijklmnopqrstuvwxyz2",
                                        "timestamp": "1623456790",
                                        "text": {
                                            "body": "Show low stock items"
                                        },
                                        "type": "text"
                                    }
                                ]
                            },
                            "field": "messages"
                        }
                    ]
                }
            ]
        }
        
        # Process the webhook payload
        result = self.handler.handle_webhook_payload(payload)
        
        # Verify the payload was processed correctly
        self.assertEqual(result["status"], "success")
        self.assertEqual(len(result["responses"]), 2)
        
        # Verify the first message
        self.assertEqual(result["responses"][0]["to"], "1234567890")
        self.assertEqual(result["responses"][0]["response"], "Here is your inventory: Item 1, Item 2, Item 3")
        
        # Verify the second message
        self.assertEqual(result["responses"][1]["to"], "1234567890")
        self.assertEqual(result["responses"][1]["response"], "Low stock items: Item 2")
        
        # Verify the messages were parsed and routed
        mock_parse_command.assert_has_calls([
            call("Show my inventory"),
            call("Show low stock items")
        ])
        self.assertEqual(mock_parse_command.call_count, 2)
        
        mock_route_command.assert_has_calls([
            call({"intent": "get_inventory", "entities": {}, "language": "en"}, user_id=f"whatsapp-1234567890"),
            call({"intent": "get_low_stock", "entities": {}, "language": "en"}, user_id=f"whatsapp-1234567890")
        ])
        self.assertEqual(mock_route_command.call_count, 2)
        
        # Verify responses were sent via WhatsApp
        self.assertEqual(len(self.gateway.sent_messages), 2)
        self.assertEqual(self.gateway.sent_messages[0]["to"], "1234567890")
        self.assertEqual(self.gateway.sent_messages[0]["text"], "Here is your inventory: Item 1, Item 2, Item 3")
        self.assertEqual(self.gateway.sent_messages[1]["to"], "1234567890")
        self.assertEqual(self.gateway.sent_messages[1]["text"], "Low stock items: Item 2")
    
    @patch("nlp.multilingual_handler.parse_multilingual_command")
    @patch("nlp.command_router.route_command")
    def test_error_handling(self, mock_route_command, mock_parse_command):
        """Test handling of errors during message processing"""
        # Set up the mocks to raise an exception
        mock_parse_command.side_effect = Exception("Test error")
        
        # Create a mock webhook payload
        payload = {
            "object": "whatsapp_business_account",
            "entry": [
                {
                    "id": "123456789",
                    "changes": [
                        {
                            "value": {
                                "messaging_product": "whatsapp",
                                "metadata": {
                                    "display_phone_number": "9876543210",
                                    "phone_number_id": "987654321098765"
                                },
                                "contacts": [
                                    {
                                        "profile": {
                                            "name": "Test User"
                                        },
                                        "wa_id": "1234567890"
                                    }
                                ],
                                "messages": [
                                    {
                                        "from": "1234567890",
                                        "id": "wamid.abcdefghijklmnopqrstuvwxyz",
                                        "timestamp": "1623456789",
                                        "text": {
                                            "body": "Show my inventory"
                                        },
                                        "type": "text"
                                    }
                                ]
                            },
                            "field": "messages"
                        }
                    ]
                }
            ]
        }
        
        # Process the webhook payload
        result = self.handler.handle_webhook_payload(payload)
        
        # Verify the error was handled correctly
        self.assertEqual(result["status"], "error")
        self.assertEqual(result["message"], "Test error")
        
        # Verify no responses were sent via WhatsApp
        self.assertEqual(len(self.gateway.sent_messages), 0)

if __name__ == "__main__":
    unittest.main()