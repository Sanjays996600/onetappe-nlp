#!/usr/bin/env python3
"""
Chatbot Integration for Multilingual NLP Model

This script demonstrates how to integrate the enhanced multilingual NLP model
with a WhatsApp chatbot backend, handling messages in English, Hindi, and mixed languages.
"""

import json
import logging
import os
from datetime import datetime
from typing import Dict, Any, Optional, List, Tuple

# Import the enhanced language model
from enhanced_language_model import parse_multilingual_command, detect_mixed_language

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("chatbot.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("chatbot_integration")

# API endpoint configuration
API_BASE_URL = "https://api.onetappe.com/v1"  # Replace with actual API base URL
API_ENDPOINTS = {
    "get_inventory": "/seller/inventory",
    "get_low_stock": "/seller/inventory/low-stock",
    "get_report": "/seller/reports",
    "get_top_products": "/seller/reports/top-products",
    "get_customer_data": "/seller/customers",
    "add_product": "/seller/products/add",
    "edit_stock": "/seller/products/update-stock",
    "get_orders": "/seller/orders",
    "search_product": "/seller/products/search"
}

# Response templates for different languages
RESPONSE_TEMPLATES = {
    "en": {
        "get_inventory_success": "Here's your current inventory:\n{inventory_list}",
        "get_low_stock_success": "Products with low stock:\n{low_stock_list}",
        "get_report_success": "Here's your {time_range} report:\nTotal Sales: ₹{total_sales}\nTotal Orders: {total_orders}\nAverage Order Value: ₹{average_order_value}",
        "get_top_products_success": "Your top {limit} products for {time_range}:\n{top_products_list}",
        "get_customer_data_success": "Customer data for {time_range}:\nTotal Customers: {total_customers}\nNew Customers: {new_customers}\nRepeat Customers: {repeat_customers}",
        "add_product_success": "Product '{product_name}' added successfully with price ₹{price} and stock {stock}.",
        "edit_stock_success": "Stock for '{product_name}' updated to {stock} units.",
        "get_orders_success": "Orders for {time_range}:\n{orders_list}",
        "search_product_success": "Found {count} results for '{product_name}':\n{search_results}",
        "error_unknown_intent": "I'm not sure what you're asking for. Could you please rephrase?",
        "error_missing_entity": "I need more information to process your request. {missing_info}",
        "error_api_failure": "Sorry, I couldn't complete your request due to a technical issue. Please try again later.",
        "error_product_not_found": "Sorry, I couldn't find the product '{product_name}' in your inventory.",
        "mixed_language_detected": "I noticed you're using mixed languages. I'll respond in {primary_language}.",
        # Fallback responses
        "fallback_unknown_intent": "Sorry, I couldn't understand what you're trying to do. Could you please rephrase?",
        "fallback_missing_product_name_edit": "Please mention the product name you'd like to update.",
        "fallback_missing_product_name_search": "Please specify which product you're looking for.",
        "fallback_missing_price": "Please specify the price for the product.",
        "fallback_missing_stock": "Please specify the stock quantity.",
        "fallback_generic": "I need more information to process your request. Please provide: {missing_entities}.",
        "fallback_default": "I'm not sure what you're asking for. Could you please provide more details?"
    },
    "hi": {
        "get_inventory_success": "आपका वर्तमान इन्वेंटरी यहां है:\n{inventory_list}",
        "get_low_stock_success": "कम स्टॉक वाले प्रोडक्ट्स:\n{low_stock_list}",
        "get_report_success": "आपका {time_range} रिपोर्ट यहां है:\nकुल बिक्री: ₹{total_sales}\nकुल ऑर्डर्स: {total_orders}\nऔसत ऑर्डर मूल्य: ₹{average_order_value}",
        "get_top_products_success": "{time_range} के लिए आपके शीर्ष {limit} प्रोडक्ट्स:\n{top_products_list}",
        "get_customer_data_success": "{time_range} के लिए कस्टमर डेटा:\nकुल कस्टमर्स: {total_customers}\nनए कस्टमर्स: {new_customers}\nदोहराए गए कस्टमर्स: {repeat_customers}",
        "add_product_success": "प्रोडक्ट '{product_name}' को ₹{price} कीमत और {stock} स्टॉक के साथ सफलतापूर्वक जोड़ा गया।",
        "edit_stock_success": "'{product_name}' का स्टॉक {stock} यूनिट्स अपडेट किया गया।",
        "get_orders_success": "{time_range} के लिए ऑर्डर्स:\n{orders_list}",
        "search_product_success": "'{product_name}' के लिए {count} परिणाम मिले:\n{search_results}",
        "error_unknown_intent": "मुझे समझ नहीं आ रहा कि आप क्या पूछ रहे हैं। क्या आप कृपया दोबारा कह सकते हैं?",
        "error_missing_entity": "मुझे आपके अनुरोध को प्रोसेस करने के लिए अधिक जानकारी की आवश्यकता है। {missing_info}",
        "error_api_failure": "क्षमा करें, मैं तकनीकी समस्या के कारण आपके अनुरोध को पूरा नहीं कर सका। कृपया बाद में पुनः प्रयास करें।",
        "error_product_not_found": "क्षमा करें, मुझे आपके इन्वेंटरी में '{product_name}' प्रोडक्ट नहीं मिला।",
        "mixed_language_detected": "मैंने देखा कि आप मिश्रित भाषाओं का उपयोग कर रहे हैं। मैं {primary_language} में जवाब दूंगा।",
        # Fallback responses
        "fallback_unknown_intent": "माफ़ कीजिए, मैं आपका आदेश समझ नहीं पाया। कृपया दोबारा लिखें।",
        "fallback_missing_product_name_edit": "कृपया बताएं किस प्रोडक्ट का स्टॉक बदलना है।",
        "fallback_missing_product_name_search": "कृपया बताएं आप किस प्रोडक्ट को खोज रहे हैं।",
        "fallback_missing_price": "कृपया प्रोडक्ट का मूल्य बताएं।",
        "fallback_missing_stock": "कृपया स्टॉक की मात्रा बताएं।",
        "fallback_generic": "आपके अनुरोध को पूरा करने के लिए मुझे अधिक जानकारी चाहिए। कृपया यह बताएं: {missing_entities}।",
        "fallback_default": "मुझे समझ नहीं आ रहा कि आप क्या पूछ रहे हैं। कृपया अधिक विवरण प्रदान करें।"
    }
}

# Time range mapping for English and Hindi
TIME_RANGE_MAPPING = {
    "en": {
        "today": "today",
        "yesterday": "yesterday",
        "this-week": "this week",
        "last-week": "last week",
        "this-month": "this month",
        "last-month": "last month",
        "this-year": "this year",
        "last-year": "last year",
        "last-7-days": "last 7 days",
        "last-30-days": "last 30 days",
        "last-90-days": "last 90 days",
        "custom": "custom period"
    },
    "hi": {
        "today": "आज",
        "yesterday": "कल",
        "this-week": "इस हफ्ते",
        "last-week": "पिछले हफ्ते",
        "this-month": "इस महीने",
        "last-month": "पिछले महीने",
        "this-year": "इस साल",
        "last-year": "पिछले साल",
        "last-7-days": "पिछले 7 दिन",
        "last-30-days": "पिछले 30 दिन",
        "last-90-days": "पिछले 90 दिन",
        "custom": "कस्टम अवधि"
    }
}

class ChatbotIntegration:
    """Integration class for the multilingual NLP chatbot"""
    
    def __init__(self, api_base_url: str = API_BASE_URL):
        """Initialize the chatbot integration"""
        self.api_base_url = api_base_url
        logger.info("Chatbot integration initialized")
    
    def process_message(self, message: str, user_id: str) -> str:
        """Process incoming message and generate response"""
        logger.info(f"Processing message from user {user_id}: {message}")
        
        try:
            # Parse the command using our enhanced model
            parsed_result = parse_multilingual_command(message)
            logger.debug(f"Parsed result: {json.dumps(parsed_result, ensure_ascii=False)}")
            
            # Get raw and normalized text for fallback responses
            raw_text = parsed_result.get("raw_text") or parsed_result.get("original_text", message)
            normalized_text = parsed_result.get("normalized_text", message)
            
            # Check if intent was recognized
            if parsed_result["intent"] == "unknown":
                return self._get_fallback_response(
                    "unknown", 
                    parsed_result["language"], 
                    parsed_result["entities"],
                    raw_text,
                    normalized_text
                )
            
            # Format API parameters based on parsed result
            api_params = self._format_api_params(parsed_result)
            
            # Check if required entities are missing
            if "missing_entity" in api_params:
                # Extract missing entities from the error message
                missing_info = api_params["missing_entity"]
                missing_entities = [entity.strip() for entity in missing_info.replace("Please provide ", "").replace(".", "").split(", ")]
                
                return self._get_fallback_response(
                    parsed_result["intent"],
                    parsed_result["language"],
                    parsed_result["entities"],
                    raw_text,
                    normalized_text,
                    missing_entities
                )
            
            # Call API with parameters
            api_response = self._call_api(parsed_result["intent"], api_params)
            
            # Format user response based on API response
            user_response = self._format_user_response(parsed_result, api_response)
            
            # Add mixed language notification if needed
            if parsed_result["is_mixed_language"]:
                primary_lang = "English" if parsed_result["language"] == "en" else "हिंदी"
                mixed_lang_notice = self._get_template(
                    "mixed_language_detected", 
                    parsed_result["language"],
                    {"primary_language": primary_lang}
                )
                user_response = f"{mixed_lang_notice}\n\n{user_response}"
            
            return user_response
            
        except Exception as e:
            logger.error(f"Error processing message: {str(e)}", exc_info=True)
            # Default to English for error messages if language detection fails
            return self._format_error_response("error_api_failure", "en")
    
    def _format_api_params(self, parsed_result: Dict[str, Any]) -> Dict[str, Any]:
        """Format API parameters based on parsed intent and entities"""
        intent = parsed_result["intent"]
        entities = parsed_result["entities"]
        params = {}
        
        if intent == "get_inventory":
            # No additional parameters needed
            pass
            
        elif intent == "get_low_stock":
            # Extract threshold if available
            if "threshold" in entities:
                params["threshold"] = entities["threshold"]
            else:
                # Default threshold
                params["threshold"] = 10
                
        elif intent == "get_report":
            # Extract time range
            if "time_range" in entities:
                params["time_range"] = entities["time_range"]
                
                # Add start_date and end_date if custom range
                if entities["time_range"] == "custom" and "start_date" in entities and "end_date" in entities:
                    params["start_date"] = entities["start_date"]
                    params["end_date"] = entities["end_date"]
            else:
                # Default to today if no time range specified
                params["time_range"] = "today"
                
        elif intent == "get_top_products":
            # Extract time range and limit
            if "time_range" in entities:
                params["time_range"] = entities["time_range"]
            else:
                params["time_range"] = "this-month"
                
            if "limit" in entities:
                params["limit"] = entities["limit"]
            else:
                params["limit"] = 5
                
        elif intent == "get_customer_data":
            # Extract time range
            if "time_range" in entities:
                params["time_range"] = entities["time_range"]
            else:
                params["time_range"] = "this-month"
                
        elif intent == "add_product":
            # Check for required entities
            required_entities = ["product_name", "price", "stock"]
            missing = [entity for entity in required_entities if entity not in entities]
            
            if missing:
                missing_str = ", ".join(missing)
                params["missing_entity"] = f"Please provide {missing_str}."
                return params
            
            params["product_name"] = entities["product_name"]
            params["price"] = entities["price"]
            params["stock"] = entities["stock"]
            
        elif intent == "edit_stock":
            # Check for required entities
            required_entities = ["product_name", "stock"]
            missing = [entity for entity in required_entities if entity not in entities]
            
            if missing:
                missing_str = ", ".join(missing)
                params["missing_entity"] = f"Please provide {missing_str}."
                return params
            
            params["product_name"] = entities["product_name"]
            params["stock"] = entities["stock"]
            
        elif intent == "get_orders":
            # Extract time range
            if "time_range" in entities:
                params["time_range"] = entities["time_range"]
                
                # Add start_date and end_date if custom range
                if entities["time_range"] == "custom" and "start_date" in entities and "end_date" in entities:
                    params["start_date"] = entities["start_date"]
                    params["end_date"] = entities["end_date"]
            else:
                # Default to all if no time range specified
                params["time_range"] = "all"
                
        elif intent == "search_product":
            # Check for required entities
            if "product_name" not in entities:
                params["missing_entity"] = "Please provide a product name to search for."
                return params
            
            params["query"] = entities["product_name"]
        
        return params
    
    def _call_api(self, intent: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Call the appropriate API endpoint based on intent and parameters"""
        # In a real implementation, this would make HTTP requests to the actual API
        # For this example, we'll simulate API responses
        
        logger.info(f"Calling API for intent: {intent} with params: {params}")
        
        # Simulate API call
        if intent == "get_inventory":
            return self._mock_get_inventory()
            
        elif intent == "get_low_stock":
            return self._mock_get_low_stock(params.get("threshold", 10))
            
        elif intent == "get_report":
            return self._mock_get_report(
                params.get("time_range", "today"),
                params.get("start_date"),
                params.get("end_date")
            )
            
        elif intent == "get_top_products":
            return self._mock_get_top_products(
                params.get("time_range", "this-month"),
                params.get("limit", 5)
            )
            
        elif intent == "get_customer_data":
            return self._mock_get_customer_data(params.get("time_range", "this-month"))
            
        elif intent == "add_product":
            return self._mock_add_product(
                params.get("product_name", ""),
                params.get("price", 0),
                params.get("stock", 0)
            )
            
        elif intent == "edit_stock":
            return self._mock_edit_stock(
                params.get("product_name", ""),
                params.get("stock", 0)
            )
            
        elif intent == "get_orders":
            return self._mock_get_orders(params.get("time_range", "all"))
            
        elif intent == "search_product":
            return self._mock_search_product(params.get("query", ""))
            
        else:
            return {"error": "Unknown intent"}
    
    def _format_user_response(self, parsed_result: Dict[str, Any], api_response: Dict[str, Any]) -> str:
        """Format user response based on API response and language"""
        intent = parsed_result["intent"]
        language = parsed_result["language"]
        entities = parsed_result["entities"]
        raw_text = parsed_result.get("raw_text") or parsed_result.get("original_text")
        normalized_text = parsed_result.get("normalized_text")
        
        # Check for unknown intent or missing required entities
        if intent == "unknown":
            logger.info(f"Unknown intent detected for text: {raw_text}")
            return self._get_fallback_response(intent, language, entities, raw_text, normalized_text)
        
        # Check for missing required entities based on intent
        missing_entities = self._check_missing_required_entities(intent, entities)
        if missing_entities:
            logger.info(f"Missing required entities for intent {intent}: {missing_entities}")
            return self._get_fallback_response(intent, language, entities, raw_text, normalized_text, missing_entities)
        
        # Check for API error
        if "error" in api_response:
            if api_response["error"] == "product_not_found":
                return self._format_error_response(
                    "error_product_not_found", 
                    language,
                    {"product_name": entities.get("product_name", "")}
                )
            else:
                return self._format_error_response("error_api_failure", language)
        
        # Format success response based on intent
        template_key = f"{intent}_success"
        
        if intent == "get_inventory":
            inventory_list = self._format_inventory_list(api_response["inventory"], language)
            return self._get_template(template_key, language, {"inventory_list": inventory_list})
            
        elif intent == "get_low_stock":
            low_stock_list = self._format_inventory_list(api_response["low_stock"], language)
            return self._get_template(template_key, language, {"low_stock_list": low_stock_list})
            
        elif intent == "get_report":
            time_range = self._format_time_range(entities.get("time_range", "today"), language)
            return self._get_template(template_key, language, {
                "time_range": time_range,
                "total_sales": api_response["total_sales"],
                "total_orders": api_response["total_orders"],
                "average_order_value": api_response["average_order_value"]
            })
            
        elif intent == "get_top_products":
            time_range = self._format_time_range(entities.get("time_range", "this-month"), language)
            limit = entities.get("limit", 5)
            top_products_list = self._format_top_products_list(api_response["top_products"], language)
            return self._get_template(template_key, language, {
                "time_range": time_range,
                "limit": limit,
                "top_products_list": top_products_list
            })
            
        elif intent == "get_customer_data":
            time_range = self._format_time_range(entities.get("time_range", "this-month"), language)
            return self._get_template(template_key, language, {
                "time_range": time_range,
                "total_customers": api_response["total_customers"],
                "new_customers": api_response["new_customers"],
                "repeat_customers": api_response["repeat_customers"]
            })
            
        elif intent == "add_product":
            return self._get_template(template_key, language, {
                "product_name": api_response["product_name"],
                "price": api_response["price"],
                "stock": api_response["stock"]
            })
            
        elif intent == "edit_stock":
            return self._get_template(template_key, language, {
                "product_name": api_response["product_name"],
                "stock": api_response["stock"]
            })
            
        elif intent == "get_orders":
            time_range = self._format_time_range(entities.get("time_range", "all"), language)
            orders_list = self._format_orders_list(api_response["orders"], language)
            return self._get_template(template_key, language, {
                "time_range": time_range,
                "orders_list": orders_list
            })
            
        elif intent == "search_product":
            search_results = self._format_search_results(api_response["results"], language)
            return self._get_template(template_key, language, {
                "product_name": entities.get("product_name", ""),
                "count": len(api_response["results"]),
                "search_results": search_results
            })
            
        else:
            return self._format_error_response("error_unknown_intent", language)
    
    def _get_template(self, template_key: str, language: str, params: Dict[str, Any] = None) -> str:
        """Get response template and format with parameters"""
        if language not in RESPONSE_TEMPLATES:
            language = "en"  # Default to English if language not supported
        
        if template_key not in RESPONSE_TEMPLATES[language]:
            template_key = "error_unknown_intent"  # Default to unknown intent error
        
        template = RESPONSE_TEMPLATES[language][template_key]
        
        if params:
            return template.format(**params)
        else:
            return template
    
    def _format_error_response(self, error_key: str, language: str, params: Dict[str, Any] = None) -> str:
        """Format error response based on error key and language"""
        return self._get_template(error_key, language, params)
    
    def _format_time_range(self, time_range_key: str, language: str) -> str:
        """Format time range for display in responses"""
        if language not in TIME_RANGE_MAPPING:
            language = "en"  # Default to English if language not supported
        
        if time_range_key not in TIME_RANGE_MAPPING[language]:
            time_range_key = "today"  # Default to today if time range not recognized
        
        return TIME_RANGE_MAPPING[language][time_range_key]
    
    def _format_inventory_list(self, inventory: List[Dict[str, Any]], language: str) -> str:
        """Format inventory list for display in responses"""
        if not inventory:
            return "No items found." if language == "en" else "कोई आइटम नहीं मिला।"
        
        formatted_list = ""
        for item in inventory:
            if language == "en":
                formatted_list += f"- {item['name']}: {item['stock']} units at ₹{item['price']} each\n"
            else:  # Hindi
                formatted_list += f"- {item['name']}: {item['stock']} यूनिट्स, ₹{item['price']} प्रति यूनिट\n"
        
        return formatted_list
    
    def _format_top_products_list(self, products: List[Dict[str, Any]], language: str) -> str:
        """Format top products list for display in responses"""
        if not products:
            return "No products found." if language == "en" else "कोई प्रोडक्ट नहीं मिला।"
        
        formatted_list = ""
        for i, product in enumerate(products, 1):
            if language == "en":
                formatted_list += f"{i}. {product['name']}: {product['quantity']} units sold, ₹{product['revenue']} revenue\n"
            else:  # Hindi
                formatted_list += f"{i}. {product['name']}: {product['quantity']} यूनिट्स बिके, ₹{product['revenue']} राजस्व\n"
        
        return formatted_list
    
    def _format_orders_list(self, orders: List[Dict[str, Any]], language: str) -> str:
        """Format orders list for display in responses"""
        if not orders:
            return "No orders found." if language == "en" else "कोई ऑर्डर नहीं मिला।"
        
        formatted_list = ""
        for order in orders:
            date = order["date"]
            items = order["items"]
            total = order["total"]
            
            if language == "en":
                formatted_list += f"- Order #{order['id']} ({date}): {items} items, ₹{total}\n"
            else:  # Hindi
                formatted_list += f"- ऑर्डर #{order['id']} ({date}): {items} आइटम्स, ₹{total}\n"
        
        return formatted_list
    
    def _format_search_results(self, results: List[Dict[str, Any]], language: str) -> str:
        """Format search results for display in responses"""
        if not results:
            return "No products found." if language == "en" else "कोई प्रोडक्ट नहीं मिला।"
        
        formatted_list = ""
        for i, result in enumerate(results, 1):
            if language == "en":
                formatted_list += f"{i}. {result['name']}: {result['stock']} units at ₹{result['price']} each\n"
            else:  # Hindi
                formatted_list += f"{i}. {result['name']}: {result['stock']} यूनिट्स, ₹{result['price']} प्रति यूनिट\n"
        
        return formatted_list
    
    def _check_missing_required_entities(self, intent: str, entities: Dict[str, Any]) -> List[str]:
        """Check for missing required entities based on intent"""
        required_entities = []
        
        if intent == "add_product":
            required_entities = ["product_name", "price", "stock"]
        elif intent == "edit_stock":
            required_entities = ["product_name", "stock"]
        elif intent == "search_product":
            required_entities = ["product_name"]
        
        # Return list of missing required entities
        return [entity for entity in required_entities if entity not in entities]
    
    def _get_fallback_response(self, intent: str, language: str, entities: Dict[str, Any], 
                             raw_text: str, normalized_text: str, missing_entities: List[str] = None) -> str:
        """Generate appropriate fallback message based on intent, language, and missing entities"""
        # Default to English if language not supported
        if language not in RESPONSE_TEMPLATES:
            language = "en"
            
        # Log the fallback scenario
        logger.info(f"Generating fallback response for intent: {intent}, language: {language}, "
                   f"missing_entities: {missing_entities}, raw_text: {raw_text}")
        
        # Fallback responses for unknown intent
        if intent == "unknown":
            return self._get_template("fallback_unknown_intent", language)
        
        # Fallback responses for missing entities
        if missing_entities:
            if "product_name" in missing_entities:
                if intent == "edit_stock":
                    return self._get_template("fallback_missing_product_name_edit", language)
                elif intent == "search_product":
                    return self._get_template("fallback_missing_product_name_search", language)
            
            if "price" in missing_entities and len(missing_entities) == 1:
                return self._get_template("fallback_missing_price", language)
            
            if "stock" in missing_entities and len(missing_entities) == 1:
                return self._get_template("fallback_missing_stock", language)
            
            # Generic fallback for other missing entities
            missing_str = ", ".join(missing_entities)
            return self._get_template("fallback_generic", language, {"missing_entities": missing_str})
        
        # Default fallback response
        return self._get_template("fallback_default", language)
    
    # Mock API response methods for testing
    def _mock_get_inventory(self) -> Dict[str, Any]:
        return {
            "inventory": [
                {"name": "Rice", "stock": 50, "price": 60},
                {"name": "Wheat", "stock": 30, "price": 40},
                {"name": "Sugar", "stock": 25, "price": 50},
                {"name": "Salt", "stock": 45, "price": 20},
                {"name": "Oil", "stock": 15, "price": 120}
            ]
        }
    
    def _mock_get_low_stock(self, threshold: int) -> Dict[str, Any]:
        return {
            "low_stock": [
                {"name": "Oil", "stock": 15, "price": 120},
                {"name": "Sugar", "stock": 25, "price": 50}
            ] if threshold > 20 else [
                {"name": "Oil", "stock": 15, "price": 120}
            ]
        }
    
    def _mock_get_report(self, time_range: str, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        # Different values based on time range
        if time_range == "today":
            return {"total_sales": 5000, "total_orders": 10, "average_order_value": 500}
        elif time_range == "this-week":
            return {"total_sales": 25000, "total_orders": 45, "average_order_value": 555}
        elif time_range == "this-month":
            return {"total_sales": 120000, "total_orders": 200, "average_order_value": 600}
        else:
            return {"total_sales": 50000, "total_orders": 100, "average_order_value": 500}
    
    def _mock_get_top_products(self, time_range: str, limit: int) -> Dict[str, Any]:
        products = [
            {"name": "Rice", "quantity": 100, "revenue": 6000},
            {"name": "Oil", "quantity": 50, "revenue": 6000},
            {"name": "Wheat", "quantity": 80, "revenue": 3200},
            {"name": "Sugar", "quantity": 60, "revenue": 3000},
            {"name": "Salt", "quantity": 120, "revenue": 2400}
        ]
        
        return {"top_products": products[:limit]}
    
    def _mock_get_customer_data(self, time_range: str) -> Dict[str, Any]:
        # Different values based on time range
        if time_range == "today":
            return {"total_customers": 8, "new_customers": 3, "repeat_customers": 5}
        elif time_range == "this-week":
            return {"total_customers": 35, "new_customers": 12, "repeat_customers": 23}
        elif time_range == "this-month":
            return {"total_customers": 150, "new_customers": 45, "repeat_customers": 105}
        else:
            return {"total_customers": 80, "new_customers": 30, "repeat_customers": 50}
    
    def _mock_add_product(self, product_name: str, price: float, stock: int) -> Dict[str, Any]:
        if not product_name:
            return {"error": "missing_product_name"}
        
        return {"product_name": product_name, "price": price, "stock": stock}
    
    def _mock_edit_stock(self, product_name: str, stock: int) -> Dict[str, Any]:
        if not product_name:
            return {"error": "missing_product_name"}
        
        # Check if product exists (mock check)
        if product_name.lower() not in ["rice", "wheat", "sugar", "salt", "oil", "चावल", "गेहूं", "चीनी", "नमक", "तेल"]:
            return {"error": "product_not_found"}
        
        return {"product_name": product_name, "stock": stock}
    
    def _mock_get_orders(self, time_range: str) -> Dict[str, Any]:
        orders = [
            {"id": "ORD001", "date": "2023-06-15", "items": 3, "total": 500},
            {"id": "ORD002", "date": "2023-06-14", "items": 2, "total": 300},
            {"id": "ORD003", "date": "2023-06-13", "items": 5, "total": 800},
            {"id": "ORD004", "date": "2023-06-10", "items": 1, "total": 200},
            {"id": "ORD005", "date": "2023-06-05", "items": 4, "total": 600}
        ]
        
        # Filter orders based on time range
        if time_range == "today":
            filtered_orders = [orders[0]]
        elif time_range == "this-week":
            filtered_orders = orders[:3]
        elif time_range == "this-month":
            filtered_orders = orders
        else:
            filtered_orders = orders
        
        return {"orders": filtered_orders}
    
    def _mock_search_product(self, query: str) -> Dict[str, Any]:
        if not query:
            return {"results": []}
        
        # Mock search results based on query
        all_products = [
            {"name": "Rice", "stock": 50, "price": 60},
            {"name": "Basmati Rice", "stock": 30, "price": 120},
            {"name": "Brown Rice", "stock": 20, "price": 80},
            {"name": "Wheat", "stock": 30, "price": 40},
            {"name": "Wheat Flour", "stock": 25, "price": 45},
            {"name": "Sugar", "stock": 25, "price": 50},
            {"name": "Brown Sugar", "stock": 15, "price": 70},
            {"name": "Salt", "stock": 45, "price": 20},
            {"name": "Rock Salt", "stock": 20, "price": 30},
            {"name": "Oil", "stock": 15, "price": 120},
            {"name": "Olive Oil", "stock": 10, "price": 250},
            {"name": "Mustard Oil", "stock": 12, "price": 180}
        ]
        
        # Simple search implementation
        query_lower = query.lower()
        results = [p for p in all_products if query_lower in p["name"].lower()]
        
        return {"results": results}

# Example usage
def main():
    # Initialize chatbot integration
    chatbot = ChatbotIntegration()
    
    # Test with English commands
    english_commands = [
        "Show me my inventory",
        "Update rice stock to 50",
        "Show me low stock items below 20",
        "Generate a report for this month",
        "Search for oil"
    ]
    
    print("\nTesting English commands:")
    for command in english_commands:
        print(f"\nCommand: {command}")
        response = chatbot.process_message(command, "user123")
        print(f"Response:\n{response}")
    
    # Test with Hindi commands
    hindi_commands = [
        "मेरा इन्वेंटरी दिखाओ",
        "चावल का स्टॉक 50 अपडेट करो",
        "20 से कम स्टॉक वाले आइटम दिखाओ",
        "इस महीने का रिपोर्ट जनरेट करो",
        "तेल के लिए सर्च करो"
    ]
    
    print("\nTesting Hindi commands:")
    for command in hindi_commands:
        print(f"\nCommand: {command}")
        response = chatbot.process_message(command, "user123")
        print(f"Response:\n{response}")
    
    # Test with mixed language commands
    mixed_commands = [
        "Show me चावल inventory",
        "Update चावल stock to 50",
        "Show me low stock items below 20 यूनिट्स",
        "Generate a report for इस महीने",
        "Search for तेल"
    ]
    
    print("\nTesting mixed language commands:")
    for command in mixed_commands:
        print(f"\nCommand: {command}")
        response = chatbot.process_message(command, "user123")
        print(f"Response:\n{response}")

if __name__ == "__main__":
    main()