#!/usr/bin/env python3
"""
Test file for mixed Hindi-English add_product commands with comma-separated values
"""

import sys
import json
import unittest
sys.path.append('/Users/sanjaysuman/One Tappe')

from OneTappeProject.nlp.enhanced_multilingual_parser import parse_multilingual_command
from OneTappeProject.nlp.mixed_entity_extraction import extract_mixed_product_details

class TestMixedLanguageAddProductCommands(unittest.TestCase):
    """
    Test class for mixed Hindi-English add_product commands with comma-separated values
    """
    
    def test_mixed_add_product_with_commas(self):
        """
        Test mixed Hindi-English add_product commands with comma-separated values
        """
        # Test cases for mixed language commands with comma-separated attributes
        test_cases = [
            {
                "command": "Add product Aata, ₹55, 10 kg",
                "expected_intent": "add_product",
                "expected_entities": {"name": "aata", "price": 55, "stock": 10}
            },
            {
                "command": "Add product चावल, price 60, stock 5",
                "expected_intent": "add_product",
                "expected_entities": {"name": "चावल", "price": 60, "stock": 5}
            },
            {
                "command": "Add product दाल, ₹80, मात्रा 8",
                "expected_intent": "add_product",
                "expected_entities": {"name": "दाल", "price": 80, "stock": 8}
            },
            {
                "command": "नया प्रोडक्ट Basmati Rice, कीमत 120, quantity 15",
                "expected_intent": "add_product",
                "expected_entities": {"name": "basmati rice", "price": 120, "stock": 15}
            },
            {
                "command": "प्रोडक्ट Toor Dal, मूल्य 90, स्टॉक 12",
                "expected_intent": "add_product",
                "expected_entities": {"name": "toor dal", "price": 90, "stock": 12}
            },
            {
                "command": "Add product रेड शर्ट, ₹500, 10 qty",
                "expected_intent": "add_product",
                "expected_entities": {"name": "रेड शर्ट", "price": 500, "stock": 10}
            },
            {
                "command": "प्रोडक्ट black pant, दाम 600, मात्रा 5",
                "expected_intent": "add_product",
                "expected_entities": {"name": "black pant", "price": 600, "stock": 5}
            },
            {
                "command": "Add प्रोडक्ट blue जींस, price 800, स्टॉक 7",
                "expected_intent": "add_product",
                "expected_entities": {"name": "blue जींस", "price": 800, "stock": 7}
            }
        ]
        
        print("\nTesting mixed Hindi-English add_product commands with comma-separated values:\n")
        
        for test_case in test_cases:
            command = test_case["command"]
            expected_intent = test_case["expected_intent"]
            expected_entities = test_case["expected_entities"]
            
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
            self.assertEqual(result['intent'], expected_intent, 
                            f"Expected '{expected_intent}' intent, got '{result['intent']}'")
            
            # Verify entities are extracted correctly
            self.assertIn('name', result['entities'], "Product name not extracted")
            self.assertIn('price', result['entities'], "Price not extracted")
            self.assertIn('stock', result['entities'], "Stock not extracted")
            
            # Verify entity values match expected values
            self.assertEqual(result['entities']['name'], expected_entities['name'], 
                            f"Expected name '{expected_entities['name']}', got '{result['entities']['name']}'")
            self.assertEqual(result['entities']['price'], expected_entities['price'], 
                            f"Expected price {expected_entities['price']}, got {result['entities']['price']}")
            self.assertEqual(result['entities']['stock'], expected_entities['stock'], 
                            f"Expected stock {expected_entities['stock']}, got {result['entities']['stock']}")
    
    def test_malformed_mixed_add_product_commands(self):
        """
        Test malformed mixed Hindi-English add_product commands with missing attributes
        """
        # Test cases for malformed mixed language commands
        test_cases = [
            {
                "command": "Add product Aata, ₹55",  # Missing stock
                "expected_intent": "add_product",
                "expected_entities": {"name": "aata", "price": 55}
            },
            {
                "command": "Add product चावल, stock 5",  # Missing price
                "expected_intent": "add_product",
                "expected_entities": {"name": "चावल", "stock": 5}
            },
            {
                "command": "नया प्रोडक्ट Basmati Rice",  # Missing price and stock
                "expected_intent": "add_product",
                "expected_entities": {"name": "basmati rice"}
            },
            {
                "command": "प्रोडक्ट, मूल्य 90, स्टॉक 12",  # Missing product name
                "expected_intent": "add_product",
                "expected_entities": {"price": 90, "stock": 12}
            }
        ]
        
        print("\nTesting malformed mixed Hindi-English add_product commands:\n")
        
        for test_case in test_cases:
            command = test_case["command"]
            expected_intent = test_case["expected_intent"]
            expected_entities = test_case["expected_entities"]
            
            print(f"\nCommand: '{command}'")
            
            # Test direct extraction
            direct_result = extract_mixed_product_details(command)
            print(f"Direct extraction result: {direct_result}")
            
            # Test parsing through enhanced_multilingual_parser
            result = parse_multilingual_command(command)
            print(f"Intent: {result['intent']}")
            print(f"Entities: {result['entities']}")
            
            # Verify the intent is correctly recognized
            self.assertEqual(result['intent'], expected_intent, 
                            f"Expected '{expected_intent}' intent, got '{result['intent']}'")
            
            # Verify available entities match expected values
            for key, value in expected_entities.items():
                self.assertIn(key, result['entities'], f"Expected entity '{key}' not found")
                self.assertEqual(result['entities'][key], value, 
                                f"Expected {key} '{value}', got '{result['entities'][key]}'")
    
    def test_pipe_separated_mixed_add_product_commands(self):
        """
        Test mixed Hindi-English add_product commands with pipe-separated values
        """
        # Test cases for pipe-separated mixed language commands
        test_cases = [
            {
                "command": "Add product Aata | ₹55 | 10 kg",
                "expected_intent": "add_product",
                "expected_entities": {"name": "aata", "price": 55, "stock": 10}
            },
            {
                "command": "Add product चावल | price 60 | stock 5",
                "expected_intent": "add_product",
                "expected_entities": {"name": "चावल", "price": 60, "stock": 5}
            },
            {
                "command": "नया प्रोडक्ट Basmati Rice | कीमत 120 | quantity 15",
                "expected_intent": "add_product",
                "expected_entities": {"name": "basmati rice", "price": 120, "stock": 15}
            }
        ]
        
        print("\nTesting mixed Hindi-English add_product commands with pipe-separated values:\n")
        
        for test_case in test_cases:
            command = test_case["command"]
            expected_intent = test_case["expected_intent"]
            expected_entities = test_case["expected_entities"]
            
            print(f"\nCommand: '{command}'")
            
            # Test parsing through enhanced_multilingual_parser
            result = parse_multilingual_command(command)
            print(f"Intent: {result['intent']}")
            print(f"Entities: {result['entities']}")
            
            # Verify the intent is correctly recognized
            self.assertEqual(result['intent'], expected_intent, 
                            f"Expected '{expected_intent}' intent, got '{result['intent']}'")
            
            # Verify entities are extracted correctly
            self.assertIn('name', result['entities'], "Product name not extracted")
            self.assertIn('price', result['entities'], "Price not extracted")
            self.assertIn('stock', result['entities'], "Stock not extracted")
            
            # Verify entity values match expected values
            self.assertEqual(result['entities']['name'], expected_entities['name'], 
                            f"Expected name '{expected_entities['name']}', got '{result['entities']['name']}'")
            self.assertEqual(result['entities']['price'], expected_entities['price'], 
                            f"Expected price {expected_entities['price']}, got {result['entities']['price']}")
            self.assertEqual(result['entities']['stock'], expected_entities['stock'], 
                            f"Expected stock {expected_entities['stock']}, got {result['entities']['stock']}")

class TestNegationDetection(unittest.TestCase):
    """
    Test class for negation detection in Hindi, English, and mixed language queries
    """
    
    def test_hindi_negation(self):
        """
        Test negation detection in Hindi queries
        """
        test_cases = [
            {
                "command": "नमकीन नहीं चाहिए",
                "expected_intent": None,
                "expected_has_negation": True
            },
            {
                "command": "नहीं चाहिए दूध",
                "expected_intent": None,
                "expected_has_negation": True
            },
            {
                "command": "मुझे साबुन नहीं चाहिए",
                "expected_intent": None,
                "expected_has_negation": True
            },
            {
                "command": "आलू मत दिखाओ",
                "expected_intent": None,
                "expected_has_negation": True
            }
        ]
        
        print("\nTesting Hindi negation detection:\n")
        
        for test_case in test_cases:
            command = test_case["command"]
            expected_intent = test_case["expected_intent"]
            expected_has_negation = test_case["expected_has_negation"]
            
            print(f"\nCommand: '{command}'")
            
            # Test parsing through enhanced_multilingual_parser
            result = parse_multilingual_command(command)
            print(f"Intent: {result['intent']}")
            print(f"Has negation: {result.get('has_negation', False)}")
            
            # Verify the intent is None (no intent for negation)
            self.assertEqual(result['intent'], expected_intent, 
                            f"Expected '{expected_intent}' intent, got '{result['intent']}'")
            
            # Verify has_negation flag is set
            self.assertEqual(result.get('has_negation', False), expected_has_negation, 
                            f"Expected has_negation={expected_has_negation}, got {result.get('has_negation', False)}")
    
    def test_english_negation(self):
        """
        Test negation detection in English queries
        """
        test_cases = [
            {
                "command": "don't want chips",
                "expected_intent": None,
                "expected_has_negation": True
            },
            {
                "command": "do not need milk",
                "expected_intent": None,
                "expected_has_negation": True
            },
            {
                "command": "not interested in soap",
                "expected_intent": None,
                "expected_has_negation": True
            },
            {
                "command": "no need for potatoes",
                "expected_intent": None,
                "expected_has_negation": True
            }
        ]
        
        print("\nTesting English negation detection:\n")
        
        for test_case in test_cases:
            command = test_case["command"]
            expected_intent = test_case["expected_intent"]
            expected_has_negation = test_case["expected_has_negation"]
            
            print(f"\nCommand: '{command}'")
            
            # Test parsing through enhanced_multilingual_parser
            result = parse_multilingual_command(command)
            print(f"Intent: {result['intent']}")
            print(f"Has negation: {result.get('has_negation', False)}")
            
            # Verify the intent is None (no intent for negation)
            self.assertEqual(result['intent'], expected_intent, 
                            f"Expected '{expected_intent}' intent, got '{result['intent']}'")
            
            # Verify has_negation flag is set
            self.assertEqual(result.get('has_negation', False), expected_has_negation, 
                            f"Expected has_negation={expected_has_negation}, got {result.get('has_negation', False)}")
    
    def test_mixed_language_negation(self):
        """
        Test negation detection in mixed Hindi-English queries
        """
        test_cases = [
            {
                "command": "नहीं need chips",
                "expected_intent": None,
                "expected_has_negation": True
            },
            {
                "command": "don't चाहिए milk",
                "expected_intent": None,
                "expected_has_negation": True
            },
            {
                "command": "no ज़रूरत for soap",
                "expected_intent": None,
                "expected_has_negation": True
            },
            {
                "command": "cancel करो potato order",
                "expected_intent": None,
                "expected_has_negation": True
            }
        ]
        
        print("\nTesting mixed language negation detection:\n")
        
        for test_case in test_cases:
            command = test_case["command"]
            expected_intent = test_case["expected_intent"]
            expected_has_negation = test_case["expected_has_negation"]
            
            print(f"\nCommand: '{command}'")
            
            # Test parsing through enhanced_multilingual_parser
            result = parse_multilingual_command(command)
            print(f"Intent: {result['intent']}")
            print(f"Has negation: {result.get('has_negation', False)}")
            
            # Verify the intent is None (no intent for negation)
            self.assertEqual(result['intent'], expected_intent, 
                            f"Expected '{expected_intent}' intent, got '{result['intent']}'")
            
            # Verify has_negation flag is set
            self.assertEqual(result.get('has_negation', False), expected_has_negation, 
                            f"Expected has_negation={expected_has_negation}, got {result.get('has_negation', False)}")

if __name__ == "__main__":
    unittest.main()