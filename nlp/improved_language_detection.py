#!/usr/bin/env python3
"""
Improved Language Detection Module

This module enhances the language detection capabilities for the NLP system,
focusing on better distinguishing between English, Hindi, and mixed language inputs.
"""

import re
import json
import sys
sys.path.append('/Users/sanjaysuman/One Tappe/OneTappeProject')

# Define character ranges for different languages
HINDI_CHAR_RANGE = r'[\u0900-\u097F]'
ENGLISH_CHAR_RANGE = r'[a-zA-Z]'

# Define common Hindi transliterated words for detection
HINDI_TRANSLITERATION_MAP = {
    # Common verbs
    "dikhao": "दिखाओ",
    "batao": "बताओ",
    "karo": "करो",
    "do": "दो",
    "bhejo": "भेजो",
    "jodo": "जोड़ो",
    "jodein": "जोड़ें",
    "add": "एड",
    "update": "अपडेट",
    "banao": "बनाओ",
    "create": "बनाओ",
    "rakho": "रखो",
    "lagao": "लगाओ",
    
    # Common nouns
    "report": "रिपोर्ट",
    "order": "ऑर्डर",
    "orders": "ऑर्डर्स",
    "product": "प्रोडक्ट",
    "stock": "स्टॉक",
    "price": "प्राइस",
    "mulya": "मूल्य",
    "kimat": "कीमत",
    "matra": "मात्रा",
    "cheez": "चीज़",
    "vastu": "वस्तु",
    "samaan": "सामान",
    "item": "आइटम",
    "rate": "रेट",
    "daam": "दाम",
    "quantity": "मात्रा",
    
    # Time-related words
    "aaj": "आज",
    "kal": "कल",
    "is": "इस",
    "pichhle": "पिछले",
    "pichle": "पिछले",
    "hafte": "हफ्ते",
    "mahine": "महीने",
    "din": "दिन",
    "saptah": "सप्ताह",
    
    # Connectors
    "ka": "का",
    "ki": "की",
    "ke": "के",
    "se": "से",
    "tak": "तक",
    "aur": "और",
    "with": "के साथ",
    "at": "पर",
    "par": "पर",
    "mein": "में",
    "me": "में",
    "and": "और",
    
    # Other common words
    "naya": "नया",
    "purana": "पुराना",
    "sabhi": "सभी",
    "sab": "सब",
    "naam": "नाम",
    "name": "नाम",
    
    # Units and quantities
    "kilo": "किलो",
    "gram": "ग्राम",
    "liter": "लीटर",
    "mili": "मिली",
    "qty": "मात्रा",
    "piece": "नग",
    "pieces": "नग",
    "pcs": "नग",
    "unit": "इकाई",
    "units": "इकाई",
    "packet": "पैकेट",
    "box": "डिब्बा",
    "dozen": "दर्जन",
    
    # Currency related
    "rupees": "रुपये",
    "rupee": "रुपया",
    "rs": "रुपये",
    "rupaye": "रुपये",
}

def detect_language(text):
    """
    Enhanced language detection function that detects English, Hindi, or mixed language.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        str: Language code ('en' for English, 'hi' for Hindi, 'mixed' for mixed language)
    """
    # Check for Hindi and English characters
    hindi_pattern = re.compile(HINDI_CHAR_RANGE)
    english_pattern = re.compile(ENGLISH_CHAR_RANGE)
    
    has_hindi = hindi_pattern.search(text) is not None
    has_english = english_pattern.search(text) is not None
    
    # Check for transliterated Hindi words
    words = text.lower().split()
    hindi_transliterated_words = [word for word in words if word in HINDI_TRANSLITERATION_MAP]
    
    if has_hindi and has_english:
        return "mixed"
    elif has_hindi:
        return "hi"
    elif has_english and hindi_transliterated_words:
        return "mixed"  # English with transliterated Hindi words
    else:
        return "en"

def detect_language_with_confidence(text):
    """
    Enhanced language detection that returns the detected language
    and a confidence score, including mixed language detection.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Contains language code and confidence score
    """
    # Count Hindi and English characters
    hindi_chars = len(re.findall(HINDI_CHAR_RANGE, text))
    english_chars = len(re.findall(ENGLISH_CHAR_RANGE, text))
    
    # Check for transliterated Hindi words
    words = text.lower().split()
    hindi_transliterated_words = [word for word in words if word in HINDI_TRANSLITERATION_MAP]
    transliterated_count = len(hindi_transliterated_words)
    
    # Calculate the ratio of Hindi to total relevant characters
    total_relevant_chars = hindi_chars + english_chars
    if total_relevant_chars == 0:
        return {"language": "en", "confidence": 0.5}  # Default to English with low confidence
    
    hindi_ratio = hindi_chars / total_relevant_chars
    english_ratio = english_chars / total_relevant_chars
    
    # Determine if the text is mixed language
    is_mixed = (hindi_chars > 0 and english_chars > 0) or (english_chars > 0 and transliterated_count > 0)
    
    if is_mixed:
        # Calculate confidence based on character distribution and transliterated words
        mixed_confidence = max(0.6, min(0.9, (hindi_ratio + english_ratio) / 2 + (transliterated_count / len(words)) * 0.2))
        return {"language": "mixed", "confidence": mixed_confidence}
    elif hindi_ratio > english_ratio:
        return {"language": "hi", "confidence": hindi_ratio}
    else:
        return {"language": "en", "confidence": english_ratio}

def detect_mixed_language(text):
    """
    Detects if text contains a significant mix of both English and Hindi,
    including transliterated Hindi words.
    
    Args:
        text (str): The text to analyze
        
    Returns:
        dict: Contains primary language, secondary language (if mixed), and their ratios
    """
    # Count Hindi and English characters
    hindi_chars = len(re.findall(HINDI_CHAR_RANGE, text))
    english_chars = len(re.findall(ENGLISH_CHAR_RANGE, text))
    
    # Check for transliterated Hindi words
    words = text.lower().split()
    hindi_transliterated_words = [word for word in words if word in HINDI_TRANSLITERATION_MAP]
    transliterated_count = len(hindi_transliterated_words)
    
    # Calculate ratios
    total_relevant_chars = hindi_chars + english_chars
    if total_relevant_chars == 0:
        return {"primary_language": "en", "is_mixed": False, "hindi_ratio": 0, "english_ratio": 0, "transliterated_ratio": 0}
    
    hindi_ratio = hindi_chars / total_relevant_chars
    english_ratio = english_chars / total_relevant_chars
    transliterated_ratio = transliterated_count / len(words) if words else 0
    
    # Determine if the text is significantly mixed
    # Either by having both Hindi and English characters, or by having English characters and transliterated Hindi words
    is_mixed = (hindi_chars > 0 and english_chars > 0) or (english_chars > 0 and transliterated_count > 0)
    
    if hindi_ratio > english_ratio:
        return {
            "primary_language": "hi",
            "secondary_language": "en" if is_mixed else None,
            "is_mixed": is_mixed,
            "hindi_ratio": hindi_ratio,
            "english_ratio": english_ratio,
            "transliterated_ratio": transliterated_ratio,
            "transliterated_words": hindi_transliterated_words
        }
    else:
        return {
            "primary_language": "en",
            "secondary_language": "hi" if is_mixed else None,
            "is_mixed": is_mixed,
            "hindi_ratio": hindi_ratio,
            "english_ratio": english_ratio,
            "transliterated_ratio": transliterated_ratio,
            "transliterated_words": hindi_transliterated_words
        }

def handle_mixed_language_input(text):
    """
    Processes mixed language input by identifying the primary language
    and providing appropriate handling suggestions.
    
    Args:
        text (str): The mixed language text to process
        
    Returns:
        dict: Contains processing information and suggestions
    """
    language_info = detect_mixed_language(text)
    
    if not language_info["is_mixed"]:
        return {
            "is_mixed": False,
            "primary_language": language_info["primary_language"],
            "suggestion": f"Process using {language_info['primary_language']} language handler"
        }
    
    # For mixed language text
    primary = language_info["primary_language"]
    secondary = language_info["secondary_language"]
    
    # Extract segments by language
    hindi_segments = re.findall(f"{HINDI_CHAR_RANGE}+", text)
    english_segments = re.findall(f"{ENGLISH_CHAR_RANGE}+", text)
    
    return {
        "is_mixed": True,
        "primary_language": primary,
        "secondary_language": secondary,
        "hindi_ratio": language_info["hindi_ratio"],
        "english_ratio": language_info["english_ratio"],
        "transliterated_ratio": language_info["transliterated_ratio"],
        "hindi_segments": hindi_segments,
        "english_segments": english_segments,
        "transliterated_words": language_info.get("transliterated_words", []),
        "suggestion": f"Process using mixed language handler with {primary} as primary language"
    }

def test_language_detection():
    """
    Test the enhanced language detection with various inputs.
    """
    test_cases = [
        "Show me all orders",
        "Get inventory status",
        "सभी ऑर्डर दिखाओ",
        "इन्वेंटरी स्थिति दिखाएं",
        "Update Sugar stock to 20",
        "चीनी का स्टॉक 15 करो",
        "Show me चीनी inventory",  # Mixed
        "मुझे Sugar का स्टॉक दिखाओ",  # Mixed
        "pichhle hafte ka report dikhao",  # Transliterated Hindi
        "aaj ke orders batao",  # Transliterated Hindi
        "Report from 1 जनवरी to 31 जनवरी",  # Mixed with Hindi months
        "123456",  # Numbers only
        ""  # Empty string
    ]
    
    print("\nTesting Enhanced Language Detection:\n")
    print("{:<40} {:<10}".format("Text", "Language"))
    print("-" * 50)
    
    for text in test_cases:
        lang = detect_language(text)
        print("{:<40} {:<10}".format(text[:40], lang))
    
    print("\nTesting Language Detection with Confidence:\n")
    print("{:<40} {:<10} {:<10}".format("Text", "Language", "Confidence"))
    print("-" * 60)
    
    for text in test_cases:
        result = detect_language_with_confidence(text)
        print("{:<40} {:<10} {:.2f}".format(
            text[:40], 
            result["language"], 
            result["confidence"]
        ))
    
    print("\nTesting Mixed Language Detection:\n")
    print("{:<40} {:<10} {:<10} {:<20}".format(
        "Text", "Primary", "Mixed?", "Transliterated Words"
    ))
    print("-" * 80)
    
    for text in test_cases:
        result = detect_mixed_language(text)
        transliterated = ", ".join(result.get("transliterated_words", []))[:20]
        print("{:<40} {:<10} {:<10} {:<20}".format(
            text[:40],
            result["primary_language"],
            "Yes" if result["is_mixed"] else "No",
            transliterated
        ))

if __name__ == "__main__":
    print("===== Enhanced Language Detection =====\n")
    test_language_detection()