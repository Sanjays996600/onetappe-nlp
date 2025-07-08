#!/usr/bin/env python3

import sys
import os
import json
from typing import Dict, Any, List

# Add the parent directory to sys.path to import the modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our intent handlers
from multilingual_handler import parse_multilingual_command


def run_test_cases(test_cases: List[Dict[str, Any]]) -> None:
    """Run a series of test cases and report results."""
    passed = 0
    failed = 0
    failed_tests = []
    
    print("\n===== RUNNING COMPREHENSIVE TESTS =====\n")
    
    for i, test in enumerate(test_cases):
        command = test["command"]
        expected_intent = test["expected_intent"]
        expected_entities = test["expected_entities"]
        expected_language = test["expected_language"]
        
        print(f"\nTest #{i+1}: '{command}'")
        print(f"Expected: {expected_language} - {expected_intent} - {expected_entities}")
        
        result = parse_multilingual_command(command)
        actual_intent = result["intent"]
        actual_entities = result["entities"]
        actual_language = result["language"]
        
        print(f"Actual:   {actual_language} - {actual_intent} - {actual_entities}")
        
        # Check if the test passed
        intent_match = actual_intent == expected_intent
        entities_match = True
        
        # Check if all expected entities are present with correct values
        for key, value in expected_entities.items():
            if key not in actual_entities or actual_entities[key] != value:
                entities_match = False
                break
        
        language_match = actual_language == expected_language
        
        if intent_match and entities_match and language_match:
            print("✅ PASSED")
            passed += 1
        else:
            print("❌ FAILED")
            if not intent_match:
                print(f"  Intent mismatch: expected '{expected_intent}', got '{actual_intent}'")
            if not entities_match:
                print(f"  Entities mismatch: expected {expected_entities}, got {actual_entities}")
            if not language_match:
                print(f"  Language mismatch: expected '{expected_language}', got '{actual_language}'")
            failed += 1
            failed_tests.append({
                "test_num": i+1,
                "command": command,
                "expected": {
                    "intent": expected_intent,
                    "entities": expected_entities,
                    "language": expected_language
                },
                "actual": {
                    "intent": actual_intent,
                    "entities": actual_entities,
                    "language": actual_language
                }
            })
    
    print(f"\n===== TEST RESULTS: {passed} passed, {failed} failed =====\n")
    print(f"Success rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed > 0:
        print("\n===== FAILED TESTS SUMMARY =====\n")
        for test in failed_tests:
            print(f"Test #{test['test_num']}: '{test['command']}'")
            print(f"Expected: {test['expected']['language']} - {test['expected']['intent']} - {test['expected']['entities']}")
            print(f"Actual:   {test['actual']['language']} - {test['actual']['intent']} - {test['actual']['entities']}")
            print()


def main():
    # Define test cases with expected results
    test_cases = [
        # English - Basic inventory commands
        {
            "command": "Show my products",
            "expected_intent": "get_inventory",
            "expected_entities": {},
            "expected_language": "en"
        },
        {
            "command": "View my inventory",
            "expected_intent": "get_inventory",
            "expected_entities": {},
            "expected_language": "en"
        },
        
        # English - Report commands
        {
            "command": "Send today's report",
            "expected_intent": "get_report",
            "expected_entities": {"range": "today"},
            "expected_language": "en"
        },
        {
            "command": "Get yesterday's sales report",
            "expected_intent": "get_report",
            "expected_entities": {"range": "yesterday"},
            "expected_language": "en"
        },
        {
            "command": "Show me this week's report",
            "expected_intent": "get_report",
            "expected_entities": {"range": "week"},
            "expected_language": "en"
        },
        
        # English - Low stock commands
        {
            "command": "Show low stock items",
            "expected_intent": "get_low_stock",
            "expected_entities": {},
            "expected_language": "en"
        },
        {
            "command": "Which products are running low?",
            "expected_intent": "get_low_stock",
            "expected_entities": {},
            "expected_language": "en"
        },
        
        # English - Add product commands
        {
            "command": "Add new product Rice 50rs 20qty",
            "expected_intent": "add_product",
            "expected_entities": {"name": "rice", "price": 50, "stock": 20},
            "expected_language": "en"
        },
        {
            "command": "Add product Sugar 30 15",
            "expected_intent": "add_product",
            "expected_entities": {"name": "sugar", "price": 30, "stock": 15},
            "expected_language": "en"
        },
        
        # English - Edit stock commands
        {
            "command": "Edit stock of Rice to 100",
            "expected_intent": "edit_stock",
            "expected_entities": {"name": "rice", "stock": 100},
            "expected_language": "en"
        },
        {
            "command": "Update Sugar stock to 50",
            "expected_intent": "edit_stock",
            "expected_entities": {"name": "sugar", "stock": 50},
            "expected_language": "en"
        },
        
        # English - Order commands
        {
            "command": "Show my orders",
            "expected_intent": "get_orders",
            "expected_entities": {},
            "expected_language": "en"
        },
        {
            "command": "View recent orders",
            "expected_intent": "get_orders",
            "expected_entities": {},
            "expected_language": "en"
        },
        
        # Hindi - Basic inventory commands
        {
            "command": "मेरे प्रोडक्ट दिखाओ",
            "expected_intent": "get_inventory",
            "expected_entities": {},
            "expected_language": "hi"
        },
        {
            "command": "इन्वेंटरी दिखाओ",
            "expected_intent": "get_inventory",
            "expected_entities": {},
            "expected_language": "hi"
        },
        
        # Hindi - Report commands
        {
            "command": "आज की रिपोर्ट भेजो",
            "expected_intent": "get_report",
            "expected_entities": {"range": "today"},
            "expected_language": "hi"
        },
        {
            "command": "कल की बिक्री रिपोर्ट दिखाओ",
            "expected_intent": "get_report",
            "expected_entities": {"range": "yesterday"},
            "expected_language": "hi"
        },
        
        # Hindi - Low stock commands
        {
            "command": "कम स्टॉक वाले आइटम दिखाओ",
            "expected_intent": "get_low_stock",
            "expected_entities": {},
            "expected_language": "hi"
        },
        
        # Hindi - Add product commands
        {
            "command": "नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो",
            "expected_intent": "add_product",
            "expected_entities": {"name": "चावल", "price": 50, "stock": 20},
            "expected_language": "hi"
        },
        
        # Hindi - Edit stock commands
        {
            "command": "चावल का स्टॉक 100 करो",
            "expected_intent": "edit_stock",
            "expected_entities": {"name": "चावल", "stock": 100},
            "expected_language": "hi"
        },
        
        # Edge cases and variations
        {
            "command": "I want to add a new product called Wheat for 45 rupees with 30 pieces",
            "expected_intent": "add_product",
            "expected_entities": {"name": "wheat", "price": 45, "stock": 30},
            "expected_language": "en"
        },
        {
            "command": "मुझे चीनी का स्टॉक 75 करना है",
            "expected_intent": "edit_stock",
            "expected_entities": {"name": "चीनी", "stock": 75},
            "expected_language": "hi"
        }
    ]
    
    run_test_cases(test_cases)


if __name__ == "__main__":
    main()