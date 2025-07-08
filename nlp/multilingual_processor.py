import re
import string
import spacy
import numpy as np
from typing import Dict, List, Tuple, Any, Optional, Union
from datetime import datetime, timedelta
import pytz
import langdetect
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException

# Import existing modules if available
try:
    from OneTappeProject.nlp.mixed_entity_extraction import parse_mixed_date, extract_mixed_date_range
except ImportError:
    # Fallback implementations if modules are not available
    def parse_mixed_date(date_str):
        """Fallback implementation for parse_mixed_date"""
        return None
    
    def extract_mixed_date_range(command):
        """Fallback implementation for extract_mixed_date_range"""
        return {}

# Load language models
try:
    nlp_en = spacy.load("en_core_web_sm")
except OSError:
    print("English model not found. Installing...")
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
    nlp_en = spacy.load("en_core_web_sm")

# For Hindi, we'll use a multilingual model if available
try:
    nlp_hi = spacy.load("xx_ent_wiki_sm")
except OSError:
    try:
        # Try to download the model
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "xx_ent_wiki_sm"])
        nlp_hi = spacy.load("xx_ent_wiki_sm")
    except:
        # Fallback to English model if Hindi model is not available
        print("Hindi model not available. Using English model as fallback.")
        nlp_hi = nlp_en

# Define Hindi stopwords
HINDI_STOPWORDS = {
    'का', 'के', 'की', 'है', 'में', 'से', 'को', 'पर', 'इस', 'और', 'यह', 'वह',
    'एक', 'हैं', 'कि', 'जो', 'ने', 'हो', 'था', 'थे', 'थी', 'तो', 'ही', 'भी',
    'नहीं', 'कर', 'हम', 'तुम', 'वे', 'जब', 'अब', 'या', 'फिर', 'हुआ', 'किया',
    'गया', 'करना', 'होना', 'लिए', 'साथ', 'बाद', 'मैं', 'उस', 'यहां', 'वहां',
    'दिखाओ', 'बताओ', 'कितना', 'कितने', 'क्या', 'कौन', 'कब', 'कहां', 'क्यों',
    'कैसे', 'अपना', 'अपने', 'अपनी', 'उनका', 'उनके', 'उनकी', 'इनका', 'इनके', 'इनकी'
}

# Define Hindi month names and their English equivalents
HINDI_MONTH_MAPPING = {
    'जनवरी': 'January',
    'फरवरी': 'February',
    'मार्च': 'March',
    'अप्रैल': 'April',
    'मई': 'May',
    'जून': 'June',
    'जुलाई': 'July',
    'अगस्त': 'August',
    'सितंबर': 'September',
    'अक्टूबर': 'October',
    'नवंबर': 'November',
    'दिसंबर': 'December',
    # Transliterated versions
    'janvari': 'January',
    'farvari': 'February',
    'march': 'March',  # Same in English
    'april': 'April',  # Same in English
    'mai': 'May',
    'june': 'June',    # Same in English
    'july': 'July',    # Same in English
    'august': 'August',  # Same in English
    'september': 'September',  # Same in English
    'october': 'October',  # Same in English
    'november': 'November',  # Same in English
    'december': 'December',  # Same in English
}

# Define Hindi time period mappings
HINDI_TIME_PERIOD_MAPPING = {
    'आज': 'today',
    'कल': 'yesterday',  # Assuming 'कल' refers to yesterday in this context
    'इस हफ्ते': 'this-week',
    'इस महीने': 'this-month',
    'पिछले 7 दिन': 'last_7_days',
    'पिछले हफ्ते': 'last-week',
    'पिछले महीने': 'last-month',
    'सभी': 'all',
    # Transliterated versions
    'aaj': 'today',
    'kal': 'yesterday',
    'is hafte': 'this-week',
    'is mahine': 'this-month',
    'pichhle 7 din': 'last_7_days',
    'pichhle hafte': 'last-week',
    'pichhle mahine': 'last-month',
    'sabhi': 'all',
}

# Define intent patterns for both English and Hindi
INTENT_PATTERNS = {
    'get_inventory': {
        'en': [
            r'(?i)(?:show|get|display|view)\s+(?:inventory|stock)',
            r'(?i)(?:what|how much)\s+(?:inventory|stock)\s+(?:do\s+we\s+have|is\s+available)',
            r'(?i)current\s+inventory',
        ],
        'hi': [
            r'(?:इन्वेंटरी|स्टॉक)\s+(?:दिखाओ|बताओ)',
            r'(?:कितना|क्या)\s+(?:इन्वेंटरी|स्टॉक)\s+(?:है|उपलब्ध है)',
            r'वर्तमान\s+(?:इन्वेंटरी|स्टॉक)',
            # Transliterated versions
            r'(?i)(?:inventory|stock)\s+(?:dikhao|batao)',
            r'(?i)(?:kitna|kya)\s+(?:inventory|stock)\s+(?:hai|available hai)',
        ],
    },
    'get_low_stock': {
        'en': [
            r'(?i)(?:show|get|display|view)\s+(?:low|limited)\s+(?:inventory|stock)',
            r'(?i)(?:what|which)\s+(?:products|items)\s+(?:are|is)\s+(?:low|limited)\s+(?:in\s+stock|in\s+inventory)',
            r'(?i)low\s+stock\s+(?:report|alert|items|products)',
        ],
        'hi': [
            r'(?:कम|सीमित)\s+(?:इन्वेंटरी|स्टॉक)\s+(?:दिखाओ|बताओ)',
            r'(?:कौन|क्या)\s+(?:प्रोडक्ट्स|आइटम्स)\s+(?:कम|सीमित)\s+(?:स्टॉक|इन्वेंटरी)\s+में\s+(?:हैं|है)',
            r'(?:कम|लो)\s+स्टॉक\s+(?:रिपोर्ट|अलर्ट|आइटम्स|प्रोडक्ट्स)',
            # Transliterated versions
            r'(?i)(?:kam|limited)\s+(?:inventory|stock)\s+(?:dikhao|batao)',
            r'(?i)(?:kaun|kya)\s+(?:products|items)\s+(?:kam|limited)\s+(?:stock|inventory)\s+mein\s+(?:hain|hai)',
            r'(?i)(?:kam|low)\s+stock\s+(?:report|alert|items|products)',
        ],
    },
    'edit_stock': {
        'en': [
            r'(?i)(?:update|change|modify|edit|set)\s+(?:inventory|stock)',
            r'(?i)(?:add|remove|increase|decrease)\s+(?:\d+|some|few|many)\s+(?:items|products|units)',
            r'(?i)(?:add|remove|increase|decrease)\s+(?:inventory|stock)',
        ],
        'hi': [
            r'(?:इन्वेंटरी|स्टॉक)\s+(?:अपडेट|बदलो|संशोधित करो|एडिट करो|सेट करो)',
            r'(\d+|कुछ|थोड़े|ज्यादा)\s+(?:आइटम्स|प्रोडक्ट्स|यूनिट्स)\s+(?:जोड़ो|हटाओ|बढ़ाओ|घटाओ)',
            r'(?:इन्वेंटरी|स्टॉक)\s+(?:जोड़ो|हटाओ|बढ़ाओ|घटाओ)',
            # Transliterated versions
            r'(?i)(?:inventory|stock)\s+(?:update|badlo|edit karo|set karo)',
            r'(?i)(\d+|kuch|thode|jyada)\s+(?:items|products|units)\s+(?:jodo|hatao|badhao|ghatao)',
            r'(?i)(?:inventory|stock)\s+(?:jodo|hatao|badhao|ghatao)',
        ],
    },
    'search_product': {
        'en': [
            r'(?i)(?:search|find|look\s+for)\s+(?:product|item)',
            r'(?i)(?:show|get|display|view)\s+(?:product|item)',
            r'(?i)(?:details|info|information)\s+(?:of|about|for)\s+(?:product|item)',
        ],
        'hi': [
            r'(?:प्रोडक्ट|आइटम)\s+(?:खोजो|ढूंढो|सर्च करो)',
            r'(?:प्रोडक्ट|आइटम)\s+(?:दिखाओ|बताओ)',
            r'(?:प्रोडक्ट|आइटम)\s+(?:के|की|का)\s+(?:विवरण|जानकारी|डिटेल्स)',
            # Transliterated versions
            r'(?i)(?:product|item)\s+(?:khojo|dhundho|search karo)',
            r'(?i)(?:product|item)\s+(?:dikhao|batao)',
            r'(?i)(?:product|item)\s+(?:ke|ki|ka)\s+(?:vivaran|jankari|details)',
        ],
    },
    'get_orders': {
        'en': [
            r'(?i)(?:show|get|display|view)\s+(?:orders|sales)',
            r'(?i)(?:recent|today|yesterday|this\s+week|this\s+month|last\s+\d+\s+days)\s+(?:orders|sales)',
            r'(?i)(?:orders|sales)\s+(?:report|summary|data)',
        ],
        'hi': [
            r'(?:ऑर्डर्स|सेल्स|बिक्री)\s+(?:दिखाओ|बताओ)',
            r'(?:हाल के|आज के|कल के|इस हफ्ते के|इस महीने के|पिछले \d+ दिनों के)\s+(?:ऑर्डर्स|सेल्स|बिक्री)',
            r'(?:ऑर्डर्स|सेल्स|बिक्री)\s+(?:रिपोर्ट|सारांश|डेटा)',
            # Transliterated versions
            r'(?i)(?:orders|sales|bikri)\s+(?:dikhao|batao)',
            r'(?i)(?:hal ke|aaj ke|kal ke|is hafte ke|is mahine ke|pichhle \d+ dino ke)\s+(?:orders|sales|bikri)',
            r'(?i)(?:orders|sales|bikri)\s+(?:report|summary|data)',
        ],
    },
    'get_report': {
        'en': [
            r'(?i)(?:show|get|display|view|generate)\s+(?:report)',
            r'(?i)(?:sales|revenue|profit|performance)\s+(?:report|summary|analysis)',
            r'(?i)(?:recent|today|yesterday|this\s+week|this\s+month|last\s+\d+\s+days)\s+(?:report)',
        ],
        'hi': [
            r'(?:रिपोर्ट)\s+(?:दिखाओ|बताओ|जनरेट करो)',
            r'(?:सेल्स|रेवेन्यू|प्रॉफिट|परफॉरमेंस)\s+(?:रिपोर्ट|सारांश|विश्लेषण)',
            r'(?:हाल के|आज के|कल के|इस हफ्ते के|इस महीने के|पिछले \d+ दिनों के)\s+(?:रिपोर्ट)',
            # Transliterated versions
            r'(?i)(?:report)\s+(?:dikhao|batao|generate karo)',
            r'(?i)(?:sales|revenue|profit|performance)\s+(?:report|summary|analysis)',
            r'(?i)(?:hal ke|aaj ke|kal ke|is hafte ke|is mahine ke|pichhle \d+ dino ke)\s+(?:report)',
        ],
    },
}


class MultilingualProcessor:
    """A class for processing multilingual commands in English and Hindi."""
    
    def __init__(self):
        """Initialize the multilingual processor."""
        self.nlp_en = nlp_en
        self.nlp_hi = nlp_hi
        self.intent_patterns = INTENT_PATTERNS
        self.hindi_month_mapping = HINDI_MONTH_MAPPING
        self.hindi_time_period_mapping = HINDI_TIME_PERIOD_MAPPING
        
        # Configure langdetect to be deterministic
        langdetect.DetectorFactory.seed = 0
    
    def detect_language(self, text: str) -> str:
        """Detect the language of the input text.
        
        Args:
            text: The input text to detect language for.
            
        Returns:
            str: The detected language code ('en' for English, 'hi' for Hindi, 'mixed' for mixed language).
        """
        if not text or text.strip() == "":
            return "en"  # Default to English for empty text
        
        # Check for mixed language by looking for Hindi characters
        hindi_chars = re.findall(r'[\u0900-\u097F]', text)
        english_words = re.findall(r'\b[a-zA-Z]+\b', text)
        
        if hindi_chars and english_words:
            return "mixed"
        
        try:
            detected = detect(text)
            if detected == "hi":
                return "hi"
            else:
                # Default to English for other languages or if detection is uncertain
                return "en"
        except LangDetectException:
            # If detection fails, check for Hindi characters
            if hindi_chars:
                return "hi"
            else:
                return "en"  # Default to English
    
    def normalize_mixed_command(self, command: str) -> str:
        """Normalize mixed language commands, especially Romanized Hindi.
        
        Args:
            command: The input command to normalize.
            
        Returns:
            str: The normalized command.
        """
        # Convert common Romanized Hindi words to standard forms
        command = re.sub(r'\bdikhao\b', 'show', command, flags=re.IGNORECASE)
        command = re.sub(r'\bbatao\b', 'tell', command, flags=re.IGNORECASE)
        command = re.sub(r'\bkitna\b', 'how much', command, flags=re.IGNORECASE)
        command = re.sub(r'\bkitne\b', 'how many', command, flags=re.IGNORECASE)
        
        # Normalize month names
        for hindi_month, english_month in self.hindi_month_mapping.items():
            command = re.sub(r'\b' + hindi_month + r'\b', english_month, command, flags=re.IGNORECASE)
        
        # Normalize time periods
        for hindi_period, english_period in self.hindi_time_period_mapping.items():
            command = re.sub(r'\b' + hindi_period + r'\b', english_period, command, flags=re.IGNORECASE)
        
        return command
    
    def identify_intent(self, command: str) -> Tuple[str, str]:
        """Identify the intent of the command.
        
        Args:
            command: The input command to identify intent for.
            
        Returns:
            Tuple[str, str]: A tuple containing the identified intent and language.
        """
        # Detect language
        language = self.detect_language(command)
        
        # For mixed language, try to normalize
        if language == "mixed":
            normalized_command = self.normalize_mixed_command(command)
            # Try both English and Hindi patterns
            languages_to_try = ["en", "hi"]
        else:
            normalized_command = command
            languages_to_try = [language]
        
        # Check against patterns for the detected language(s)
        for lang in languages_to_try:
            for intent, patterns in self.intent_patterns.items():
                if lang in patterns:
                    for pattern in patterns[lang]:
                        if re.search(pattern, normalized_command):
                            return intent, language
        
        # If no intent is found, return a default
        return "unknown", language
    
    def extract_entities(self, command: str, intent: str, language: str) -> Dict[str, Any]:
        """Extract entities from the command based on intent and language.
        
        Args:
            command: The input command to extract entities from.
            intent: The identified intent of the command.
            language: The detected language of the command.
            
        Returns:
            Dict[str, Any]: A dictionary of extracted entities.
        """
        entities = {}
        
        # For mixed language, try specialized extraction first
        if language == "mixed" or language == "hi":
            # For time-based intents, extract date ranges
            if intent in ["get_orders", "get_report"]:
                date_range = extract_mixed_date_range(command)
                if date_range:
                    entities.update(date_range)
            
            # For product-related intents, extract product details
            if intent in ["edit_stock", "search_product"]:
                # Extract product details using regex patterns
                product_match = re.search(r'(?:product|प्रोडक्ट|item|आइटम)\s+([\w\s]+)', command, re.IGNORECASE)
                if product_match:
                    entities["product_name"] = product_match.group(1).strip()
                
                # Extract quantity for edit_stock
                if intent == "edit_stock":
                    quantity_match = re.search(r'(\d+)\s+(?:items|आइटम्स|units|यूनिट्स)', command, re.IGNORECASE)
                    if quantity_match:
                        entities["quantity"] = int(quantity_match.group(1))
                    
                    # Extract operation type (add/remove)
                    if re.search(r'(?:add|जोड़ो|jodo|increase|बढ़ाओ|badhao)', command, re.IGNORECASE):
                        entities["operation"] = "add"
                    elif re.search(r'(?:remove|हटाओ|hatao|decrease|घटाओ|ghatao)', command, re.IGNORECASE):
                        entities["operation"] = "remove"
        
        # If mixed extraction didn't yield results or for English, use language-specific extraction
        if not entities or language == "en":
            # Use spaCy for entity extraction
            nlp = self.nlp_en if language == "en" else self.nlp_hi
            doc = nlp(command)
            
            # Extract based on intent
            if intent == "search_product":
                # Look for product names (PRODUCT, ORG, or PERSON entities might be product names)
                for ent in doc.ents:
                    if ent.label_ in ["PRODUCT", "ORG", "PERSON"]:
                        entities["product_name"] = ent.text
                        break
                
                # If no entity found, try noun chunks
                if "product_name" not in entities:
                    for chunk in doc.noun_chunks:
                        # Skip chunks that are likely not product names
                        if chunk.text.lower() not in ["product", "item", "details", "information"]:
                            entities["product_name"] = chunk.text
                            break
            
            elif intent == "edit_stock":
                # Extract quantity
                for token in doc:
                    if token.pos_ == "NUM":
                        entities["quantity"] = int(token.text)
                        break
                
                # Extract product name
                for ent in doc.ents:
                    if ent.label_ in ["PRODUCT", "ORG", "PERSON"]:
                        entities["product_name"] = ent.text
                        break
                
                # If no entity found, try noun chunks
                if "product_name" not in entities:
                    for chunk in doc.noun_chunks:
                        # Skip chunks that are likely not product names
                        if chunk.text.lower() not in ["inventory", "stock", "items", "products", "units"]:
                            entities["product_name"] = chunk.text
                            break
                
                # Extract operation type
                if re.search(r'(?:add|increase)', command, re.IGNORECASE):
                    entities["operation"] = "add"
                elif re.search(r'(?:remove|decrease)', command, re.IGNORECASE):
                    entities["operation"] = "remove"
            
            elif intent in ["get_orders", "get_report"]:
                # Extract date range
                if re.search(r'today', command, re.IGNORECASE):
                    entities["period"] = "today"
                elif re.search(r'yesterday', command, re.IGNORECASE):
                    entities["period"] = "yesterday"
                elif re.search(r'this\s+week', command, re.IGNORECASE):
                    entities["period"] = "week"
                elif re.search(r'this\s+month', command, re.IGNORECASE):
                    entities["period"] = "month"
                elif re.search(r'last\s+(\d+)\s+days', command, re.IGNORECASE):
                    days_match = re.search(r'last\s+(\d+)\s+days', command, re.IGNORECASE)
                    if days_match:
                        entities["period"] = f"last_{days_match.group(1)}_days"
                
                # Extract custom date range
                date_pattern = r'(?:from|between)\s+([\w\s,]+)\s+(?:to|and|till)\s+([\w\s,]+)'
                date_match = re.search(date_pattern, command, re.IGNORECASE)
                if date_match:
                    start_date_str = date_match.group(1).strip()
                    end_date_str = date_match.group(2).strip()
                    
                    # Try to parse dates
                    start_date = parse_mixed_date(start_date_str)
                    end_date = parse_mixed_date(end_date_str)
                    
                    if start_date and end_date:
                        entities["range"] = "custom"
                        entities["start_date"] = start_date
                        entities["end_date"] = end_date
        
        return entities
    
    def parse_command(self, command: str) -> Dict[str, Any]:
        """Parse a command to identify intent, language, and extract entities.
        
        Args:
            command: The input command to parse.
            
        Returns:
            Dict[str, Any]: A dictionary containing the parsed command information.
        """
        # Identify intent and language
        intent, language = self.identify_intent(command)
        
        # Extract entities based on intent and language
        entities = self.extract_entities(command, intent, language)
        
        # Return the parsed command
        return {
            "command": command,
            "intent": intent,
            "language": language,
            "entities": entities
        }
    
    def generate_response(self, parsed_command: Dict[str, Any]) -> str:
        """Generate a response based on the parsed command.
        
        Args:
            parsed_command: The parsed command information.
            
        Returns:
            str: The generated response.
        """
        intent = parsed_command.get("intent", "unknown")
        language = parsed_command.get("language", "en")
        entities = parsed_command.get("entities", {})
        
        # Define response templates for different languages
        responses = {
            "get_inventory": {
                "en": "Here is the current inventory.",
                "hi": "यहां वर्तमान इन्वेंटरी है।",
                "mixed": "Here is the वर्तमान inventory."
            },
            "get_low_stock": {
                "en": "Here are the items with low stock.",
                "hi": "यहां कम स्टॉक वाले आइटम्स हैं।",
                "mixed": "Here are the कम स्टॉक items."
            },
            "edit_stock": {
                "en": "Stock updated successfully.",
                "hi": "स्टॉक सफलतापूर्वक अपडेट किया गया।",
                "mixed": "Stock सफलतापूर्वक updated."
            },
            "search_product": {
                "en": "Here are the product details.",
                "hi": "यहां प्रोडक्ट के विवरण हैं।",
                "mixed": "Here are the प्रोडक्ट details."
            },
            "get_orders": {
                "en": "Here are the orders.",
                "hi": "यहां ऑर्डर्स हैं।",
                "mixed": "Here are the ऑर्डर्स."
            },
            "get_report": {
                "en": "Here is the report.",
                "hi": "यहां रिपोर्ट है।",
                "mixed": "Here is the रिपोर्ट."
            },
            "unknown": {
                "en": "I'm sorry, I didn't understand that command.",
                "hi": "क्षमा करें, मैं उस कमांड को नहीं समझ पाया।",
                "mixed": "Sorry, मैं उस command को नहीं समझ पाया।"
            }
        }
        
        # Get the appropriate response template
        response_template = responses.get(intent, responses["unknown"]).get(language, responses[intent]["en"])
        
        # Customize response based on entities
        if intent == "search_product" and "product_name" in entities:
            product_name = entities["product_name"]
            if language == "en":
                response_template = f"Here are the details for {product_name}."
            elif language == "hi":
                response_template = f"{product_name} के विवरण यहां हैं।"
            else:  # mixed
                response_template = f"Here are the details for {product_name}."
        
        elif intent == "edit_stock" and "product_name" in entities and "operation" in entities:
            product_name = entities["product_name"]
            operation = entities["operation"]
            quantity = entities.get("quantity", "some")
            
            if language == "en":
                if operation == "add":
                    response_template = f"Added {quantity} units to {product_name} stock."
                else:  # remove
                    response_template = f"Removed {quantity} units from {product_name} stock."
            elif language == "hi":
                if operation == "add":
                    response_template = f"{product_name} स्टॉक में {quantity} यूनिट्स जोड़े गए।"
                else:  # remove
                    response_template = f"{product_name} स्टॉक से {quantity} यूनिट्स हटाए गए।"
            else:  # mixed
                if operation == "add":
                    response_template = f"Added {quantity} units to {product_name} स्टॉक."
                else:  # remove
                    response_template = f"Removed {quantity} units from {product_name} स्टॉक."
        
        elif intent in ["get_orders", "get_report"] and ("period" in entities or "range" in entities):
            period = entities.get("period", "")
            range_type = entities.get("range", "")
            
            if range_type == "custom" and "start_date" in entities and "end_date" in entities:
                start_date = entities["start_date"].strftime("%Y-%m-%d")
                end_date = entities["end_date"].strftime("%Y-%m-%d")
                
                if language == "en":
                    response_template = f"Here is the {intent.replace('get_', '')} from {start_date} to {end_date}."
                elif language == "hi":
                    response_template = f"यहां {start_date} से {end_date} तक का {intent.replace('get_', '')} है।"
                else:  # mixed
                    response_template = f"Here is the {intent.replace('get_', '')} from {start_date} to {end_date}."
            
            elif period:
                if language == "en":
                    response_template = f"Here is the {intent.replace('get_', '')} for {period}."
                elif language == "hi":
                    period_hi = {
                        "today": "आज",
                        "yesterday": "कल",
                        "week": "इस हफ्ते",
                        "month": "इस महीने"
                    }.get(period, period)
                    response_template = f"यहां {period_hi} का {intent.replace('get_', '')} है।"
                else:  # mixed
                    response_template = f"Here is the {period} का {intent.replace('get_', '')}."
        
        return response_template


# Example usage
def test_multilingual_processor():
    """Test the multilingual processor with various commands."""
    processor = MultilingualProcessor()
    
    test_commands = [
        # English commands
        "Show inventory",
        "Display low stock items",
        "Update stock for Product A, add 10 units",
        "Search for Product B",
        "Show orders for today",
        "Generate report for this month",
        
        # Hindi commands
        "इन्वेंटरी दिखाओ",
        "कम स्टॉक आइटम्स बताओ",
        "प्रोडक्ट A का स्टॉक अपडेट करो, 10 यूनिट्स जोड़ो",
        "प्रोडक्ट B खोजो",
        "आज के ऑर्डर्स दिखाओ",
        "इस महीने की रिपोर्ट जनरेट करो",
        
        # Mixed language commands
        "Show इन्वेंटरी",
        "Display कम स्टॉक items",
        "Update प्रोडक्ट A का stock, add 10 units",
        "Search for प्रोडक्ट B",
        "Show आज के orders",
        "Generate इस महीने की report",
        
        # Transliterated Hindi commands
        "Inventory dikhao",
        "Kam stock items batao",
        "Product A ka stock update karo, 10 units jodo",
        "Product B khojo",
        "Aaj ke orders dikhao",
        "Is mahine ki report generate karo",
    ]
    
    results = []
    for command in test_commands:
        parsed = processor.parse_command(command)
        response = processor.generate_response(parsed)
        
        results.append({
            "command": command,
            "intent": parsed["intent"],
            "language": parsed["language"],
            "entities": parsed["entities"],
            "response": response
        })
    
    # Print results
    for i, result in enumerate(results):
        print(f"\nTest {i+1}:")
        print(f"Command: {result['command']}")
        print(f"Intent: {result['intent']}")
        print(f"Language: {result['language']}")
        print(f"Entities: {result['entities']}")
        print(f"Response: {result['response']}")


if __name__ == "__main__":
    test_multilingual_processor()