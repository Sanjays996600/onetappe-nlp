#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Hindi-English Language QA Test Script
This script tests the WhatsApp chatbot's ability to handle commands in Hindi, English, and mixed language.
"""

import sys
import os
import json
import datetime
from typing import Dict, Any, List, Tuple

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Import required modules
from nlp.intent_handler import detect_language, parse_command
from nlp.hindi_support import parse_hindi_command
from nlp.multilingual_handler import parse_multilingual_command
from nlp.command_router import route_command

# Configure logging
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs/hindi_english_tests.log')),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Test cases
ENGLISH_TEST_CASES = [
    {"command": "Show my inventory", "expected_intent": "get_inventory"},
    {"command": "Update stock of rice to 50", "expected_intent": "edit_stock", "expected_entities": {"name": "rice", "stock": 50}},
    {"command": "Show low stock items", "expected_intent": "get_low_stock"},
    {"command": "Search for sugar", "expected_intent": "search_product", "expected_entities": {"name": "sugar"}},
    {"command": "Send today's report", "expected_intent": "get_report", "expected_entities": {"time_range": "today"}},
    {"command": "Show orders from last week", "expected_intent": "get_orders", "expected_entities": {"time_range": "last_week"}},
    {"command": "Add new product rice 50kg price 100", "expected_intent": "add_product", "expected_entities": {"name": "rice 50kg", "price": 100}}
]

HINDI_TEST_CASES = [
    {"command": "मेरा इन्वेंटरी दिखाओ", "expected_intent": "get_inventory"},
    {"command": "चावल का स्टॉक 50 करो", "expected_intent": "edit_stock", "expected_entities": {"name": "चावल", "stock": 50}},
    {"command": "कम स्टॉक वाले आइटम दिखाओ", "expected_intent": "get_low_stock"},
    {"command": "चीनी सर्च करो", "expected_intent": "search_product", "expected_entities": {"name": "चीनी"}},
    {"command": "आज की रिपोर्ट भेजो", "expected_intent": "get_report", "expected_entities": {"time_range": "today"}},
    {"command": "पिछले हफ्ते के ऑर्डर दिखाओ", "expected_intent": "get_orders", "expected_entities": {"time_range": "last_week"}},
    {"command": "नया प्रोडक्ट चावल 50kg जोड़ो ₹100 में", "expected_intent": "add_product", "expected_entities": {"name": "चावल", "price": 100, "stock": 50}}
]

MIXED_LANGUAGE_TEST_CASES = [
    {"command": "मेरा inventory दिखाओ", "expected_intent": "get_inventory"},
    {"command": "rice का स्टॉक 50 करो", "expected_intent": "edit_stock", "expected_entities": {"name": "rice", "stock": 50}},
    {"command": "Show low stock items in हिंदी", "expected_intent": "get_low_stock"},
    {"command": "sugar के लिए search करो", "expected_intent": "search_product", "expected_entities": {"name": "sugar"}},
    {"command": "आज का report in English", "expected_intent": "get_report", "expected_entities": {"time_range": "today"}}
]

LANGUAGE_SWITCHING_TEST_CASES = [
    {"command": "Switch to Hindi", "expected_intent": "switch_language", "expected_entities": {"language": "hindi"}},
    {"command": "अंग्रेजी में बदलो", "expected_intent": "switch_language", "expected_entities": {"language": "english"}},
    {"command": "हिंदी में जवाब दो", "expected_intent": "switch_language", "expected_entities": {"language": "hindi"}}
]

ERROR_HANDLING_TEST_CASES = [
    {"command": "चावल का स्टॉक करो", "expected_intent": "edit_stock", "expected_error": "missing_quantity"},
    {"command": "नया प्रोडक्ट जोड़ो", "expected_intent": "add_product", "expected_error": "missing_details"},
    {"command": "xyz123 दिखाओ", "expected_intent": "unknown", "expected_error": "unknown_command"},
    {"command": "प्रोडक्ट का प्राइस अपडेट करो", "expected_intent": "unknown", "expected_error": "unsupported_intent"},
    {"command": "मुझे चावल का रेट बताओ", "expected_intent": "unknown", "expected_error": "ambiguous_intent"}
]

def test_command(command: str, expected_intent: str, expected_entities: Dict[str, Any] = None, expected_error: str = None) -> Tuple[bool, Dict[str, Any]]:
    """
    Test a command and check if it matches the expected intent and entities
    
    Args:
        command: The command to test
        expected_intent: The expected intent
        expected_entities: The expected entities (optional)
        expected_error: The expected error (optional)
        
    Returns:
        Tuple of (success, result)
    """
    try:
        # Parse the command
        parsed_command = parse_multilingual_command(command)
        
        # Check if the intent matches
        intent_match = parsed_command["intent"] == expected_intent
        
        # Check if the entities match (if expected_entities is provided)
        entities_match = True
        if expected_entities:
            for key, value in expected_entities.items():
                if key not in parsed_command["entities"] or parsed_command["entities"][key] != value:
                    entities_match = False
                    break
        
        # Check if the error matches (if expected_error is provided)
        error_match = True
        if expected_error:
            if "error" not in parsed_command or parsed_command["error"] != expected_error:
                error_match = False
        
        # Return the result
        success = intent_match and entities_match and error_match
        return success, parsed_command
    
    except Exception as e:
        logger.error(f"Error testing command '{command}': {str(e)}")
        return False, {"error": str(e)}

def run_test_cases(test_cases: List[Dict[str, Any]], category_name: str) -> Dict[str, Any]:
    """
    Run a list of test cases and return the results
    
    Args:
        test_cases: List of test cases
        category_name: Name of the test category
        
    Returns:
        Dictionary with test results
    """
    results = {
        "category": category_name,
        "total": len(test_cases),
        "passed": 0,
        "failed": 0,
        "details": []
    }
    
    for i, test_case in enumerate(test_cases):
        command = test_case["command"]
        expected_intent = test_case["expected_intent"]
        expected_entities = test_case.get("expected_entities")
        expected_error = test_case.get("expected_error")
        
        logger.info(f"Testing {category_name} command: '{command}'")
        success, parsed_command = test_command(command, expected_intent, expected_entities, expected_error)
        
        if success:
            results["passed"] += 1
            status = "Pass"
        else:
            results["failed"] += 1
            status = "Fail"
        
        results["details"].append({
            "id": f"{category_name[:2].upper()}-{i+1:03d}",
            "command": command,
            "expected_intent": expected_intent,
            "expected_entities": expected_entities,
            "expected_error": expected_error,
            "actual_intent": parsed_command.get("intent"),
            "actual_entities": parsed_command.get("entities"),
            "actual_error": parsed_command.get("error"),
            "status": status
        })
        
        logger.info(f"Test result: {status}")
    
    return results

def generate_test_report(results: List[Dict[str, Any]]) -> str:
    """
    Generate a test report in Markdown format
    
    Args:
        results: List of test results
        
    Returns:
        Markdown formatted test report
    """
    total_tests = sum(result["total"] for result in results)
    total_passed = sum(result["passed"] for result in results)
    total_failed = sum(result["failed"] for result in results)
    
    report = "# हिंदी-अंग्रेजी भाषा QA परीक्षण परिणाम\n"
    report += "# Hindi-English Language QA Test Results\n\n"
    
    report += f"**परीक्षण तिथि / Test Date:** {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    
    report += "## परीक्षण सारांश / Test Summary\n\n"
    report += "| श्रेणी / Category | कुल / Total | पास / Pass | फेल / Fail | पास % / Pass % |\n"
    report += "|------------------|-------------|------------|------------|----------------|\n"
    
    for result in results:
        pass_percentage = (result["passed"] / result["total"]) * 100 if result["total"] > 0 else 0
        report += f"| {result['category']} | {result['total']} | {result['passed']} | {result['failed']} | {pass_percentage:.2f}% |\n"
    
    report += f"| **कुल / Total** | **{total_tests}** | **{total_passed}** | **{total_failed}** | **{(total_passed / total_tests) * 100 if total_tests > 0 else 0:.2f}%** |\n\n"
    
    for result in results:
        report += f"## {result['category']} परीक्षण विवरण / Test Details\n\n"
        report += "| ID | कमांड / Command | अपेक्षित इंटेंट / Expected Intent | वास्तविक इंटेंट / Actual Intent | स्थिति / Status |\n"
        report += "|----|----------------|----------------------------------|------------------------------|-----------------|\n"
        
        for detail in result["details"]:
            report += f"| {detail['id']} | `{detail['command']}` | {detail['expected_intent']} | {detail['actual_intent']} | {'✅' if detail['status'] == 'Pass' else '❌'} |\n"
        
        report += "\n"
    
    report += "## विफल परीक्षण विवरण / Failed Test Details\n\n"
    
    failed_tests = []
    for result in results:
        for detail in result["details"]:
            if detail["status"] == "Fail":
                failed_tests.append(detail)
    
    if failed_tests:
        for i, test in enumerate(failed_tests):
            report += f"### {i+1}. {test['command']}\n\n"
            report += f"**श्रेणी / Category:** {test['id'][:2]}\n\n"
            report += f"**अपेक्षित इंटेंट / Expected Intent:** {test['expected_intent']}\n\n"
            report += f"**वास्तविक इंटेंट / Actual Intent:** {test['actual_intent']}\n\n"
            
            if test['expected_entities']:
                report += f"**अपेक्षित एंटिटीज / Expected Entities:** {json.dumps(test['expected_entities'], ensure_ascii=False)}\n\n"
                report += f"**वास्तविक एंटिटीज / Actual Entities:** {json.dumps(test['actual_entities'], ensure_ascii=False)}\n\n"
            
            if test['expected_error']:
                report += f"**अपेक्षित त्रुटि / Expected Error:** {test['expected_error']}\n\n"
                report += f"**वास्तविक त्रुटि / Actual Error:** {test['actual_error']}\n\n"
            
            report += "---\n\n"
    else:
        report += "कोई विफल परीक्षण नहीं / No failed tests\n\n"
    
    return report

def run_all_tests():
    """
    Run all test cases and generate a report
    """
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
    
    logger.info("Starting Hindi-English language QA tests")
    
    # Run all test cases
    english_results = run_test_cases(ENGLISH_TEST_CASES, "English Commands")
    hindi_results = run_test_cases(HINDI_TEST_CASES, "Hindi Commands")
    mixed_results = run_test_cases(MIXED_LANGUAGE_TEST_CASES, "Mixed Language Commands")
    switching_results = run_test_cases(LANGUAGE_SWITCHING_TEST_CASES, "Language Switching Commands")
    error_results = run_test_cases(ERROR_HANDLING_TEST_CASES, "Error Handling Commands")
    
    # Generate the report
    results = [english_results, hindi_results, mixed_results, switching_results, error_results]
    report = generate_test_report(results)
    
    # Write the report to a file
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'hindi_english_test_results.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    logger.info(f"Test report generated at {report_path}")
    
    # Print summary
    total_tests = sum(result["total"] for result in results)
    total_passed = sum(result["passed"] for result in results)
    total_failed = sum(result["failed"] for result in results)
    
    logger.info(f"Test Summary: {total_passed}/{total_tests} tests passed ({(total_passed / total_tests) * 100 if total_tests > 0 else 0:.2f}%)")
    
    return results

if __name__ == "__main__":
    run_all_tests()