import logging
from typing import Dict, Any

# Import our intent handlers using relative imports
from .intent_handler import parse_command, detect_language
from .hindi_support import parse_hindi_command

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='multilingual_nlp.log'
)
logger = logging.getLogger(__name__)

def parse_multilingual_command(message: str) -> Dict[str, Any]:
    """
    Parse a command message in any supported language and return the recognized intent and entities.
    
    Args:
        message: The command message from the user
        
    Returns:
        A dictionary with 'intent', 'entities', and 'language' keys
    """
    # Detect the language
    language = detect_language(message)
    logger.info(f"Detected language: {language} for message: {message}")
    
    # Parse based on language
    if language == 'hi':
        result = parse_hindi_command(message)
        logger.info(f"Hindi intent recognized: {result['intent']}")
    else:  # Default to English
        result = parse_command(message)
        logger.info(f"English intent recognized: {result['intent']}")
    
    # Add language to the result
    result['language'] = language
    
    return result

# Example usage
if __name__ == "__main__":
    # Test cases in multiple languages
    test_commands = [
        # English commands
        "Show my products",
        "Send today's report",
        "Show low stock items",
        "Add new product Rice 50rs 20qty",
        "Edit stock of Rice to 100",
        "Do you have sugar in stock?",  # Search product
        "Search for rice",  # Search product
        "Is salt available?",  # Search product
        
        # Hindi commands
        "मेरे प्रोडक्ट दिखाओ",  # Show my products
        "आज की रिपोर्ट भेजो",    # Send today's report
        "कम स्टॉक वाले आइटम दिखाओ",  # Show low stock items
        "नया प्रोडक्ट चावल 50 रुपये 20 पीस जोड़ो",  # Add new product Rice 50rs 20pcs
        "चावल का स्टॉक 100 करो",  # Update Rice stock to 100
        "चाय उपलब्ध है क्या?",  # Search product
        "चावल सर्च करो",  # Search product
        "नमक है क्या स्टॉक में?"  # Search product
    ]
    
    print("\nTesting multilingual intent recognition:\n")
    for cmd in test_commands:
        result = parse_multilingual_command(cmd)
        print(f"Command: '{cmd}'")
        print(f"Language: {result['language']}")
        print(f"Intent: {result['intent']}")
        print(f"Entities: {result['entities']}\n")