#!/usr/bin/env python3

import sys
import os
import logging

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from multilingual_handler import parse_multilingual_command
from command_router import route_command

# Setup logging
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
log_file = os.path.join(logs_dir, 'edge_case_test.log')

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

logger.info("Edge Case Testing started")

def test_edge_case(command):
    """Test a single edge case command"""
    try:
        print(f"\nTesting: '{command}'")
        result = parse_multilingual_command(command)
        print(f"Language: {result['language']}")
        print(f"Intent: {result['intent']}")
        print(f"Entities: {result['entities']}")
        
        # Try to route the command
        try:
            response = route_command(result)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Routing error: {str(e)}")
        
        return result
    except Exception as e:
        print(f"Error: {str(e)}")
        return {"error": str(e)}

def run_edge_case_tests():
    """Run a series of edge case tests"""
    edge_cases = [
        # Empty command
        "",
        # Whitespace only
        "   ",
        # Single character
        "a",
        # Misspelled commands
        "Shw my prodcts",
        "Add prodct Rice 50 20",
        "Updat Suger stok to 50",
        # Ambiguous commands
        "Rice 50",
        "Show",
        "Add",
        # Mixed language
        "Show मेरे प्रोडक्ट",
        "Add नया प्रोडक्ट Rice",
        # Partial commands
        "Add product",
        "Update stock",
        # Non-command text
        "Hello, how are you?",
        "What can you do?",
        # Special characters
        "Show inventory!",
        "Add product Rice @50 #20",
    ]
    
    print("\n===== EDGE CASE TESTING =====\n")
    
    results = {}
    for case in edge_cases:
        results[case] = test_edge_case(case)
    
    return results

if __name__ == "__main__":
    print("Starting Edge Case Tests")
    try:
        results = run_edge_case_tests()
        print("\n===== EDGE CASE TEST SUMMARY =====\n")
        print(f"Total tests: {len(results)}")
        
        # Count successful parses (where an intent was identified)
        successful = sum(1 for r in results.values() if isinstance(r, dict) and r.get('intent') != 'unknown')
        print(f"Commands with recognized intent: {successful}")
        print(f"Commands with unknown intent: {len(results) - successful}")
        
    except Exception as e:
        logger.critical(f"Test suite failed with exception: {str(e)}", exc_info=True)
        print(f"\n❌ Test suite failed with exception: {str(e)}")