#!/usr/bin/env python3
"""
Improved Time Parsing Module

This module enhances the recognition and parsing of time-related expressions
in both English and Hindi for get_orders and get_report commands.
"""

import re
import json
import datetime
import sys
sys.path.append('/Users/sanjaysuman/One Tappe/OneTappeProject')

# Define enhanced time range patterns for English
ENHANCED_TIME_RANGE_PATTERNS = {
    # Today patterns
    "today": [
        r"(?i)\b(?:today|current day|this day)\b",
    ],
    # Yesterday patterns
    "yesterday": [
        r"(?i)\b(?:yesterday|previous day|last day)\b",
    ],
    # This week patterns
    "week": [
        r"(?i)\b(?:this week|current week)\b",
    ],
    # Last week patterns
    "last_week": [
        r"(?i)\b(?:last week|previous week|past week)\b",
    ],
    # This month patterns
    "month": [
        r"(?i)\b(?:this month|current month)\b",
    ],
    # Last month patterns
    "last_month": [
        r"(?i)\b(?:last month|previous month|past month)\b",
    ],
    # All time patterns
    "all": [
        r"(?i)\b(?:all|all time|everything|entire|complete)\b",
    ],
    # Custom date range patterns
    "custom_range": [
        r"(?i)\b(?:from|between)\s+([\w\s,]+)\s+(?:to|and|till|until)\s+([\w\s,]+)\b",
    ]
}

# Define enhanced time range patterns for Hindi
ENHANCED_HINDI_TIME_RANGE_PATTERNS = {
    # Today patterns
    "today": [
        r"\b(?:आज|वर्तमान दिन|इस दिन)\b",
    ],
    # Yesterday patterns
    "yesterday": [
        r"\b(?:कल|बीता दिन|पिछला दिन|गत दिन)\b",
    ],
    # This week patterns
    "week": [
        r"\b(?:इस सप्ताह|इस हफ्ते|वर्तमान सप्ताह|वर्तमान हफ्ते)\b",
    ],
    # Last week patterns
    "last_week": [
        r"\b(?:पिछले सप्ताह|पिछले हफ्ते|बीते सप्ताह|बीते हफ्ते|गत सप्ताह|गत हफ्ते)\b",
    ],
    # This month patterns
    "month": [
        r"\b(?:इस महीने|इस माह|वर्तमान महीने|वर्तमान माह)\b",
    ],
    # Last month patterns
    "last_month": [
        r"\b(?:पिछले महीने|पिछले माह|बीते महीने|बीते माह|गत महीने|गत माह)\b",
    ],
    # All time patterns
    "all": [
        r"\b(?:सभी|पूरा|संपूर्ण|सम्पूर्ण|सारा|सब)\b",
    ],
    # Custom date range patterns
    "custom_range": [
        r"\b(?:से|के बीच)\s+([\u0900-\u097F\s,]+)\s+(?:तक|और|से)\s+([\u0900-\u097F\s,]+)\b",
    ]
}

def extract_time_range(text, language="en"):
    """
    Extract time range from text in either English or Hindi.
    
    Args:
        text (str): The command text to extract time range from
        language (str): Language code ('en' for English, 'hi' for Hindi)
        
    Returns:
        dict: A dictionary containing the time range information
    """
    patterns = ENHANCED_TIME_RANGE_PATTERNS if language == "en" else ENHANCED_HINDI_TIME_RANGE_PATTERNS
    
    # Check for each time range pattern
    for range_type, pattern_list in patterns.items():
        for pattern in pattern_list:
            match = re.search(pattern, text)
            if match:
                if range_type == "custom_range" and match.groups():
                    # Handle custom date range
                    start_date = match.group(1)
                    end_date = match.group(2)
                    return {"range": "custom", "start_date": start_date, "end_date": end_date}
                else:
                    return {"range": range_type}
    
    # Default to "all" if no time range is specified
    return {"range": "all"}

def get_date_range_for_time_period(time_period):
    """
    Convert a time period string to actual date range.
    
    Args:
        time_period (str): Time period identifier (today, yesterday, week, etc.)
        
    Returns:
        tuple: (start_date, end_date) as datetime objects
    """
    today = datetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if time_period == "today":
        return today, today.replace(hour=23, minute=59, second=59)
    
    elif time_period == "yesterday":
        yesterday = today - datetime.timedelta(days=1)
        return yesterday, yesterday.replace(hour=23, minute=59, second=59)
    
    elif time_period == "week":
        # This week (starting from Monday)
        start_of_week = today - datetime.timedelta(days=today.weekday())
        return start_of_week, today.replace(hour=23, minute=59, second=59)
    
    elif time_period == "last_week":
        # Last week (Monday to Sunday)
        start_of_last_week = today - datetime.timedelta(days=today.weekday() + 7)
        end_of_last_week = start_of_last_week + datetime.timedelta(days=6, hours=23, minutes=59, seconds=59)
        return start_of_last_week, end_of_last_week
    
    elif time_period == "month":
        # This month (1st to today)
        start_of_month = today.replace(day=1)
        return start_of_month, today.replace(hour=23, minute=59, second=59)
    
    elif time_period == "last_month":
        # Last month
        if today.month == 1:
            start_of_last_month = today.replace(year=today.year-1, month=12, day=1)
        else:
            start_of_last_month = today.replace(month=today.month-1, day=1)
        
        # End of last month
        end_of_last_month = today.replace(day=1) - datetime.timedelta(days=1)
        end_of_last_month = end_of_last_month.replace(hour=23, minute=59, second=59)
        
        return start_of_last_month, end_of_last_month
    
    elif time_period == "all":
        # All time - use a far past date and today
        far_past = today.replace(year=today.year-10)  # 10 years ago
        return far_past, today.replace(hour=23, minute=59, second=59)
    
    # Default to today if unknown time period
    return today, today.replace(hour=23, minute=59, second=59)

def test_time_range_extraction():
    """
    Test the enhanced time range extraction with various English and Hindi commands.
    """
    english_commands = [
        "Show me orders from today",
        "Get yesterday's orders",
        "Show this week's report",
        "Get orders from last week",
        "Show me this month's sales",
        "Get report for last month",
        "Show all orders",
        "Get orders from January 1 to February 28"
    ]
    
    hindi_commands = [
        "आज के ऑर्डर दिखाओ",
        "कल के ऑर्डर दिखाओ",
        "इस हफ्ते की रिपोर्ट दिखाओ",
        "पिछले हफ्ते के ऑर्डर दिखाओ",
        "इस महीने की बिक्री दिखाओ",
        "पिछले महीने की रिपोर्ट दिखाओ",
        "सभी ऑर्डर दिखाओ",
        "1 जनवरी से 28 फरवरी तक के ऑर्डर दिखाओ"
    ]
    
    print("\nTesting Enhanced English Time Range Extraction:\n")
    for cmd in english_commands:
        time_range = extract_time_range(cmd, "en")
        print(f"Command: {cmd}")
        print(f"Extracted: {json.dumps(time_range, ensure_ascii=False)}")
        
        # If it's not a custom range, show the actual date range
        if time_range.get("range") != "custom":
            start_date, end_date = get_date_range_for_time_period(time_range.get("range"))
            print(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n")
        else:
            print("\n")
    
    print("\nTesting Enhanced Hindi Time Range Extraction:\n")
    for cmd in hindi_commands:
        time_range = extract_time_range(cmd, "hi")
        print(f"Command: {cmd}")
        print(f"Extracted: {json.dumps(time_range, ensure_ascii=False)}")
        
        # If it's not a custom range, show the actual date range
        if time_range.get("range") != "custom":
            start_date, end_date = get_date_range_for_time_period(time_range.get("range"))
            print(f"Date Range: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}\n")
        else:
            print("\n")

def compare_with_test_cases():
    """
    Compare the enhanced time parsing with test cases.
    """
    test_cases = [
        # English test cases
        {"text": "Show me orders from today", "language": "en", "expected": {"range": "today"}},
        {"text": "Get yesterday's orders", "language": "en", "expected": {"range": "yesterday"}},
        {"text": "Show this week's report", "language": "en", "expected": {"range": "week"}},
        {"text": "Get orders from last week", "language": "en", "expected": {"range": "last_week"}},
        {"text": "Show me this month's sales", "language": "en", "expected": {"range": "month"}},
        {"text": "Get report for last month", "language": "en", "expected": {"range": "last_month"}},
        {"text": "Show all orders", "language": "en", "expected": {"range": "all"}},
        
        # Hindi test cases
        {"text": "आज के ऑर्डर दिखाओ", "language": "hi", "expected": {"range": "today"}},
        {"text": "कल के ऑर्डर दिखाओ", "language": "hi", "expected": {"range": "yesterday"}},
        {"text": "इस हफ्ते की रिपोर्ट दिखाओ", "language": "hi", "expected": {"range": "week"}},
        {"text": "पिछले हफ्ते के ऑर्डर दिखाओ", "language": "hi", "expected": {"range": "last_week"}},
        {"text": "इस महीने की बिक्री दिखाओ", "language": "hi", "expected": {"range": "month"}},
        {"text": "पिछले महीने की रिपोर्ट दिखाओ", "language": "hi", "expected": {"range": "last_month"}},
        {"text": "सभी ऑर्डर दिखाओ", "language": "hi", "expected": {"range": "all"}}
    ]
    
    success_count = 0
    
    print("\nComparing Enhanced Time Range Extraction with Test Cases:\n")
    print("{:<40} {:<20} {:<20}".format("Test Case", "Expected", "Result"))
    print("-" * 80)
    
    for case in test_cases:
        text = case["text"]
        language = case["language"]
        expected = case["expected"]
        
        result = extract_time_range(text, language)
        success = result.get("range") == expected.get("range")
        
        if success:
            success_count += 1
        
        print("{:<40} {:<20} {:<20} {}".format(
            text, 
            expected.get("range"), 
            result.get("range"),
            "✅ Pass" if success else "❌ Fail"
        ))
    
    total_cases = len(test_cases)
    print(f"\nAccuracy: {success_count}/{total_cases} ({success_count/total_cases*100:.1f}%)")

def integration_example():
    """
    Example of how to integrate the enhanced time parsing into the existing system.
    """
    print("\nIntegration Example:\n")
    
    # Example for get_orders command
    order_command_en = "Show me orders from last week"
    order_command_hi = "पिछले हफ्ते के ऑर्डर दिखाओ"
    
    # Parse the commands
    time_range_en = extract_time_range(order_command_en, "en")
    time_range_hi = extract_time_range(order_command_hi, "hi")
    
    # Get actual date ranges
    start_date_en, end_date_en = get_date_range_for_time_period(time_range_en.get("range"))
    start_date_hi, end_date_hi = get_date_range_for_time_period(time_range_hi.get("range"))
    
    # Format for API request
    api_params_en = {
        "start_date": start_date_en.strftime("%Y-%m-%d"),
        "end_date": end_date_en.strftime("%Y-%m-%d")
    }
    
    api_params_hi = {
        "start_date": start_date_hi.strftime("%Y-%m-%d"),
        "end_date": end_date_hi.strftime("%Y-%m-%d")
    }
    
    print("English Command: " + order_command_en)
    print("Extracted Time Range: " + time_range_en.get("range"))
    print("API Parameters: " + json.dumps(api_params_en))
    
    print("\nHindi Command: " + order_command_hi)
    print("Extracted Time Range: " + time_range_hi.get("range"))
    print("API Parameters: " + json.dumps(api_params_hi))
    
    print("\nTo integrate this enhanced time parsing into the existing system:")
    print("1. Update the time range extraction functions in both English and Hindi modules")
    print("2. Add the date range conversion function to convert time periods to actual dates")
    print("3. Modify the API request generation to include the proper date parameters")

if __name__ == "__main__":
    print("\n===== Enhanced Time Range Parsing =====\n")
    test_time_range_extraction()
    compare_with_test_cases()
    integration_example()