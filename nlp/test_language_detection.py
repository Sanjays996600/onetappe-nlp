import unittest
import sys
import os

# Add the parent directory to the path so we can import the module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.mixed_entity_extraction import detect_language, normalize_transliterated_hindi

class TestLanguageDetection(unittest.TestCase):
    def test_language_detection(self):
        """Test the language detection functionality"""
        # Test pure Hindi
        self.assertEqual(detect_language("आज का मौसम अच्छा है"), "hindi")
        
        # Test pure English
        self.assertEqual(detect_language("Today's weather is good"), "english")
        
        # Test mixed with Hindi dominance
        self.assertEqual(detect_language("आज का weather अच्छा है"), "mixed")
        
        # Test mixed with English dominance
        self.assertEqual(detect_language("Today's मौसम is good"), "mixed")
        
        # Test with emojis
        self.assertEqual(detect_language("Today's weather is good 🌞"), "mixed")
        
        # Test with transliterated Hindi
        self.assertEqual(detect_language("aaj ka mausam accha hai"), "mixed")
        
        # Test with numbers
        self.assertEqual(detect_language("Stock 5 kg"), "english")
        self.assertEqual(detect_language("स्टॉक 5 किलो"), "hindi")
        
        # Test with empty string
        self.assertEqual(detect_language(""), "english")
        
        # Test with only punctuation and spaces
        self.assertEqual(detect_language("!@#$%^&*()"), "english")

class TestTransliteration(unittest.TestCase):
    def test_normalize_transliterated_hindi(self):
        """Test the transliteration normalization functionality"""
        # Test basic transliteration
        self.assertEqual(
            normalize_transliterated_hindi("aaj ka mausam accha hai"),
            "आज का मौसम अच्छा है"
        )
        
        # Test mixed language
        self.assertEqual(
            normalize_transliterated_hindi("aaj ka weather accha hai"),
            "आज का weather अच्छा है"
        )
        
        # Test with product names
        self.assertEqual(
            normalize_transliterated_hindi("chawal ka stock update karo"),
            "चावल का स्टॉक अपडेट करो"
        )
        
        # Test with numbers and units
        self.assertEqual(
            normalize_transliterated_hindi("aalu 5 kilo update karo"),
            "आलू 5 किलो अपडेट करो"
        )
        
        # Test with compound words
        self.assertEqual(
            normalize_transliterated_hindi("stockupdate karo"),
            "स्टॉकअपडेट करो"
        )
        
        # Test with punctuation and spaces
        self.assertEqual(
            normalize_transliterated_hindi("chawal, aalu, pyaaz"),
            "चावल, आलू, प्याज"
        )
        
        # Test with empty string
        self.assertEqual(normalize_transliterated_hindi(""), "")
        
        # Test with pure Hindi (should remain unchanged)
        self.assertEqual(
            normalize_transliterated_hindi("आज का मौसम अच्छा है"),
            "आज का मौसम अच्छा है"
        )
        
        # Test with pure English (should remain mostly unchanged)
        self.assertEqual(
            normalize_transliterated_hindi("update stock of rice"),
            "update स्टॉक of rice"
        )

if __name__ == "__main__":
    unittest.main()