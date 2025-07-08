import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the modules to test
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command

class TestSearchProduct(unittest.TestCase):
    
    def test_search_product_command_english(self):
        """Test English search_product command"""
        # Test basic search command
        command = "Search for sugar"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent and language detection
        self.assertEqual(parsed_result["intent"], "search_product")
        self.assertEqual(parsed_result["language"], "en")
        self.assertEqual(parsed_result["entities"].get("name"), "sugar")
        
        # Test alternative phrasing
        command = "Do you have rice in stock?"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent, language detection, and product name extraction
        self.assertEqual(parsed_result["intent"], "search_product")
        self.assertEqual(parsed_result["language"], "en")
        self.assertEqual(parsed_result["entities"].get("name"), "rice")
        
        # Test another alternative phrasing
        command = "Is salt available?"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent, language detection, and product name extraction
        self.assertEqual(parsed_result["intent"], "search_product")
        self.assertEqual(parsed_result["language"], "en")
        self.assertEqual(parsed_result["entities"].get("name"), "salt")
        
        # Test routing the command - product found
        with patch("nlp.command_router.make_api_request") as mock_api:
            # Mock API response for product found
            mock_api.return_value = {
                "success": True,
                "found": True,
                "name": parsed_result["entities"]["name"],
                "stock": 15,
                "price": 40
            }
            
            # Update parsed_result to search for sugar
            parsed_result["entities"]["name"] = "sugar"
            
            response = route_command(parsed_result)
            
            # Verify response indicates product is available
            self.assertIn("available", response.lower())
            self.assertIn("sugar", response.lower())
            self.assertIn("15", response)
        
        # Test routing the command - product not found
        with patch("nlp.command_router.make_api_request") as mock_api:
            # Mock API response for product not found
            mock_api.return_value = {
                "success": True,
                "found": False,
                "message": "Product 'coffee' not found"
            }
            
            # Update entities to search for coffee
            parsed_result["entities"]["name"] = "coffee"
            
            response = route_command(parsed_result)
            
            # Verify response indicates product is not available
            self.assertIn("not available", response.lower())
            self.assertIn("coffee", response.lower())
    
    def test_search_product_command_hindi(self):
        """Test Hindi search_product command"""
        # Test basic Hindi search command
        command = "चाय सर्च करो"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent and language detection
        self.assertEqual(parsed_result["intent"], "search_product")
        self.assertEqual(parsed_result["language"], "hi")
        self.assertEqual(parsed_result["entities"].get("name"), "चाय")
        
        # Test alternative phrasing
        command = "चावल उपलब्ध है क्या?"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent, language detection, and product name extraction
        self.assertEqual(parsed_result["intent"], "search_product")
        self.assertEqual(parsed_result["language"], "hi")
        self.assertEqual(parsed_result["entities"].get("name"), "चावल")
        
        # Test another alternative phrasing
        command = "नमक है क्या स्टॉक में?"
        parsed_result = parse_multilingual_command(command)
        
        # Verify intent, language detection, and product name extraction
        self.assertEqual(parsed_result["intent"], "search_product")
        self.assertEqual(parsed_result["language"], "hi")
        self.assertEqual(parsed_result["entities"].get("name"), "नमक")
        
        # Test routing the command - product found
        with patch("nlp.command_router.make_api_request") as mock_api:
            # Mock API response for product found
            mock_api.return_value = {
                "success": True,
                "found": True,
                "name": parsed_result["entities"]["name"],
                "stock": 20,
                "price": 150
            }
            
            # Update parsed_result to search for चाय
            parsed_result["entities"]["name"] = "चाय"
            
            response = route_command(parsed_result)
            
            # Verify response indicates product is available in Hindi
            self.assertIn("उपलब्ध", response)
            self.assertIn("चाय", response)
            self.assertIn("20", response)
        
        # Test routing the command - product not found
        with patch("nlp.command_router.make_api_request") as mock_api:
            # Mock API response for product not found
            mock_api.return_value = {
                "success": True,
                "found": False,
                "message": "Product 'कॉफी' not found"
            }
            
            # Update entities to search for coffee
            parsed_result["entities"]["name"] = "कॉफी"
            
            response = route_command(parsed_result)
            
            # Verify response indicates product is not available in Hindi
            self.assertIn("उपलब्ध नहीं", response)
            self.assertIn("कॉफी", response)

if __name__ == "__main__":
    unittest.main()