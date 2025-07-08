import unittest
import requests
import json
import os
import sys
import logging
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Base URL for API endpoints
BASE_URL = "http://127.0.0.1:8000"

def test_get_inventory_report_command():
    """
    Test the get_inventory_report intent with English commands
    """
    print("\nTesting get_inventory_report intent with English command...")
    
    # Mock the command router and API response
    with patch('nlp.command_router.make_api_request') as mock_api:
        # Configure mock to return a success response
        mock_api.return_value = {
            "success": True,
            "message": "Inventory report generated successfully"
        }
        
        # Import here to use the patched version
        from nlp.command_router import process_command
        
        # Test English command
        result = process_command("inventory report", "en", "user123")
        print(f"Command: 'inventory report'")
        print(f"Result: {result}")
        assert "generated successfully" in result.lower(), "Expected success message not found"
        
        # Test another English command variation
        result = process_command("generate inventory report", "en", "user123")
        print(f"Command: 'generate inventory report'")
        print(f"Result: {result}")
        assert "generated successfully" in result.lower(), "Expected success message not found"

def test_get_inventory_report_command_hindi():
    """
    Test the get_inventory_report intent with Hindi commands
    """
    print("\nTesting get_inventory_report intent with Hindi command...")
    
    # Mock the command router and API response
    with patch('nlp.command_router.make_api_request') as mock_api:
        # Configure mock to return a success response
        mock_api.return_value = {
            "success": True,
            "message": "Inventory report generated successfully"
        }
        
        # Import here to use the patched version
        from nlp.command_router import process_command
        
        # Test Hindi command
        result = process_command("इन्वेंटरी रिपोर्ट", "hi", "user123")
        print(f"Command: 'इन्वेंटरी रिपोर्ट'")
        print(f"Result: {result}")
        assert "सफलतापूर्वक" in result.lower(), "Expected success message not found"
        
        # Test another Hindi command variation
        result = process_command("इन्वेंटरी रिपोर्ट जनरेट करें", "hi", "user123")
        print(f"Command: 'इन्वेंटरी रिपोर्ट जनरेट करें'")
        print(f"Result: {result}")
        assert "सफलतापूर्वक" in result.lower(), "Expected success message not found"

def test_inventory_report_api_endpoint():
    """
    Test the inventory report API endpoint directly
    """
    print("\nTesting inventory report API endpoint...")
    
    # This test requires a running API server and valid authentication
    # Skip this test in CI environments or when API is not available
    try:
        # Check if API is available
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code != 200:
            print("API server not available, skipping API endpoint test")
            return
    except requests.exceptions.RequestException:
        print("API server not available, skipping API endpoint test")
        return
    
    # For actual testing, you would need valid authentication
    # This is a placeholder for manual testing
    print("To test the API endpoint manually:")
    print(f"1. GET {BASE_URL}/inventory/report")
    print("2. Include valid authentication token")
    print("3. Verify that a PDF file is returned")

if __name__ == "__main__":
    # Run the tests
    test_get_inventory_report_command()
    test_get_inventory_report_command_hindi()
    test_inventory_report_api_endpoint()