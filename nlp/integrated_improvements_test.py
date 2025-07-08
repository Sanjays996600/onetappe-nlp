#!/usr/bin/env python3
"""
Integrated Test Script for NLP Improvements

This script demonstrates the combined improvements for all commands in both English and Hindi.
It tests language detection, intent recognition, entity extraction, and time parsing.
"""

import re
import json
from datetime import datetime, timedelta
import random

# Define character ranges for language detection
HINDI_CHAR_RANGE = r'[\u0900-\u097F]'
ENGLISH_CHAR_RANGE = r'[a-zA-Z]'

# Enhanced language detection
def detect_language_with_confidence(text):
    """Detect language with confidence score"""
    hindi_chars = len(re.findall(HINDI_CHAR_RANGE, text))
    english_chars = len(re.findall(ENGLISH_CHAR_RANGE, text))
    
    total_chars = hindi_chars + english_chars
    if total_chars == 0:
        return "unknown", 0.0
    
    hindi_ratio = hindi_chars / total_chars
    english_ratio = english_chars / total_chars
    
    if hindi_ratio > english_ratio:
        return "hi", hindi_ratio
    else:
        return "en", english_ratio

def detect_mixed_language(text):
    """Detect if text contains mixed languages"""
    lang, confidence = detect_language_with_confidence(text)
    
    # If confidence is below threshold, it might be mixed
    if confidence < 0.8:
        hindi_segments = re.findall(f"{HINDI_CHAR_RANGE}+", text)
        english_segments = re.findall(f"{ENGLISH_CHAR_RANGE}+", text)
        
        if hindi_segments and english_segments:
            return True, {
                "primary": lang,
                "segments": {
                    "hi": hindi_segments,
                    "en": english_segments
                }
            }
    
    return False, {"primary": lang}

# Enhanced intent patterns
INTENT_PATTERNS = {
    'edit_stock': [
        r"(?i)(?:update|change|modify|edit|set)\s+(?:the\s+)?(?:stock|inventory|quantity)\s+(?:of|for)?\s+([\w\s]+)\s+(?:to|as)\s+(\d+)(?:\s*(?:units|items|pieces|qty|quantity))?",
        r"(?i)(?:make|set)\s+([\w\s]+)\s+(?:stock|inventory|quantity)\s+(?:to|as)\s+(\d+)(?:\s*(?:units|items|pieces|qty|quantity))?",
        r"(?i)(?:change|update)\s+([\w\s]+)\s+(?:to|as)\s+(\d+)(?:\s*(?:units|items|pieces|qty|quantity))?",
        r"(?i)([\w\s]+)\s+(?:stock|inventory|quantity)\s+(?:update|change|modify|edit|set)\s+(?:to|as)?\s+(\d+)(?:\s*(?:units|items|pieces|qty|quantity))?"
    ],
    'get_orders': [
        r"(?i)(?:show|get|fetch|display|list)\s+(?:me\s+)?(?:the\s+)?(?:orders|sales)(?:\s+from)?(?:\s+(.+))?",
        r"(?i)(?:orders|sales)(?:\s+from)?(?:\s+(.+))?"
    ],
    'get_report': [
        r"(?i)(?:show|get|fetch|display|generate)\s+(?:me\s+)?(?:the\s+)?(?:report|reports|sales report|sales summary)(?:\s+for)?(?:\s+(.+))?",
        r"(?i)(?:report|reports|sales report|sales summary)(?:\s+for)?(?:\s+(.+))?"
    ],
    'get_low_stock': [
        r"(?i)(?:show|get|fetch|display|list)\s+(?:me\s+)?(?:the\s+)?(?:low stock|items with low stock|products with low stock|low inventory)",
        r"(?i)(?:low stock|items with low stock|products with low stock|low inventory)"
    ],
    'search_product': [
        r"(?i)(?:search|find|look for|locate)\s+(?:product|item)?\s*([\w\s]+)",
        r"(?i)(?:product|item)\s+(?:search|lookup)\s+(?:for)?\s*([\w\s]+)"
    ]
}

HINDI_INTENT_PATTERNS = {
    'edit_stock': [
        r"([\u0900-\u097F\s]+)\s+(?:का|की|के)\s+(?:स्टॉक|मात्रा|इन्वेंटरी)\s+(\d+)\s+(?:करो|करें|कर|बनाओ|बनाएं|अपडेट|अपडेट करो|अपडेट करें|सेट करो|सेट करें)",
        r"([\u0900-\u097F\s]+)\s+(?:स्टॉक|मात्रा|इन्वेंटरी)\s+(\d+)\s+(?:करो|करें|कर|बनाओ|बनाएं|अपडेट|अपडेट करो|अपडेट करें|सेट करो|सेट करें)",
        r"(?:स्टॉक|मात्रा|इन्वेंटरी)\s+(?:अपडेट|बदलो|बदलें|सेट)\s+([\u0900-\u097F\s]+)\s+(\d+)\s+(?:करो|करें|कर|बनाओ|बनाएं)",
        r"([\u0900-\u097F\s]+)\s+(\d+)\s+(?:स्टॉक|मात्रा|इन्वेंटरी)\s+(?:करो|करें|कर|बनाओ|बनाएं|अपडेट|अपडेट करो|अपडेट करें|सेट करो|सेट करें)"
    ],
    'get_orders': [
        r"(?:ऑर्डर|ऑर्डर्स|सेल्स|बिक्री|बिक्री के ऑर्डर)\s+(?:दिखाओ|दिखाएं|दिखाइए|दिखाना|दिखा दो|दिखा दें|दिखा|देखना|देखें|देखिए|देखो|लाओ|लाएं|लाइए)(?:\s+(.+))?",
        r"(?:मुझे|हमें)?\s+(?:ऑर्डर|ऑर्डर्स|सेल्स|बिक्री|बिक्री के ऑर्डर)\s+(?:दिखाओ|दिखाएं|दिखाइए|दिखाना|दिखा दो|दिखा दें|दिखा|देखना|देखें|देखिए|देखो|लाओ|लाएं|लाइए)(?:\s+(.+))?"
    ],
    'get_report': [
        r"(?:रिपोर्ट|रिपोर्ट्स|सेल्स रिपोर्ट|बिक्री रिपोर्ट|बिक्री की रिपोर्ट)\s+(?:दिखाओ|दिखाएं|दिखाइए|दिखाना|दिखा दो|दिखा दें|दिखा|देखना|देखें|देखिए|देखो|लाओ|लाएं|लाइए|जनरेट करो|जनरेट करें|बनाओ|बनाएं)(?:\s+(.+))?",
        r"(?:मुझे|हमें)?\s+(?:रिपोर्ट|रिपोर्ट्स|सेल्स रिपोर्ट|बिक्री रिपोर्ट|बिक्री की रिपोर्ट)\s+(?:दिखाओ|दिखाएं|दिखाइए|दिखाना|दिखा दो|दिखा दें|दिखा|देखना|देखें|देखिए|देखो|लाओ|लाएं|लाइए|जनरेट करो|जनरेट करें|बनाओ|बनाएं)(?:\s+(.+))?"
    ],
    'get_low_stock': [
        r"(?:कम स्टॉक|लो स्टॉक|कम इन्वेंटरी|कम मात्रा वाले प्रोडक्ट|कम स्टॉक वाले आइटम)\s+(?:दिखाओ|दिखाएं|दिखाइए|दिखाना|दिखा दो|दिखा दें|दिखा|देखना|देखें|देखिए|देखो|लाओ|लाएं|लाइए)",
        r"(?:मुझे|हमें)?\s+(?:कम स्टॉक|लो स्टॉक|कम इन्वेंटरी|कम मात्रा वाले प्रोडक्ट|कम स्टॉक वाले आइटम)\s+(?:दिखाओ|दिखाएं|दिखाइए|दिखाना|दिखा दो|दिखा दें|दिखा|देखना|देखें|देखिए|देखो|लाओ|लाएं|लाइए)"
    ],
    'search_product': [
        r"([\u0900-\u097F\s]+)\s+(?:सर्च करो|सर्च करें|सर्च|खोजो|खोजें|खोज|ढूंढो|ढूंढें|ढूंढ|फाइंड करो|फाइंड करें|फाइंड)",
        r"(?:सर्च करो|सर्च करें|सर्च|खोजो|खोजें|खोज|ढूंढो|ढूंढें|ढूंढ|फाइंड करो|फाइंड करें|फाइंड)\s+([\u0900-\u097F\s]+)",
        r"(?:प्रोडक्ट|आइटम|वस्तु)\s+(?:सर्च|खोज|ढूंढ|फाइंड)\s+([\u0900-\u097F\s]+)"
    ]
}

# Enhanced time parsing
ENHANCED_TIME_RANGE_PATTERNS = {
    "today": r"(?i)(?:today|current day|this day)",
    "yesterday": r"(?i)(?:yesterday|previous day|last day)",
    "this_week": r"(?i)(?:this week|current week)",
    "last_week": r"(?i)(?:last week|previous week|past week)",
    "this_month": r"(?i)(?:this month|current month)",
    "last_month": r"(?i)(?:last month|previous month|past month)",
    "this_year": r"(?i)(?:this year|current year)",
    "last_year": r"(?i)(?:last year|previous year|past year)",
    "last_7_days": r"(?i)(?:last|past)\s+(?:7|seven)\s+days",
    "last_30_days": r"(?i)(?:last|past)\s+(?:30|thirty)\s+days",
    "last_90_days": r"(?i)(?:last|past)\s+(?:90|ninety)\s+days",
    "all": r"(?i)(?:all|all time|everything|entire|complete)"
}

ENHANCED_HINDI_TIME_RANGE_PATTERNS = {
    "today": r"(?:आज|आज का|आज के|वर्तमान दिन|इस दिन)",
    "yesterday": r"(?:कल|बीता दिन|पिछला दिन|गत दिन)",
    "this_week": r"(?:इस सप्ताह|इस हफ्ते|वर्तमान सप्ताह|वर्तमान हफ्ते|चालू सप्ताह|चालू हफ्ते)",
    "last_week": r"(?:पिछले सप्ताह|पिछले हफ्ते|गत सप्ताह|गत हफ्ते|बीते सप्ताह|बीते हफ्ते)",
    "this_month": r"(?:इस महीने|इस माह|वर्तमान महीने|वर्तमान माह|चालू महीने|चालू माह)",
    "last_month": r"(?:पिछले महीने|पिछले माह|गत महीने|गत माह|बीते महीने|बीते माह)",
    "this_year": r"(?:इस साल|इस वर्ष|वर्तमान साल|वर्तमान वर्ष|चालू साल|चालू वर्ष)",
    "last_year": r"(?:पिछले साल|पिछले वर्ष|गत साल|गत वर्ष|बीते साल|बीते वर्ष)",
    "last_7_days": r"(?:पिछले|बीते|गत)\s+(?:7|सात)\s+(?:दिन|दिनों)",
    "last_30_days": r"(?:पिछले|बीते|गत)\s+(?:30|तीस)\s+(?:दिन|दिनों)",
    "last_90_days": r"(?:पिछले|बीते|गत)\s+(?:90|नब्बे)\s+(?:दिन|दिनों)",
    "all": r"(?:सभी|पूरा|संपूर्ण|सम्पूर्ण|सारा|सारे|सब)"
}

def extract_time_range(text, language="en"):
    """Extract time range from text using enhanced patterns"""
    patterns = ENHANCED_TIME_RANGE_PATTERNS if language == "en" else ENHANCED_HINDI_TIME_RANGE_PATTERNS
    
    for time_period, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE if language == "en" else 0):
            return time_period
    
    return "all"  # Default to all time if no specific period is mentioned

def get_date_range_for_time_period(time_period):
    """Convert time period to actual date range"""
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    if time_period == "today":
        start_date = today
        end_date = today + timedelta(days=1) - timedelta(microseconds=1)
    elif time_period == "yesterday":
        start_date = today - timedelta(days=1)
        end_date = today - timedelta(microseconds=1)
    elif time_period == "this_week":
        start_date = today - timedelta(days=today.weekday())
        end_date = start_date + timedelta(days=7) - timedelta(microseconds=1)
    elif time_period == "last_week":
        start_date = today - timedelta(days=today.weekday() + 7)
        end_date = start_date + timedelta(days=7) - timedelta(microseconds=1)
    elif time_period == "this_month":
        start_date = today.replace(day=1)
        if today.month == 12:
            end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(microseconds=1)
        else:
            end_date = today.replace(month=today.month + 1, day=1) - timedelta(microseconds=1)
    elif time_period == "last_month":
        if today.month == 1:
            start_date = today.replace(year=today.year - 1, month=12, day=1)
        else:
            start_date = today.replace(month=today.month - 1, day=1)
        end_date = today.replace(day=1) - timedelta(microseconds=1)
    elif time_period == "this_year":
        start_date = today.replace(month=1, day=1)
        end_date = today.replace(year=today.year + 1, month=1, day=1) - timedelta(microseconds=1)
    elif time_period == "last_year":
        start_date = today.replace(year=today.year - 1, month=1, day=1)
        end_date = today.replace(month=1, day=1) - timedelta(microseconds=1)
    elif time_period == "last_7_days":
        start_date = today - timedelta(days=7)
        end_date = today - timedelta(microseconds=1)
    elif time_period == "last_30_days":
        start_date = today - timedelta(days=30)
        end_date = today - timedelta(microseconds=1)
    elif time_period == "last_90_days":
        start_date = today - timedelta(days=90)
        end_date = today - timedelta(microseconds=1)
    else:  # "all" or default
        start_date = datetime(2000, 1, 1)
        end_date = today + timedelta(days=1) - timedelta(microseconds=1)
    
    return {
        "start_date": start_date.strftime("%Y-%m-%d"),
        "end_date": end_date.strftime("%Y-%m-%d")
    }

# Integrated command parsing
def detect_intent(text, language="en"):
    """Detect intent from text using enhanced patterns"""
    patterns = INTENT_PATTERNS if language == "en" else HINDI_INTENT_PATTERNS
    
    for intent, intent_patterns in patterns.items():
        for pattern in intent_patterns:
            match = re.search(pattern, text, re.IGNORECASE if language == "en" else 0)
            if match:
                return intent, match
    
    return "unknown", None

def extract_entities(text, intent, match, language="en"):
    """Extract entities based on intent and language"""
    entities = {}
    
    if intent == "edit_stock":
        if match and match.groups():
            if len(match.groups()) >= 2:
                entities["product_name"] = match.group(1).strip()
                entities["quantity"] = int(match.group(2))
    
    elif intent in ["get_orders", "get_report"]:
        time_period = extract_time_range(text, language)
        entities["time_period"] = time_period
        entities.update(get_date_range_for_time_period(time_period))
    
    elif intent == "search_product":
        if match and match.groups():
            entities["product_name"] = match.group(1).strip()
    
    return entities

def parse_command(text):
    """Parse command using all enhanced features"""
    # Detect language with mixed language support
    is_mixed, lang_info = detect_mixed_language(text)
    primary_language = lang_info["primary"]
    
    # Detect intent
    intent, match = detect_intent(text, primary_language)
    
    # Extract entities
    entities = extract_entities(text, intent, match, primary_language)
    
    # Generate normalized text
    normalized_text = text.lower() if primary_language == "en" else text
    
    # Prepare response
    response = {
        "raw_text": text,
        "original_text": text,
        "normalized_text": normalized_text,
        "language": primary_language,
        "is_mixed_language": is_mixed,
        "intent": intent,
        "entities": entities,
        "status": "success" if intent != "unknown" else "failed",
        "api_params": format_api_params(intent, entities)
    }
    
    return response

def format_api_params(intent, entities):
    """Format entities into API parameters"""
    if intent == "edit_stock":
        return {
            "action": "update_inventory",
            "product_name": entities.get("product_name", ""),
            "quantity": entities.get("quantity", 0)
        }
    
    elif intent == "get_orders":
        return {
            "action": "fetch_orders",
            "start_date": entities.get("start_date", ""),
            "end_date": entities.get("end_date", "")
        }
    
    elif intent == "get_report":
        return {
            "action": "generate_report",
            "start_date": entities.get("start_date", ""),
            "end_date": entities.get("end_date", "")
        }
    
    elif intent == "get_low_stock":
        return {
            "action": "fetch_low_stock",
            "threshold": 10  # Default threshold
        }
    
    elif intent == "search_product":
        return {
            "action": "search_products",
            "query": entities.get("product_name", "")
        }
    
    return {}

# Mock API calls for testing
def mock_api_call(api_params):
    """Mock API call for testing"""
    action = api_params.get("action", "")
    
    if action == "update_inventory":
        return {
            "success": True,
            "message": f"Updated inventory for {api_params.get('product_name')} to {api_params.get('quantity')}"
        }
    
    elif action == "fetch_orders":
        return {
            "success": True,
            "orders": [
                {"id": f"ORD-{random.randint(1000, 9999)}", "date": api_params.get("start_date"), "amount": random.randint(100, 5000)},
                {"id": f"ORD-{random.randint(1000, 9999)}", "date": api_params.get("end_date"), "amount": random.randint(100, 5000)}
            ]
        }
    
    elif action == "generate_report":
        return {
            "success": True,
            "report": {
                "period": f"{api_params.get('start_date')} to {api_params.get('end_date')}",
                "total_sales": random.randint(5000, 50000),
                "total_orders": random.randint(10, 100)
            }
        }
    
    elif action == "fetch_low_stock":
        return {
            "success": True,
            "low_stock_items": [
                {"name": "Sugar", "quantity": random.randint(1, 9)},
                {"name": "Rice", "quantity": random.randint(1, 9)},
                {"name": "Wheat", "quantity": random.randint(1, 9)}
            ]
        }
    
    elif action == "search_products":
        return {
            "success": True,
            "products": [
                {"name": api_params.get("query"), "price": random.randint(10, 1000), "quantity": random.randint(1, 100)}
            ]
        }
    
    return {"success": False, "message": "Unknown action"}

# Format response for user
def format_user_response(parsed_command, api_response):
    """Format response for user based on intent and language"""
    intent = parsed_command["intent"]
    language = parsed_command["language"]
    raw_text = parsed_command.get("raw_text", parsed_command.get("original_text"))
    normalized_text = parsed_command.get("normalized_text")
    
    if language == "en":
        if intent == "edit_stock":
            return f"Stock updated: {api_response.get('message', '')}"
        
        elif intent == "get_orders":
            orders = api_response.get("orders", [])
            return f"Found {len(orders)} orders for the period {parsed_command['entities'].get('time_period')}"
        
        elif intent == "get_report":
            report = api_response.get("report", {})
            return f"Sales report for {report.get('period')}: ₹{report.get('total_sales')} from {report.get('total_orders')} orders"
        
        elif intent == "get_low_stock":
            items = api_response.get("low_stock_items", [])
            return f"Found {len(items)} items with low stock"
        
        elif intent == "search_product":
            products = api_response.get("products", [])
            return f"Found {len(products)} products matching '{parsed_command['entities'].get('product_name', '')}'" 
    
    else:  # Hindi
        if intent == "edit_stock":
            return f"स्टॉक अपडेट किया गया: {api_response.get('message', '')}"
        
        elif intent == "get_orders":
            orders = api_response.get("orders", [])
            return f"{parsed_command['entities'].get('time_period')} के लिए {len(orders)} ऑर्डर मिले"
        
        elif intent == "get_report":
            report = api_response.get("report", {})
            return f"{report.get('period')} की बिक्री रिपोर्ट: ₹{report.get('total_sales')} ({report.get('total_orders')} ऑर्डर)"
        
        elif intent == "get_low_stock":
            items = api_response.get("low_stock_items", [])
            return f"{len(items)} आइटम कम स्टॉक में हैं"
        
        elif intent == "search_product":
            products = api_response.get("products", [])
            return f"'{parsed_command['entities'].get('product_name', '')}' से मिलते जुलते {len(products)} प्रोडक्ट मिले"
    
    return "I couldn't understand that command" if language == "en" else "मैं इस कमांड को समझ नहीं पाया"

# Test commands
ENGLISH_TEST_COMMANDS = [
    # Edit stock commands
    "Update sugar stock to 50 units",
    "Set rice inventory to 100",
    "Change wheat quantity to 75 pieces",
    "Sugar stock update to 25",
    
    # Get orders commands
    "Show me orders from yesterday",
    "Get orders from last week",
    "Display orders from this month",
    "Orders from last 30 days",
    
    # Get report commands
    "Show me the sales report for this week",
    "Generate report for last month",
    "Get sales summary for last 90 days",
    "Report for this year",
    
    # Get low stock commands
    "Show me low stock items",
    "Display products with low stock",
    "List low inventory",
    "Get items with low stock",
    
    # Search product commands
    "Search for sugar",
    "Find rice",
    "Look for wheat flour",
    "Product search for salt"
]

HINDI_TEST_COMMANDS = [
    # Edit stock commands
    "चीनी का स्टॉक 50 करो",
    "चावल की मात्रा 100 अपडेट करें",
    "गेहूं 75 स्टॉक बनाओ",
    "स्टॉक अपडेट चीनी 25",
    
    # Get orders commands
    "कल के ऑर्डर दिखाओ",
    "पिछले हफ्ते के ऑर्डर्स दिखाएं",
    "इस महीने की बिक्री दिखाओ",
    "पिछले 30 दिनों के ऑर्डर",
    
    # Get report commands
    "इस हफ्ते की सेल्स रिपोर्ट दिखाओ",
    "पिछले महीने की रिपोर्ट जनरेट करो",
    "पिछले 90 दिनों की बिक्री रिपोर्ट दिखाएं",
    "इस साल की रिपोर्ट",
    
    # Get low stock commands
    "कम स्टॉक वाले आइटम दिखाओ",
    "लो स्टॉक दिखाएं",
    "कम इन्वेंटरी दिखाओ",
    "कम मात्रा वाले प्रोडक्ट दिखाएं",
    
    # Search product commands
    "चीनी सर्च करो",
    "चावल खोजो",
    "गेहूं का आटा ढूंढो",
    "नमक फाइंड करें"
]

# Mixed language test commands
MIXED_TEST_COMMANDS = [
    "Show me चीनी inventory",
    "चावल stock update to 50",
    "Get orders from पिछले हफ्ते",
    "इस महीने की sales report दिखाओ",
    "Search for गेहूं"
]

# Run tests and save results
def run_tests():
    results = {
        "english": [],
        "hindi": [],
        "mixed": []
    }
    
    print("\n===== TESTING ENGLISH COMMANDS =====\n")
    for command in ENGLISH_TEST_COMMANDS:
        print(f"\nCommand: {command}")
        parsed = parse_command(command)
        api_response = mock_api_call(parsed["api_params"])
        user_response = format_user_response(parsed, api_response)
        
        print(f"Intent: {parsed['intent']}")
        print(f"Entities: {json.dumps(parsed['entities'], indent=2)}")
        print(f"API Params: {json.dumps(parsed['api_params'], indent=2)}")
        print(f"Response: {user_response}")
        
        results["english"].append({
            "command": command,
            "parsed": parsed,
            "response": user_response,
            "success": parsed["status"] == "success"
        })
    
    print("\n===== TESTING HINDI COMMANDS =====\n")
    for command in HINDI_TEST_COMMANDS:
        print(f"\nCommand: {command}")
        parsed = parse_command(command)
        api_response = mock_api_call(parsed["api_params"])
        user_response = format_user_response(parsed, api_response)
        
        print(f"Intent: {parsed['intent']}")
        print(f"Entities: {json.dumps(parsed['entities'], indent=2)}")
        print(f"API Params: {json.dumps(parsed['api_params'], indent=2)}")
        print(f"Response: {user_response}")
        
        results["hindi"].append({
            "command": command,
            "parsed": parsed,
            "response": user_response,
            "success": parsed["status"] == "success"
        })
    
    print("\n===== TESTING MIXED LANGUAGE COMMANDS =====\n")
    for command in MIXED_TEST_COMMANDS:
        print(f"\nCommand: {command}")
        parsed = parse_command(command)
        api_response = mock_api_call(parsed["api_params"])
        user_response = format_user_response(parsed, api_response)
        
        print(f"Intent: {parsed['intent']}")
        print(f"Is Mixed: {parsed['is_mixed_language']}")
        print(f"Primary Language: {parsed['language']}")
        print(f"Entities: {json.dumps(parsed['entities'], indent=2)}")
        print(f"API Params: {json.dumps(parsed['api_params'], indent=2)}")
        print(f"Response: {user_response}")
        
        results["mixed"].append({
            "command": command,
            "parsed": parsed,
            "response": user_response,
            "success": parsed["status"] == "success"
        })
    
    # Calculate accuracy
    accuracy = calculate_accuracy(results)
    print("\n===== ACCURACY SUMMARY =====\n")
    print(json.dumps(accuracy, indent=2))
    
    # Save results to file
    save_results(results, accuracy)
    
    return results, accuracy

def calculate_accuracy(results):
    """Calculate accuracy for each intent and language"""
    accuracy = {
        "english": {},
        "hindi": {},
        "mixed": {},
        "overall": {}
    }
    
    # Group by intent
    english_by_intent = {}
    hindi_by_intent = {}
    mixed_by_intent = {}
    
    for result in results["english"]:
        intent = result["parsed"]["intent"]
        if intent not in english_by_intent:
            english_by_intent[intent] = []
        english_by_intent[intent].append(result["success"])
    
    for result in results["hindi"]:
        intent = result["parsed"]["intent"]
        if intent not in hindi_by_intent:
            hindi_by_intent[intent] = []
        hindi_by_intent[intent].append(result["success"])
    
    for result in results["mixed"]:
        intent = result["parsed"]["intent"]
        if intent not in mixed_by_intent:
            mixed_by_intent[intent] = []
        mixed_by_intent[intent].append(result["success"])
    
    # Calculate accuracy by intent
    for intent, successes in english_by_intent.items():
        accuracy["english"][intent] = sum(successes) / len(successes) * 100
    
    for intent, successes in hindi_by_intent.items():
        accuracy["hindi"][intent] = sum(successes) / len(successes) * 100
    
    for intent, successes in mixed_by_intent.items():
        accuracy["mixed"][intent] = sum(successes) / len(successes) * 100
    
    # Calculate overall accuracy
    all_english_successes = [r["success"] for r in results["english"]]
    all_hindi_successes = [r["success"] for r in results["hindi"]]
    all_mixed_successes = [r["success"] for r in results["mixed"]]
    
    accuracy["overall"]["english"] = sum(all_english_successes) / len(all_english_successes) * 100
    accuracy["overall"]["hindi"] = sum(all_hindi_successes) / len(all_hindi_successes) * 100
    accuracy["overall"]["mixed"] = sum(all_mixed_successes) / len(all_mixed_successes) * 100
    
    all_successes = all_english_successes + all_hindi_successes + all_mixed_successes
    accuracy["overall"]["total"] = sum(all_successes) / len(all_successes) * 100
    
    return accuracy

def save_results(results, accuracy):
    """Save test results and accuracy to file"""
    output = {
        "results": results,
        "accuracy": accuracy,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    with open("integrated_test_results.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("\nResults saved to integrated_test_results.json")

if __name__ == "__main__":
    run_tests()