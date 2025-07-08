#!/usr/bin/env python3
"""
Enhanced NLP Implementation Module

This module provides enhanced NLP capabilities for the OneTappe application,
focusing on improved multilingual support for English, Hindi, and mixed language inputs.
"""

import re
import sys
import json
sys.path.append('/Users/sanjaysuman/One Tappe/OneTappeProject')

# Import existing modules
from nlp.intent_handler import INTENT_PATTERNS
from nlp.hindi_support import HINDI_INTENT_PATTERNS

# Import enhanced modules
from nlp.mixed_entity_extraction import extract_mixed_product_details, normalize_mixed_command
from nlp.enhanced_multilingual_parser import parse_multilingual_command

# Define enhanced intent patterns with improved add_product support
def get_enhanced_intent_patterns():
    """
    Create enhanced intent patterns by merging existing patterns with improvements.
    
    Returns:
        tuple: (enhanced_english_patterns, enhanced_hindi_patterns)
    """
    # Create copies of the original patterns
    enhanced_english_patterns = INTENT_PATTERNS.copy()
    enhanced_hindi_patterns = HINDI_INTENT_PATTERNS.copy()
    
    # Enhanced add_product patterns for English
    enhanced_english_patterns['add_product'] = [
        r"(?i)add\s+(?:new\s+)?(?:product\s+)?(\w+)",
        r"(?i)add\s+(?:new\s+)?(?:product\s+)?(\w+)\s+(?:with\s+)?(?:price|at|rate)\s+([₹$]?\d+)",
        r"(?i)add\s+(?:new\s+)?(?:product\s+)?(\w+)\s+(?:with\s+)?(?:stock|qty|quantity)\s+(\d+)",
        r"(?i)add\s+(?:new\s+)?(?:product\s+)?(\w+)\s+(?:with\s+)?(?:price|at|rate)\s+([₹$]?\d+)\s+(?:and\s+)?(?:stock|qty|quantity)\s+(\d+)",
        r"(?i)add\s+(?:new\s+)?(?:product\s+)?(\w+)\s+(?:with\s+)?(?:stock|qty|quantity)\s+(\d+)\s+(?:and\s+)?(?:price|at|rate)\s+([₹$]?\d+)",
        # Mixed language patterns (English base)
        r"(?i)add\s+(?:new\s+)?(?:product\s+)?([\w\s]+)\s+(?:price|at|rate)\s+([₹$]?\d+)\s+(?:stock|qty|quantity)\s+(\d+)",
        r"(?i)add\s+(?:new\s+)?(?:product\s+)?([\w\s]+)\s+(?:stock|qty|quantity)\s+(\d+)\s+(?:price|at|rate)\s+([₹$]?\d+)",
        r"(?i)add\s+(?:नया|नई|नए)\s+(?:product|प्रोडक्ट)\s+([\w\s]+)",
        r"(?i)([\w\s]+)\s+(?:नाम का|नाम की)\s+(?:product|प्रोडक्ट)\s+add\s+(?:करो|करें|karo|karen)"
    ]
    
    # Enhanced add_product patterns for Hindi
    enhanced_hindi_patterns['add_product'] = [
        r"(?:नया|नई|नए)\s+(?:प्रोडक्ट|प्रॉडक्ट|उत्पाद)\s+([\u0900-\u097F\s]+)\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)",
        r"([\u0900-\u097F\s]+)\s+(?:नाम का|नाम की)\s+(?:प्रोडक्ट|प्रॉडक्ट|उत्पाद)\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)",
        r"(?:प्रोडक्ट|प्रॉडक्ट|उत्पाद)\s+([\u0900-\u097F\s]+)\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)",
        r"([\u0900-\u097F\s]+)\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)",
        # Mixed language patterns (Hindi base)
        r"(?:नया|नई|नए)\s+product\s+([\w\s]+)\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)",
        r"([\w\s]+)\s+(?:नाम का|नाम की)\s+product\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)",
        r"product\s+([\w\s]+)\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)",
        r"([\w\s]+)\s+product\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)",
        r"(?:नया|नई|नए)\s+product\s+add\s+(?:करो|करें)\s+([\w\s]+)"
    ]
    
    return enhanced_english_patterns, enhanced_hindi_patterns

# Get the enhanced patterns
ENHANCED_INTENT_PATTERNS, ENHANCED_HINDI_INTENT_PATTERNS = get_enhanced_intent_patterns()

def process_add_product_intent(command_text, language="en", is_mixed=False):
    """
    Process add_product intent with enhanced support for mixed language inputs.
    
    Args:
        command_text (str): The command text to process
        language (str): The primary language of the command ('en' or 'hi')
        is_mixed (bool): Whether the command contains mixed language
        
    Returns:
        dict: Extracted product details
    """
    # For mixed language or complex commands, use the specialized mixed entity extraction
    if is_mixed or '\u0900' <= command_text[0] <= '\u097F' or any(word in command_text.lower() for word in ['नया', 'नई', 'नए', 'जोड़ो', 'जोड़ें', 'एड']):
        product_details = extract_mixed_product_details(command_text)
        if product_details:
            # Convert to standard format
            result = {}
            if "product_name" in product_details:
                result["name"] = product_details["product_name"]
            if "price" in product_details:
                result["price"] = product_details["price"]
            if "stock" in product_details:
                result["quantity"] = product_details["stock"]
            return result
    
    # If mixed entity extraction failed or wasn't applicable, try language-specific extraction
    result = {}
    
    # Extract product name
    if language == "en":
        # English patterns
        name_patterns = [
            r"(?i)add\s+(?:new\s+)?(?:product\s+)?([\w\s]+?)(?:\s+with|\s+price|\s+at|\s+stock|\s+qty|$)",
            r"(?i)add\s+(?:new\s+)?(?:product\s+)?([\w\s]+)\s+(?:price|at|rate|stock|qty)"
        ]
    else:  # Hindi
        # Hindi patterns
        name_patterns = [
            r"(?:नया|नई|नए)\s+(?:प्रोडक्ट|प्रॉडक्ट|उत्पाद)\s+([\u0900-\u097F\s]+?)(?:\s+|$)",
            r"([\u0900-\u097F\s]+)\s+(?:नाम का|नाम की)\s+(?:प्रोडक्ट|प्रॉडक्ट|उत्पाद)",
            r"(?:प्रोडक्ट|प्रॉडक्ट|उत्पाद)\s+([\u0900-\u097F\s]+)\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)",
            r"([\u0900-\u097F\s]+?)\s+(?:जोड़ो|जोड़ें|एड करो|एड करें)"
        ]
    
    # Try to extract product name
    for pattern in name_patterns:
        match = re.search(pattern, command_text)
        if match:
            result["name"] = match.group(1).strip()
            break
    
    # Extract price
    price_patterns = [
        r"(?i)(?:price|at|rate|मूल्य|कीमत|प्राइस|रेट)\s+([₹$]?\d+)",
        r"([₹$]?\d+)\s+(?:rs|रुपए|रुपये|rupees|rupee)"
    ]
    
    for pattern in price_patterns:
        match = re.search(pattern, command_text)
        if match:
            result["price"] = match.group(1).strip()
            break
    
    # Extract stock/quantity
    stock_patterns = [
        r"(?i)(?:stock|qty|quantity|स्टॉक|मात्रा)\s+(\d+)",
        r"(\d+)\s+(?:units|pieces|pcs|इकाई|नग)"
    ]
    
    for pattern in stock_patterns:
        match = re.search(pattern, command_text)
        if match:
            result["quantity"] = match.group(1).strip()
            break
    
    return result if result else None

def handle_add_product_command(command_text):
    """
    Handle add_product command with enhanced multilingual support.
    
    Args:
        command_text (str): The command text to process
        
    Returns:
        dict: Processed command with intent and entities
    """
    # Parse the command using the enhanced multilingual parser
    parsed_command = parse_multilingual_command(command_text)
    
    # If the intent is add_product, process it with our specialized function
    if parsed_command["intent"] == "add_product":
        entities = process_add_product_intent(
            command_text, 
            language=parsed_command["language"],
            is_mixed=parsed_command.get("is_mixed", False)
        )
        
        if entities:
            parsed_command["entities"] = entities
    
    return parsed_command

def test_add_product_handling():
    """
    Test the enhanced add_product intent handling with various commands.
    """
    test_commands = [
        # English commands
        "Add new product Sugar price 50 stock 100",
        "Add Rice with price 40 and stock 200",
        "Add product Wheat at 30 with quantity 150",
        
        # Hindi commands
        "नया प्रोडक्ट चीनी जोड़ो कीमत 50 स्टॉक 100",
        "चावल नाम का प्रोडक्ट जोड़ो कीमत 40 स्टॉक 200",
        "गेहूं प्रोडक्ट जोड़ो कीमत 30 स्टॉक 150",
        
        # Mixed language commands
        "नया product add करो Sugar price 50 stock 100",
        "Add नया product Rice price 40 stock 200",
        "Wheat नाम का product add करो price 30 stock 150",
        
        # Incomplete commands (for fallback testing)
        "नया product जोड़ो Sugar",
        "Add product Rice",
        "Wheat product add करो"
    ]
    
    print("\nTesting Enhanced Add Product Intent Handling:\n")
    
    for cmd in test_commands:
        result = handle_add_product_command(cmd)
        
        print(f"Command: {cmd}")
        print(f"Intent: {result['intent']}")
        print(f"Language: {result['language']}")
        print(f"Mixed Language: {'Yes' if result.get('is_mixed', False) else 'No'}")
        print(f"Entities: {json.dumps(result.get('entities', {}), ensure_ascii=False)}")
        print("---")

if __name__ == "__main__":
    test_add_product_handling()