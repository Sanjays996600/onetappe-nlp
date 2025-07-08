#!/usr/bin/env python3
"""
Test Mixed Search Product Entity Extraction

This module tests the functionality of the extract_mixed_search_product_details function
from mixed_entity_extraction.py module, focusing on product name extraction from
mixed language (Hinglish) search queries.
"""

import sys
sys.path.append('/Users/sanjaysuman/One Tappe/OneTappeProject')

from nlp.mixed_entity_extraction import extract_mixed_search_product_details, normalize_mixed_command

def test_mixed_search_product_extraction():
    """
    Test the mixed language search product extraction with various commands.
    """
    test_cases = [
        # English search queries
        "search for rice",
        "find sugar",
        "check if wheat is available",
        "is salt available",
        "do you have tea",
        "information about coffee",
        "details of milk",
        
        # Hindi search queries
        "चावल के बारे में जानकारी दो",
        "चीनी खोजो",
        "गेहूं उपलब्ध है क्या",
        "क्या नमक है",
        "चाय है क्या",
        "कॉफी के बारे में बताओ",
        "दूध की जानकारी दो",
        
        # Mixed language search queries
        "rice के बारे में information दो",
        "search for चावल",
        "find चीनी",
        "check if गेहूं is available",
        "क्या salt available है",
        "is चाय available",
        "do you have कॉफी",
        "milk है क्या",
        "information about दूध",
        "दाल के details बताओ",
        "मसाला search करो",
        "oil की जानकारी दो",
        
        # Edge cases and variations
        "rice information",
        "चावल details",
        "search चीनी",
        "find गेहूं",
        "नमक available?",
        "tea उपलब्ध है?",
        "coffee stock में है?",
        "milk in stock?",
        "दूध है?",
        "oil stock check",
        "मसाला खोजो",
        "दाल search",
        
        # Complex mixed queries
        "क्या आपके पास rice है",
        "do you have चावल in stock",
        "चीनी के बारे में details provide करो",
        "give me information about गेहूं",
        "नमक stock में है या नहीं बताओ",
        "tell me if tea is available",
        "coffee के बारे में जानकारी चाहिए",
        "need details about milk",
        "दूध available है क्या store में",
        "is oil in stock in your store",
        "मसाला के बारे में search करो",
        "search for दाल in inventory"
    ]
    
    print("\nTesting Mixed Language Search Product Extraction:\n")
    print("{:<50} {:<20}".format("Command", "Extracted Product"))
    print("-" * 70)
    
    success_count = 0
    total_cases = len(test_cases)
    
    for cmd in test_cases:
        try:
            # First normalize the command
            normalized_cmd = normalize_mixed_command(cmd)
            
            # Extract product name
            result = extract_mixed_search_product_details(normalized_cmd)
            
            # Format output
            if result and result.get("name"):
                success_count += 1
                print("{:<50} {:<20}".format(
                    cmd[:50], 
                    result.get("name", "")
                ))
            else:
                print("{:<50} {:<20} ❌".format(
                    cmd[:50],
                    "Not found"
                ))
        except Exception as e:
            print("{:<50} {:<20} ❌".format(
                cmd[:50],
                f"Error: {str(e)[:20]}"
            ))
    
    print(f"\nAccuracy: {success_count}/{total_cases} ({success_count/total_cases*100:.1f}%)")

if __name__ == "__main__":
    print("===== Testing Mixed Language Search Product Extraction =====")
    test_mixed_search_product_extraction()