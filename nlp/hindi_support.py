# Hindi language support for the WhatsApp Command Intent Handler
# This is a basic implementation to demonstrate multilingual capabilities

import re
from typing import Dict, Any

# Hindi intent patterns with example phrases
HINDI_INTENT_PATTERNS = {
    "get_inventory": [
        r"मेरे\s+(?:प्रोडक्ट|आइटम|सामान|इन्वेंटरी)\s+(?:दिखाओ|दिखाएं|देखना\s+है)",
        r"(?:प्रोडक्ट|आइटम|सामान|इन्वेंटरी)\s+(?:दिखाओ|दिखाएं|देखना\s+है)",
        r"(?:कौन|क्या)\s+(?:प्रोडक्ट|आइटम|सामान)\s+(?:हैं|है|उपलब्ध\s+हैं)",
        r"मेरे\s+प्रोडक्ट\s+दिखाओ",
        r"सभी\s+प्रोडक्ट\s+दिखाओ",
        r"इन्वेंटरी\s+दिखाओ",
        r"प्रोडक्ट\s+लिस्ट",
        r"मेरा\s+स्टॉक\s+दिखाओ",
        r"सारे\s+प्रोडक्ट\s+दिखाओ"
    ],
    "get_customer_data": [
        r"कस्टमर\s+का\s+डाटा\s+दिखाओ",
        r"ग्राहकों\s+की\s+जानकारी\s+दो",
        r"(?:टॉप|बेस्ट)\s+(?:\d+\s+)?कस्टमर\s+दिखाओ",
        r"कौन\s+से\s+(?:कस्टमर|ग्राहक)\s+(?:टॉप|बेस्ट)\s+हैं"
    ],
    "get_low_stock": [
        r"(?:कम|सीमित)\s+(?:स्टॉक|इन्वेंटरी)\s+(?:दिखाओ|दिखाएं|देखना\s+है)?",
        r"कम\s+स्टॉक\s+वाले\s+(?:आइटम|प्रोडक्ट)\s*(?:दिखाओ|दिखाएं|देखना\s+है)?",
        r"(?:कौन|क्या)\s+(?:प्रोडक्ट|आइटम)\s+(?:कम|सीमित)\s+(?:स्टॉक|मात्रा)\s+में\s+(?:हैं|है)",
        r"(?:कौन|क्या)\s+(?:प्रोडक्ट|आइटम)\s+(?:रीस्टॉक|रीऑर्डर)\s+करने\s+(?:हैं|है|की\s+जरूरत\s+है)",
        r"(\d+)\s+से\s+(?:कम|नीचे)\s+स्टॉक\s+वाले\s+(?:आइटम|प्रोडक्ट)\s+(?:दिखाओ|दिखाएं|देखना\s+है)",
        r"कम\s+स्टॉक\s+वाले\s+आइटम\s+दिखाओ",
        r"कम\s+स्टॉक\s+वाले\s+प्रोडक्ट(?:\s+दिखाओ)?",
        r"स्टॉक\s+कम\s+है",
        r"कम\s+स्टॉक\s+दिखाओ",
        r"कम\s+इन्वेंटरी",
        r"कम\s+मात्रा\s+वाले\s+प्रोडक्ट",
        r"3\s+से\s+कम\s+स्टॉक"
    ],
    "get_report": [
        r"(?:बिक्री|सेल्स)\s+(?:रिपोर्ट|रिपोर्ट)\s+(?:दिखाओ|दिखाएं|देखना\s+है|भेजो|भेजें)",
        r"(?:आज|कल|इस\s+हफ्ते|इस\s+महीने)\s+की\s+(?:बिक्री|सेल्स)\s+(?:रिपोर्ट|रिपोर्ट)\s+(?:दिखाओ|दिखाएं|देखना\s+है|भेजो|भेजें)",
        r"(?:आज|कल|इस\s+हफ्ते|इस\s+महीने)\s+(?:कितना|कितनी)\s+(?:बिक्री|सेल्स)\s+(?:हुई|हुआ)",
        r"आज\s+की\s+रिपोर्ट\s+भेजो",
        r"इस\s+हफ्ते\s+की\s+रिपोर्ट",
        r"इस\s+महीने\s+की\s+रिपोर्ट",
        r"रिपोर्ट\s+दिखाओ",
        r"(.+?)\s+से\s+(.+?)\s+तक\s+की\s+(?:बिक्री\s+|सेल्स\s+)?रिपोर्ट\s+(?:दिखाओ|भेजो|दो)",
        r"रिपोर्ट\s+(?:दिखाओ|भेजो|दो)\s+(.+?)\s+से\s+(.+?)\s+तक"
    ],
    "get_top_products": [
        r"(?:टॉप|बेस्ट)\s+(?:प्रोडक्ट|प्रोडक्ट्स|आइटम|सामान)\s+(?:दिखाओ|दिखाएं|देखना\s+है|बताओ)",
        r"(?:टॉप|बेस्ट)\s+(\d+)\s+(?:प्रोडक्ट|प्रोडक्ट्स|आइटम|सामान)\s+(?:दिखाओ|दिखाएं|देखना\s+है|बताओ)",
        r"(?:आज|कल|इस\s+हफ्ते|इस\s+महीने|सभी\s+समय)\s+के\s+(?:टॉप|बेस्ट)\s+(?:प्रोडक्ट|प्रोडक्ट्स|आइटम|सामान)",
        r"(?:आज|कल|इस\s+हफ्ते|इस\s+महीने|सभी\s+समय)\s+के\s+(?:टॉप|बेस्ट)\s+(\d+)\s+(?:प्रोडक्ट|प्रोडक्ट्स|आइटम|सामान)",
        r"सबसे\s+ज्यादा\s+बिकने\s+वाले\s+(?:प्रोडक्ट|प्रोडक्ट्स|आइटम|सामान)",
        r"सबसे\s+लोकप्रिय\s+(?:प्रोडक्ट|प्रोडक्ट्स|आइटम|सामान)",
        r"सभी\s+समय\s+के\s+(?:टॉप|बेस्ट)\s+(?:प्रोडक्ट|प्रोडक्ट्स|आइटम|सामान)",
        r"सभी\s+समय\s+के\s+(?:टॉप|बेस्ट)\s+(\d+)\s+(?:प्रोडक्ट|प्रोडक्ट्स|आइटम|सामान)"
    ],
    "add_product": [
        r"(?:नया|एक)\s+(?:प्रोडक्ट|आइटम|सामान)\s+(?:जोड़ो|जोड़ें|जोड़ना\s+है)",
        r"(?:इन्वेंटरी|स्टॉक)\s+में\s+(?:नया|एक)\s+(?:प्रोडक्ट|आइटम|सामान)\s+(?:जोड़ो|जोड़ें|जोड़ना\s+है)",
        r"नया\s+प्रोडक्ट\s+(.+?)\s+जोड़ो",
        r"प्रोडक्ट\s+(.+?)\s+जोड़ो",
        r"नया\s+प्रोडक्ट\s+(.+)",
        r"प्रोडक्ट\s+जोड़ो\s+(.+)",
        r"(\d+)\s+(\S+)\s+जोड़ो\s+₹(\d+)\s+में"
    ],
    "edit_stock": [
        r"(?:स्टॉक|इन्वेंटरी)\s+(?:अपडेट|बदलो|बदलें|अपडेट\s+करो|अपडेट\s+करें)",
        r"(.+?)\s+का\s+(?:स्टॉक|इन्वेंटरी)\s+(\d+)\s+(?:करो|करें|कर\s+दो|कर\s+दें)",
        r"(.+?)\s+(?:स्टॉक|इन्वेंटरी)\s+(?:अपडेट|बदलो|बदलें|अपडेट\s+करो|अपडेट\s+करें)\s+(\d+)",
        r"(\S+)\s+का\s+स्टॉक\s+(\d+)\s+करो",
        r"(\S+)\s+का\s+स्टॉक\s+(\d+)\s+कर\s+दो",
        r"(\S+)\s+स्टॉक\s+अपडेट\s+करो\s+(\d+)",
        r"स्टॉक\s+अपडेट\s+(\S+)\s+(\d+)",
        r"मुझे\s+(\S+)\s+का\s+स्टॉक\s+(\d+)\s+करना\s+है"
    ],
    "get_orders": [
        r"(?:ऑर्डर|आर्डर)\s+(?:दिखाओ|दिखाएं|देखना\s+है)",
        r"(?:हाल|रीसेंट)\s+(?:के|ही)\s+(?:ऑर्डर|आर्डर)\s+(?:दिखाओ|दिखाएं|देखना\s+है)",
        r"(?:कौन|क्या)\s+(?:ऑर्डर|आर्डर)\s+(?:हैं|है|आए\s+हैं)",
        r"मेरे\s+ऑर्डर\s+दिखाओ",
        r"ऑर्डर\s+लिस्ट\s+दिखाओ",
        r"नए\s+ऑर्डर\s+दिखाओ",
        r"आज\s+के\s+(?:ऑर्डर|आर्डर)\s+(?:दिखाओ|दिखाएं|देखना\s+है)"
    ],
    "search_product": [
        r"(.+?)\s+(?:सर्च|खोज|ढूंढ)\s+(?:करो|करें)",
        r"(.+?)\s+(?:उपलब्ध|स्टॉक\s+में)\s+(?:है|हैं)\s+(?:क्या)",
        r"क्या\s+(.+?)\s+(?:उपलब्ध|स्टॉक\s+में)\s+(?:है|हैं)",
        r"क्या\s+(?:आपके|हमारे|मेरे)\s+पास\s+(.+?)\s+(?:है|हैं)",
        r"(.+?)\s+(?:है|हैं)\s+(?:क्या)\s+(?:स्टॉक\s+में)"
    ]
}

# Entity extraction for Hindi commands
def extract_hindi_product_details(text: str) -> Dict[str, Any]:
    """
    Extract product name, price, and stock from Hindi text like:
    "नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो" or
    "मुझे एक नया प्रोडक्ट गेहूं 45 रुपये के साथ 30 पीस जोड़ना है"
    """
    # Check for the specific pattern "20 नमक जोड़ो ₹30 में"
    specific_pattern = r"(\d+)\s+(\S+)\s+जोड़ो\s+₹(\d+)\s+में"
    match = re.search(specific_pattern, text)
    if match:
        stock = int(match.group(1))
        name = match.group(2).strip()
        price = int(match.group(3))
        return {"name": name, "price": price, "stock": stock}
    
    # Try to match pattern with currency and quantity indicators
    pattern1 = r"नया\s+प्रोडक्ट\s+([\u0900-\u097F\s]+?)\s+(\d+)\s+(?:रुपये|₹)?\s+(\d+)\s+(?:पीस|इकाई)?\s+जोड़ो"
    match = re.search(pattern1, text)
    
    if match:
        name = match.group(1).strip()
        price = int(match.group(2))
        stock = int(match.group(3))
        return {"name": name, "price": price, "stock": stock}
    
    # Try simpler pattern with just numbers
    pattern2 = r"नया\s+प्रोडक्ट\s+([\u0900-\u097F\s]+?)\s+(\d+)\s+(\d+)"
    match = re.search(pattern2, text)
    
    if match:
        name = match.group(1).strip()
        price = int(match.group(2))
        stock = int(match.group(3))
        return {"name": name, "price": price, "stock": stock}
    
    # Pattern for "मुझे एक नया प्रोडक्ट [name] [price] रुपये के साथ [stock] पीस जोड़ना है"
    pattern3 = r"नया\s+प्रोडक्ट\s+([\u0900-\u097F]+)\s+(\d+)\s+रुपये\s+के\s+साथ\s+(\d+)\s+पीस"
    match = re.search(pattern3, text)
    
    if match:
        name = match.group(1).strip()
        price = int(match.group(2))
        stock = int(match.group(3))
        return {"name": name, "price": price, "stock": stock}
    
    # Extract from any text containing product name and two numbers
    words = text.split()
    product_name = ""
    numbers = []
    
    for word in words:
        if word.isdigit():
            numbers.append(int(word))
        elif not (word in ["नया", "प्रोडक्ट", "जोड़ो", "जोड़ना", "है", "रुपये", "पीस", "इकाई", "के", "साथ", "मुझे", "एक"]):
            product_name += word + " "
    
    if product_name and len(numbers) >= 2:
        return {
            "name": product_name.strip(),
            "price": numbers[0],
            "stock": numbers[1]
        }
    
    return {}

def extract_hindi_edit_stock_details(text: str) -> Dict[str, Any]:
    """
    Extract product name and new stock value from Hindi text like:
    "चावल का स्टॉक 100 करो" or
    "चीनी का स्टॉक 15 कर दो" or
    "मुझे चीनी का स्टॉक 75 करना है"
    """
    # Pattern for "[product] का स्टॉक [number] करो"
    pattern1 = r"(\S+)\s+का\s+स्टॉक\s+(-?\d+)\s+करो"
    match = re.search(pattern1, text)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Pattern for "[product] का स्टॉक [number] कर दो"
    pattern2 = r"(\S+)\s+का\s+स्टॉक\s+(-?\d+)\s+कर\s+दो"
    match = re.search(pattern2, text)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Pattern for "[product] का स्टॉक [number] कर दो"
    pattern1a = r"(\S+)\s+का\s+स्टॉक\s+(-?\d+)\s+कर\s+दो"
    match = re.search(pattern1a, text)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Pattern for "मुझे [product] का स्टॉक [number] करना है"
    pattern2a = r"मुझे\s+(\S+)\s+का\s+स्टॉक\s+(-?\d+)\s+करना\s+है"
    match = re.search(pattern2a, text)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Pattern for "[product] स्टॉक अपडेट करो [number]"
    pattern2 = r"(\S+)\s+स्टॉक\s+अपडेट\s+करो\s+(-?\d+)"
    match = re.search(pattern2, text)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Pattern for "स्टॉक अपडेट [product] [number]"
    pattern3 = r"स्टॉक\s+अपडेट\s+(\S+)\s+(-?\d+)"
    match = re.search(pattern3, text)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Pattern for "[product] स्टॉक [number]"
    pattern4 = r"(\S+)\s+स्टॉक\s+(-?\d+)"
    match = re.search(pattern4, text)
    
    if match:
        name = match.group(1).strip()
        stock = int(match.group(2))
        return {"name": name, "stock": stock}
    
    # Extract product name and number from any text
    words = text.split()
    product_name = ""
    stock_value = None
    
    # Find the stock value (usually the last number in the text)
    for word in words:
        # Check for negative numbers as well
        if word.startswith('-') and word[1:].isdigit():
            stock_value = int(word)
        elif word.isdigit():
            stock_value = int(word)
    
    # Extract product name (words before "स्टॉक" or "का")
    for word in words:
        if word in ["स्टॉक", "का", "अपडेट", "करो", "को", "मुझे", "करना", "है"]:
            break
        product_name += word + " "
    
    if product_name and stock_value:
        return {"name": product_name.strip(), "stock": stock_value}
    
    return {}

def extract_hindi_get_low_stock_details(text: str) -> Dict[str, int]:
    """
    Extract stock threshold from Hindi text like:
    "3 से कम स्टॉक" or "5 से नीचे स्टॉक वाले प्रोडक्ट"
    
    Returns:
        Dictionary with threshold value
    """
    # Default threshold
    threshold = 5
    
    # Look for patterns like "3 से कम", "5 से नीचे"
    pattern = r"(\d+)\s+से\s+(?:कम|नीचे)"
    match = re.search(pattern, text)
    
    if match:
        threshold = int(match.group(1))
    
    return {"threshold": threshold}

def extract_hindi_search_product_details(text: str) -> Dict[str, str]:
    """
    Extract product name from Hindi search queries like:
    "चाय उपलब्ध है क्या?" or "चावल सर्च करो"
    
    Returns:
        Dictionary with product name
    """
    product_name = ""
    
    # Pattern for "X सर्च करो"
    pattern1 = r"(.+?)\s+(?:सर्च|खोज|ढूंढ)\s+(?:करो|करें)"
    match = re.search(pattern1, text)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # Pattern for "X उपलब्ध है क्या"
    pattern2 = r"(.+?)\s+(?:उपलब्ध|स्टॉक\s+में)\s+(?:है|हैं)\s+(?:क्या)"
    match = re.search(pattern2, text)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # Pattern for "क्या X उपलब्ध है"
    pattern3 = r"क्या\s+(.+?)\s+(?:उपलब्ध|स्टॉक\s+में)\s+(?:है|हैं)"
    match = re.search(pattern3, text)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # Pattern for "क्या आपके पास X है"
    pattern4 = r"क्या\s+(?:आपके|हमारे|मेरे)\s+पास\s+(.+?)\s+(?:है|हैं)"
    match = re.search(pattern4, text)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # Pattern for "X है क्या स्टॉक में"
    pattern5 = r"(.+?)\s+(?:है|हैं)\s+(?:क्या)\s+(?:स्टॉक\s+में)"
    match = re.search(pattern5, text)
    if match:
        product_name = match.group(1).strip()
        return {"name": product_name}
    
    # If no specific pattern matched, try to extract product name from the text
    # by removing common Hindi words and keeping the most likely product name
    words = text.split()
    filtered_words = []
    for word in words:
        if word not in ["सर्च", "खोज", "ढूंढ", "करो", "करें", "उपलब्ध", "स्टॉक", "में", "है", "हैं", "क्या", "आपके", "हमारे", "मेरे", "पास"]:
            filtered_words.append(word)
    
    if filtered_words:
        product_name = " ".join(filtered_words).strip()
    
    return {"name": product_name}

import datetime

def extract_hindi_custom_date_range(text: str) -> Dict[str, str]:
    """
    Extract custom date range from Hindi text like:
    "1 जून से 20 जून तक की रिपोर्ट दिखाओ" or "रिपोर्ट दिखाओ 1 जून से 20 जून तक"
    
    Returns:
        Dictionary with start_date and end_date in YYYY-MM-DD format
    """
    # Print for debugging
    print(f"Extracting Hindi custom date range from: '{text}'")
    
    # Define Hindi month pattern for reuse
    hindi_month_pattern = r"जनवरी|फरवरी|मार्च|अप्रैल|मई|जून|जुलाई|अगस्त|सितंबर|अक्टूबर|नवंबर|दिसंबर|जन|फर|मार|अप्र|जुल|अग|सित|अक्ट|नव|दिस"
    date_pattern = f"(\\d+\\s+({hindi_month_pattern}))"
    
    # Pattern for "रिपोर्ट दिखाओ [date] से [date] तक"
    pattern1 = f"(?:रिपोर्ट|रिपोर्ट्स|बिक्री|सेल्स)\\s+(?:दिखाओ|दिखाए|बताओ|बताए|भेजो|भेजें|दो)\\s+{date_pattern}\\s+से\\s+{date_pattern}\\s+तक"
    match = re.search(pattern1, text)
    
    if not match:
        # Pattern for "[date] से [date] तक की रिपोर्ट"
        pattern2 = f"{date_pattern}\\s+से\\s+{date_pattern}\\s+तक\\s+की\\s+(?:रिपोर्ट|रिपोर्ट्स|बिक्री|सेल्स)"
        match = re.search(pattern2, text)
    
    if not match:
        # Pattern for "[date] से [date] तक"
        pattern3 = f"{date_pattern}\\s+से\\s+{date_pattern}\\s+तक"
        match = re.search(pattern3, text)
        
    # Additional pattern for "रिपोर्ट [date] से [date]"
    if not match:
        pattern4 = f"(?:रिपोर्ट|रिपोर्ट्स|बिक्री|सेल्स)\\s+{date_pattern}\\s+से\\s+{date_pattern}"
        match = re.search(pattern4, text)
    
    if match:
        # Extract the date strings based on the pattern matched
        # The group indices will be different depending on which pattern matched
        if len(match.groups()) >= 4:  # For patterns with nested capture groups due to date_pattern
            start_date_str = match.group(1).strip()
            end_date_str = match.group(3).strip()  # Group 3 because of nested capture groups
        else:
            start_date_str = match.group(1).strip()
            end_date_str = match.group(2).strip()
        
        print(f"Matched Hindi date range: '{start_date_str}' से '{end_date_str}' तक")
        
        # Try to parse dates
        try:
            # Parse start date
            start_date = parse_hindi_date(start_date_str)
            
            # Parse end date
            end_date = parse_hindi_date(end_date_str)
            
            if start_date and end_date:
                result = {
                    "start_date": start_date.strftime("%Y-%m-%d"),
                    "end_date": end_date.strftime("%Y-%m-%d")
                }
                print(f"Parsed Hindi date range: {result}")
                return result
            else:
                print(f"Failed to parse Hindi dates: start_date={start_date}, end_date={end_date}")
        except Exception as e:
            print(f"Error parsing Hindi dates: {e}")
    else:
        print("No Hindi date range pattern matched")
    
    return {}

# Define Hindi month mapping at module level for global access
HINDI_MONTH_MAPPING = {
    "जनवरी": "January",
    "फरवरी": "February",
    "मार्च": "March",
    "अप्रैल": "April",
    "मई": "May",
    "जून": "June",
    "जुलाई": "July",
    "अगस्त": "August",
    "सितंबर": "September",
    "अक्टूबर": "October",
    "नवंबर": "November",
    "दिसंबर": "December",
    # Short forms
    "जन": "Jan",
    "फर": "Feb",
    "मार": "Mar",
    "अप्र": "Apr",
    "जुल": "Jul",
    "अग": "Aug",
    "सित": "Sep",
    "अक्ट": "Oct",
    "नव": "Nov",
    "दिस": "Dec"
}

def parse_hindi_date(date_str: str) -> datetime.datetime:
    """
    Parse a Hindi date string
    
    Args:
        date_str: Date string like "1 जून", "2 जनवरी", etc.
        
    Returns:
        datetime object or None if parsing fails
    """
    # Print for debugging
    print(f"Parsing Hindi date: '{date_str}'")
    
    # Handle ordinal suffixes in Hindi numbers
    date_str = re.sub(r'(\d+)\s*(वां|वा|वीं|वी|थ)', r'\1', date_str)
    
    # Clean up the date string
    date_str = date_str.strip()
    
    # Extract day and month
    # Pattern for "[day] [month]" - using a more specific pattern for Hindi months
    pattern = r"(\d+)\s+(जनवरी|फरवरी|मार्च|अप्रैल|मई|जून|जुलाई|अगस्त|सितंबर|अक्टूबर|नवंबर|दिसंबर|जन|फर|मार|अप्र|जुल|अग|सित|अक्ट|नव|दिस)"
    match = re.search(pattern, date_str)
    
    if match:
        day = match.group(1)
        hindi_month = match.group(2)
        
        print(f"Extracted day: '{day}', month: '{hindi_month}'")
        print(f"Available Hindi months: {list(HINDI_MONTH_MAPPING.keys())}")
        
        # Convert Hindi month to English using global mapping
        if hindi_month in HINDI_MONTH_MAPPING:
            english_month = HINDI_MONTH_MAPPING[hindi_month]
            print(f"Converted Hindi month: '{hindi_month}' to '{english_month}'")
            
            # Create date string in English format
            english_date_str = f"{day} {english_month}"
            print(f"English date string: '{english_date_str}'")
            
            # Parse using English date parsing
            try:
                parsed_date = datetime.datetime.strptime(english_date_str, "%d %B")
                current_year = datetime.datetime.now().year
                parsed_date = parsed_date.replace(year=current_year)
                print(f"Successfully parsed date: {parsed_date}")
                return parsed_date
            except ValueError:
                try:
                    parsed_date = datetime.datetime.strptime(english_date_str, "%d %b")
                    current_year = datetime.datetime.now().year
                    parsed_date = parsed_date.replace(year=current_year)
                    print(f"Successfully parsed date with abbreviated month: {parsed_date}")
                    return parsed_date
                except ValueError:
                    print(f"Failed to parse '{english_date_str}' with standard formats")
    
    # If parsing fails, try numeric formats
    numeric_formats = [
        "%d/%m",           # 01/06
        "%d-%m",           # 01-06
        "%d/%m/%Y",        # 01/06/2023
        "%d-%m-%Y"         # 01-06-2023
    ]
    
    for fmt in numeric_formats:
        try:
            parsed_date = datetime.datetime.strptime(date_str, fmt)
            if "%Y" not in fmt:
                current_year = datetime.datetime.now().year
                parsed_date = parsed_date.replace(year=current_year)
            print(f"Successfully parsed with numeric format '{fmt}': {parsed_date}")
            return parsed_date
        except ValueError:
            continue
    
    # Try to extract just the day and month name from English month names
    # This is for cases where Hindi month names were already converted to English
    day_month_pattern = r"(\d+)\s+([a-zA-Z]+)"
    match = re.search(day_month_pattern, date_str)
    if match:
        try:
            day = int(match.group(1))
            month_name = match.group(2).capitalize()
            
            # Convert month name to month number
            month_names = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12,
                "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "Jun": 6,
                "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
            }
            
            if month_name in month_names:
                month = month_names[month_name]
                year = datetime.datetime.now().year
                result = datetime.datetime(year, month, day)
                print(f"Successfully parsed day-month pattern: {result}")
                return result
        except Exception as e:
            print(f"Error parsing day-month pattern: {e}")
    
    print(f"Failed to parse Hindi date: '{date_str}'")
    # If all formats fail, return None
    return None

def extract_hindi_report_range(text: str) -> Dict[str, str]:
    """
    Extract report time range from Hindi text
    """
    # Print for debugging
    print(f"Extracting Hindi report range from: '{text}'")
    
    # First check for custom date range
    custom_range = extract_hindi_custom_date_range(text)
    if custom_range:
        print(f"Found Hindi custom date range: {custom_range}")
        return custom_range
    
    # Then check for predefined ranges
    if re.search(r"कल\s+की", text):
        print("Found Hindi predefined range: yesterday")
        return {"range": "yesterday"}
    elif re.search(r"आज\s+की", text):
        print("Found Hindi predefined range: today")
        return {"range": "today"}
    elif re.search(r"इस\s+हफ्ते\s+की", text):
        print("Found Hindi predefined range: week")
        return {"range": "week"}
    elif re.search(r"इस\s+महीने\s+की", text):
        print("Found Hindi predefined range: this-month")
        return {"range": "this-month"}
    elif re.search(r"पिछले\s+हफ्ते\s+की", text):
        print("Found Hindi predefined range: last-week")
        return {"range": "last-week"}
    elif re.search(r"पिछले\s+महीने\s+की", text):
        print("Found Hindi predefined range: last-month")
        return {"range": "last-month"}
    
    # Check if the text contains 'रिपोर्ट' (report) but no specific range
    if "रिपोर्ट" in text and not any(pattern in text for pattern in ["आज", "कल", "हफ्ते", "महीने"]):
        print("Hindi report mentioned but no range specified, returning empty dict")
        return {}
    
    # Default to today if no range specified
    print("No Hindi range found, defaulting to today")
    return {"range": "today"}  # Default to today

def extract_hindi_order_range_details(text: str) -> Dict[str, str]:
    """
    Extract order time range from Hindi text like:
    "आज के ऑर्डर दिखाओ" or "कल के ऑर्डर दिखाओ"
    
    Returns:
        Dictionary with time range
    """
    if re.search(r"कल\s+के", text):
        return {"range": "yesterday"}
    elif re.search(r"आज\s+के", text):
        return {"range": "today"}
    elif re.search(r"इस\s+हफ्ते\s+के", text):
        return {"range": "week"}
    elif re.search(r"इस\s+महीने\s+के", text):
        return {"range": "this-month"}
    elif re.search(r"हाल\s+(?:के|ही|में)", text):
        return {"range": "recent"}
    elif re.search(r"नए", text):
        return {"range": "recent"}
    else:
        return {"range": "all"}  # Default to all orders


def extract_hindi_top_products_details(text: str) -> Dict[str, Any]:
    """
    Extract top products details from Hindi text like:
    "टॉप 5 प्रोडक्ट दिखाओ" or "इस हफ्ते के बेस्ट प्रोडक्ट"
    
    Returns:
        Dictionary with time range and limit
    """
    # Extract limit if specified
    limit_match = re.search(r'टॉप\s+(\d+)', text)
    limit = int(limit_match.group(1)) if limit_match else 5  # Default to top 5 if not specified
    
    # Check for predefined time ranges
    if re.search(r'आज', text):
        return {"range": "today", "limit": limit}
    elif re.search(r'कल', text):
        return {"range": "yesterday", "limit": limit}
    elif re.search(r'इस\s+हफ्ते', text):
        return {"range": "week", "limit": limit}
    elif re.search(r'इस\s+महीने', text):
        return {"range": "this-month", "limit": limit}
    elif re.search(r'सभी\s+समय', text):
        return {"range": "all", "limit": limit}
    
    # Extract custom date range if present
    custom_range = extract_hindi_custom_date_range(text)
    if custom_range:
        custom_range["limit"] = limit
        return custom_range
    
    # Default to all-time if no range specified
    return {"range": "all", "limit": limit}

def extract_hindi_customer_data_details(text: str) -> Dict[str, Any]:
    """
    Extract customer data details from Hindi text like:
    "इस महीने के कस्टमर का डाटा दिखाओ" or "कल के ग्राहकों की जानकारी दो"
    
    Returns:
        Dictionary with time range and optional limit
    """
    entities = {}
    
    # Extract limit if specified
    limit_match = re.search(r'टॉप\s+(\d+)\s+(?:कस्टमर|ग्राहक)', text)
    if limit_match:
        entities["limit"] = int(limit_match.group(1))
    
    # Check for predefined time ranges
    if re.search(r'आज', text):
        entities["range"] = "today"
    elif re.search(r'कल', text):
        entities["range"] = "yesterday"
    elif re.search(r'इस\s+हफ्ते|पिछले\s+हफ्ते', text):
        entities["range"] = "week"
    elif re.search(r'इस\s+महीने', text):
        entities["range"] = "this-month"
    elif re.search(r'सभी\s+समय', text):
        entities["range"] = "all"
    
    # Extract custom date range if present
    custom_range = extract_hindi_custom_date_range(text)
    if custom_range:
        entities.update(custom_range)
    elif "range" not in entities:
        # Default to this month if no range specified
        entities["range"] = "this-month"
    
    return entities

def parse_hindi_command(message: str) -> Dict[str, Any]:
    """
    Parse a Hindi command message and return the recognized intent and extracted entities
    
    Args:
        message: The Hindi command message
        
    Returns:
        A dictionary with 'intent', 'entities', and 'language' keys
    """
    # Normalize the message
    normalized_message = message.strip()
    
    # First check for custom date range in report commands
    if "रिपोर्ट" in normalized_message:
        # Try to extract custom date range first
        custom_range = extract_hindi_custom_date_range(normalized_message)
        if custom_range and "start_date" in custom_range and "end_date" in custom_range:
            print(f"Found Hindi custom date range for report: {custom_range}")
            return {
                "intent": "get_report",
                "entities": custom_range,
                "language": "hi"
            }
    
    # Define priority order for intent matching to handle overlapping patterns
    priority_intents = ["get_low_stock", "add_product", "edit_stock", "get_report", "get_orders", "search_product", "get_inventory", "get_top_products", "get_customer_data"]
    
    # Then try to match intents in priority order
    for intent in priority_intents:
        patterns = HINDI_INTENT_PATTERNS.get(intent, [])
        for pattern in patterns:
            if re.search(pattern, normalized_message, re.IGNORECASE):
                # Extract entities based on intent
                entities = {}
                
                if intent == "add_product":
                    entities = extract_hindi_product_details(normalized_message)
                elif intent == "edit_stock":
                    entities = extract_hindi_edit_stock_details(normalized_message)
                elif intent == "get_report":
                    entities = extract_hindi_report_range(normalized_message)
                elif intent == "get_low_stock":
                    entities = extract_hindi_get_low_stock_details(normalized_message)
                elif intent == "search_product":
                    entities = extract_hindi_search_product_details(normalized_message)
                elif intent == "get_orders":
                    entities = extract_hindi_order_range_details(normalized_message)
                elif intent == "get_top_products":
                    entities = extract_hindi_top_products_details(normalized_message)
                elif intent == "get_customer_data":
                    entities = extract_hindi_customer_data_details(normalized_message)
                
                return {
                    "intent": intent,
                    "entities": entities,
                    "language": "hi"
                }
    
    # If no intent matched
    return {
        "intent": "unknown",
        "entities": {}
    }

# Example usage
if __name__ == "__main__":
    # Test cases
    test_commands = [
        "मेरे प्रोडक्ट दिखाओ",  # Show my products
        "आज की रिपोर्ट भेजो",    # Send today's report
        "कम स्टॉक वाले आइटम दिखाओ",  # Show low stock items
        "नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो",  # Add new product Rice 50rs 20pcs
        "चावल का स्टॉक 100 करो",  # Update Rice stock to 100
        "आज के ऑर्डर दिखाओ",  # Show today's orders
        "कल के ऑर्डर दिखाओ",  # Show yesterday's orders
        "इस हफ्ते के ऑर्डर दिखाओ",  # Show this week's orders
        "इस महीने के ऑर्डर दिखाओ",  # Show this month's orders
        "हाल के ऑर्डर दिखाओ",  # Show recent orders
        "सभी ऑर्डर दिखाओ"  # Show all orders
    ]
    
    print("\nTesting Hindi intent recognition:\n")
    for cmd in test_commands:
        result = parse_hindi_command(cmd)
        print(f"Command: '{cmd}'")
        print(f"Result: {result}\n")