#!/usr/bin/env python3

import sys
import os

# Add the parent directory to the path so we can import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.hindi_support import extract_hindi_custom_date_range, parse_hindi_date, parse_hindi_command

# Test cases for Hindi custom date range extraction
test_cases = [
    "रिपोर्ट दिखाओ 1 जनवरी से 31 जनवरी तक",
    "1 जनवरी से 31 जनवरी तक की रिपोर्ट दिखाओ",
    "1 जून से 20 जून तक की रिपोर्ट दिखाओ",
    "रिपोर्ट दिखाओ 1 जून से 20 जून तक",
    "रिपोर्ट 1 जनवरी से 31 जनवरी",
    "बिक्री रिपोर्ट 1 जून से 20 जून"
]

print("\nTesting Hindi custom date range extraction:\n")
for i, test in enumerate(test_cases):
    print(f"\nTest case {i+1}: '{test}'")
    print("Direct extraction:")
    result = extract_hindi_custom_date_range(test)
    print(f"Custom range result: {result}")
    
    print("\nFull command parsing:")
    parsed = parse_hindi_command(test)
    print(f"Intent: {parsed.get('intent')}")
    print(f"Language: {parsed.get('language')}")
    print(f"Entities: {parsed.get('entities')}")