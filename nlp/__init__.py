# NLP module for intent recognition and entity extraction

# Import key modules to make them available when importing from nlp package
from .intent_handler import parse_command, detect_language, INTENT_PATTERNS, extract_product_details
from .hindi_support import parse_hindi_command, HINDI_INTENT_PATTERNS, extract_hindi_product_details, extract_hindi_edit_stock_details
from .multilingual_handler import parse_multilingual_command
from .command_router import route_command, make_api_request

# Make enhanced modules available
from .enhanced_multilingual_parser import parse_multilingual_command as enhanced_parse_multilingual_command