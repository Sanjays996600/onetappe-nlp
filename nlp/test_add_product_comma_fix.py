import sys
import os
import logging
import json
from typing import Dict, Any

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from nlp.multilingual_handler import parse_multilingual_command
from nlp.enhanced_multilingual_parser import parse_multilingual_command as enhanced_parse
from nlp.intent_handler import parse_command
from nlp.hindi_support import parse_hindi_command
from nlp.mixed_entity_extraction import extract_mixed_product_details

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='test_add_product_comma_fix.log'
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
        
        # Test direct extraction with mixed_entity_extraction
        print(f"\nDirect extraction with extract_mixed_product_details:")
        entities = extract_mixed_product_details(cmd)
        print(f"Extracted entities: {entities}")
        
        # Test with enhanced multilingual parser
        print(f"\nEnhanced multilingual parser:")
        result = enhanced_parse(cmd)
        print(f"Intent: {result['intent']}")
        print(f"Entities: {result['entities']}")
        print(f"Language: {result['language']}")
        print(f"Is mixed: {result['is_mixed']}")

def test_edge_cases():
    """
    Test edge cases for add_product intent
    """
    print("\n===== Testing edge cases for add_product =====\n")
    
    # Edge cases
    test_commands = [
        "Add product red shirt price 500 stock 10",  # No commas
        "Add product red shirt, price 500, stock 10",  # With commas
        "Add product red shirt,price 500,stock 10",  # No spaces after commas
        "Add product red shirt, ₹500, 10 qty",  # Mixed format
        "Add product red shirt, rupees 500, quantity 10"  # Text indicators
    ]
    
    for cmd in test_commands:
        print(f"\nCommand: '{cmd}'")
        
        # Test with enhanced multilingual parser
        result = enhanced_parse(cmd)
        print(f"Intent: {result['intent']}")
        print(f"Entities: {result['entities']}")
        
        # Verify that we have all required entities
        assert result['intent'] == 'add_product', f"Expected 'add_product' intent, got {result['intent']}"
        assert 'name' in result['entities'], "Missing 'name' entity"
        assert 'price' in result['entities'], "Missing 'price' entity"
        assert 'stock' in result['entities'], "Missing 'stock' entity"

if __name__ == "__main__":
    print("Testing add_product intent with comma-separated attributes")
    test_comma_separated_attributes()
    try:
        test_edge_cases()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")