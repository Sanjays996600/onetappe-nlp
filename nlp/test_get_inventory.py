import sys
import os
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
    filename='logs/test.log'
)
logger = logging.getLogger(__name__)

def test_get_inventory_command():
    """
    Test the get_inventory intent with English commands
    """
    print("\nTesting get_inventory intent with English command...")
    
    # Test command
    command = "Show my inventory"
    print(f"Command: '{command}'")
    
    # Parse the command
    parsed_result = parse_multilingual_command(command)
    print(f"Parsed result: {parsed_result}")
    
    # Verify intent
    assert parsed_result["intent"] == "get_inventory", f"Expected intent 'get_inventory', got '{parsed_result['intent']}'"
    assert parsed_result["language"] == "en", f"Expected language 'en', got '{parsed_result['language']}'"
    
    # Route the command
    response = route_command(parsed_result, user_id="test_user")
    print(f"Response: {response}")
    
    # Verify response contains inventory data
    assert "Here's your current inventory:" in response, "Response should contain inventory header"
    assert "Rice" in response, "Response should contain product 'Rice'"
    assert "qty" in response, "Response should contain 'qty' for English"
    
    print("✅ English get_inventory test passed!")
    return response

def test_hindi_get_inventory_command():
    """
    Test the get_inventory intent with Hindi commands
    """
    print("\nTesting get_inventory intent with Hindi command...")
    
    # Test command
    command = "मेरा स्टॉक दिखाओ"
    print(f"Command: '{command}'")
    
    # Parse the command
    parsed_result = parse_multilingual_command(command)
    print(f"Parsed result: {parsed_result}")
    
    # Verify intent
    assert parsed_result["intent"] == "get_inventory", f"Expected intent 'get_inventory', got '{parsed_result['intent']}'"
    assert parsed_result["language"] == "hi", f"Expected language 'hi', got '{parsed_result['language']}'"
    
    # Route the command
    response = route_command(parsed_result, user_id="test_user")
    print(f"Response: {response}")
    
    # Verify response contains inventory data in Hindi
    assert "आपका वर्तमान इन्वेंटरी:" in response, "Response should contain Hindi inventory header"
    assert "चावल" in response, "Response should contain product 'चावल'"
    assert "मात्रा" in response, "Response should contain 'मात्रा' for Hindi"
    
    print("✅ Hindi get_inventory test passed!")
    return response

if __name__ == "__main__":
    # Run the tests
    english_response = test_get_inventory_command()
    hindi_response = test_hindi_get_inventory_command()
    
    print("\n✅ All tests passed!")
    print("\nSample English response:")
    print(english_response)
    print("\nSample Hindi response:")
    print(hindi_response)