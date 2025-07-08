import sys
import os
import json
import logging

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command
from nlp.mixed_entity_extraction import extract_mixed_edit_stock_details

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_edit_stock_command():
    """
    Test the edit_stock intent with a sample command
    """
    # Sample command to update stock
    command = "Update stock of Sugar to 15qty"
    user_id = "test_user"
    
    logger.info(f"Testing command: '{command}'")
    
    # Parse the command using multilingual handler
    parsed_result = parse_multilingual_command(command)
    logger.info(f"Parsed result: {json.dumps(parsed_result, indent=2)}")
    
    # Check if the intent was correctly identified
    if parsed_result.get("intent") != "edit_stock":
        logger.error(f"Expected intent 'edit_stock', got '{parsed_result.get('intent')}'")
        return False
    
    # Check if entities were correctly extracted
    entities = parsed_result.get("entities", {})
    if not entities or "name" not in entities or "stock" not in entities:
        logger.error(f"Missing required entities. Got: {entities}")
        return False
    
    logger.info(f"Extracted entities: name='{entities.get('name')}', stock={entities.get('stock')}")
    
    # Route the command to get the API response
    response = route_command(parsed_result, user_id)
    logger.info(f"API Response: {response}")
    
    return True

def test_hindi_edit_stock_command():
    """
    Test the edit_stock intent with a Hindi command
    """
    # Sample Hindi command to update stock
    command = "चीनी का स्टॉक 15 करो"
    user_id = "test_user"
    
    logger.info(f"Testing Hindi command: '{command}'")
    
    # Parse the command using multilingual handler
    parsed_result = parse_multilingual_command(command)
    logger.info(f"Parsed result: {json.dumps(parsed_result, indent=2)}")
    
    # Check if the intent was correctly identified
    if parsed_result.get("intent") != "edit_stock":
        logger.error(f"Expected intent 'edit_stock', got '{parsed_result.get('intent')}'")
        return False
    
    # Check if entities were correctly extracted
    entities = parsed_result.get("entities", {})
    if not entities or "name" not in entities or "stock" not in entities:
        logger.error(f"Missing required entities. Got: {entities}")
        return False
    
    logger.info(f"Extracted entities: name='{entities.get('name')}', stock={entities.get('stock')}")
    
    # Route the command to get the API response
    response = route_command(parsed_result, user_id)
    logger.info(f"API Response: {response}")
    
    return True

def test_negative_stock_validation():
    """
    Test the negative stock validation in edit_stock intent
    """
    # Sample command with negative stock value
    command = "Update stock of Sugar to -5"
    user_id = "test_user"
    
    print(f"\n\n*** Testing negative stock command: '{command}'")
    
    # Parse the command using multilingual handler
    parsed_result = parse_multilingual_command(command)
    print(f"*** Parsed result: {json.dumps(parsed_result, indent=2)}")
    
    # Check if the intent was correctly identified
    if parsed_result.get("intent") != "edit_stock":
        print(f"*** ERROR: Expected intent 'edit_stock', got '{parsed_result.get('intent')}'")
        return False
    
    # Check if entities were correctly extracted
    entities = parsed_result.get("entities", {})
    if not entities or "name" not in entities or "stock" not in entities:
        print(f"*** ERROR: Missing required entities. Got: {entities}")
        return False
    
    # Debug: Check if stock is actually negative
    stock = entities.get("stock")
    print(f"*** Extracted entities: name='{entities.get('name')}', stock={stock}, type={type(stock)}")
    if stock >= 0:
        print(f"*** ERROR: Expected negative stock value, got {stock}")
        return False
    
    # Route the command to get the API response
    response = route_command(parsed_result, user_id)
    print(f"*** API Response: {json.dumps(response, indent=2)}")
    
    # Check if the response contains the error message for negative quantity
    if "error" in response and "Quantity cannot be negative" in response["error"]:
        print("*** Negative stock validation passed")
        return True
    else:
        print(f"*** ERROR: Negative stock validation failed. Response: {json.dumps(response, indent=2)}")
        return False

def debug_negative_stock_command():
    """
    Debug function to examine the normalized text and parsing of negative stock commands
    """
    command = "Update stock of Sugar to -5"
    print(f"\n\n*** DEBUG: Testing negative stock command: '{command}'")
    
    # Import the normalize_mixed_command function directly
    from nlp.mixed_entity_extraction import normalize_mixed_command
    
    # Test the normalization function
    normalized = normalize_mixed_command(command)
    print(f"*** DEBUG: Normalized text: '{normalized}'")
    
    # Parse the command using multilingual handler
    parsed_result = parse_multilingual_command(command)
    print(f"*** DEBUG: Parsed result: {json.dumps(parsed_result, indent=2)}")
    
    # Check intent patterns
    from nlp.intent_handler import INTENT_PATTERNS
    print("\n*** DEBUG: Edit stock patterns:")
    for pattern in INTENT_PATTERNS.get("edit_stock", []):
        print(f"  - {pattern}")
        import re
        match = re.search(pattern, normalized, re.IGNORECASE)
        print(f"    Matches: {bool(match)}")
        if match:
            print(f"    Groups: {match.groups()}")
    
    return parsed_result

def test_mixed_language_edit_stock_command():
    """
    Test the edit_stock intent with mixed language commands
    """
    # Test cases for mixed language commands
    test_cases = [
        {"command": "चीनी का स्टॉक बदलो 5 किलो", "expected_name": "चीनी", "expected_stock": 5},
        {"command": "आलू स्टॉक अपडेट करें 10 किलो", "expected_name": "आलू", "expected_stock": 10},
        {"command": "बदलें स्टॉक साबुन 3", "expected_name": "साबुन", "expected_stock": 3},
        {"command": "Update stock of आलू to 10 किलो", "expected_name": "आलू", "expected_stock": 10}
    ]
    
    for test_case in test_cases:
        command = test_case["command"]
        expected_name = test_case["expected_name"]
        expected_stock = test_case["expected_stock"]
        
        logger.info(f"Testing mixed language command: '{command}'")
        
        # Extract entities directly using the mixed entity extraction function
        result = extract_mixed_edit_stock_details(command)
        logger.info(f"Extracted result: {json.dumps(result, ensure_ascii=False, indent=2)}")
        
        # Check if entities were correctly extracted
        if not result or "name" not in result or "stock" not in result:
            logger.error(f"Missing required entities. Got: {result}")
            return False
        
        # Verify the extracted entities match the expected values
        if result.get("name") != expected_name or result.get("stock") != expected_stock:
            logger.error(f"Extraction mismatch. Expected: name='{expected_name}', stock={expected_stock}. Got: name='{result.get('name')}', stock={result.get('stock')}")
            return False
        
        logger.info(f"Extraction successful: name='{result.get('name')}', stock={result.get('stock')}")
    
    return True

if __name__ == "__main__":
    print("\nTesting edit_stock intent with English command:\n")
    success = test_edit_stock_command()
    print(f"Test {'passed' if success else 'failed'}\n")
    
    print("\nTesting edit_stock intent with Hindi command:\n")
    success = test_hindi_edit_stock_command()
    print(f"Test {'passed' if success else 'failed'}\n")
    
    print("\nTesting edit_stock intent with mixed language commands:\n")
    success = test_mixed_language_edit_stock_command()
    print(f"Test {'passed' if success else 'failed'}\n")
    
    print("\nTesting edit_stock with negative quantity validation:\n")
    success = test_negative_stock_validation()
    print(f"Test {'passed' if success else 'failed'}\n")
    
    print("\nDebugging negative stock command:\n")
    debug_negative_stock_command()