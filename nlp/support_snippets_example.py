#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
One Tappe Support Snippets Example

This script demonstrates how to use the WhatsApp support snippets
in a Python application for responding to seller queries.
"""

import json
import os
import re
from datetime import datetime

# Load the support snippets
def load_snippets(file_path):
    """Load the support snippets from the JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {file_path}")
        return {}

# Detect language (simple implementation)
def detect_language(text):
    """Detect if the text is primarily in Hindi or English."""
    # This is a simplified detection - in production, use a proper language detection library
    # Check for Devanagari Unicode range (Hindi)
    hindi_pattern = re.compile(r'[\u0900-\u097F]')
    hindi_chars = len(hindi_pattern.findall(text))
    
    # If significant Hindi characters are found, assume Hindi
    if hindi_chars > len(text) * 0.1:  # If more than 10% is Hindi
        return 'hi'
    return 'en'  # Default to English

# Get appropriate snippet based on query
def get_snippet(snippets, category, subcategory, language):
    """Get the appropriate snippet based on category, subcategory, and language."""
    try:
        return snippets[category][subcategory][language]
    except KeyError:
        # Fallback to English if the requested language is not available
        try:
            return snippets[category][subcategory]['en']
        except KeyError:
            return "Sorry, I don't have information on that topic."

# Personalize the snippet
def personalize_snippet(snippet, replacements):
    """Replace placeholders in the snippet with personalized information."""
    for placeholder, value in replacements.items():
        snippet = snippet.replace(placeholder, value)
    return snippet

# Example usage function
def respond_to_query(snippets, query, seller_info):
    """Generate a response to a seller query using the appropriate snippet."""
    # Detect language
    language = detect_language(query)
    
    # Simple intent detection (in production, use NLP model)
    query_lower = query.lower()
    
    # Log the query
    log_query(seller_info, query)
    
    # Match query to appropriate snippet
    if any(word in query_lower for word in ['inventory', 'stock', 'product', 'इन्वेंटरी', 'स्टॉक', 'प्रोडक्ट']):
        if any(word in query_lower for word in ['show', 'view', 'list', 'दिखाओ', 'देखना']):
            return get_snippet(snippets, 'inventory_commands', 'view_inventory', language)
        elif any(word in query_lower for word in ['add', 'create', 'new', 'जोड़', 'नया']):
            return get_snippet(snippets, 'inventory_commands', 'add_product', language)
        elif any(word in query_lower for word in ['update', 'edit', 'change', 'अपडेट', 'बदलें']):
            return get_snippet(snippets, 'inventory_commands', 'update_stock', language)
        elif any(word in query_lower for word in ['low', 'कम']):
            return get_snippet(snippets, 'inventory_commands', 'low_stock', language)
        elif any(word in query_lower for word in ['search', 'find', 'खोज', 'ढूंढ']):
            return get_snippet(snippets, 'inventory_commands', 'search_product', language)
    
    elif any(word in query_lower for word in ['report', 'sales', 'रिपोर्ट', 'बिक्री']):
        if any(word in query_lower for word in ['today', 'आज']):
            return get_snippet(snippets, 'sales_report_queries', 'today_report', language)
        elif any(word in query_lower for word in ['week', 'month', 'yesterday', 'हफ्ता', 'महीना', 'कल']):
            return get_snippet(snippets, 'sales_report_queries', 'time_period_report', language)
        elif any(word in query_lower for word in ['from', 'between', 'से', 'के बीच']):
            return get_snippet(snippets, 'sales_report_queries', 'custom_date_report', language)
        elif any(word in query_lower for word in ['top', 'best', 'टॉप', 'बेस्ट']):
            return get_snippet(snippets, 'sales_report_queries', 'top_products', language)
    
    elif any(word in query_lower for word in ['order', 'ऑर्डर']):
        if any(word in query_lower for word in ['today', 'आज']):
            return get_snippet(snippets, 'order_help', 'today_orders', language)
        else:
            return get_snippet(snippets, 'order_help', 'view_orders', language)
    
    elif any(word in query_lower for word in ['customer', 'client', 'ग्राहक', 'कस्टमर']):
        return get_snippet(snippets, 'order_help', 'customer_data', language)
    
    elif any(word in query_lower for word in ['help', 'support', 'मदद', 'सहायता']):
        if any(word in query_lower for word in ['human', 'person', 'talk', 'इंसान', 'व्यक्ति', 'बात']):
            return get_snippet(snippets, 'help_escalation', 'human_support', language)
        elif any(word in query_lower for word in ['bug', 'issue', 'problem', 'बग', 'समस्या']):
            return get_snippet(snippets, 'help_escalation', 'bug_report', language)
        elif any(word in query_lower for word in ['feature', 'suggestion', 'idea', 'फीचर', 'सुझाव', 'आइडिया']):
            return get_snippet(snippets, 'help_escalation', 'feature_request', language)
        else:
            return get_snippet(snippets, 'help_escalation', 'general_help', language)
    
    # If it's a new user or greeting
    elif any(word in query_lower for word in ['hi', 'hello', 'hey', 'नमस्ते', 'हैलो']):
        # Personalize the welcome message
        snippet = get_snippet(snippets, 'welcome_onboarding', 'initial_greeting', language)
        return personalize_snippet(snippet, {'[Seller Name]': seller_info['name']})
    
    # Default response if no intent is matched
    return get_snippet(snippets, 'error_responses', 'command_not_recognized', language)

# Log the query (in a real application, this would write to a database)
def log_query(seller_info, query):
    """Log the seller query for tracking purposes."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] Query from {seller_info['name']} ({seller_info['phone']}): {query}")

# Main function to demonstrate usage
def main():
    # Path to the snippets file
    snippets_file = "whatsapp_support_snippets.json"
    
    # Check if file exists in current directory, if not, use absolute path
    if not os.path.exists(snippets_file):
        snippets_file = "/Users/sanjaysuman/One Tappe/OneTappeProject/nlp/whatsapp_support_snippets.json"
    
    # Load the snippets
    snippets = load_snippets(snippets_file)
    if not snippets:
        print("Failed to load snippets. Exiting.")
        return
    
    # Example seller information
    seller_info = {
        'name': 'Sharma General Store',
        'phone': '+919876543210',
        'language_preference': 'hi',  # Default language preference
        'business_type': 'retail'
    }
    
    # Example queries and responses
    example_queries = [
        "Hello, I'm new to One Tappe",
        "How do I add a new product?",
        "मेरे प्रोडक्ट कैसे दिखाऊं?",  # How do I view my products?
        "Show me today's sales report",
        "कम स्टॉक वाले आइटम दिखाओ",  # Show low stock items
        "I found a bug in the system",
        "मुझे मदद चाहिए"  # I need help
    ]
    
    # Process each example query
    print("\n=== Example WhatsApp Support Interactions ===\n")
    for query in example_queries:
        print(f"Seller: {query}")
        response = respond_to_query(snippets, query, seller_info)
        print(f"Support: {response}\n")

# Run the example if script is executed directly
if __name__ == "__main__":
    main()