import sys
import os
import logging
import json
from typing import Dict, Any

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command, BASE_URL

# Setup logging
# Use the existing logs directory
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')

# Configure logging to write to the logs directory
log_file = os.path.join(logs_dir, 'test.log')  # Use the test.log file we confirmed works

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

logger.info("Test Command Router started - Testing API integration")

def test_end_to_end_flow(command: str, user_id: str = "test_user") -> Dict[str, Any]:
    """
    Test the end-to-end flow from natural language command to API response
    
    Args:
        command: Natural language command
        user_id: User ID for authentication
        
    Returns:
        Dictionary with parsed result and response
    """
    logger.info(f"\n{'='*50}\nTesting command: '{command}'\n{'='*50}")
    
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

def run_test_cases():
    """
    Run a series of test cases to demonstrate the end-to-end flow
    """
    # Log backend server information
    logger.info(f"Testing against backend server: {BASE_URL}")
    
    test_cases = [
        # English commands
        "Show my inventory",
        "Add new product Rice 50rs 20qty",
        "Update Sugar stock to 50",
        "Show low stock items",
        "Get today's report",
        "View recent orders",
        "I want to add a new product called Wheat for 45 rupees with 30 pieces",
        
        # Hindi commands
        "मेरे प्रोडक्ट दिखाओ",  # Show my products
        "नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो",  # Add new product Rice 50rs 20pcs
        "चावल का स्टॉक 100 करो",  # Update Rice stock to 100
        "कम स्टॉक वाले आइटम दिखाओ",  # Show low stock items
        "आज की रिपोर्ट भेजो",  # Send today's report
        "मुझे चीनी का स्टॉक 75 करना है",  # I need to update Sugar stock to 75
    ]
    
    print(f"\n===== TESTING END-TO-END COMMAND FLOW =====")
    print(f"Backend server: {BASE_URL}\n")
    
    success_count = 0
    failure_count = 0
    
    for i, command in enumerate(test_cases):
        print(f"\nTest #{i+1}: '{command}'")
        try:
            result = test_end_to_end_flow(command)
            
            parsed = result["parsed_result"]
            print(f"Language: {parsed['language']}")
            print(f"Intent: {parsed['intent']}")
            print(f"Entities: {parsed['entities']}")
            print(f"Response: {result['response']}")
            
            # Check if there was an error in the response
            if "error" in result["response"]:
                print(f"⚠️ API Error: {result['response']}")
                failure_count += 1
            else:
                success_count += 1
                
        except Exception as e:
            print(f"❌ Test failed with exception: {str(e)}")
            logger.error(f"Test failed for command '{command}': {str(e)}", exc_info=True)
            failure_count += 1
    
    print(f"\n===== TEST SUMMARY =====")
    print(f"Total tests: {len(test_cases)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {failure_count}")

if __name__ == "__main__":
    print(f"Starting API integration tests for One Tappe NLP System")
    print(f"Logs will be written to command_router.log")
    try:
        run_test_cases()
    except Exception as e:
        logger.critical(f"Test suite failed with exception: {str(e)}", exc_info=True)
        print(f"\n❌ Test suite failed with exception: {str(e)}")
        print("Check command_router.log for details")