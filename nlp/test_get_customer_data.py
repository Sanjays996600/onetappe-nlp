import sys
import os
import unittest
from unittest.mock import patch, MagicMock
import logging
from typing import Dict, Any

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/test_get_customer_data.log'
)
logger = logging.getLogger(__name__)

class TestGetCustomerData(unittest.TestCase):
    
    def test_get_customer_data_command_english(self):
        """Test English get_customer_data command"""
        # Test cases for different limits and time ranges
        test_cases = [
            {"command": "Show me top 5 customers", "expected_limit": 5, "expected_range": "this-month"},
            {"command": "Top 3 customers this week", "expected_limit": 3, "expected_range": "week"},
            {"command": "Give me the top customers this month", "expected_limit": 10, "expected_range": "this-month"},
            {"command": "Show top customers", "expected_limit": 10, "expected_range": "this-month"},
            {"command": "Who are my best customers", "expected_limit": 10, "expected_range": "this-month"}
        ]
        
        for test_case in test_cases:
            command = test_case["command"]
            expected_limit = test_case["expected_limit"]
            expected_range = test_case["expected_range"]
            
            print(f"\nCommand: '{command}'")
            
            # Parse the command
            parsed_result = parse_multilingual_command(command)
            print(f"Parsed result: {parsed_result}")
            
            # Verify intent and language
            self.assertEqual(parsed_result["intent"], "get_customer_data", 
                             f"Expected intent 'get_customer_data', got '{parsed_result['intent']}'")
            self.assertEqual(parsed_result["language"], "en", 
                             f"Expected language 'en', got '{parsed_result['language']}'")
            
            # Verify limit and time range extraction
            extracted_limit = parsed_result["entities"].get("limit", 0)
            extracted_range = parsed_result["entities"].get("range", "")
            
            self.assertEqual(extracted_limit, expected_limit, 
                             f"Expected limit '{expected_limit}', got '{extracted_limit}'")
            self.assertEqual(extracted_range, expected_range, 
                             f"Expected range '{expected_range}', got '{extracted_range}'")
            
            # Test routing the command with mocked API response
            with patch("nlp.command_router.make_api_request") as mock_api:
                # Mock API response
                mock_api.return_value = {
                    "customers": [
                        {"name": "Rahul Sharma", "total_spent": 25000, "order_count": 12},
                        {"name": "Priya Patel", "total_spent": 18500, "order_count": 8},
                        {"name": "Amit Singh", "total_spent": 15000, "order_count": 6}
                    ],
                    "time_range": extracted_range
                }
                
                response = route_command(parsed_result, user_id="test_user")
                print(f"Response: {response}")
                
                # Verify response contains customer data
                self.assertIn("Rahul Sharma", response)
                self.assertIn("25000", response)
                self.assertIn("12", response)
                
                # Verify response contains correct time range text
                if expected_range == "week":
                    self.assertIn("this week", response.lower())
                elif expected_range == "this-month":
                    self.assertIn("this month", response.lower())
    
    def test_get_customer_data_command_hindi(self):
        """Test Hindi get_customer_data command"""
        # Test cases for different limits and time ranges
        test_cases = [
            {"command": "टॉप 5 ग्राहक दिखाओ", "expected_limit": 5, "expected_range": "this-month"},
            {"command": "इस हफ्ते के टॉप 3 ग्राहक बताओ", "expected_limit": 3, "expected_range": "week"},
            {"command": "इस महीने के टॉप ग्राहक बताओ", "expected_limit": 10, "expected_range": "this-month"},
            {"command": "सबसे अच्छे ग्राहक कौन हैं", "expected_limit": 10, "expected_range": "this-month"}
        ]
        
        for test_case in test_cases:
            command = test_case["command"]
            expected_limit = test_case["expected_limit"]
            expected_range = test_case["expected_range"]
            
            print(f"\nCommand: '{command}'")
            
            # Parse the command
            parsed_result = parse_multilingual_command(command)
            print(f"Parsed result: {parsed_result}")
            
            # Verify intent and language
            self.assertEqual(parsed_result["intent"], "get_customer_data", 
                             f"Expected intent 'get_customer_data', got '{parsed_result['intent']}'")
            self.assertEqual(parsed_result["language"], "hi", 
                             f"Expected language 'hi', got '{parsed_result['language']}'")
            
            # Verify limit and time range extraction
            extracted_limit = parsed_result["entities"].get("limit", 0)
            extracted_range = parsed_result["entities"].get("range", "")
            
            self.assertEqual(extracted_limit, expected_limit, 
                             f"Expected limit '{expected_limit}', got '{extracted_limit}'")
            self.assertEqual(extracted_range, expected_range, 
                             f"Expected range '{expected_range}', got '{extracted_range}'")
            
            # Test routing the command with mocked API response
            with patch("nlp.command_router.make_api_request") as mock_api:
                # Mock API response
                mock_api.return_value = {
                    "customers": [
                        {"name": "राहुल शर्मा", "total_spent": 25000, "order_count": 12},
                        {"name": "प्रिया पटेल", "total_spent": 18500, "order_count": 8},
                        {"name": "अमित सिंह", "total_spent": 15000, "order_count": 6}
                    ],
                    "time_range": extracted_range
                }
                
                response = route_command(parsed_result, user_id="test_user")
                print(f"Response: {response}")
                
                # Verify response contains customer data in Hindi
                self.assertIn("राहुल शर्मा", response)
                self.assertIn("25000", response)
                self.assertIn("12", response)
                
                # Verify response contains correct time range text in Hindi
                if expected_range == "week":
                    self.assertIn("इस हफ्ते", response)
                elif expected_range == "this-month":
                    self.assertIn("इस महीने", response)
    
    def test_error_handling(self):
        """Test error handling for get_customer_data intent"""
        command = "Show top 5 customers"
        parsed_result = parse_multilingual_command(command)
        
        # Test API error response
        with patch("nlp.command_router.make_api_request") as mock_api:
            # Mock API error response
            mock_api.return_value = {"error": "Database connection failed"}
            
            response = route_command(parsed_result, user_id="test_user")
            print(f"Error response: {response}")
            
            # Verify error message is properly formatted
            self.assertIn("Failed to retrieve", response)
            self.assertIn("Database connection failed", response)
        
        # Test Hindi error response
        hindi_command = "टॉप 5 ग्राहक दिखाओ"
        hindi_parsed_result = parse_multilingual_command(hindi_command)
        
        with patch("nlp.command_router.make_api_request") as mock_api:
            # Mock API error response
            mock_api.return_value = {"error": "Database connection failed"}
            
            hindi_response = route_command(hindi_parsed_result, user_id="test_user")
            print(f"Hindi error response: {hindi_response}")
            
            # Verify error message is properly formatted in Hindi
            self.assertIn("प्राप्त करने में विफल", hindi_response)
            self.assertIn("Database connection failed", hindi_response)
    
    def test_edge_cases(self):
        """Test edge cases for get_customer_data intent"""
        # Test with very large limit
        command = "Show top 100 customers"
        parsed_result = parse_multilingual_command(command)
        
        self.assertEqual(parsed_result["intent"], "get_customer_data")
        self.assertEqual(parsed_result["entities"].get("limit"), 100)
        
        # Test with unusual time range
        command = "Show top customers from last year"
        parsed_result = parse_multilingual_command(command)
        
        self.assertEqual(parsed_result["intent"], "get_customer_data")
        # The system might default to a standard range if "last year" isn't supported
        self.assertIn(parsed_result["entities"].get("range"), ["this-month", "all"])

if __name__ == "__main__":
    unittest.main()