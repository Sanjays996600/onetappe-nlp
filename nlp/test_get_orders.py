import unittest
from unittest.mock import patch, MagicMock
import sys
import os
from datetime import datetime, timedelta

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our modules (assuming these exist in the actual implementation)
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command

class TestGetOrders(unittest.TestCase):
    
    def test_english_get_orders_intent(self):
        """Test that English get_orders commands are correctly identified"""
        test_commands = [
            "show my recent orders",
            "get orders from last week",
            "display today's orders",
            "list all pending orders",
            "show completed orders"
        ]
        
        for command in test_commands:
            result = parse_multilingual_command(command)
            self.assertEqual(result["intent"], "get_orders", f"Failed to identify get_orders intent in: {command}")
            self.assertEqual(result["language"], "en", f"Failed to identify English language in: {command}")
    
    def test_hindi_get_orders_intent(self):
        """Test that Hindi get_orders commands are correctly identified"""
        test_commands = [
            "मेरे हाल के ऑर्डर दिखाएं",
            "पिछले सप्ताह के ऑर्डर दिखाओ",
            "आज के ऑर्डर दिखाएं",
            "सभी लंबित ऑर्डर दिखाएं",
            "पूरे हुए ऑर्डर दिखाओ"
        ]
        
        for command in test_commands:
            result = parse_multilingual_command(command)
            self.assertEqual(result["intent"], "get_orders", f"Failed to identify get_orders intent in: {command}")
            self.assertEqual(result["language"], "hi", f"Failed to identify Hindi language in: {command}")
    
    def test_english_time_period_extraction(self):
        """Test that time periods are correctly extracted from English commands"""
        test_cases = [
            ("show my recent orders", "recent"),
            ("get orders from last week", "last week"),
            ("display today's orders", "today"),
            ("show orders from yesterday", "yesterday"),
            ("list orders from last month", "last month")
        ]
        
        for command, expected_period in test_cases:
            result = parse_multilingual_command(command)
            self.assertEqual(result["entities"].get("time_period"), expected_period, 
                             f"Failed to extract time period from: {command}")
    
    def test_hindi_time_period_extraction(self):
        """Test that time periods are correctly extracted from Hindi commands"""
        test_cases = [
            ("मेरे हाल के ऑर्डर दिखाएं", "हाल के"),
            ("पिछले सप्ताह के ऑर्डर दिखाओ", "पिछले सप्ताह"),
            ("आज के ऑर्डर दिखाएं", "आज"),
            ("कल के ऑर्डर दिखाओ", "कल"),
            ("पिछले महीने के ऑर्डर दिखाएं", "पिछले महीने")
        ]
        
        for command, expected_period in test_cases:
            result = parse_multilingual_command(command)
            self.assertEqual(result["entities"].get("time_period"), expected_period, 
                             f"Failed to extract time period from: {command}")
    
    def test_english_order_status_extraction(self):
        """Test that order status is correctly extracted from English commands"""
        test_cases = [
            ("list all pending orders", "pending"),
            ("show completed orders", "completed"),
            ("display cancelled orders", "cancelled"),
            ("get all delivered orders", "delivered"),
            ("show processing orders", "processing")
        ]
        
        for command, expected_status in test_cases:
            result = parse_multilingual_command(command)
            self.assertEqual(result["entities"].get("order_status"), expected_status, 
                             f"Failed to extract order status from: {command}")
    
    def test_hindi_order_status_extraction(self):
        """Test that order status is correctly extracted from Hindi commands"""
        test_cases = [
            ("सभी लंबित ऑर्डर दिखाएं", "लंबित"),
            ("पूरे हुए ऑर्डर दिखाओ", "पूरे हुए"),
            ("रद्द किए गए ऑर्डर दिखाएं", "रद्द किए गए"),
            ("सभी डिलीवर किए गए ऑर्डर दिखाओ", "डिलीवर किए गए"),
            ("प्रोसेसिंग ऑर्डर दिखाएं", "प्रोसेसिंग")
        ]
        
        for command, expected_status in test_cases:
            result = parse_multilingual_command(command)
            self.assertEqual(result["entities"].get("order_status"), expected_status, 
                             f"Failed to extract order status from: {command}")
    
    def test_english_orders_routing(self):
        """Test that get_orders commands are correctly routed with API calls in English"""
        command = "show orders from last week"
        parsed_result = {
            "intent": "get_orders",
            "language": "en",
            "entities": {
                "time_period": "last week"
            }
        }
        
        # Mock the API response
        mock_api_response = {
            "success": True,
            "orders": [
                {
                    "order_id": "ORD12345",
                    "date": "2023-06-15",
                    "customer": "John Doe",
                    "amount": 1250,
                    "status": "delivered",
                    "items": 5
                },
                {
                    "order_id": "ORD12346",
                    "date": "2023-06-16",
                    "customer": "Jane Smith",
                    "amount": 850,
                    "status": "processing",
                    "items": 3
                },
                {
                    "order_id": "ORD12347",
                    "date": "2023-06-17",
                    "customer": "Bob Johnson",
                    "amount": 2100,
                    "status": "pending",
                    "items": 8
                }
            ],
            "total_orders": 3,
            "total_amount": 4200
        }
        
        with patch("nlp.command_router.make_api_request") as mock_api:
            mock_api.return_value = mock_api_response
            
            # Mock the parse_multilingual_command function
            with patch("nlp.multilingual_handler.parse_multilingual_command", return_value=parsed_result):
                response = route_command(parsed_result)
                
                # Verify API was called with correct parameters
                mock_api.assert_called_once()
                args, kwargs = mock_api.call_args
                self.assertEqual(kwargs.get("endpoint"), "get_orders")
                self.assertEqual(kwargs.get("params").get("time_period"), "last week")
                
                # Verify response contains order information
                self.assertIn("Orders from last week", response)
                self.assertIn("ORD12345", response)
                self.assertIn("John Doe", response)
                self.assertIn("1250", response)
                self.assertIn("Total orders: 3", response)
                self.assertIn("Total amount: 4200", response)
    
    def test_hindi_orders_routing(self):
        """Test that get_orders commands are correctly routed with API calls in Hindi"""
        command = "पिछले सप्ताह के ऑर्डर दिखाओ"
        parsed_result = {
            "intent": "get_orders",
            "language": "hi",
            "entities": {
                "time_period": "पिछले सप्ताह"
            }
        }
        
        # Mock the API response
        mock_api_response = {
            "success": True,
            "orders": [
                {
                    "order_id": "ORD12345",
                    "date": "2023-06-15",
                    "customer": "राजेश कुमार",
                    "amount": 1250,
                    "status": "डिलीवर किया गया",
                    "items": 5
                },
                {
                    "order_id": "ORD12346",
                    "date": "2023-06-16",
                    "customer": "सुनीता शर्मा",
                    "amount": 850,
                    "status": "प्रोसेसिंग",
                    "items": 3
                },
                {
                    "order_id": "ORD12347",
                    "date": "2023-06-17",
                    "customer": "अमित पटेल",
                    "amount": 2100,
                    "status": "लंबित",
                    "items": 8
                }
            ],
            "total_orders": 3,
            "total_amount": 4200
        }
        
        with patch("nlp.command_router.make_api_request") as mock_api:
            mock_api.return_value = mock_api_response
            
            # Mock the parse_multilingual_command function
            with patch("nlp.multilingual_handler.parse_multilingual_command", return_value=parsed_result):
                response = route_command(parsed_result)
                
                # Verify API was called with correct parameters
                mock_api.assert_called_once()
                args, kwargs = mock_api.call_args
                self.assertEqual(kwargs.get("endpoint"), "get_orders")
                self.assertEqual(kwargs.get("params").get("time_period"), "पिछले सप्ताह")
                
                # Verify response contains order information in Hindi
                self.assertIn("पिछले सप्ताह के ऑर्डर", response)
                self.assertIn("ORD12345", response)
                self.assertIn("राजेश कुमार", response)
                self.assertIn("1250", response)
                self.assertIn("कुल ऑर्डर: 3", response)
                self.assertIn("कुल राशि: 4200", response)
    
    def test_order_status_filtering(self):
        """Test filtering orders by status"""
        parsed_result = {
            "intent": "get_orders",
            "language": "en",
            "entities": {
                "order_status": "pending"
            }
        }
        
        # Mock the API response with filtered orders
        mock_api_response = {
            "success": True,
            "orders": [
                {
                    "order_id": "ORD12347",
                    "date": "2023-06-17",
                    "customer": "Bob Johnson",
                    "amount": 2100,
                    "status": "pending",
                    "items": 8
                },
                {
                    "order_id": "ORD12350",
                    "date": "2023-06-18",
                    "customer": "Sarah Williams",
                    "amount": 1500,
                    "status": "pending",
                    "items": 6
                }
            ],
            "total_orders": 2,
            "total_amount": 3600
        }
        
        with patch("nlp.command_router.make_api_request") as mock_api:
            mock_api.return_value = mock_api_response
            
            response = route_command(parsed_result)
            
            # Verify API was called with correct parameters
            mock_api.assert_called_once()
            args, kwargs = mock_api.call_args
            self.assertEqual(kwargs.get("endpoint"), "get_orders")
            self.assertEqual(kwargs.get("params").get("order_status"), "pending")
            
            # Verify response contains only pending orders
            self.assertIn("Pending orders", response)
            self.assertIn("ORD12347", response)
            self.assertIn("ORD12350", response)
            self.assertIn("Total orders: 2", response)
    
    def test_no_orders_found(self):
        """Test handling when no orders match the criteria"""
        parsed_result = {
            "intent": "get_orders",
            "language": "en",
            "entities": {
                "order_status": "cancelled"
            }
        }
        
        # Mock the API response with no orders
        mock_api_response = {
            "success": True,
            "orders": [],
            "total_orders": 0,
            "total_amount": 0
        }
        
        with patch("nlp.command_router.make_api_request") as mock_api:
            mock_api.return_value = mock_api_response
            
            response = route_command(parsed_result)
            
            # Verify appropriate message for no orders
            self.assertIn("No cancelled orders found", response)
    
    def test_api_error_handling(self):
        """Test handling of API errors during order retrieval"""
        parsed_result = {
            "intent": "get_orders",
            "language": "en",
            "entities": {
                "time_period": "last week"
            }
        }
        
        # Mock the API response with an error
        mock_api_response = {
            "success": False,
            "error": "Failed to retrieve orders",
            "error_code": 500
        }
        
        with patch("nlp.command_router.make_api_request") as mock_api:
            mock_api.return_value = mock_api_response
            
            response = route_command(parsed_result)
            
            # Verify error message is properly handled
            self.assertIn("error", response.lower())
            self.assertIn("orders", response.lower())
            self.assertIn("retrieve", response.lower())

if __name__ == "__main__":
    unittest.main()