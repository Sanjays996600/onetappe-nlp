import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command

class TestGetLowStock(unittest.TestCase):
    
    def test_get_low_stock_command(self):
        """Test English get_low_stock command"""
        # Test basic low stock command
        command = "Show low stock items"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent and language detection
        self.assertEqual(parsed_result["intent"], "get_low_stock")
        self.assertEqual(parsed_result["language"], "en")
        
        # Test with threshold
        command = "Show items with stock below 10"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent, language detection, and threshold extraction
        self.assertEqual(parsed_result["intent"], "get_low_stock")
        self.assertEqual(parsed_result["language"], "en")
        self.assertEqual(parsed_result["entities"].get("threshold", 0), 10)
        
        # Test routing the command
        with patch("nlp.command_router.make_api_request") as mock_api:
            # Mock API response
            mock_api.return_value = {
                "products": [
                    {"name": "Salt", "price": 20, "stock": 3},
                    {"name": "Tea", "price": 120, "stock": 4}
                ]
            }
            
            response = route_command(parsed_result)
            
            # Verify response contains low stock items
            self.assertIn("low stock", response.lower())
            self.assertIn("salt", response.lower())
            self.assertIn("tea", response.lower())
    
    def test_hindi_get_low_stock_command(self):
        """Test Hindi get_low_stock command"""
        # Test basic Hindi low stock command
        command = "कम स्टॉक दिखाओ"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent and language detection
        self.assertEqual(parsed_result["intent"], "get_low_stock")
        self.assertEqual(parsed_result["language"], "hi")
        
        # Test with threshold
        command = "8 से कम स्टॉक वाले प्रोडक्ट दिखाओ"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent, language detection, and threshold extraction
        self.assertEqual(parsed_result["intent"], "get_low_stock")
        self.assertEqual(parsed_result["language"], "hi")
        self.assertEqual(parsed_result["entities"].get("threshold", 0), 8)
        
        # Test routing the command
        with patch("nlp.command_router.make_api_request") as mock_api:
            # Mock API response
            mock_api.return_value = {
                "products": [
                    {"name": "नमक", "price": 20, "stock": 3},
                    {"name": "चाय", "price": 120, "stock": 4}
                ]
            }
            
            response = route_command(parsed_result)
            
            # Verify response contains low stock items in Hindi
            self.assertIn("कम स्टॉक", response)
            self.assertIn("नमक", response)
            self.assertIn("चाय", response)

if __name__ == "__main__":
    unittest.main()