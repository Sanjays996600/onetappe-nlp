import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
import json

# Import the parser module
from OneTappeProject.nlp.enhanced_multilingual_parser import parse_multilingual_command, extract_entities, format_response

class TestMultilingualParser(unittest.TestCase):
    """Test cases for the enhanced multilingual parser."""
    
    def test_english_command_parsing(self):
        """Test parsing of English commands."""
        # Test basic inventory query
        command = "Show inventory"
        result = parse_multilingual_command(command)
        self.assertEqual(result["language"], "en")
        self.assertEqual(result["intent"], "get_inventory")
        self.assertFalse(result["is_mixed_language"])
        self.assertEqual(result["raw_text"], command)
        self.assertIsNotNone(result["normalized_text"])
        
        # Test stock update command
        command = "Update rice stock to 50"
        result = parse_multilingual_command(command)
        self.assertEqual(result["language"], "en")
        self.assertEqual(result["intent"], "edit_stock")
        self.assertFalse(result["is_mixed_language"])
        self.assertEqual(result["raw_text"], command)
        self.assertIsNotNone(result["normalized_text"])
        
        # Test entity extraction for stock update
        entities = extract_entities("Update rice stock to 50", "edit_stock", "en")
        self.assertEqual(entities["product"], "rice")
        self.assertEqual(entities["quantity"], "50")
    
    def test_hindi_command_parsing(self):
        """Test parsing of Hindi commands."""
        # Test basic inventory query
        command = "इन्वेंटरी दिखाओ"
        result = parse_multilingual_command(command)
        self.assertEqual(result["language"], "hi")
        self.assertEqual(result["intent"], "get_inventory")
        self.assertFalse(result["is_mixed_language"])
        self.assertEqual(result["raw_text"], command)
        self.assertIsNotNone(result["normalized_text"])
        
        # Test stock update command
        command = "चावल स्टॉक 50 करो"
        result = parse_multilingual_command(command)
        self.assertEqual(result["language"], "hi")
        self.assertEqual(result["intent"], "edit_stock")
        self.assertFalse(result["is_mixed_language"])
        self.assertEqual(result["raw_text"], command)
        self.assertIsNotNone(result["normalized_text"])
        
        # Test entity extraction for stock update
        entities = extract_entities("चावल स्टॉक 50 करो", "edit_stock", "hi")
        self.assertEqual(entities["product"], "चावल")
        self.assertEqual(entities["quantity"], "50")
    
    def test_mixed_language_command_parsing(self):
        """Test parsing of mixed language commands."""
        # Test mixed language inventory query
        command = "Show मेरा inventory"
        result = parse_multilingual_command(command)
        self.assertEqual(result["intent"], "get_inventory")
        self.assertTrue(result["is_mixed_language"])
        self.assertEqual(result["raw_text"], command)
        self.assertIsNotNone(result["normalized_text"])
        
        # Test mixed language stock update
        command = "Update चावल stock to 50"
        result = parse_multilingual_command(command)
        self.assertEqual(result["intent"], "edit_stock")
        self.assertTrue(result["is_mixed_language"])
        self.assertEqual(result["raw_text"], command)
        self.assertIsNotNone(result["normalized_text"])
        
        # Test entity extraction for mixed language stock update
        entities = extract_entities("Update चावल stock to 50", "edit_stock", "mixed")
        self.assertEqual(entities["product"], "चावल")
        self.assertEqual(entities["quantity"], "50")
    
    def test_romanized_hindi_command_parsing(self):
        """Test parsing of romanized Hindi (Hinglish) commands."""
        # Test romanized Hindi inventory query
        command = "Inventory dikhao"
        result = parse_multilingual_command(command)
        self.assertEqual(result["language"], "hi-en")
        self.assertEqual(result["intent"], "get_inventory")
        self.assertEqual(result["raw_text"], command)
        self.assertIsNotNone(result["normalized_text"])
        
        # Test romanized Hindi stock update
        command = "Chawal stock 50 karo"
        result = parse_multilingual_command(command)
        self.assertEqual(result["language"], "hi-en")
        self.assertEqual(result["intent"], "edit_stock")
        self.assertEqual(result["raw_text"], command)
        self.assertIsNotNone(result["normalized_text"])
        
        # Test entity extraction for romanized Hindi stock update
        entities = extract_entities("Chawal stock 50 karo", "edit_stock", "hi-en")
        self.assertEqual(entities["product"], "chawal")
        self.assertEqual(entities["quantity"], "50")
    
    def test_response_formatting(self):
        """Test response formatting in different languages."""
        # Test English response
        entities = {"product": "rice", "quantity": "50"}
        raw_text = "Update rice stock to 50"
        normalized_text = "update rice stock to 50"
        response = format_response("edit_stock", entities, "en", raw_text, normalized_text)
        self.assertIn("rice", response)
        self.assertIn("50", response)
        
        # Test Hindi response
        entities = {"product": "चावल", "quantity": "50"}
        raw_text = "चावल स्टॉक 50 करो"
        normalized_text = "चावल स्टॉक 50 करो"
        response = format_response("edit_stock", entities, "hi", raw_text, normalized_text)
        self.assertIn("चावल", response)
        self.assertIn("50", response)
        
        # Test mixed language response
        entities = {"product": "चावल", "quantity": "50"}
        raw_text = "Update चावल stock to 50"
        normalized_text = "update चावल stock to 50"
        response = format_response("edit_stock", entities, "mixed", raw_text, normalized_text)
        self.assertIn("चावल", response)
        self.assertIn("50", response)
    
    def test_error_handling(self):
        """Test error handling for invalid commands."""
        # Test invalid command
        command = "xyz123"
        result = parse_multilingual_command(command)
        self.assertEqual(result["intent"], "unknown")
        self.assertEqual(result["raw_text"], command)
        self.assertIsNotNone(result["normalized_text"])
        
        # Test missing entities
        result = parse_multilingual_command("Update stock")
        self.assertEqual(result["intent"], "edit_stock")
        entities = extract_entities("Update stock", "edit_stock", "en")
        self.assertNotIn("product", entities)
        
        # Test response for unknown intent
        raw_text = "xyz123"
        normalized_text = "xyz123"
        response = format_response("unknown", {}, "en", raw_text, normalized_text)
        self.assertIn("understand", response.lower())

if __name__ == "__main__":
    unittest.main()