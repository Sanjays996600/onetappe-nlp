#!/usr/bin/env python3
"""
Test file for Hindi add_product commands with comma-separated attributes
"""

import sys
import json
sys.path.append('/Users/sanjaysuman/One Tappe/OneTappeProject')

from nlp.enhanced_multilingual_parser import parse_multilingual_command
from nlp.mixed_entity_extraction import extract_mixed_product_details

def test_hindi_add_product_comma():
    """
    Test Hindi add_product commands with comma-separated attributes
    """
    # Test cases for Hindi commands with comma-separated attributes
    test_cases = [
        "प्रोडक्ट पंखा, ₹500, मात्रा 3",
        "प्रोडक्ट चावल, कीमत 50, स्टॉक 20",
        "नया प्रोडक्ट साबुन, मूल्य 30, मात्रा 15",
        "प्रोडक्ट टूथपेस्ट, स्टॉक 25, कीमत 45"
    ]
    
    print("\nTesting Hindi add_product commands with comma-separated attributes:\n")
    
    for command in test_cases:
        print(f"\nCommand: '{command}'")
        
        # Test direct extraction
        direct_result = extract_mixed_product_details(command)
        print(f"Direct extraction result: {direct_result}")
        
        # Test parsing through enhanced_multilingual_parser
        result = parse_multilingual_command(command)
        print(f"Intent: {result['intent']}")
        print(f"Entities: {result['entities']}")
        print(f"Language: {result['language']}")
        print(f"Is mixed: {result['is_mixed']}")
        
        # Verify the intent is correctly recognized
        assert result['intent'] == 'add_product', f"Expected 'add_product' intent, got {result['intent']}"
        
        # Verify entities are extracted correctly
        assert 'name' in result['entities'], "Product name not extracted"
        assert 'price' in result['entities'], "Price not extracted"
        assert 'stock' in result['entities'], "Stock not extracted"

def test_mixed_language_add_product_comma():
    """
    Test mixed language add_product commands with comma-separated attributes
    """
    # Test cases for mixed language commands with comma-separated attributes
    test_cases = [
        "प्रोडक्ट shirt, price 300, stock 5",
        "प्रोडक्ट mobile, ₹15000, मात्रा 2",
        "नया प्रोडक्ट laptop, कीमत 50000, quantity 3",
        "प्रोडक्ट headphones, स्टॉक 10, price 1200"
    ]
    
    print("\nTesting mixed language add_product commands with comma-separated attributes:\n")
    
    for command in test_cases:
        print(f"\nCommand: '{command}'")
        
        # Test direct extraction
        direct_result = extract_mixed_product_details(command)
        print(f"Direct extraction result: {direct_result}")
        
        # Test parsing through enhanced_multilingual_parser
        result = parse_multilingual_command(command)
        print(f"Intent: {result['intent']}")
        print(f"Entities: {result['entities']}")
        print(f"Language: {result['language']}")
        print(f"Is mixed: {result['is_mixed']}")
        
        # Verify the intent is correctly recognized
        assert result['intent'] == 'add_product', f"Expected 'add_product' intent, got {result['intent']}"
        
        # Verify entities are extracted correctly
        assert 'name' in result['entities'], "Product name not extracted"
        assert 'price' in result['entities'], "Price not extracted"
        assert 'stock' in result['entities'], "Stock not extracted"

if __name__ == "__main__":
    try:
        test_hindi_add_product_comma()
        test_mixed_language_add_product_comma()
        print("\n✅ All tests passed!")
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")