import requests
import json
import logging
import datetime
import re
from typing import Dict, Any, Optional, Union, Tuple, List
from urllib.parse import urljoin
from fastapi import APIRouter
from pydantic import BaseModel
from nlp.enhanced_multilingual_parser import parse_multilingual_command, format_response

router = APIRouter()

class CommandInput(BaseModel):
    text: str

@router.post("/process", tags=["NLP Parser"])
async def process_command(input: CommandInput):
    result = parse_multilingual_command(input.text)
    return format_response(
        intent=result.get('intent'),
        entities=result.get('entities', {}),
        language=result.get('language'),
        raw_text=result.get('raw_text'),
        normalized_text=result.get('normalized_text')
    )

# Setup logging
import os

# Use the existing logs directory
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')

# Configure logging to write to the logs directory
log_file = os.path.join(logs_dir, 'command_router.log')  # Use command_router.log as specified in requirements

# Configure file handler
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Configure console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

logger.info("Command Router initialized - API integration active")
logger.info(f"Log file location: {log_file}")

# Base URL for API endpoints (configurable)
BASE_URL = "http://127.0.0.1:8000"

# Response templates for different languages
RESPONSE_TEMPLATES = {
    "en": {
        "register": {
            "success": "Business '{business_name}' registered successfully at {location}. Welcome to One Tappe!",
            "error": "Failed to register business. Error: {error}",
            "missing_info": "Please provide both business name and location for registration. Format: register business_name=YourBusinessName location=YourLocation"
        },
        "add_product": {
            "success": "Product {name} added successfully with price ₹{price} and stock {stock}.",
            "error": "Failed to add product {name}. Error: {error}"
        },
        "edit_stock": {
            "success": "Stock updated for {name} to {stock} units.",
            "error": "Failed to update stock for {name}. Error: {error}"
        },
        "get_inventory": {
            "success": "Current inventory:\n{inventory}",
            "error": "Failed to retrieve inventory. Error: {error}"
        },
        "get_low_stock": {
            "success": "Low stock items:\n{low_stock}",
            "error": "Failed to retrieve low stock items. Error: {error}"
        },
        "get_report": {
            "success": "Sales report for {range}:\n{report}",
            "error": "Failed to generate {range} report. Error: {error}"
        },
        "get_inventory_report": {
            "success": "Inventory report generated successfully. You can download it from the link provided.",
            "error": "Failed to generate inventory report. Error: {error}"
        },
        "get_orders": {
            "success": "{range} orders:\n{orders}",
            "error": "Failed to retrieve {range} orders. Error: {error}"
        },
        "get_top_products": {
            "success": "Top {limit} products for {range}:\n{products}",
            "error": "Failed to retrieve top products for {range}. Error: {error}"
        },
        "get_customer_data": {
            "success": "Top {limit} Customers {range}:\n{customers}",
            "error": "Failed to retrieve customer data for {range}. Error: {error}"
        },
        "search_product": {
            "success": "Yes, {name} is available (Stock: {stock}).",
            "not_found": "Sorry, {name} is not available in your inventory.",
            "error": "Failed to check availability of {name}. Error: {error}"
        },
        "unknown": "Sorry, I couldn't understand that command."
    },
    "hi": {
        "register": {
            "success": "व्यापार '{business_name}' {location} में सफलतापूर्वक पंजीकृत किया गया। One Tappe में आपका स्वागत है!",
            "error": "व्यापार पंजीकरण में विफल। त्रुटि: {error}",
            "missing_info": "कृपया पंजीकरण के लिए व्यापार का नाम और स्थान दोनों प्रदान करें। प्रारूप: रजिस्टर व्यापार=आपकाव्यापारनाम स्थान=आपकास्थान"
        },
        "add_product": {
            "success": "प्रोडक्ट {name} को ₹{price} कीमत और {stock} स्टॉक के साथ सफलतापूर्वक जोड़ा गया।",
            "error": "प्रोडक्ट {name} को जोड़ने में विफल। त्रुटि: {error}"
        },
        "edit_stock": {
            "success": "{name} का स्टॉक {stock} इकाइयों में अपडेट किया गया।",
            "error": "{name} के लिए स्टॉक अपडेट करने में विफल। त्रुटि: {error}"
        },
        "get_inventory": {
            "success": "वर्तमान इन्वेंटरी:\n{inventory}",
            "error": "इन्वेंटरी प्राप्त करने में विफल। त्रुटि: {error}"
        },
        "get_low_stock": {
            "success": "कम स्टॉक वाले प्रोडक्ट:\n{low_stock}",
            "error": "कम स्टॉक वाले आइटम प्राप्त करने में विफल। त्रुटि: {error}"
        },
        "get_report": {
            "success": "{range} के लिए बिक्री रिपोर्ट:\n{report}",
            "error": "{range} रिपोर्ट जनरेट करने में विफल। त्रुटि: {error}"
        },
        "get_inventory_report": {
            "success": "इन्वेंटरी रिपोर्ट सफलतापूर्वक जनरेट की गई है। आप दिए गए लिंक से इसे डाउनलोड कर सकते हैं।",
            "error": "इन्वेंटरी रिपोर्ट जनरेट करने में विफल। त्रुटि: {error}"
        },
        "get_orders": {
            "success": "{range} के ऑर्डर:\n{orders}",
            "error": "{range} के ऑर्डर प्राप्त करने में विफल। त्रुटि: {error}"
        },
        "get_top_products": {
            "success": "{range} के लिए टॉप {limit} प्रोडक्ट्स:\n{products}",
            "error": "{range} के लिए टॉप प्रोडक्ट्स प्राप्त करने में विफल। त्रुटि: {error}"
        },
        "get_customer_data": {
            "success": "{range} के टॉप {limit} ग्राहक:\n{customers}",
            "error": "{range} के लिए ग्राहक डेटा प्राप्त करने में विफल। त्रुटि: {error}"
        },
        "search_product": {
            "success": "हाँ, {name} उपलब्ध है (स्टॉक: {stock})।",
            "not_found": "क्षमा करें, {name} आपके इन्वेंटरी में उपलब्ध नहीं है।",
            "error": "{name} की उपलब्धता जांचने में विफल। त्रुटि: {error}"
        },
        "unknown": "क्षमा करें, मैं उस कमांड को समझ नहीं पाया।"
    }
}

# API endpoint mappings
API_ENDPOINTS = {
    "register": {
        "path": "/seller/register",
        "method": "POST"
    },
    "add_product": {
        "path": "/products",
        "method": "POST"
    },
    "edit_stock": {
        "path": "/seller/products/update-stock",
        "method": "POST"
    },
    "get_inventory": {
        "path": "/seller/products",
        "method": "GET"
    },
    "get_low_stock": {
        "path": "/seller/products/low-stock",
        "method": "POST"
    },
    "get_report": {
        "path": "/seller/report",
        "method": "GET"
    },
    "get_inventory_report": {
        "path": "/inventory/report",
        "method": "GET"
    },
    "get_orders": {
        "path": "/seller/orders",
        "method": "GET"
    },
    "get_top_products": {
        "path": "/seller/products/top",
        "method": "GET"
    },
    "search_product": {
        "path": "/seller/products/check-stock",
        "method": "POST"
    },
    "get_customer_data": {
        "path": "/seller/customers/report",
        "method": "GET"
    }
}

def make_api_request(endpoint: str, method: str, params: Dict[str, Any] = None, data: Dict[str, Any] = None, user_id: str = None) -> Dict[str, Any]:
    """
    Make an API request to the backend service
    
    Args:
        endpoint: API endpoint path
        method: HTTP method (GET, POST, etc.)
        params: Query parameters for GET requests
        data: JSON data for POST requests
        user_id: User ID for authentication
        
    Returns:
        API response as dictionary
    """
    url = urljoin(BASE_URL, endpoint)
    headers = {
        "Content-Type": "application/json"
    }
    
    # Add authentication if user_id is provided
    if user_id:
        headers["Authorization"] = f"Bearer {user_id}"
    
    # Log request details
    logger.info(f"API Request: {method} {url}")
    logger.info(f"Headers: {headers}")
    if params:
        logger.info(f"Query Params: {params}")
    if data:
        logger.info(f"Request Data: {json.dumps(data)}")
    
    try:
        if method.upper() == "GET":
            response = requests.get(url, params=params, headers=headers)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        else:
            logger.error(f"Unsupported HTTP method: {method}")
            return {"error": f"Unsupported HTTP method: {method}"}
        
        # Log response status and content
        logger.info(f"Response Status: {response.status_code}")
        logger.info(f"Response Content: {response.text[:500]}" + ("..." if len(response.text) > 500 else ""))
        
        # Check if request was successful
        response.raise_for_status()
        
        # Parse JSON response
        response_data = response.json()
        return response_data
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {str(e)}")
        return {"error": str(e)}
    except json.JSONDecodeError as e:
        logger.error(f"Failed to parse API response: {str(e)}")
        return {"error": "Invalid response format"}

def format_inventory_response(inventory_data: list, language: str) -> str:
    """
    Format inventory data into a readable string
    
    Args:
        inventory_data: List of inventory items
        language: Language code ('en' or 'hi')
        
    Returns:
        Formatted inventory string
    """
    if not inventory_data:
        return "No products found." if language == "en" else "कोई प्रोडक्ट नहीं मिला।"
    
    formatted_items = []
    for i, item in enumerate(inventory_data, 1):
        if language == "en":
            formatted_items.append(f"{i}. {item['name']} – ₹{item['price']} – {item['stock']} qty")
        else:  # Hindi
            formatted_items.append(f"{i}. {item['name']} – ₹{item['price']} – {item['stock']} मात्रा")
    
    return "\n".join(formatted_items)

def format_orders_response(orders_data: list, language: str, time_range: str = "all") -> str:
    """
    Format orders data into a readable string
    
    Args:
        orders_data: List of order items
        language: Language code ('en' or 'hi')
        time_range: Time range for the orders (default: "all")
        
    Returns:
        Formatted orders string
    """
    # Translate time range for Hindi
    range_translation = {
        "today": "आज",
        "yesterday": "कल",
        "week": "इस हफ्ते",
        "this-week": "इस हफ्ते",
        "this-month": "इस महीने",
        "recent": "हाल के",
        "all": "सभी"
    }
    
    display_range = time_range
    if language == "hi" and time_range in range_translation:
        display_range = range_translation[time_range]
    
    if not orders_data:
        if language == "en":
            return f"No orders found for {display_range}."
        else:  # Hindi
            return f"{display_range} के लिए कोई ऑर्डर नहीं मिला।"
    
    formatted_items = []
    for order in orders_data:
        if language == "en":
            formatted_items.append(f"- Order #{order['id']}: {order['status']}, Total: ₹{order['total']}")
        else:  # Hindi
            formatted_items.append(f"- ऑर्डर #{order['id']}: {order['status']}, कुल: ₹{order['total']}")
    
    return "\n".join(formatted_items)

def format_date_for_display(date_str: str, language: str = "en") -> str:
    """
    Format a date string (YYYY-MM-DD) for display in the given language
    
    Args:
        date_str: Date string in YYYY-MM-DD format
        language: Language code (en/hi)
        
    Returns:
        Formatted date string for display
    """
    try:
        # Parse the date string
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        if language == "hi":
            # Hindi month names
            hindi_months = [
                "जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून", 
                "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"
            ]
            return f"{date_obj.day} {hindi_months[date_obj.month - 1]}"
        else:
            # English format
            return date_obj.strftime("%d %B")
    except Exception:
        return date_str

def format_date_for_display(date_str: str, language: str) -> str:
    """
    Format a date string for display in the response
    
    Args:
        date_str: Date string in ISO format (YYYY-MM-DD)
        language: Language code
        
    Returns:
        Formatted date string for display
    """
    try:
        # Parse the ISO date
        date_obj = datetime.datetime.strptime(date_str, "%Y-%m-%d")
        
        # Get month name
        month_names_en = ["January", "February", "March", "April", "May", "June", 
                         "July", "August", "September", "October", "November", "December"]
        month_names_hi = ["जनवरी", "फरवरी", "मार्च", "अप्रैल", "मई", "जून", 
                         "जुलाई", "अगस्त", "सितंबर", "अक्टूबर", "नवंबर", "दिसंबर"]
        
        # Format the date as "1 January" or "1 जनवरी"
        day = date_obj.day
        month_idx = date_obj.month - 1
        
        if language == "hi":
            return f"{day} {month_names_hi[month_idx]}"
        else:
            return f"{day} {month_names_en[month_idx]}"
    except Exception as e:
        logger.error(f"Error formatting date {date_str}: {str(e)}")
        return date_str

def format_top_products_response(products_data: list, language: str, time_range: str, limit: int) -> str:
    """
    Format top products data into a readable string
    
    Args:
        products_data: List of top product items
        language: Language code (en/hi)
        time_range: Time range for the products
        limit: Number of products to display
        
    Returns:
        Formatted top products string
    """
    if not products_data:
        return "No products found."
    
    products_str = ""
    for idx, product in enumerate(products_data):
        products_str += f"{idx+1}. {product['name']} - {product['sales']} units, ₹{product['revenue']}\n"
    
    return products_str

def register_seller(entities: Dict[str, Any], language: str, user_id: str = None) -> str:
    """
    Register a new seller with the provided business name and location
    
    Args:
        entities: Dictionary containing business_name and location
        language: Language code ('en' or 'hi')
        user_id: User ID for authentication (WhatsApp number)
        
    Returns:
        Response message
    """
    import time
    from nlp.entity_utils import validate_register_entities
    from nlp.response_utils import get_response_template, format_error_details
    
    start_time = time.time()
    
    # Log the registration attempt with metadata
    logger.info(f"Processing seller registration: user_id={user_id}, language={language}")
    
    # Validate required entities
    validation_errors = validate_register_entities(entities)
    
    if validation_errors:
        error_details = format_error_details(validation_errors, language)
        logger.warning(f"Validation errors in seller registration: {validation_errors}, user_id={user_id}")
        
        # Return specific error message based on missing fields
        if 'business_name' in validation_errors and 'location' in validation_errors:
            return get_response_template('register', 'missing_info', language)
        elif 'business_name' in validation_errors:
            return get_response_template('register', 'missing_business_name', language)
        elif 'location' in validation_errors:
            return get_response_template('register', 'missing_location', language)
        else:
            return get_response_template('register', 'validation_error', language).format(error_details=error_details)
    
    # Extract validated entities
    business_name = entities.get('business_name')
    location = entities.get('location')
    
    # Add WhatsApp number and registration timestamp if not already present
    if 'whatsapp_number' not in entities and user_id:
        entities['whatsapp_number'] = user_id
    
    if 'registered_at' not in entities:
        entities['registered_at'] = int(time.time())  # Unix timestamp
    
    # Prepare data for API request
    data = {
        'business_name': business_name,
        'location': location,
        'whatsapp_number': entities.get('whatsapp_number', user_id),
        'registered_at': entities.get('registered_at')
    }
    
    # Get API endpoint details
    endpoint_info = API_ENDPOINTS.get('register')
    if not endpoint_info:
        logger.error("API endpoint for register not found")
        return get_response_template('register', 'error', language).format(error="API configuration error")
    
    # Make API request
    response = make_api_request(
        endpoint=endpoint_info['path'],
        method=endpoint_info['method'],
        data=data,
        user_id=user_id
    )
    
    # Calculate and log processing duration
    processing_time = (time.time() - start_time) * 1000  # in milliseconds
    logger.info(f"Seller registration processing completed in {processing_time:.2f}ms for user_id={user_id}")
    
    # Check for errors
    if 'error' in response:
        error_message = response['error']
        logger.error(f"Error registering seller: {error_message}, user_id={user_id}")
        
        # Check for duplicate registration
        if "duplicate" in error_message.lower() or "already exists" in error_message.lower():
            return get_response_template('register', 'duplicate', language)
        
        return get_response_template('register', 'error', language).format(error=error_message)
    
    # Return success message
    logger.info(f"Seller registered successfully: business_name={business_name}, location={location}, user_id={user_id}")
    return get_response_template('register', 'success', language).format(
        business_name=business_name,
        location=location,
        whatsapp_number=entities.get('whatsapp_number', user_id)
    )

def format_customer_data_response(customers_data: list, language: str, time_range: str) -> str:
    """
    Format customer data into a readable string
    
    Args:
        customers_data: List of customer items
        language: Language code (en/hi)
        time_range: Time range for the customer data
        
    Returns:
        Formatted customer data string
    """
    if not customers_data:
        if language == "en":
            return "No customer data found for this period."
        else:  # Hindi
            return "इस अवधि के लिए कोई ग्राहक डेटा नहीं मिला।"
    
    formatted_items = []
    for i, customer in enumerate(customers_data, 1):
        if language == "en":
            formatted_items.append(f"{i}. {customer['name']} – ₹{customer['total_spent']} ({customer['order_count']} orders)")
        else:  # Hindi
            formatted_items.append(f"{i}. {customer['name']} – ₹{customer['total_spent']} ({customer['order_count']} ऑर्डर)")
    
    return "\n".join(formatted_items)


def format_report_response(report_data: Dict[str, Any], language: str, time_range: str) -> str:
    """
    Format report data into a readable string
    
    Args:
        report_data: Report data from API
        language: Language code (en/hi)
        time_range: Time range for the report
        
    Returns:
        Formatted report string
    """
    # Check if this is a custom date range report
    if "start_date" in report_data and "end_date" in report_data:
        start_date = report_data.get("start_date")
        end_date = report_data.get("end_date")
        
        # Format dates for display
        start_display = format_date_for_display(start_date, language)
        end_display = format_date_for_display(end_date, language)
        
        if language == "hi":
            # Simple date formatting for Hindi
            return f"{start_display} से {end_display} तक की बिक्री: ₹{report_data['sales']}\nऑर्डर: {report_data['orders']}\nटॉप प्रोडक्ट: {report_data.get('top_product', 'N/A')}"
        else:
            # Simple date formatting for English
            return f"Sales from {start_display} to {end_display}: ₹{report_data['sales']}\nOrders: {report_data['orders']}\nTop product: {report_data.get('top_product', 'N/A')}"
    
    # Translate time range for Hindi
    range_translation = {
        "today": "आज",
        "yesterday": "कल",
        "week": "इस हफ्ते",
        "this-week": "इस हफ्ते",
        "this-month": "इस महीने",
        "recent": "हाल के",
        "all": "सभी"
    }
    
    display_range = time_range
    if language == "hi" and time_range in range_translation:
        display_range = range_translation[time_range]
    
    if not report_data or "sales" not in report_data:
        if language == "en":
            return f"No data available for {display_range} report."
        else:  # Hindi
            return f"{display_range} की रिपोर्ट के लिए कोई डेटा उपलब्ध नहीं है।"
    
    if language == "en":
        return f"Sales for {display_range}: ₹{report_data['sales']}\nOrders: {report_data['orders']}\nTop product: {report_data.get('top_product', 'N/A')}"
    else:  # Hindi
        return f"{display_range} की बिक्री: ₹{report_data['sales']}\nऑर्डर: {report_data['orders']}\nटॉप प्रोडक्ट: {report_data.get('top_product', 'N/A')}"

def route_command(intent_or_parsed_result: Union[str, Dict[str, Any]], entities: Dict[str, Any] = None, language: str = None, user_id: str = None) -> str:
    """
    Route the parsed command to the appropriate API endpoint and return a response
    
    Args:
        intent_or_parsed_result: Either the intent string or the parsed command result from NLP module
        entities: The entities extracted from the command (if intent is provided separately)
        language: The language code (if intent is provided separately)
        user_id: User ID for authentication
        
    Returns:
        A formatted response string
    """
    # Handle both function signatures for backward compatibility
    if isinstance(intent_or_parsed_result, dict):
        parsed_result = intent_or_parsed_result
        intent = parsed_result.get("intent", "unknown")
        entities = parsed_result.get("entities", {})
        language = parsed_result.get("language", "en")
    else:
        intent = intent_or_parsed_result
        entities = entities or {}
        language = language or "en"
    
    # If language is not supported, default to English
    if language not in RESPONSE_TEMPLATES:
        language = "en"
    
    # Handle unknown intent
    if intent == "unknown":
        return RESPONSE_TEMPLATES[language]["unknown"]
    
    # Get API endpoint configuration
    if intent not in API_ENDPOINTS:
        logger.error(f"Unknown intent: {intent}")
        return RESPONSE_TEMPLATES[language]["unknown"]
    
    endpoint_config = API_ENDPOINTS[intent]
    endpoint_path = endpoint_config["path"]
    method = endpoint_config["method"]
    
    # Prepare request parameters based on intent
    params = {}
    data = {}
    
    if intent == "register":
        # For register intent, call the dedicated function
        return register_seller(entities, language, user_id)
    elif intent == "add_product":
        data = {
            "product_name": entities.get("name", ""),
            "price": entities.get("price", 0),
            "stock": entities.get("stock", 0),
            "description": f"Added via NLP command"
        }
    elif intent == "edit_stock":
        data = {
            "name": entities.get("name", ""),
            "stock": entities.get("stock", 0)
        }
    elif intent == "get_low_stock":
        data = {
            "threshold": entities.get("threshold", 5)
        }
        logger.info(f"Processing get_low_stock intent with threshold: {data['threshold']}")
    elif intent == "search_product":
        data = {
            "name": entities.get("name", "")
        }
        logger.info(f"Processing search_product intent for: {data['name']}")
    elif intent == "get_report":
        params = {"range": entities.get("range", "today")}
    elif intent == "get_orders":
        params = {"range": entities.get("range", "all")}
    elif intent == "get_customer_data":
        params = {
            "range": entities.get("range", "this-month"),
            "limit": entities.get("limit", 10)
        }
        logger.info(f"Processing get_customer_data intent with range: {params['range']} and limit: {params['limit']}")
    
    # Make API request
    try:
        # Make actual API calls to the backend
        response = make_api_request(endpoint_path, method, params, data, user_id)
        
        # Special handling for add_product intent
        if intent == "add_product":
            logger.info(f"Processing add_product intent with data: {json.dumps(data)}")
            
            # Log the full request and response for debugging
            logger.info(f"Request URL: {BASE_URL}{endpoint_path}")
            logger.info(f"Request Method: {method}")
            logger.info(f"Request Data: {json.dumps(data)}")
            logger.info(f"Response: {json.dumps(response)}")
            
            # Check if there was an error in the response
            if "error" in response:
                logger.error(f"Error adding product: {response['error']}")
                return RESPONSE_TEMPLATES[language][intent]["error"].format(
                    **entities, error=response["error"]
                )
            
            # Return success message
            return RESPONSE_TEMPLATES[language][intent]["success"].format(**entities)
        
        # If backend is not available, fall back to simulation for testing
        if "error" in response and "ConnectionError" in response["error"]:
            logger.warning(f"Backend connection failed, falling back to simulation: {response['error']}")
            response = simulate_api_response(intent, entities)
            logger.info(f"Simulated response for {intent}: {json.dumps(response)}")
        
        # Format response based on intent and language
        if "error" in response:
            # Special handling for get_orders and get_customer_data intents to include range in error message
            if intent in ["get_orders", "get_customer_data"]:
                default_range = "all" if intent == "get_orders" else "this-month"
                time_range = entities.get("range", default_range)
                range_translation = {
                    "today": "आज" if language == "hi" else "today",
                    "yesterday": "कल" if language == "hi" else "yesterday",
                    "week": "इस हफ्ते" if language == "hi" else "this week",
                    "this-week": "इस हफ्ते" if language == "hi" else "this week",
                    "this-month": "इस महीने" if language == "hi" else "this month",
                    "recent": "हाल के" if language == "hi" else "recent",
                    "all": "सभी" if language == "hi" else "all"
                }
                display_range = range_translation.get(time_range, time_range)
                return RESPONSE_TEMPLATES[language][intent]["error"].format(
                    range=display_range, error=response["error"]
                )
            
            return RESPONSE_TEMPLATES[language][intent]["error"].format(
                **entities, error=response["error"]
            )
        
        if intent == "get_inventory":
            inventory_str = format_inventory_response(response.get("products", []), language)
            return RESPONSE_TEMPLATES[language][intent]["success"].format(inventory=inventory_str)
        
        elif intent == "get_low_stock":
            low_stock_str = format_inventory_response(response.get("products", []), language)
            return RESPONSE_TEMPLATES[language][intent]["success"].format(low_stock=low_stock_str)
        
        elif intent == "get_orders":
            time_range = entities.get("range", "all")
            orders_str = format_orders_response(response.get("orders", []), language, time_range)
            
            # Translate time range for display in response
            range_translation = {
                "today": "आज" if language == "hi" else "today",
                "yesterday": "कल" if language == "hi" else "yesterday",
                "week": "इस हफ्ते" if language == "hi" else "this week",
                "this-week": "इस हफ्ते" if language == "hi" else "this week",
                "this-month": "इस महीने" if language == "hi" else "this month",
                "recent": "हाल के" if language == "hi" else "recent",
                "all": "सभी" if language == "hi" else "all"
            }
            
            display_range = range_translation.get(time_range, time_range)
            return RESPONSE_TEMPLATES[language][intent]["success"].format(range=display_range, orders=orders_str)
        
        elif intent == "get_report":
            time_range = entities.get("range", "today")
            report_str = format_report_response(response, language, time_range)
            
            # Translate time range for display in response
            range_translation = {
                "today": "आज" if language == "hi" else "today",
                "yesterday": "कल" if language == "hi" else "yesterday",
                "week": "इस हफ्ते" if language == "hi" else "this week",
                "this-week": "इस हफ्ते" if language == "hi" else "this week",
                "this-month": "इस महीने" if language == "hi" else "this month",
                "recent": "हाल के" if language == "hi" else "recent",
                "all": "सभी" if language == "hi" else "all"
            }
            
            display_range = range_translation.get(time_range, time_range)
            return RESPONSE_TEMPLATES[language][intent]["success"].format(
                range=display_range, report=report_str
            )
            
        elif intent == "get_inventory_report":
            # For inventory report, we just need to return a success message
            # The actual PDF will be downloaded by the user from the link
            return RESPONSE_TEMPLATES[language][intent]["success"]
        
        elif intent == "search_product":
            # Check if product was found
            if response.get("found", False):
                return RESPONSE_TEMPLATES[language][intent]["success"].format(
                    name=entities.get("name", ""),
                    stock=response.get("stock", 0)
                )
            else:
                return RESPONSE_TEMPLATES[language][intent]["not_found"].format(
                    name=entities.get("name", "")
                )
        
        elif intent == "get_customer_data":
            time_range = entities.get("range", "this-month")
            limit = entities.get("limit", 10)
            customers_str = format_customer_data_response(response.get("customers", []), language, time_range)
            
            # Translate time range for display in response
            range_translation = {
                "today": "आज" if language == "hi" else "today",
                "yesterday": "कल" if language == "hi" else "yesterday",
                "week": "इस हफ्ते" if language == "hi" else "this week",
                "this-week": "इस हफ्ते" if language == "hi" else "this week",
                "this-month": "इस महीने" if language == "hi" else "this month",
                "recent": "हाल के" if language == "hi" else "recent",
                "all": "सभी" if language == "hi" else "all"
            }
            
            display_range = range_translation.get(time_range, time_range)
            return RESPONSE_TEMPLATES[language][intent]["success"].format(
                range=display_range, limit=limit, customers=customers_str
            )
        
        else:  # edit_stock
            return RESPONSE_TEMPLATES[language][intent]["success"].format(**entities)
    
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        
        # Special handling for get_orders, get_report, and get_customer_data intents to include range in error message
        if intent in ["get_orders", "get_report", "get_customer_data"]:
            default_range = "all" if intent == "get_orders" else "today" if intent == "get_report" else "this-month"
            time_range = entities.get("range", default_range)
            range_translation = {
                "today": "आज" if language == "hi" else "today",
                "yesterday": "कल" if language == "hi" else "yesterday",
                "week": "इस हफ्ते" if language == "hi" else "this week",
                "this-week": "इस हफ्ते" if language == "hi" else "this week",
                "this-month": "इस महीने" if language == "hi" else "this month",
                "recent": "हाल के" if language == "hi" else "recent",
                "all": "सभी" if language == "hi" else "all"
            }
            display_range = range_translation.get(time_range, time_range)
            return RESPONSE_TEMPLATES[language][intent]["error"].format(
                range=display_range, error="Internal server error"
            )
        
        return RESPONSE_TEMPLATES[language][intent]["error"].format(
            **entities, error="Internal server error"
        )

def simulate_api_response(intent: str, entities: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulate API responses for testing purposes
    
    Args:
        intent: The intent of the command
        entities: Extracted entities
        
    Returns:
        Simulated API response
    """
    # datetime is already imported at the top of the file
    if intent == "add_product":
        return {
            "success": True,
            "product": {
                "name": entities.get("name", ""),
                "price": entities.get("price", 0),
                "stock": entities.get("stock", 0),
                "id": "sim123"
            }
        }
    
    elif intent == "edit_stock":
        # Check for negative stock value
        stock = entities.get("stock", 0)
        if stock < 0:
            return {
                "error": "Quantity cannot be negative"
            }
        
        return {
            "success": True,
            "product": {
                "name": entities.get("name", ""),
                "stock": stock,
                "id": "sim123"
            }
        }
    
    elif intent == "get_inventory":
        return {
            "products": [
                {"name": "Rice", "price": 50, "stock": 100},
                {"name": "Wheat", "price": 40, "stock": 75},
                {"name": "Sugar", "price": 45, "stock": 60},
                {"name": "चावल", "price": 50, "stock": 100},
                {"name": "गेहूं", "price": 40, "stock": 75},
                {"name": "चीनी", "price": 45, "stock": 60}
            ]
        }
    
    elif intent == "get_low_stock":
        return {
            "products": [
                {"name": "Salt", "price": 20, "stock": 5},
                {"name": "Tea", "price": 120, "stock": 8},
                {"name": "नमक", "price": 20, "stock": 5},
                {"name": "चाय", "price": 120, "stock": 8}
            ]
        }
        
    elif intent == "get_top_products":
        # Get the limit and time range from entities
        limit = entities.get("limit", 5)
        time_range = entities.get("range", "week")
        
        # Define sample top products for simulation
        top_products = [
            {"name": "Rice", "sales": 500, "revenue": 25000},
            {"name": "Sugar", "sales": 350, "revenue": 21000},
            {"name": "Tea", "sales": 300, "revenue": 36000},
            {"name": "Coffee", "sales": 250, "revenue": 37500},
            {"name": "Wheat", "sales": 200, "revenue": 15000},
            {"name": "Salt", "sales": 180, "revenue": 3600},
            {"name": "Oil", "sales": 150, "revenue": 22500},
            {"name": "Spices", "sales": 120, "revenue": 18000},
            {"name": "Pulses", "sales": 100, "revenue": 12000},
            {"name": "Flour", "sales": 80, "revenue": 8000}
        ]
        
        # Limit the number of products as per the request
        top_products = top_products[:limit]
        
        return {
            "products": top_products,
            "time_range": time_range
        }
    
    elif intent == "get_orders":
        time_range = entities.get("range", "all")
        
        # Define different orders for different time ranges
        today_orders = [
            {"id": "ORD001", "status": "Delivered", "total": 500},
            {"id": "ORD002", "status": "Processing", "total": 350}
        ]
        
        yesterday_orders = [
            {"id": "ORD003", "status": "Delivered", "total": 720},
            {"id": "ORD004", "status": "Delivered", "total": 250}
        ]
        
        week_orders = [
            {"id": "ORD005", "status": "Delivered", "total": 800},
            {"id": "ORD006", "status": "Processing", "total": 450},
            {"id": "ORD007", "status": "Pending", "total": 600}
        ]
        
        month_orders = [
            {"id": "ORD008", "status": "Delivered", "total": 1200},
            {"id": "ORD009", "status": "Delivered", "total": 950},
            {"id": "ORD010", "status": "Processing", "total": 750}
        ]
        
        all_orders = [
            {"id": "ORD001", "status": "Delivered", "total": 500},
            {"id": "ORD002", "status": "Processing", "total": 350},
            {"id": "ORD003", "status": "Delivered", "total": 720},
            {"id": "ORD004", "status": "Delivered", "total": 250},
            {"id": "ORD005", "status": "Delivered", "total": 800}
        ]
        
        # Return orders based on time range
        if time_range == "today":
            return {"orders": today_orders}
        elif time_range == "yesterday":
            return {"orders": yesterday_orders}
        elif time_range == "week":
            return {"orders": week_orders}
        elif time_range == "this-month":
            return {"orders": month_orders}
        elif time_range == "recent":
            # Recent orders are a combination of today and yesterday
            return {"orders": today_orders + yesterday_orders}
        else:  # all
            return {"orders": all_orders}
    
    elif intent == "get_report":
        time_range = entities.get("range", "today")
        
        # Check if this is a custom date range report
        if "start_date" in entities and "end_date" in entities:
            # For custom date range, return a report with the dates included
            return {
                "start_date": entities.get("start_date"),
                "end_date": entities.get("end_date"),
                "sales": 45000,
                "orders": 95,
                "top_product": "Rice"
            }
        
        # Define different report data for different time ranges
        today_report = {
            "sales": 12500,
            "orders": 25,
            "top_product": "Rice"
        }
        
        yesterday_report = {
            "sales": 10800,
            "orders": 22,
            "top_product": "Wheat"
        }
        
        week_report = {
            "sales": 85000,
            "orders": 175,
            "top_product": "Sugar"
        }
        
        month_report = {
            "sales": 320000,
            "orders": 650,
            "top_product": "Rice"
        }
        
        # Return report data based on time range
        if time_range == "today":
            return today_report
        elif time_range == "yesterday":
            return yesterday_report
        elif time_range == "week" or time_range == "this-week":
            return week_report
        elif time_range == "this-month":
            return month_report
        else:  # all or recent
            return {
                "sales": 428300,
                "orders": 872,
                "top_product": "Rice"
            }
            
    elif intent == "get_inventory_report":
        # For inventory report simulation, we just need to return a success response
        # The actual PDF would be generated by the backend
        return {
            "success": True,
            "message": "Inventory report generated successfully"
        }
    
    elif intent == "get_customer_data":
        # Get the limit and time range from entities
        limit = entities.get("limit", 10)
        time_range = entities.get("range", "this-month")
        
        # Define sample customer data for simulation
        all_customers = [
            {"name": "Rahul Sharma", "total_spent": 25000, "order_count": 12},
            {"name": "Priya Patel", "total_spent": 18500, "order_count": 8},
            {"name": "Amit Singh", "total_spent": 15000, "order_count": 6},
            {"name": "Neha Gupta", "total_spent": 12800, "order_count": 5},
            {"name": "Vikram Malhotra", "total_spent": 10500, "order_count": 4},
            {"name": "Ananya Desai", "total_spent": 9200, "order_count": 7},
            {"name": "Rajesh Kumar", "total_spent": 8500, "order_count": 3},
            {"name": "Sunita Verma", "total_spent": 7800, "order_count": 5},
            {"name": "Deepak Joshi", "total_spent": 6500, "order_count": 4},
            {"name": "Meera Reddy", "total_spent": 5200, "order_count": 3},
            {"name": "Sanjay Kapoor", "total_spent": 4800, "order_count": 2},
            {"name": "Pooja Mehta", "total_spent": 3500, "order_count": 2}
        ]
        
        # Limit the number of customers as per the request
        customers = all_customers[:limit]
        
        return {
            "customers": customers,
            "time_range": time_range
        }
    
    elif intent == "get_top_products":
        # Get the limit and time range from entities
        limit = entities.get("limit", 5)
        time_range = entities.get("range", "week")
        
        try:
            # Make API request to get top products
            response = make_api_request(
                endpoint=API_ENDPOINTS[intent]["path"],
                method=API_ENDPOINTS[intent]["method"],
                params={"limit": limit, "range": time_range},
                user_id=user_id
            )
            
            # If backend is not available, fall back to simulation for testing
            if "error" in response and "ConnectionError" in response["error"]:
                logger.warning(f"Backend connection failed, falling back to simulation: {response['error']}")
                response = simulate_api_response(intent, entities)
                logger.info(f"Simulated response for {intent}: {json.dumps(response)}")
            
            # Format the response
            products_data = response.get("products", [])
            products_str = format_top_products_response(products_data, language, time_range, limit)
            
            # Translate time range for display
            range_translation = {
                "today": "आज" if language == "hi" else "today",
                "yesterday": "कल" if language == "hi" else "yesterday",
                "week": "इस सप्ताह" if language == "hi" else "this week",
                "this-week": "इस सप्ताह" if language == "hi" else "this week",
                "this-month": "इस महीने" if language == "hi" else "this month",
                "month": "इस महीने" if language == "hi" else "this month",
                "all": "सभी समय" if language == "hi" else "all time"
            }
            
            display_range = range_translation.get(time_range, time_range)
            return RESPONSE_TEMPLATES[language][intent]["success"].format(range=display_range, limit=limit, products=products_str)
            
        except Exception as e:
            logger.error(f"Error processing command: {str(e)}")
            return RESPONSE_TEMPLATES[language][intent]["error"].format(range=time_range, error="Internal server error")
        
    elif intent == "search_product":
        # Get the product name from entities
        product_name = entities.get("name", "").lower()
        
        # Define a list of available products for simulation
        available_products = {
            "rice": 100,
            "wheat": 75,
            "sugar": 60,
            "salt": 5,
            "tea": 8,
            "coffee": 15,
            "चावल": 100,
            "गेहूं": 75,
            "चीनी": 60,
            "नमक": 5,
            "चाय": 8,
            "कॉफी": 15
        }
        
        # Check if the product is available
        if product_name in available_products:
            return {
                "found": True,
                "name": product_name,
                "stock": available_products[product_name],
                "price": 50  # Default price for simulation
            }
        else:
            return {
                "found": False,
                "name": product_name
            }
    
    return {"error": "Unknown intent"}

# Example usage
if __name__ == "__main__":
    # Test with English commands
    test_commands = [
        {
            "intent": "add_product",
            "entities": {"name": "Rice", "price": 50, "stock": 20},
            "language": "en"
        },
        {
            "intent": "edit_stock",
            "entities": {"name": "Wheat", "stock": 75},
            "language": "en"
        },
        {
            "intent": "get_inventory",
            "entities": {},
            "language": "en"
        },
        {
            "intent": "get_report",
            "entities": {"range": "today"},
            "language": "en"
        },
        {
            "intent": "get_top_products",
            "entities": {"limit": 3, "range": "week"},
            "language": "en"
        }
    ]
    
    # Test with Hindi commands
    hindi_test_commands = [
        {
            "intent": "add_product",
            "entities": {"name": "चावल", "price": 50, "stock": 20},
            "language": "hi"
        },
        {
            "intent": "edit_stock",
            "entities": {"name": "गेहूं", "stock": 75},
            "language": "hi"
        },
        {
            "intent": "get_inventory",
            "entities": {},
            "language": "hi"
        },
        {
            "intent": "get_report",
            "entities": {"range": "today"},
            "language": "hi"
        },
        {
            "intent": "get_top_products",
            "entities": {"limit": 5, "range": "month"},
            "language": "hi"
        }
    ]
    
    print("\nTesting English commands:\n")
    for cmd in test_commands:
        response = route_command(cmd, user_id="test_user")
        print(f"Intent: {cmd['intent']}")
        print(f"Entities: {cmd['entities']}")
        print(f"Response: {response}\n")


async def process_command(text: str, user_id: str) -> str:
    """
    Process a raw text command from WhatsApp and return a response
    
    Args:
        text: The raw text message from the user
        user_id: The WhatsApp user ID (phone number)
        
    Returns:
        Response message to send back to the user
    """
    logger.info(f"Processing command from user {user_id}: {text}")
    
    try:
        # Parse the command to extract intent and entities
        parsed_result = parse_command(text)
        
        # Route the command to the appropriate handler
        response = route_command(parsed_result, user_id=user_id)
        
        logger.info(f"Response for user {user_id}: {response}")
        return response
    except ImportError as ie:
        logger.error(f"Import error in command processing: {str(ie)}")
        return "Our service is currently undergoing maintenance. Please try again in a few minutes."
    except ValueError as ve:
        logger.error(f"Value error in command processing: {str(ve)}")
        return "I couldn't understand your request format. Please check your input and try again, or type 'help' for assistance."
    except Exception as e:
        logger.error(f"Error processing command: {str(e)}")
        # Return a friendly error message with more specific guidance
        return "Sorry, I couldn't process your request. Please try again with a simpler command or type 'help' for a list of available commands."


def parse_command(text: str) -> Dict[str, Any]:
    """
    Parse a raw text command to extract intent and entities
    
    Args:
        text: The raw text message from the user
        
    Returns:
        Dictionary with intent, entities, and language
    """
    # Validate input
    if not text:
        logger.warning("Empty text received")
        return {
            "intent": "unknown",
            "entities": {},
            "language": "en"
        }
        
    if not isinstance(text, str):
        logger.warning(f"Invalid text type received: {type(text)}")
        return {
            "intent": "unknown",
            "entities": {},
            "language": "en"
        }
        
    # Trim excessive whitespace
    text = text.strip()
    if not text:
        logger.warning("Text contains only whitespace")
        return {
            "intent": "unknown",
            "entities": {},
            "language": "en"
        }
        
    # Detect language (simple implementation - can be enhanced)
    language = detect_language(text)
    
    # Convert text to lowercase for easier matching
    text_lower = text.lower()
    
    # Initialize result
    result = {
        "intent": "unknown",
        "entities": {},
        "language": language
    }
    
    # Check for help command
    if text_lower in ["help", "मदद", "सहायता"]:
        result["intent"] = "help"
        return result
    
    # Match register command
    register_match = re.search(r'register\s+(?:business_?name=)?([\w\s]+)\s+(?:location=)?([\w\s]+)', text_lower)
    if register_match:
        result["intent"] = "register"
        result["entities"] = {
            "business_name": register_match.group(1).strip(),
            "location": register_match.group(2).strip()
        }
        return result
    
    # Match add product command
    add_product_match = re.search(r'add\s+product\s+(?:name=)?([\w\s]+)\s+(?:price=)?(\d+)\s+(?:stock=)?(\d+)', text_lower)
    if add_product_match:
        result["intent"] = "add_product"
        result["entities"] = {
            "name": add_product_match.group(1).strip(),
            "price": int(add_product_match.group(2)),
            "stock": int(add_product_match.group(3))
        }
        return result
    
    # Match edit stock command
    edit_stock_match = re.search(r'(?:edit|update)\s+stock\s+(?:name=)?([\w\s]+)\s+(?:stock=)?(\d+)', text_lower)
    if edit_stock_match:
        result["intent"] = "edit_stock"
        result["entities"] = {
            "name": edit_stock_match.group(1).strip(),
            "stock": int(edit_stock_match.group(2))
        }
        return result
    
    # Match get inventory command
    if re.search(r'(?:get|show)\s+(?:my\s+)?inventory', text_lower):
        result["intent"] = "get_inventory"
        return result
    
    # Match get low stock command
    if re.search(r'(?:get|show)\s+(?:my\s+)?low\s+stock', text_lower):
        result["intent"] = "get_low_stock"
        return result
    
    # Match get report command
    report_match = re.search(r'(?:get|show)\s+(?:my\s+)?(?:sales\s+)?report(?:\s+for\s+(.+))?', text_lower)
    if report_match:
        result["intent"] = "get_report"
        time_range = report_match.group(1) if report_match.group(1) else "today"
        result["entities"] = {"range": time_range}
        return result
    
    # Match get orders command
    orders_match = re.search(r'(?:get|show)\s+(?:my\s+)?orders(?:\s+for\s+(.+))?', text_lower)
    if orders_match:
        result["intent"] = "get_orders"
        time_range = orders_match.group(1) if orders_match.group(1) else "today"
        result["entities"] = {"range": time_range}
        return result
    
    # Match get top products command
    top_products_match = re.search(r'(?:get|show)\s+(?:my\s+)?top\s+(\d+)?\s*products(?:\s+for\s+(.+))?', text_lower)
    if top_products_match:
        result["intent"] = "get_top_products"
        limit = int(top_products_match.group(1)) if top_products_match.group(1) else 5
        time_range = top_products_match.group(2) if top_products_match.group(2) else "month"
        result["entities"] = {"limit": limit, "range": time_range}
        return result
    
    # Match search product command
    search_match = re.search(r'(?:search|find|check)\s+(?:product\s+)?([\w\s]+)', text_lower)
    if search_match:
        result["intent"] = "search_product"
        result["entities"] = {"name": search_match.group(1).strip()}
        return result
    
    # If no intent matched, return unknown
    return result


def detect_language(text: str) -> str:
    """
    Detect the language of the text
    
    Args:
        text: The text to detect language for
        
    Returns:
        Language code (en/hi)
    """
    if not text:
        return "en"
        
    # Simple language detection based on common Hindi words and patterns
    hindi_words = [
        "मेरा", "हमारा", "आप", "तुम", "है", "हैं", "था", "थे", "की", "का", "के", "में", "पर", "से", "को", 
        "मदद", "सहायता", "दिखाओ", "स्टॉक", "रिपोर्ट", "बिक्री", "उत्पाद", "जोड़ें", "अपडेट", "रजिस्टर",
        "दिखाना", "बताओ", "कितना", "कौनसा", "कब", "क्यों", "कैसे", "कहां", "मिला", "चाहिए"
    ]
    
    # Hindi command patterns
    hindi_patterns = [
        r'स्टॉक\s+दिखाओ',
        r'रिपोर्ट\s+दिखाओ',
        r'उत्पाद\s+जोड़ें',
        r'स्टॉक\s+अपडेट',
        r'बिक्री\s+रिपोर्ट',
        r'मेरा\s+स्टॉक',
        r'मेरी\s+बिक्री',
        r'कम\s+स्टॉक',
        r'नया\s+उत्पाद'
    ]
    
    # Count Hindi words in the text
    hindi_word_count = sum(1 for word in hindi_words if word in text.lower())
    
    # Check for Hindi patterns
    hindi_pattern_match = any(re.search(pattern, text.lower()) for pattern in hindi_patterns)
    
    # If Hindi words or patterns are found, consider it Hindi
    # Adjusted threshold to be more sensitive to Hindi content
    if hindi_word_count >= 1 or hindi_pattern_match:
        logger.info(f"Detected Hindi language in text: {text} (word count: {hindi_word_count})")
        return "hi"
    
    # Default to English
    logger.info(f"Detected English language in text: {text}")
    return "en"
    
    print("\nTesting Hindi commands:\n")
    for cmd in hindi_test_commands:
        response = route_command(cmd, user_id="test_user")
        print(f"Intent: {cmd['intent']}")
        print(f"Entities: {cmd['entities']}")
        print(f"Response: {response}\n")