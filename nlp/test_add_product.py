import sys
import os
import logging
import json
from typing import Dict, Any

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from nlp.enhanced_multilingual_parser import parse_multilingual_command
from nlp.command_router import route_command, BASE_URL

# Setup logging
# Use the existing logs directory
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')

# Configure logging to write to the logs directory
log_file = os.path.join(logs_dir, 'command_router.log')

# Configure file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Configure console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Test Add Product started - Testing API integration")

def test_add_product_command(command: str, user_id: str = "test_user") -> Dict[str, Any]:
    """
    Test the add_product command with the real API endpoint
    
    Args:
        command: Natural language command
        user_id: User ID for authentication
        
    Returns:
        Dictionary with parsed result and response
    """
    logger.info(f"\n{'='*50}\nTesting add_product command: '{command}'\n{'='*50}")
    
    # Step 1: Parse the command using our multilingual NLP system
    parsed_result = parse_multilingual_command(command)
    logger.info(f"Parsed result: {json.dumps(parsed_result, ensure_ascii=False)}")
    
    # Step 2: Route the parsed command to the appropriate API endpoint
    response = route_command(parsed_result, user_id)
    logger.info(f"Final response: {json.dumps(response, ensure_ascii=False)}")
    
    return {
        "command": command,
        "parsed_result": parsed_result,
        "response": response
    }

if __name__ == "__main__":
    print(f"Testing add_product API integration for One Tappe NLP System")
    print(f"Logs will be written to {log_file}")
    
    # Test the example command from the requirements
    command = "Add new product Rice 50rs 20qty"
    
    try:
        result = test_add_product_command(command)
        
        parsed = result["parsed_result"]
        print(f"Language: {parsed['language']}")
        print(f"Intent: {parsed['intent']}")
        print(f"Entities: {parsed['entities']}")
        print(f"Response: {result['response']}")
        
        # Check if there was an error in the response
        if "error" in result["response"]:
            print(f"⚠️ API Error: {result['response']}")
        else:
            print(f"✅ Test successful!")
            
    except Exception as e:
        print(f"❌ Test failed with exception: {str(e)}")
        logger.error(f"Test failed for command '{command}': {str(e)}", exc_info=True)