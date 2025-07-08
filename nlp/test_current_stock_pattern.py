import sys
import os
import json
import logging
import re

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from nlp.intent_handler import parse_command, INTENT_PATTERNS
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command
from nlp.mixed_entity_extraction import normalize_mixed_command

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/test.log'
)
logger = logging.getLogger(__name__)

def debug_pattern_matching(command):
    """
    Debug function to check if a command matches any of the intent patterns
    """
    print(f"\nDebugging pattern matching for: '{command}'")
    
    # Apply normalization
    normalized = normalize_mixed_command(command.lower().strip())
    print(f"Normalized command: '{normalized}'")
    
    # Check each pattern
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, normalized, re.IGNORECASE):
                print(f"✅ Matched pattern '{pattern}' for intent '{intent}'")
            else:
                print(f"❌ No match for pattern '{pattern}' for intent '{intent}'")

def test_current_stock_pattern():
    """
    Test the 'current stock' pattern in intent_handler.py
    This pattern should map to the 'get_inventory' intent
    """
    print("\nTesting 'current stock' pattern...")
    
    # Test various commands using the 'current stock' pattern
    test_commands = [
        "Show current stock",
        "What is my current stock",
        "Check current stock",
        "Display current stock",
        "Current stock"
    ]
    
    # Debug the pattern matching for the first command
    debug_pattern_matching(test_commands[0])
    
    for command in test_commands:
        print(f"\nCommand: '{command}'")
        
        # Parse the command using the intent_handler directly
        direct_result = parse_command(command)
        print(f"Direct parse result: {json.dumps(direct_result, indent=2)}")
        
        # Verify intent with direct parsing
        assert direct_result["intent"] == "get_inventory", f"Expected intent 'get_inventory', got '{direct_result['intent']}'" 
        
        # Parse the command using the multilingual handler
        parsed_result = parse_multilingual_command(command)
        print(f"Multilingual parse result: {json.dumps(parsed_result, indent=2)}")
        
        # Verify intent with multilingual parsing
        assert parsed_result["intent"] == "get_inventory", f"Expected intent 'get_inventory', got '{parsed_result['intent']}'" 
        
        # Route the command (optional, if you want to test the full flow)
        # response = route_command(parsed_result, user_id="test_user")
        # print(f"Response: {response}")
    
    print("\n✅ All 'current stock' pattern tests passed!")

def test_current_stock_variations():
    """
    Test variations of the 'current stock' pattern with different prefixes and suffixes
    """
    print("\nTesting variations of 'current stock' pattern...")
    
    # Test variations with prefixes and suffixes
    test_variations = [
        "Show me the current stock",
        "I want to see current stock",
        "What's the current stock level",
        "Current stock status",
        "Get current stock information",
        "Tell me about current stock",
        "How is my current stock",
        "Current stock report",
        "Give me current stock details"
    ]
    
    for command in test_variations:
        print(f"\nCommand: '{command}'")
        
        # Parse the command
        parsed_result = parse_command(command)
        print(f"Parse result: {json.dumps(parsed_result, indent=2)}")
        
        # Verify intent
        assert parsed_result["intent"] == "get_inventory", f"Expected intent 'get_inventory', got '{parsed_result['intent']}'" 
    
    print("\n✅ All 'current stock' variation tests passed!")

def test_edge_cases():
    """
    Test edge cases for the 'current stock' pattern
    """
    print("\nTesting edge cases for 'current stock' pattern...")
    
    # Test edge cases
    edge_cases = [
        "CURRENT STOCK",  # All caps
        "current stock",  # All lowercase
        "Current Stock",  # Title case
        "  current stock  ",  # Extra spaces
        "current-stock",  # With hyphen
        "current.stock"  # With period
    ]
    
    for command in edge_cases:
        print(f"\nCommand: '{command}'")
        
        # Parse the command
        parsed_result = parse_command(command)
        print(f"Parse result: {json.dumps(parsed_result, indent=2)}")
        
        # Verify intent
        assert parsed_result["intent"] == "get_inventory", f"Expected intent 'get_inventory', got '{parsed_result['intent']}'" 
    
    print("\n✅ All edge case tests passed!")

if __name__ == "__main__":
    # Run the tests
    test_current_stock_pattern()
    test_current_stock_variations()
    test_edge_cases()
    
    print("\n✅ All tests completed successfully!")