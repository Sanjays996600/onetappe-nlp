import unittest
import sys
import os

# Add the parent directory to the path so we can import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from OneTappeProject.nlp.mixed_entity_extraction import (
    extract_mixed_product_details, 
    extract_mixed_date_range, 
    parse_mixed_date,
    detect_language,
    normalize_transliterated_hindi,
    normalize_mixed_command
)
from OneTappeProject.nlp.enhanced_multilingual_parser import parse_multilingual_command, extract_entities

class TestEnhancedEntityExtraction(unittest.TestCase):
    
    def test_enhanced_product_extraction(self):
        """Test the enhanced product extraction functionality with various mixed language patterns"""
        test_cases = [
            # Standard mixed language patterns
            {
                "command": "add product red shirt price 500 stock 10",
                "expected": {"product_name": "red shirt", "price": "500", "stock": "10"}
            },
            {
                "command": "add product लाल शर्ट price 500 stock 10",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            # New Hindi patterns
            {
                "command": "नया product add करो लाल शर्ट मूल्य 500 स्टॉक 10",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            {
                "command": "add नया product लाल शर्ट मूल्य 500 स्टॉक 10",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            {
                "command": "लाल शर्ट नाम का product add करो मूल्य 500 स्टॉक 10",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            # Reversed order patterns
            {
                "command": "add product लाल शर्ट स्टॉक 10 मूल्य 500",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            {
                "command": "नया product add करो लाल शर्ट स्टॉक 10 मूल्य 500",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            # Different word orders
            {
                "command": "लाल शर्ट product जोड़ो price 500 stock 10",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            {
                "command": "लाल शर्ट product जोड़ो stock 10 price 500",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            {
                "command": "product लाल शर्ट जोड़ो price 500 stock 10",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            {
                "command": "product लाल शर्ट जोड़ो stock 10 price 500",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            # With currency and unit words
            {
                "command": "add product red shirt price 500 रुपए stock 10 इकाई",
                "expected": {"product_name": "red shirt", "price": "500", "stock": "10"}
            },
            {
                "command": "add product लाल शर्ट price 500 stock 10 pieces",
                "expected": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
        ]
        
        for test_case in test_cases:
            result = extract_mixed_product_details(test_case["command"])
            self.assertIsNotNone(result, f"Failed to extract from: {test_case['command']}")
            self.assertEqual(result["product_name"], test_case["expected"]["product_name"], 
                             f"Product name mismatch for: {test_case['command']}")
            self.assertEqual(result["price"], test_case["expected"]["price"], 
                             f"Price mismatch for: {test_case['command']}")
            self.assertEqual(result["stock"], test_case["expected"]["stock"], 
                             f"Stock mismatch for: {test_case['command']}")
    
    def test_multilingual_parser_integration(self):
        """Test the integration of enhanced entity extraction with the multilingual parser"""
        test_cases = [
            # English commands
            {
                "command": "add product red shirt price 500 stock 10",
                "expected_intent": "add_product",
                "expected_entities": {"product_name": "red shirt", "price": "500", "stock": "10"}
            },
            # Hindi commands
            {
                "command": "नया product लाल शर्ट मूल्य 500 स्टॉक 10 add करो",
                "expected_intent": "add_product",
                "expected_entities": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            # Mixed language commands
            {
                "command": "लाल शर्ट product जोड़ो price 500 stock 10",
                "expected_intent": "add_product",
                "expected_entities": {"product_name": "लाल शर्ट", "price": "500", "stock": "10"}
            },
            # Date range commands
            {
                "command": "show report for pichhle hafte",
                "expected_intent": "get_report",
                "expected_date_range": "last-week"
            },
            {
                "command": "1 जनवरी to 31 जनवरी की report dikhao",
                "expected_intent": "get_report",
                "expected_date_format": "custom"
            },
        ]
        
        for test_case in test_cases:
            result = parse_multilingual_command(test_case["command"])
            self.assertIsNotNone(result, f"Failed to parse: {test_case['command']}")
            self.assertEqual(result["intent"], test_case["expected_intent"], 
                             f"Intent mismatch for: {test_case['command']}")
            
            if "expected_entities" in test_case:
                for key, value in test_case["expected_entities"].items():
                    self.assertEqual(result["entities"].get(key), value, 
                                     f"{key} mismatch for: {test_case['command']}")
            
            if "expected_date_range" in test_case:
                self.assertEqual(result["entities"].get("date_range"), test_case["expected_date_range"], 
                                 f"Date range mismatch for: {test_case['command']}")
            
            if "expected_date_format" in test_case:
                self.assertEqual(result["entities"].get("date_format"), test_case["expected_date_format"], 
                                 f"Date format mismatch for: {test_case['command']}")

    def test_language_detection(self):
        """Test the language detection functionality"""
        # Test pure Hindi
        self.assertEqual(detect_language("आज का मौसम अच्छा है"), "hindi")
        
        # Test pure English
        self.assertEqual(detect_language("Today's weather is good"), "english")
        
        # Test mixed with Hindi dominance
        self.assertEqual(detect_language("आज का weather अच्छा है"), "mixed")
        
        # Test mixed with English dominance
        self.assertEqual(detect_language("Today's मौसम is good"), "mixed")
        
        # Test with emojis
        self.assertEqual(detect_language("Today's weather is good 🌞"), "mixed")
        
        # Test with transliterated Hindi
        self.assertEqual(detect_language("aaj ka mausam accha hai"), "mixed")
        
        # Test with numbers
        self.assertEqual(detect_language("Stock 5 kg"), "english")
        self.assertEqual(detect_language("स्टॉक 5 किलो"), "hindi")
        
        # Test with empty string
        self.assertEqual(detect_language(""), "english")
        
        # Test with only punctuation and spaces
        self.assertEqual(detect_language("!@#$%^&*()"), "english")

    def test_normalize_transliterated_hindi(self):
        """Test the transliteration normalization functionality"""
        # Test basic transliteration
        self.assertEqual(
            normalize_transliterated_hindi("aaj ka mausam accha hai"),
            "आज का मौसम अच्छा है"
        )
        
        # Test mixed language
        self.assertEqual(
            normalize_transliterated_hindi("aaj ka weather accha hai"),
            "आज का weather अच्छा है"
        )
        
        # Test with product names
        self.assertEqual(
            normalize_transliterated_hindi("chawal ka stock update karo"),
            "चावल का स्टॉक अपडेट करो"
        )
        
        # Test with numbers and units
        self.assertEqual(
            normalize_transliterated_hindi("aalu 5 kilo update karo"),
            "आलू 5 किलो अपडेट करो"
        )
        
        # Test with compound words
        self.assertEqual(
            normalize_transliterated_hindi("stockupdate karo"),
            "स्टॉकअपडेट करो"
        )
        
        # Test with punctuation and spaces
        self.assertEqual(
            normalize_transliterated_hindi("chawal, aalu, pyaaz"),
            "चावल, आलू, प्याज"
        )
        
        # Test with empty string
        self.assertEqual(normalize_transliterated_hindi(""), "")
        
        # Test with pure Hindi (should remain unchanged)
        self.assertEqual(
            normalize_transliterated_hindi("आज का मौसम अच्छा है"),
            "आज का मौसम अच्छा है"
        )
        
        # Test with pure English (should remain mostly unchanged)
        self.assertEqual(
            normalize_transliterated_hindi("update stock of rice"),
            "update स्टॉक of rice"
        )

    def test_enhanced_mixed_command_normalization(self):
        """Test the enhanced mixed command normalization with transliteration"""
        # Test with transliterated Hindi
        self.assertEqual(
            normalize_mixed_command("aaj ka stock update karo"),
            "आज का स्टॉक अपडेट करो"
        )
        
        # Test with emojis
        self.assertEqual(
            normalize_mixed_command("🍚 5 किलो 📦 अपडेट"),
            "चावल 5 किलो स्टॉक अपडेट"
        )
        
        # Test with structured format
        self.assertEqual(
            normalize_mixed_command("product: aalu\nquantity: 5 kg"),
            "आलू का स्टॉक 5 किलो अपडेट करो"
        )
        
        # Test with negative numbers
        self.assertEqual(
            normalize_mixed_command("update stock of aalu to -5"),
            "update स्टॉक of आलू to -5"
        )
        
        # Test with multi-line input
        self.assertEqual(
            normalize_mixed_command("tamatar\nstock\n10 kg"),
            "टमाटर स्टॉक 10 किलो"
        )
        
        # Test with hybrid spellings
        self.assertEqual(
            normalize_mixed_command("tomatr ka stock update karo"),
            "टमाटर का स्टॉक अपडेट करो"
        )

if __name__ == "__main__":
    unittest.main()