import sys
import os
import json
import logging
from typing import Dict, Any, Optional

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command
from utils.logger import whatsapp_logger

class MessageRouter:
    """Class for routing WhatsApp messages to the appropriate handler"""
    
    def __init__(self):
        """Initialize the message router"""
        self.user_sessions = {}  # Store user session data
    
    def process_message(self, phone_number: str, message_text: str, user_id: Optional[str] = None) -> str:
        """Process a WhatsApp message and return a response
        
        Args:
            phone_number: The phone number of the sender
            message_text: The text of the message
            user_id: Optional user ID
            
        Returns:
            The response message
        """
        # If no user_id provided, use phone number as identifier
        if not user_id:
            user_id = f"whatsapp-{phone_number}"
        
        # Log the incoming message
        whatsapp_logger.log_incoming_message(phone_number, message_text, user_id)
        
        try:
            # Parse the message using the NLP system
            parsed_result = parse_multilingual_command(message_text)
            whatsapp_logger.log_parsed_result(parsed_result, user_id)
            
            # Store the session data for this user
            self.user_sessions[user_id] = {
                "last_intent": parsed_result["intent"],
                "language": parsed_result["language"],
                "last_message": message_text
            }
            
            # Route the command to get a response
            whatsapp_logger.log_route_command(parsed_result, user_id)
            response = route_command(parsed_result, user_id=user_id)
            
            # Log the outgoing message
            whatsapp_logger.log_outgoing_message(phone_number, response, user_id)
            
            return response
        
        except Exception as e:
            # Log the error
            error_message = str(e)
            whatsapp_logger.log_error(error_message, type(e).__name__, user_id)
            
            # Return a default error message
            language = self.get_user_language(user_id)
            if language == "hi":
                response = "क्षमा करें, एक त्रुटि हुई है। कृपया बाद में पुन: प्रयास करें।"
            else:  # Default to English
                response = "Sorry, an error occurred. Please try again later."
            
            # Log the outgoing message
            whatsapp_logger.log_outgoing_message(phone_number, response, user_id)
            
            return response
    
    def get_user_session(self, user_id: str) -> Dict[str, Any]:
        """Get the session data for a user
        
        Args:
            user_id: The user ID
            
        Returns:
            The session data for the user
        """
        return self.user_sessions.get(user_id, {})
    
    def get_user_language(self, user_id: str) -> str:
        """Get the language preference for a user
        
        Args:
            user_id: The user ID
            
        Returns:
            The language preference for the user
        """
        session = self.get_user_session(user_id)
        return session.get("language", "en")
    
    def handle_webhook_payload(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Handle a webhook payload from WhatsApp
        
        Args:
            payload: The webhook payload
            
        Returns:
            A dictionary with the status and responses
        """
        try:
            # Extract the message data from the payload
            message_data = payload.get("entry", [])[0].get("changes", [])[0].get("value", {})
            messages = message_data.get("messages", [])
            
            if not messages:
                whatsapp_logger.log_error("No messages found in webhook payload", "ValidationError", None)
                return {"status": "error", "message": "No messages found"}
            
            # Process each message in the payload
            responses = []
            for message in messages:
                phone_number = message.get("from")
                message_text = message.get("text", {}).get("body", "")
                
                if not phone_number or not message_text:
                    whatsapp_logger.log_error("Invalid message format in webhook payload", "ValidationError", None)
                    continue
                
                # Process the message
                response = self.process_message(phone_number, message_text)
                responses.append({"to": phone_number, "response": response})
            
            return {"status": "success", "responses": responses}
        
        except Exception as e:
            # Log the error
            error_message = str(e)
            whatsapp_logger.log_error(error_message, type(e).__name__, None)
            
            return {"status": "error", "message": error_message}

# Create a default message router instance
message_router = MessageRouter()

# Export the message router instance
__all__ = ["MessageRouter", "message_router"]

# Example usage
if __name__ == "__main__":
    # Test with some example messages
    test_messages = [
        {"phone": "1234567890", "text": "Show my inventory"},
        {"phone": "1234567890", "text": "Add new product Rice 50rs 20qty"},
        {"phone": "1234567890", "text": "मेरे प्रोडक्ट दिखाओ"},  # Show my products in Hindi
        {"phone": "1234567890", "text": "नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो"}  # Add new product Rice 50rs 20pcs in Hindi
    ]
    
    # Process each message
    for message in test_messages:
        phone = message["phone"]
        text = message["text"]
        
        print(f"\nProcessing message: '{text}'")
        response = message_router.process_message(phone, text)
        print(f"Response: '{response}'")