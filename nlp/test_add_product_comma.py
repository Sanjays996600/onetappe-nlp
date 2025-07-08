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
from nlp.mixed_entity_extraction import extract_mixed_product_details

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='test_add_product_comma.log'
)
logger = logging.getLogger(__name__)

def test_comma_separated_attributes():
    """
    Test add_product intent with comma-separated attributes
    """
    print("\n===== Testing add_product with comma-separated attributes =====\n")
    
    # Test cases with comma-separated attributes
    test_commands = [
        "Add product fan, ₹500, 3 qty",
        "Add product table, price 1000, stock 5",
        "Add new product chair, ₹800, quantity 10",
        "पंखा, ₹500, quantity 3",
        "Add product मेज़, ₹1000, स्टॉक 5"
    ]
    
    for cmd in test_commands:
        print(f"\nCommand: '{cmd}'")
        
        # Test with parse_multilingual_command
        result = parse_multilingual_command(cmd)
        print(f"parse_multilingual_command result:")
        print(f"  Intent: {result['intent']}")
        print(f"  Entities: {result['entities']}")
        if 'language' in result:
            print(f"  Language: {result['language']}")
        if 'is_mixed' in result:
            print(f"  Is mixed: {result['is_mixed']}")

def test_extract_product_details():
    """
    Test extract_mixed_product_details function directly with comma-separated attributes
    """
    print("\n===== Testing extract_mixed_product_details with comma-separated attributes =====\n")
    
    # Test cases with comma-separated attributes
    test_commands = [
        "Add product fan, ₹500, 3 qty",
        "Add product table, price 1000, stock 5",
        "Add new product chair, ₹800, quantity 10",
        "पंखा, ₹500, quantity 3",
        "Add product मेज़, ₹1000, स्टॉक 5"
    ]
    
    for cmd in test_commands:
        print(f"\nCommand: '{cmd}'")
        entities = extract_mixed_product_details(cmd)
        print(f"Extracted entities: {entities}")

if __name__ == "__main__":
    print("Testing add_product intent with comma-separated attributes")
    test_comma_separated_attributes()
    test_extract_product_details()