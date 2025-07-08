import re
import logging
from typing import Dict, Any, List, Tuple, Optional

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='nlp_intent_handler.log'
)
logger = logging.getLogger(__name__)

# Intent patterns with example phrases
INTENT_PATTERNS = {
    "get_inventory": [
        r"show\s+(?:my\s+)?(?:products|inventory)",
        r"view\s+(?:my\s+)?(?:products|inventory)",
        r"list\s+(?:my\s+)?(?:products|inventory)",
        r"what\s+(?:products|items)\s+do\s+i\s+have",
        r"inventory\s+status",
        r"current\s*[-\.]?\s*stock",
        r"current\s*[-\.]?\s*स्टॉक",
        r"show\s+current\s*[-\.]?\s*स्टॉक",
        r"check\s+current\s*[-\.]?\s*स्टॉक",
        r"display\s+current\s*[-\.]?\s*स्टॉक"
    ],
    "get_low_stock": [
        r"(?:show|view|list|get)\s+(?:me\s+)?(?:the\s+)?(?:low|out\s+of)\s+stock\s+(?:items|products)",
        r"(?:which|what)\s+(?:products|items)\s+(?:are\s+)?(?:running|getting)\s+low",
        r"(?:products|items)\s+(?:running|getting)\s+low",
        r"low\s+stock\s+(?:items|products|alert)",
        r"(?:items|products)\s+(?:with\s+)?low\s+stock",
        r"(?:show|view|list|get)\s+(?:me\s+)?(?:the\s+)?(?:items|products)\s+(?:with\s+)?(?:stock\s+)?(?:below|less\s+than|under)\s+\d+"
    ],
    "get_report": [
        r"(?:send|get|show|view)\s+(?:me\s+)?(?:the\s+)?(yesterday|today|this\s+week|this\s+month)(?:'s)?\s+(?:sales\s+)?report",
        r"(?:sales\s+)?report\s+for\s+(yesterday|today|this\s+week|this\s+month)",
        r"(yesterday|today|this\s+week|this\s+month)(?:'s)?\s+(?:sales\s+)?report",
        r"(?:send|get|show|view)\s+(?:me\s+)?(?:the\s+)?(?:sales\s+)?report",
        r"(?:show|get|view)\s+(?:me\s+)?(?:the\s+)?report\s+from\s+(.+?)\s+to\s+(.+?)(?:\s+|$)",
        r"(?:show|get|view)\s+(?:me\s+)?(?:the\s+)?report\s+between\s+(.+?)\s+and\s+(.+?)(?:\s+|$)"
    ],
    "get_top_products": [
        r"(?:show|get|view|display)\s+(?:me\s+)?(?:the\s+)?top\s+(?:selling\s+)?products",
        r"(?:show|get|view|display)\s+(?:me\s+)?(?:the\s+)?top\s+(\d+)\s+(?:selling\s+)?products",
        r"top\s+(?:selling\s+)?products\s+(?:this|for)\s+(?:week|month|day)",
        r"top\s+(\d+)\s+(?:selling\s+)?products\s+(?:this|for)\s+(?:week|month|day)",
        r"(?:show|get|view|display)\s+(?:me\s+)?(?:the\s+)?top\s+(?:selling\s+)?products\s+from\s+(.+?)\s+to\s+(.+?)(?:\s+|$)",
        r"(?:show|get|view|display)\s+(?:me\s+)?(?:the\s+)?top\s+(\d+)\s+(?:selling\s+)?products\s+from\s+(.+?)\s+to\s+(.+?)(?:\s+|$)"
    ],
    "get_customer_data": [
        r"show\s+(?:me\s+)?(?:the\s+)?customer\s+(?:data|details|insights|information)",
        r"get\s+(?:me\s+)?(?:the\s+)?customer\s+(?:data|details|insights|information)",
        r"(?:show|list|display)\s+(?:my\s+)?(?:top\s+)?(?:\d+\s+)?customers",
        r"who\s+(?:are|were)\s+(?:my\s+)?(?:top\s+)?(?:\d+\s+)?customers"
    ],
    "add_product": [
        r"add\s+(?:new\s+)?product\s+(.+)",
        r"create\s+(?:new\s+)?product\s+(.+)",
        r"register\s+(?:new\s+)?product\s+(.+)",
        r"i\s+want\s+to\s+add\s+(?:a\s+)?(?:new\s+)?product",
        r"add\s+(?:a\s+)?(?:new\s+)?(?:product|item)\s+called"
    ],
    "edit_stock": [
        r"edit\s+stock\s+(?:of\s+)?(.+?)\s+to\s+(-?\d+)",
        r"update\s+(?:the\s+)?(?:stock\s+(?:of\s+)?)?(.+?)\s+(?:stock\s+)?to\s+(-?\d+)",
        r"change\s+stock\s+(?:of\s+)?(.+?)\s+to\s+(-?\d+)",
        r"set\s+stock\s+(?:of\s+)?(.+?)\s+to\s+(-?\d+)",
        r"(?:change|update)\s+(?:the\s+)?quantity",
        r"stock\s+(?:update|change)",
        r"update\s+stock\s+of\s+(\w+)\s+to\s+(-?\d+)",
        r"change\s+stock\s+of\s+(\w+)\s+to\s+(-?\d+)",
        r"update\s+(.+?)\s+stock\s+to\s+(-?\d+)",
        # Add patterns for transliterated Hindi words
        r"अपडेट\s+स्टॉक\s+(?:of\s+)?(.+?)\s+to\s+(-?\d+)",
        r"अपडेट\s+(?:the\s+)?(?:स्टॉक\s+(?:of\s+)?)?(.+?)\s+(?:स्टॉक\s+)?to\s+(-?\d+)",
        r"अपडेट\s+(.+?)\s+स्टॉक\s+to\s+(-?\d+)"
    ],
    "get_orders": [
        r"show\s+(?:my\s+)?(?:orders|recent\s+orders)",
        r"list\s+(?:my\s+)?(?:orders|recent\s+orders)",
        r"view\s+(?:my\s+)?(?:orders|recent\s+orders)",
        r"get\s+(?:my\s+)?(?:orders|recent\s+orders)",
        r"get\s+(?:today's|todays|today)\s+orders",
        r"order\s+history",
        r"customer\s+orders",
        r"recent\s+orders"
    ],
    "search_product": [
        r"(?:search|look)\s+for\s+(.+?)(?:\s+|$)",
        r"do\s+(?:you|we|I)\s+have\s+(.+?)(?:\s+in\s+stock|\s+available|$)",
        r"is\s+(.+?)(?:\s+in\s+stock|\s+available|$)",
        r"check\s+(?:if|whether)\s+(.+?)\s+(?:is|are)\s+(?:in\s+stock|available)",
        r"(?:find|locate)\s+(.+?)(?:\s+|$)"
    ]
}

# Entity extraction patterns
def extract_product_details(text: str) -> Dict[str, Any]:
    """
    Extract product name, price, and stock from text like:
    "Add new product Rice 50rs 20qty" or "Add product Rice 50 20"
    or "I want to add a new product called Wheat for 45 rupees with 30 pieces"
    or "Add product Sugar at ₹40 with 20 units"
    """
    text = text.lower()
    
    # Pattern for "add product [name] at ₹[price] with [stock] units"
    pattern0 = r"add\s+(?:new\s+)?product\s+([\w\s]+?)\s+at\s+(?:₹|rs\.?|rupees)\s*(\d+)\s+with\s+(\d+)\s+units"
    match = re.search(pattern0, text, re.IGNORECASE)
    
    if match:
        name = match.group(1).strip()
        price = int(match.group(2))
        stock = int(match.group(3))
        return {"name": name, "price": price, "stock": stock}
    
    # Pattern for "add new product [name] [price]rs [stock]qty"
    pattern1 = r"add\s+(?:new\s+)?product\s+([\w\s]+?)\s+(\d+)(?:rs|rupees|₹)?\s+(\d+)(?:qty|units|pcs)?"
    match = re.search(pattern1, text, re.IGNORECASE)
    
    if match:
        name = match.group(1).strip()
        price = int(match.group(2))
        stock = int(match.group(3))
        return {"name": name, "price": price, "stock": stock}
    
    # Pattern for "add product [name] [price] [stock]"
    pattern2 = r"add\s+(?:new\s+)?product\s+([\w]+)\s+(\d+)\s+(\d+)"
    match = re.search(pattern2, text, re.IGNORECASE)
    
    if match:
        name = match.group(1).strip()
        price = int(match.group(2))
        stock = int(match.group(3))
        return {"name": name, "price": price, "stock": stock}
    
    # Pattern for "add a new product called [name] for [price] rupees with [stock] pieces"
    pattern3 = r"add\s+(?:a\s+)?(?:new\s+)?product\s+called\s+([\w]+)\s+for\s+(\d+)\s+rupees\s+with\s+(\d+)\s+pieces"
    match = re.search(pattern3, text, re.IGNORECASE)
    
    if match:
        name = match.group(1).strip()
        price = int(match.group(2))
        stock = int(match.group(3))
        return {"name": name, "price": price, "stock": stock}
    
    # Pattern for "I want to add a new product called [name] for [price] rupees with [stock] pieces"
    pattern4 = r"i\s+want\s+to\s+add\s+(?:a\s+)?(?:new\s+)?product\s+called\s+([\w]+)\s+for\s+(\d+)\s+rupees\s+with\s+(\d+)\s+pieces"
    match = re.search(pattern4, text, re.IGNORECASE)
    
    if match:
        name = match.group(1).strip()
        price = int(match.group(2))
        stock = int(match.group(3))
        return {"name": name, "price": price, "stock": stock}
    
    # Extract from any text containing product name and two numbers
    words = text.split()
    product_name = ""
    numbers = []
    
    # Look for "called" keyword which often precedes product name
    called_idx = -1
    for i, word in enumerate(words):
        if word == "called":
            called_idx = i
            break
    
    if called_idx >= 0 and called_idx + 1 < len(words):
        product_name = words[called_idx + 1]
    else:
        # Skip the command words
        start_idx = 0
        for i, word in enumerate(words):
            if word in ["add", "new", "product", "create", "register"]:
                start_idx = i + 1
        
        # Extract numbers and potential product name
        for i, word in enumerate(words[start_idx:], start_idx):
            if word.isdigit():
                numbers.append(int(word))
            elif not (word in ["rs", "rupees", "₹", "qty", "units", "pcs", "for", "with"]):
                if i == start_idx:  # First word after command is likely the product name
                    product_name = word
    
    # Extract all numbers from text
    if not numbers:
        for word in words:
            if word.isdigit():
                numbers.append(int(word))
    
    if product_name and len(numbers) >= 2:
        return {
            "name": product_name.strip(),
            "price": numbers[0],
            "stock": numbers[1]
        }
    
    # If no match, try to at least extract the name
    if called_idx >= 0 and called_idx + 1 < len(words):
        return {"name": words[called_idx + 1], "price": None, "stock": None}
    
    return {}

def extract_edit_stock_details(text: str) -> Dict[str, Any]:
    """
    Extract product name and new stock value from text like:
    "Edit stock of Rice to 100" or "Update Rice stock to 50"
    """
    text = text.lower()
    
    # Pattern for "update|change stock of [product] to [number]"
    pattern = r"(?:update|change)\s+stock\s+of\s+(\w+)\s+to\s+(-?\d+)"
    match = re.search(pattern, text, re.IGNORECASE)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Pattern for "update [product] stock to [number]"
    pattern2 = r"(?:edit|update)\s+([\w]+)\s+stock\s+(?:to\s+)?(-?\d+)"
    match = re.search(pattern2, text, re.IGNORECASE)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Pattern for "[product] stock [number]"
    pattern3 = r"([\w]+)\s+stock\s+(-?\d+)"
    match = re.search(pattern3, text, re.IGNORECASE)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Extract from any text containing a product name and a number
    words = text.split()
    product_name = ""
    stock_value = None
    
    # Skip the command words
    start_idx = 0
    for i, word in enumerate(words):
        if word in ["edit", "update", "change", "set", "make"]:
            start_idx = i + 1
            break
    
    # Find the first word that's not a command word or "stock", "to", etc.
    for i, word in enumerate(words[start_idx:], start_idx):
        if word not in ["stock", "to", "of", "the", "inventory"]:
            product_name = word
            break
    
    # Find the first number (including negative numbers)
    for word in words:
        # Check for negative numbers or positive numbers
        if word.startswith('-') and word[1:].isdigit():
            stock_value = int(word)
            break
        elif word.isdigit():
            stock_value = int(word)
            break
    
    if product_name and stock_value is not None:
        return {"name": product_name, "stock": stock_value}
    
    return {}

def extract_get_low_stock_details(command: str, lang: str) -> dict:
    """
    Extract stock threshold or default to 5 if not mentioned
    
    Args:
        command: The command text
        lang: Language code ('en' or 'hi')
        
    Returns:
        Dictionary with threshold value
    """
    # Default threshold
    threshold = 5
    
    # Check for English threshold patterns
    if lang == 'en':
        # Look for patterns like "below 10", "less than 15", "under 20"
        below_pattern = r"(?:below|less\s+than|under|<=|<)\s*(\d+)"
        match = re.search(below_pattern, command, re.IGNORECASE)
        if match:
            threshold = int(match.group(1))
    
    # Check for Hindi threshold patterns
    elif lang == 'hi':
        # Look for patterns like "5 से कम", "10 से नीचे"
        hindi_pattern = r"(\d+)\s+से\s+(?:कम|नीचे)"
        match = re.search(hindi_pattern, command)
        if match:
            threshold = int(match.group(1))
    
    return {"threshold": threshold}

def extract_search_product_details(text: str) -> Dict[str, str]:
    """
    Extract product name from search queries like:
    "Do you have sugar in stock?" or "Search for rice"
    
    Returns:
        Dictionary with product name
    """
    product_name = ""
    
    # Pattern for "search for X"
    pattern1 = r"(?:search|look)\s+for\s+(.+?)(?:\s+|$)"
    match = re.search(pattern1, text, re.IGNORECASE)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # Pattern for "do you have X in stock"
    pattern2 = r"do\s+(?:you|we|I)\s+have\s+(.+?)(?:\s+in\s+stock|\s+available|$)"
    match = re.search(pattern2, text, re.IGNORECASE)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # Pattern for "is X in stock"
    pattern3 = r"is\s+(.+?)(?:\s+in\s+stock|\s+available|$)"
    match = re.search(pattern3, text, re.IGNORECASE)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # Pattern for "check if X is in stock"
    pattern4 = r"check\s+(?:if|whether)\s+(.+?)\s+(?:is|are)\s+(?:in\s+stock|available)"
    match = re.search(pattern4, text, re.IGNORECASE)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # Pattern for "find X"
    pattern5 = r"(?:find|locate)\s+(.+?)(?:\s+|$)"
    match = re.search(pattern5, text, re.IGNORECASE)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # If no specific pattern matched, try to extract product name from the text
    # by removing common words and keeping the most likely product name
    words = text.split()
    filtered_words = []
    for word in words:
        if word.lower() not in ["search", "for", "do", "you", "have", "in", "stock", "available", "is", "check", "if", "whether", "are", "find", "locate"]:
            filtered_words.append(word)
    
    if filtered_words:
        product_name = " ".join(filtered_words).strip()
    
    return {"name": product_name}

import datetime

def extract_custom_date_range(text: str) -> Dict[str, str]:
    """
    Extract custom date range from text like:
    "Show report from 1 June to 20 June" or "Get report between 1st Jan and 31st Jan"
    
    Returns:
        Dictionary with start_date and end_date in YYYY-MM-DD format
    """
    # Print for debugging
    print(f"Extracting custom date range from: '{text}'")
    
    # Pattern for "report from [date] to [date]"
    pattern1 = r"(?:report|reports?)\s+from\s+(\d+\s*(?:st|nd|rd|th)?\s+[a-zA-Z]+|\d+[/\-]\d+(?:[/\-]\d+)?)\s+to\s+(\d+\s*(?:st|nd|rd|th)?\s+[a-zA-Z]+|\d+[/\-]\d+(?:[/\-]\d+)?)(?:\s+|$)"
    match = re.search(pattern1, text.lower(), re.IGNORECASE)
    
    if not match:
        # Pattern for "from [date] to [date]"
        pattern2 = r"from\s+(\d+\s*(?:st|nd|rd|th)?\s+[a-zA-Z]+|\d+[/\-]\d+(?:[/\-]\d+)?)\s+to\s+(\d+\s*(?:st|nd|rd|th)?\s+[a-zA-Z]+|\d+[/\-]\d+(?:[/\-]\d+)?)(?:\s+|$)"
        match = re.search(pattern2, text.lower(), re.IGNORECASE)
    
    if not match:
        # Pattern for "report between [date] and [date]"
        pattern3 = r"(?:report|reports?)\s+between\s+(\d+\s*(?:st|nd|rd|th)?\s+[a-zA-Z]+|\d+[/\-]\d+(?:[/\-]\d+)?)\s+and\s+(\d+\s*(?:st|nd|rd|th)?\s+[a-zA-Z]+|\d+[/\-]\d+(?:[/\-]\d+)?)(?:\s+|$)"
        match = re.search(pattern3, text.lower(), re.IGNORECASE)
    
    if not match:
        # Pattern for "between [date] and [date]"
        pattern4 = r"between\s+(\d+\s*(?:st|nd|rd|th)?\s+[a-zA-Z]+|\d+[/\-]\d+(?:[/\-]\d+)?)\s+and\s+(\d+\s*(?:st|nd|rd|th)?\s+[a-zA-Z]+|\d+[/\-]\d+(?:[/\-]\d+)?)(?:\s+|$)"
        match = re.search(pattern4, text.lower(), re.IGNORECASE)
    
    if match:
        start_date_str = match.group(1).strip()
        end_date_str = match.group(2).strip()
        
        print(f"Matched date range: '{start_date_str}' to '{end_date_str}'")
        
        # Try to parse dates
        try:
            # Parse start date
            start_date = parse_date(start_date_str)
            
            # Parse end date
            end_date = parse_date(end_date_str)
            
            if start_date and end_date:
                result = {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
                print(f"Parsed date range: {result}")
                return result
            else:
                print(f"Failed to parse dates: start_date={start_date}, end_date={end_date}")
        except Exception as e:
            print(f"Error parsing dates: {e}")
    else:
        print("No date range pattern matched")
    
    return {}

def parse_date(date_str: str) -> datetime.datetime:
    """
    Parse a date string in various formats
    
    Args:
        date_str: Date string like "1 June", "1st Jan", etc.
        
    Returns:
        datetime object or None if parsing fails
    """
    # Try different date formats
    formats = [
        "%d %B",           # 1 June
        "%d %b",           # 1 Jun
        "%dst %B",         # 1st June
        "%dnd %B",         # 2nd June
        "%drd %B",         # 3rd June
        "%dth %B",         # 4th June
        "%dst %b",         # 1st Jun
        "%dnd %b",         # 2nd Jun
        "%drd %b",         # 3rd Jun
        "%dth %b",         # 4th Jun
        "%B %d",           # June 1
        "%b %d",           # Jun 1
        "%d/%m",           # 01/06
        "%d-%m",           # 01-06
        "%d/%m/%Y",        # 01/06/2023
        "%d-%m-%Y"         # 01-06-2023
    ]
    
    # Clean up the date string
    date_str = date_str.strip()
    
    # Try each format
    for fmt in formats:
        try:
            # If year is not in the format, use current year
            parsed_date = datetime.datetime.strptime(date_str, fmt)
            if "%Y" not in fmt:
                current_year = datetime.datetime.now().year
                parsed_date = parsed_date.replace(year=current_year)
            return parsed_date
        except ValueError:
            continue
    
    # If all formats fail, return None
    return None

def extract_report_range(text: str) -> Dict[str, str]:
    """
    Extract report time range from text like:
    "Send today's report" or "Get this month's report"
    """
    # Print for debugging
    print(f"Extracting report range from: '{text}'")
    
    # First check for custom date range
    custom_range = extract_custom_date_range(text)
    if custom_range:
        print(f"Found custom date range: {custom_range}")
        return custom_range
    
    # Then check for predefined ranges
    if re.search(r"yesterday(?:'s|s)?", text, re.IGNORECASE):
        print("Found predefined range: yesterday")
        return {"range": "yesterday"}
    elif re.search(r"today(?:'s|s)?", text, re.IGNORECASE):
        print("Found predefined range: today")
        return {"range": "today"}
    elif re.search(r"this\s+week(?:'s|s)?", text, re.IGNORECASE):
        print("Found predefined range: week")
        return {"range": "week"}
    elif re.search(r"this\s*-?\s*week(?:'s|s)?", text, re.IGNORECASE):
        print("Found predefined range: week")
        return {"range": "week"}
    elif re.search(r"this\s+month(?:'s|s)?", text, re.IGNORECASE):
        print("Found predefined range: this-month")
        return {"range": "this-month"}
    
    # Check if the text contains 'report' but no specific range
    if "report" in text.lower() and not any(pattern in text.lower() for pattern in ["yesterday", "today", "week", "month"]):
        print("Report mentioned but no range specified, returning empty dict")
        return {}
    
    # Default to today if not specified
    print("No range found, defaulting to today")
    return {"range": "today"}

def extract_order_range_details(text: str) -> Dict[str, str]:
    """
    Extract order time range from text like:
    "Show today's orders" or "Get yesterday's orders"
    
    Returns:
        Dictionary with time range
    """
    if re.search(r"yesterday(?:'s|s)?", text, re.IGNORECASE):
        return {"range": "yesterday"}
    elif re.search(r"today(?:'s|s)?", text, re.IGNORECASE):
        return {"range": "today"}
    elif re.search(r"this\s+week(?:'s|s)?", text, re.IGNORECASE):
        return {"range": "week"}
    elif re.search(r"this\s+month(?:'s|s)?", text, re.IGNORECASE):
        return {"range": "this-month"}
    elif re.search(r"recent", text, re.IGNORECASE):
        return {"range": "recent"}
    elif re.search(r"new", text, re.IGNORECASE):
        return {"range": "recent"}
    else:
        return {"range": "all"}  # Default to all orders

def extract_top_products_details(text: str) -> Dict[str, Any]:
    """
    Extract top products details from text like:
    "Show top 5 products" or "Best selling products this week"
    
    Returns:
        Dictionary with time range and limit
    """
    # Extract limit if specified
    limit_match = re.search(r'top\s+(\d+)', text)
    limit = int(limit_match.group(1)) if limit_match else 5  # Default to top 5 if not specified
    
    # Check for predefined time ranges
    if re.search(r'today', text):
        return {"range": "today", "limit": limit}
    elif re.search(r'yesterday', text):
        return {"range": "yesterday", "limit": limit}
    elif re.search(r'this\s+week', text):
        return {"range": "week", "limit": limit}
    elif re.search(r'this\s+month', text):
        return {"range": "this-month", "limit": limit}
    elif re.search(r'all\s+time', text):
        return {"range": "all", "limit": limit}
    
    # Extract custom date range if present
    custom_range = extract_custom_date_range(text)
    if custom_range:
        custom_range["limit"] = limit
        return custom_range
    
    # Default to week if no range specified
    return {"range": "week", "limit": limit}

def extract_customer_data_details(text: str) -> Dict[str, Any]:
    """
    Extract time range for customer data from text like:
    "Show customer data for this month" or "Get customer details for yesterday"
    
    Returns:
        Dictionary with time range
    """
    entities = {}
    
    # Extract limit if specified (e.g., "top 3 customers")
    limit_match = re.search(r"top\s+(\d+)\s+customers", text, re.IGNORECASE)
    if limit_match:
        entities["limit"] = int(limit_match.group(1))
    
    # Check for predefined time ranges
    if re.search(r"yesterday(?:'s|s)?", text, re.IGNORECASE):
        entities["range"] = "yesterday"
    elif re.search(r"today(?:'s|s)?", text, re.IGNORECASE):
        entities["range"] = "today"
    elif re.search(r"this\s+week(?:'s|s)?|last\s+week(?:'s|s)?", text, re.IGNORECASE):
        entities["range"] = "week"
    elif re.search(r"this\s+month(?:'s|s)?", text, re.IGNORECASE):
        entities["range"] = "this-month"
    elif re.search(r"all\s+time", text, re.IGNORECASE):
        entities["range"] = "all"
    
    # Check for custom date range
    custom_date_entities = extract_custom_date_range(text)
    if custom_date_entities:
        entities.update(custom_date_entities)
    elif "range" not in entities:
        # Default to this month if no range specified
        entities["range"] = "this-month"
    
    return entities

def parse_command(message: str) -> Dict[str, Any]:
    """
    Parse a command message and return the recognized intent and extracted entities.
    
    Args:
        message: The command message from the user
        
    Returns:
        A dictionary with 'intent', 'entities', 'language', 'raw_text', and 'normalized_text' keys
    """
    # Store original text
    original_text = message
    
    # Basic normalization (lowercase and strip)
    basic_normalized_message = message.lower().strip()
    
    # Apply language-aware token normalization
    try:
        from nlp.mixed_entity_extraction import normalize_mixed_command
        normalized_message = normalize_mixed_command(basic_normalized_message)
        
        # Log raw vs normalized command
        logger.info(f"Raw command: {message}")
        logger.info(f"Normalized command: {normalized_message}")
    except Exception as e:
        logger.warning(f"Error normalizing command: {e}")
        normalized_message = basic_normalized_message
    
    # Detect language
    lang = detect_language(normalized_message)
    logger.info(f"Language detection: {lang}")
    
    # Try to match intents
    for intent, patterns in INTENT_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, normalized_message, re.IGNORECASE):
                # Extract entities based on intent
                entities = {}
                
                if intent == "add_product":
                    entities = extract_product_details(normalized_message)
                elif intent == "edit_stock":
                    entities = extract_edit_stock_details(normalized_message)
                elif intent == "get_report":
                    entities = extract_report_range(normalized_message)
                elif intent == "get_low_stock":
                    entities = extract_get_low_stock_details(normalized_message, lang)
                elif intent == "search_product":
                    entities = extract_search_product_details(normalized_message)
                elif intent == "get_orders":
                    entities = extract_order_range_details(normalized_message)
                elif intent == "get_top_products":
                    entities = extract_top_products_details(normalized_message)
                elif intent == "get_customer_data":
                    entities = extract_customer_data_details(normalized_message)
                
                # Log the recognized intent and entities
                logger.info(f"Recognized intent: {intent}, entities: {entities}")
                
                return {
                    "intent": intent,
                    "entities": entities,
                    "language": lang,
                    "raw_text": original_text,
                    "normalized_text": normalized_message
                }
    
    # If no intent matched
    logger.warning(f"No intent matched for message: {message}")
    return {
        "intent": "unknown",
        "entities": {},
        "raw_text": original_text,
        "normalized_text": normalized_message
    }

# Language detection function (placeholder for future implementation)
def detect_language(text: str) -> str:
    """
    Detect the language of the input text.
    Currently supports basic detection for English and Hindi.
    
    Args:
        text: Input text
        
    Returns:
        Language code ('en' for English, 'hi' for Hindi)
    """
    # This is a very basic implementation
    # In a real system, use a proper language detection library like langdetect
    
    # Common Hindi words/characters check
    hindi_chars = set('अआइईउऊएऐओऔकखगघचछजझटठडढणतथदधनपफबभमयरलवशषसह')
    text_chars = set(text)
    
    if any(char in hindi_chars for char in text_chars):
        return 'hi'
    
    # Default to English
    return 'en'

# Function to provide guidance on expanding the system
def get_expansion_guidance() -> str:
    """
    Returns guidance on how to expand the NLP system with ML/NLU.
    """
    guidance = """
    Expansion Guide for ML/NLU Integration:
    
    1. spaCy Integration:
       - Install spaCy: pip install spacy
       - Download language models: python -m spacy download en_core_web_md
       - Use spaCy's entity recognition and custom entity rulers
       - Example: 
         ```python
         import spacy
         nlp = spacy.load("en_core_web_md")
         doc = nlp("Add new product Rice 50rs 20qty")
         # Extract entities using doc.ents
         ```
    
    2. Intent Classification with Transformers:
       - Install transformers: pip install transformers
       - Fine-tune a pre-trained model on your intent dataset
       - Example:
         ```python
         from transformers import pipeline
         classifier = pipeline("text-classification", model="distilbert-base-uncased-finetuned-sst-2-english")
         result = classifier("Show my low stock items")
         ```
    
    3. Multi-language Support:
       - Use language detection libraries: pip install langdetect
       - Load appropriate language models for detected language
       - Example:
         ```python
         from langdetect import detect
         lang = detect("मेरे प्रोडक्ट दिखाओ")  # Detect Hindi
         # Use Hindi NLP model if available
         ```
    
    4. Training Data Collection:
       - Log user inputs and manual classifications
       - Create a dataset of commands and their intents/entities
       - Use this data to train custom models
    
    5. Hybrid Approach:
       - Combine rule-based patterns with ML for better accuracy
       - Use confidence scores to fall back to rules when ML is uncertain
    """
    return guidance

# Example usage
if __name__ == "__main__":
    # Test cases
    test_commands = [
        "Show my products",
        "Send today's report",
        "Show low stock items",
        "Add new product Rice 50rs 20qty",
        "Edit stock of Rice to 100",
        "Update Wheat stock to 75",
        "Get this month's report",
        "List my orders",
        "Show today's orders",
        "Get yesterday's orders",
        "View this week's orders",
        "Show this month's orders",
        "Show recent orders",
        "Show all orders"
    ]
    
    print("\nTesting intent recognition:\n")
    for cmd in test_commands:
        result = parse_command(cmd)
        print(f"Command: '{cmd}'")
        print(f"Result: {result}\n")
    
    print("\nExpansion guidance for ML/NLU integration:")
    print(get_expansion_guidance())