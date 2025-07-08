import sys
import os
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
    filename='logs/test.log'
)
logger = logging.getLogger(__name__)

def test_get_report_command_english():
    """
    Test the get_report intent with English commands for different time ranges
    """
    print("\nTesting get_report intent with English commands...")
    
    # Test cases for different time ranges
    test_cases = [
        {"command": "Show me today's report", "expected_range": "today"},
        {"command": "Get yesterday's report", "expected_range": "yesterday"},
        {"command": "Show this week's report", "expected_range": "week"},
        {"command": "Generate this month's report", "expected_range": "this-month"}
    ]
    
    for test_case in test_cases:
        command = test_case["command"]
        expected_range = test_case["expected_range"]
        
        print(f"\nCommand: '{command}'")
        
        # Parse the command
        parsed_result = parse_multilingual_command(command)
        print(f"Parsed result: {parsed_result}")
        
        # Verify intent and language
        assert parsed_result["intent"] == "get_report", f"Expected intent 'get_report', got '{parsed_result['intent']}'" 
        assert parsed_result["language"] == "en", f"Expected language 'en', got '{parsed_result['language']}'" 
        
        # Verify time range extraction
        extracted_range = parsed_result["entities"].get("range", "")
        assert extracted_range == expected_range, f"Expected range '{expected_range}', got '{extracted_range}'"
        
        # Route the command
        response = route_command(parsed_result, user_id="test_user")
        print(f"Response: {response}")
        
        # Verify response contains report data
        if expected_range == "today":
            assert "Sales for today:" in response, "Response should contain 'Sales for today:'"
        elif expected_range == "yesterday":
            assert "Sales for yesterday:" in response, "Response should contain 'Sales for yesterday:'"
        elif expected_range == "week":
            assert "Sales for this week:" in response or "Sales for week:" in response, "Response should contain sales for week"
        elif expected_range == "this-month":
            assert "Sales for this month:" in response or "Sales for this-month:" in response, "Response should contain sales for month"
        
        assert "Orders:" in response, "Response should contain 'Orders:'"
        assert "Top product:" in response, "Response should contain 'Top product:'"
    
    print("✅ English get_report tests passed!")
    return response

def test_get_report_command_hindi():
    """
    Test the get_report intent with Hindi commands for different time ranges
    """
    print("\nTesting get_report intent with Hindi commands...")
    
    # Test cases for different time ranges
    test_cases = [
        {"command": "आज की रिपोर्ट दिखाओ", "expected_range": "today"},
        {"command": "कल की रिपोर्ट दिखाओ", "expected_range": "yesterday"},
        {"command": "इस हफ्ते की रिपोर्ट दिखाओ", "expected_range": "week"},
        {"command": "इस महीने की रिपोर्ट दिखाओ", "expected_range": "this-month"}
    ]
    
    for test_case in test_cases:
        command = test_case["command"]
        expected_range = test_case["expected_range"]
        
        print(f"\nCommand: '{command}'")
        
        # Parse the command
        parsed_result = parse_multilingual_command(command)
        print(f"Parsed result: {parsed_result}")
        
        # Verify intent and language
        assert parsed_result["intent"] == "get_report", f"Expected intent 'get_report', got '{parsed_result['intent']}'" 
        assert parsed_result["language"] == "hi", f"Expected language 'hi', got '{parsed_result['language']}'" 
        
        # Verify time range extraction
        extracted_range = parsed_result["entities"].get("range", "")
        assert extracted_range == expected_range, f"Expected range '{expected_range}', got '{extracted_range}'"
        
        # Route the command
        response = route_command(parsed_result, user_id="test_user")
        print(f"Response: {response}")
        
        # Verify response contains report data in Hindi
        if expected_range == "today":
            assert "आज की बिक्री:" in response, "Response should contain 'आज की बिक्री:'"
        elif expected_range == "yesterday":
            assert "कल की बिक्री:" in response, "Response should contain 'कल की बिक्री:'"
        elif expected_range == "week":
            assert "इस हफ्ते की बिक्री:" in response, "Response should contain Hindi sales for week"
        elif expected_range == "this-month":
            assert "इस महीने की बिक्री:" in response or "this-month की बिक्री:" in response, "Response should contain Hindi sales for month"
        
        assert "ऑर्डर:" in response, "Response should contain 'ऑर्डर:'"
        assert "टॉप प्रोडक्ट:" in response, "Response should contain 'टॉप प्रोडक्ट:'"
    
    print("✅ Hindi get_report tests passed!")
    return response

if __name__ == "__main__":
    # Run the tests
    english_response = test_get_report_command_english()
    hindi_response = test_get_report_command_hindi()
    
    print("\n✅ All tests passed!")
    print("\nSample English response:")
    print(english_response)
    print("\nSample Hindi response:")
    print(hindi_response)