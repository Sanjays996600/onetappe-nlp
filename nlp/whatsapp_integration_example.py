import sys
import os
from typing import Dict, Any

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command

# Mock WhatsApp API client (replace with actual WhatsApp API client in production)
class WhatsAppClient:
    def send_message(self, user_id: str, message: str) -> None:
        """
        Send a message to a WhatsApp user
        
        Args:
            user_id: WhatsApp user ID
            message: Message to send
        """
        print(f"\n[WhatsApp] Sending to {user_id}: {message}")

# Initialize WhatsApp client
whatsapp_client = WhatsAppClient()

def handle_whatsapp_message(message: str, user_id: str) -> None:
    """
    Handle incoming WhatsApp message
    
    Args:
        message: The message text from WhatsApp
        user_id: WhatsApp user ID
    """
    print(f"\n[WhatsApp] Received from {user_id}: {message}")
    
    # Step 1: Parse the message using our multilingual NLP system
    parsed_result = parse_multilingual_command(message)
    
    print(f"[NLP] Detected language: {parsed_result['language']}")
    print(f"[NLP] Recognized intent: {parsed_result['intent']}")
    print(f"[NLP] Extracted entities: {parsed_result['entities']}")
    
    # Step 2: Route the parsed command to the appropriate API endpoint
    response = route_command(parsed_result, user_id)
    
    # Step 3: Send the response back to the user
    whatsapp_client.send_message(user_id, response)

def simulate_conversation():
    """
    Simulate a conversation with a WhatsApp user
    """
    user_id = "whatsapp:+919876543210"
    
    print("===== SIMULATING WHATSAPP CONVERSATION =====\n")
    
    # Simulate a series of messages from the user
    messages = [
        # English commands
        "Show my inventory",
        "Add new product Rice 50rs 20qty",
        "Update Sugar stock to 50",
        "Show low stock items",
        "Get today's report",
        "View recent orders",
        
        # Hindi commands
        "मेरे प्रोडक्ट दिखाओ",  # Show my products
        "नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो",  # Add new product Rice 50rs 20pcs
        "चावल का स्टॉक 100 करो",  # Update Rice stock to 100
        "कम स्टॉक वाले आइटम दिखाओ",  # Show low stock items
        "आज की रिपोर्ट भेजो",  # Send today's report
    ]
    
    for message in messages:
        handle_whatsapp_message(message, user_id)
        print("\n" + "-" * 50)

if __name__ == "__main__":
    simulate_conversation()