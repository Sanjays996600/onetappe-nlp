import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock

# Import the language detection module
from OneTappeProject.nlp.improved_language_detection import (
    detect_language,
    detect_language_with_confidence,
    detect_mixed_language,
    handle_mixed_language_input
)

class TestLanguageDetection(unittest.TestCase):
    """Test cases for the improved language detection module."""
    
    def test_detect_language(self):
        """Test basic language detection."""
        # Test English detection
        self.assertEqual(detect_language("Hello, how are you?"), "en")
        self.assertEqual(detect_language("Show me the inventory"), "en")
        self.assertEqual(detect_language("Update rice stock to 50"), "en")
        
        # Test Hindi detection
        self.assertEqual(detect_language("नमस्ते, आप कैसे हैं?"), "hi")
        self.assertEqual(detect_language("इन्वेंटरी दिखाओ"), "hi")
        self.assertEqual(detect_language("चावल स्टॉक 50 करो"), "hi")
        
        # Test mixed language detection
        self.assertEqual(detect_language("Hello, मेरा नाम John है"), "mixed")
        self.assertEqual(detect_language("Show मेरा inventory"), "mixed")
        self.assertEqual(detect_language("Update चावल stock to 50"), "mixed")
    
    def test_detect_language_with_confidence(self):
        """Test language detection with confidence scores."""
        # Test English detection with confidence
        lang, conf = detect_language_with_confidence("Hello, how are you?")
        self.assertEqual(lang, "en")
        self.assertGreaterEqual(conf, 0.7)
        
        # Test Hindi detection with confidence
        lang, conf = detect_language_with_confidence("नमस्ते, आप कैसे हैं?")
        self.assertEqual(lang, "hi")
        self.assertGreaterEqual(conf, 0.7)
        
        # Test mixed language detection with confidence
        lang, conf = detect_language_with_confidence("Hello, मेरा नाम John है")
        self.assertEqual(lang, "mixed")
        self.assertGreaterEqual(conf, 0.5)
    
    def test_detect_mixed_language(self):
        """Test detailed mixed language detection."""
        # Test predominantly English with Hindi
        result = detect_mixed_language("Hello, मेरा नाम John है")
        self.assertTrue(result["is_mixed"])
        self.assertIn(result["primary_language"], ["en", "hi"])
        self.assertGreaterEqual(result["en_ratio"] + result["hi_ratio"], 0.9)
        
        # Test predominantly Hindi with English
        result = detect_mixed_language("मेरा नाम John है और मैं inventory देखना चाहता हूँ")
        self.assertTrue(result["is_mixed"])
        self.assertEqual(result["primary_language"], "hi")
        self.assertGreaterEqual(result["hi_ratio"], result["en_ratio"])
        
        # Test pure English (not mixed)
        result = detect_mixed_language("Hello, my name is John")
        self.assertFalse(result["is_mixed"])
        self.assertEqual(result["primary_language"], "en")
        self.assertGreaterEqual(result["en_ratio"], 0.9)
        
        # Test pure Hindi (not mixed)
        result = detect_mixed_language("नमस्ते, मेरा नाम जॉन है")
        self.assertFalse(result["is_mixed"])
        self.assertEqual(result["primary_language"], "hi")
        self.assertGreaterEqual(result["hi_ratio"], 0.9)
    
    def test_handle_mixed_language_input(self):
        """Test handling of mixed language input."""
        # Test English with Hindi segments
        result = handle_mixed_language_input("Show मेरा inventory")
        self.assertEqual(result["primary_language"], "en")
        self.assertIn("मेरा", result["hindi_segments"])
        self.assertIn("Show", result["english_segments"])
        self.assertIn("inventory", result["english_segments"])
        
        # Test Hindi with English segments
        result = handle_mixed_language_input("मेरा inventory दिखाओ")
        self.assertEqual(result["primary_language"], "hi")
        self.assertIn("मेरा", result["hindi_segments"])
        self.assertIn("दिखाओ", result["hindi_segments"])
        self.assertIn("inventory", result["english_segments"])
        
        # Test with transliterated Hindi
        result = handle_mixed_language_input("Mera inventory dikhao")
        self.assertEqual(result["primary_language"], "hi-en")
        self.assertTrue(len(result["transliterated_segments"]) > 0)
    
    def test_edge_cases(self):
        """Test edge cases for language detection."""
        # Test empty string
        self.assertEqual(detect_language(""), "en")  # Default to English for empty string
        
        # Test string with only numbers and symbols
        self.assertEqual(detect_language("123 !@#"), "en")  # Default to English
        
        # Test very short text
        lang, conf = detect_language_with_confidence("hi")
        self.assertEqual(lang, "en")  # "hi" is an English word, not Hindi
        
        # Test with emojis
        self.assertEqual(detect_language("Hello 😊"), "en")
        self.assertEqual(detect_language("नमस्ते 😊"), "hi")

if __name__ == "__main__":
    unittest.main()