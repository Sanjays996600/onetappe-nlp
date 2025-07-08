#!/usr/bin/env python3
"""
Improved Edit Stock Command Recognition Module

This module enhances the recognition of edit_stock commands in both English and Hindi
by implementing more robust pattern matching and entity extraction.
"""

import re
import json
import sys
sys.path.append('/Users/sanjaysuman/One Tappe/OneTappeProject')

# Import the existing modules to extend them
from nlp.intent_handler import INTENT_PATTERNS, extract_product_details
from nlp.hindi_support import HINDI_INTENT_PATTERNS, extract_hindi_product_details

# Enhanced English patterns for edit_stock intent
ENHANCED_EDIT_STOCK_PATTERNS = [
    r"(?i)(?:update|change|modify|edit|set)\s+(?:the\s+)?(?:stock|inventory|quantity)\s+(?:of|for)?\s+([\w\s]+)\s+(?:to|as)\s+(\d+)(?:\s*(?:units|items|pieces|qty|quantity))?",
    r"(?i)(?:make|set)\s+([\w\s]+)\s+(?:stock|inventory|quantity)\s+(?:to|as)\s+(\d+)(?:\s*(?:units|items|pieces|qty|quantity))?",
    r"(?i)(?:change|update)\s+([\w\s]+)\s+(?:to|as)\s+(\d+)(?:\s*(?:units|items|pieces|qty|quantity))?",
    r"(?i)([\w\s]+)\s+(?:stock|inventory|quantity)\s+(?:update|change|modify|edit|set)\s+(?:to|as)?\s+(\d+)(?:\s*(?:units|items|pieces|qty|quantity))?"
]

# Enhanced Hindi patterns for edit_stock intent
ENHANCED_HINDI_EDIT_STOCK_PATTERNS = [
    r"([\u0900-\u097F\s]+)\s+(?:का|की|के)\s+(?:स्टॉक|मात्रा|इन्वेंटरी)\s+(\d+)\s+(?:करो|करें|कर|बनाओ|बनाएं|अपडेट|अपडेट करो|अपडेट करें|सेट करो|सेट करें)",
    r"([\u0900-\u097F\s]+)\s+(?:स्टॉक|मात्रा|इन्वेंटरी)\s+(\d+)\s+(?:करो|करें|कर|बनाओ|बनाएं|अपडेट|अपडेट करो|अपडेट करें|सेट करो|सेट करें)",
    r"(?:स्टॉक|मात्रा|इन्वेंटरी)\s+(?:अपडेट|बदलो|बदलें|सेट)\s+([\u0900-\u097F\s]+)\s+(\d+)\s+(?:करो|करें|कर|बनाओ|बनाएं)",
    r"([\u0900-\u097F\s]+)\s+(\d+)\s+(?:स्टॉक|मात्रा|इन्वेंटरी)\s+(?:करो|करें|कर|बनाओ|बनाएं|अपडेट|अपडेट करो|अपडेट करें|सेट करो|सेट करें)"
]

def extract_enhanced_edit_stock_details(text):
    """
    Enhanced function to extract product name and quantity from edit_stock commands in English.
    
    Args:
        text (str): The command text to extract details from
        
    Returns:
        dict: A dictionary containing product name and quantity
    """
    for pattern in ENHANCED_EDIT_STOCK_PATTERNS:
        match = re.search(pattern, text)
        if match:
            product_name = match.group(1).strip().lower()
            quantity = int(match.group(2))
            return {"name": product_name, "quantity": quantity}
    
    # Fallback to original extraction if enhanced patterns don't match
    return extract_product_details(text)

def extract_enhanced_hindi_edit_stock_details(text):
    """
    Enhanced function to extract product name and quantity from edit_stock commands in Hindi.
    
    Args:
        text (str): The command text to extract details from
        
    Returns:
        dict: A dictionary containing product name and quantity
    """
    for pattern in ENHANCED_HINDI_EDIT_STOCK_PATTERNS:
        match = re.search(pattern, text)
        if match:
            product_name = match.group(1).strip()
            quantity = int(match.group(2))
            return {"name": product_name, "quantity": quantity}
    
    # Fallback to original extraction if enhanced patterns don't match
    return extract_hindi_product_details(text)

def test_enhanced_edit_stock_recognition():
    """
    Test the enhanced edit_stock recognition with various English and Hindi commands.
    """
    english_commands = [
        "Update stock of Sugar to 15",
        "Change the inventory of Rice to 20 units",
        "Set Tea quantity to 10 pieces",
        "Make Coffee stock 25",
        "Sugar stock update to 30",
        "Modify stock for Flour to 40 qty",
        "Update Tea to 50",
        "Change Milk to 12 units"
    ]
    
    hindi_commands = [
        "चीनी का स्टॉक 15 करो",
        "चावल की मात्रा 20 अपडेट करें",
        "चाय स्टॉक 10 बनाओ",
        "कॉफी 25 स्टॉक करो",
        "आटा का स्टॉक 40 सेट करें",
        "दूध की मात्रा 12 करो",
        "स्टॉक अपडेट चीनी 30 करो",
        "चाय 50 स्टॉक अपडेट करें"
    ]
    
    print("\nTesting Enhanced English Edit Stock Commands:\n")
    for cmd in english_commands:
        details = extract_enhanced_edit_stock_details(cmd)
        print(f"Command: {cmd}")
        print(f"Extracted: {json.dumps(details, ensure_ascii=False)}\n")
    
    print("\nTesting Enhanced Hindi Edit Stock Commands:\n")
    for cmd in hindi_commands:
        details = extract_enhanced_hindi_edit_stock_details(cmd)
        print(f"Command: {cmd}")
        print(f"Extracted: {json.dumps(details, ensure_ascii=False)}\n")

def apply_enhanced_patterns():
    """
    Apply the enhanced patterns to the existing INTENT_PATTERNS and HINDI_INTENT_PATTERNS.
    This function demonstrates how to integrate the enhanced patterns into the existing system.
    """
    # Create copies of the original patterns
    enhanced_english_patterns = INTENT_PATTERNS.copy()
    enhanced_hindi_patterns = HINDI_INTENT_PATTERNS.copy()
    
    # Replace the edit_stock patterns with enhanced ones
    enhanced_english_patterns['edit_stock'] = ENHANCED_EDIT_STOCK_PATTERNS
    enhanced_hindi_patterns['edit_stock'] = ENHANCED_HINDI_EDIT_STOCK_PATTERNS
    
    return enhanced_english_patterns, enhanced_hindi_patterns

def compare_pattern_performance():
    """
    Compare the performance of original and enhanced patterns on test cases.
    """
    test_cases = [
        # English test cases
        {"text": "Update stock of Sugar to 15", "language": "en", "expected": {"name": "sugar", "quantity": 15}},
        {"text": "Change Tea to 50", "language": "en", "expected": {"name": "tea", "quantity": 50}},
        {"text": "Sugar stock update to 30", "language": "en", "expected": {"name": "sugar", "quantity": 30}},
        {"text": "Make Coffee stock 25", "language": "en", "expected": {"name": "coffee", "quantity": 25}},
        
        # Hindi test cases
        {"text": "चीनी का स्टॉक 15 करो", "language": "hi", "expected": {"name": "चीनी", "quantity": 15}},
        {"text": "चाय 50 स्टॉक अपडेट करें", "language": "hi", "expected": {"name": "चाय", "quantity": 50}},
        {"text": "स्टॉक अपडेट चीनी 30 करो", "language": "hi", "expected": {"name": "चीनी", "quantity": 30}},
        {"text": "कॉफी 25 स्टॉक करो", "language": "hi", "expected": {"name": "कॉफी", "quantity": 25}}
    ]
    
    original_success = 0
    enhanced_success = 0
    
    print("\nComparing Original vs Enhanced Pattern Performance:\n")
    print("{:<40} {:<15} {:<15}".format("Test Case", "Original", "Enhanced"))
    print("-" * 70)
    
    for case in test_cases:
        text = case["text"]
        language = case["language"]
        expected = case["expected"]
        
        # Test with original patterns
        if language == "en":
            original_result = extract_product_details(text)
        else:
            original_result = extract_hindi_product_details(text)
            
        # Test with enhanced patterns
        if language == "en":
            enhanced_result = extract_enhanced_edit_stock_details(text)
        else:
            enhanced_result = extract_enhanced_hindi_edit_stock_details(text)
        
        # Check if results match expected
        original_match = original_result == expected
        enhanced_match = enhanced_result == expected
        
        if original_match:
            original_success += 1
        if enhanced_match:
            enhanced_success += 1
        
        print("{:<40} {:<15} {:<15}".format(
            text, 
            "✅ Pass" if original_match else "❌ Fail", 
            "✅ Pass" if enhanced_match else "❌ Fail"
        ))
    
    total_cases = len(test_cases)
    print("\nSummary:")
    print(f"Original Patterns: {original_success}/{total_cases} ({original_success/total_cases*100:.1f}%)")
    print(f"Enhanced Patterns: {enhanced_success}/{total_cases} ({enhanced_success/total_cases*100:.1f}%)")

if __name__ == "__main__":
    print("\n===== Enhanced Edit Stock Command Recognition =====\n")
    test_enhanced_edit_stock_recognition()
    compare_pattern_performance()
    
    print("\n===== Integration Example =====\n")
    enhanced_english, enhanced_hindi = apply_enhanced_patterns()
    print(f"Enhanced English patterns contain {len(enhanced_english['edit_stock'])} edit_stock patterns")
    print(f"Enhanced Hindi patterns contain {len(enhanced_hindi['edit_stock'])} edit_stock patterns")
    
    print("\nTo integrate these enhanced patterns into the existing system:")
    print("1. Update the INTENT_PATTERNS['edit_stock'] in intent_handler.py")
    print("2. Update the HINDI_INTENT_PATTERNS['edit_stock'] in hindi_support.py")
    print("3. Replace the extraction functions or extend them with the enhanced versions")