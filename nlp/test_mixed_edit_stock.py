import unittest
from mixed_entity_extraction import extract_mixed_edit_stock_details

class TestMixedEditStock(unittest.TestCase):
    def test_hindi_commands(self):
        # Test pure Hindi commands
        command = "चीनी का स्टॉक बदलो 5 किलो"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चीनी")
        self.assertEqual(result.get("stock"), 5)
        
        command = "आलू स्टॉक अपडेट करें 10 किलो"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "आलू")
        self.assertEqual(result.get("stock"), 10)
        
        command = "बदलें स्टॉक साबुन 3"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "साबुन")
        self.assertEqual(result.get("stock"), 3)
        
    def test_mixed_language_commands(self):
        # Test mixed language commands
        command = "Update stock of आलू to 10 किलो"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "आलू")
        self.assertEqual(result.get("stock"), 10)
        
        # Additional mixed language test cases
        command = "edit stock of चावल to 20"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चावल")
        self.assertEqual(result.get("stock"), 20)
        
        command = "दाल stock update to 15"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "दाल")
        self.assertEqual(result.get("stock"), 15)
        
        command = "update मसाला stock to 8"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "मसाला")
        self.assertEqual(result.get("stock"), 8)
        
        command = "नमक stock बदलो 7"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "नमक")
        self.assertEqual(result.get("stock"), 7)
        
    def test_negative_stock_values(self):
        # Test negative stock values in mixed language commands
        command = "edit stock of चावल to -20"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चावल")
        self.assertEqual(result.get("stock"), -20)
        
        command = "चीनी का स्टॉक बदलो -5 किलो"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चीनी")
        self.assertEqual(result.get("stock"), -5)
        
    def test_emoji_rich_commands(self):
        # Test commands with emojis
        command = "📦 Update stock of आलू to 10 किलो 🥔"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "आलू")
        self.assertEqual(result.get("stock"), 10)
        
        command = "🔄 चावल stock update ➡️ 20kg 🍚"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चावल")
        self.assertEqual(result.get("stock"), 20)
        
    def test_multi_line_commands(self):
        # Test multi-line commands
        command = "Update stock\nof आलू\nto 10 किलो"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "आलू")
        self.assertEqual(result.get("stock"), 10)
        
        command = "चावल\nstock update\nto 20kg"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चावल")
        self.assertEqual(result.get("stock"), 20)
        
    def test_structured_format_commands(self):
        # Test structured format commands (Pattern 6)
        command = "product: चावल, quantity: 20kg"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चावल")
        self.assertEqual(result.get("stock"), 20)
        
        # Test dash/colon separated formats (Pattern 7)
        command = "edit stock: आलू - 10kg"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "आलू")
        self.assertEqual(result.get("stock"), 10)
        
        # Test fuzzy matching fallback (Pattern 8)
        command = "updt stck of चावल with 15 kg"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चावल")
        self.assertEqual(result.get("stock"), 15)
        
    def test_fuzzy_product_name_matching(self):
        # Test fuzzy matching for product names with common misspellings
        command = "update stock of chaval to 25kg"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चावल")
        self.assertEqual(result.get("stock"), 25)
        
        command = "aalu stock update to 15kg"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "आलू")
        self.assertEqual(result.get("stock"), 15)
        
        command = "update stock of chini to 8kg"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चीनी")
        self.assertEqual(result.get("stock"), 8)
        
        # Test with more extreme misspellings
        command = "update stock of choawal to 30kg"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चावल")
        self.assertEqual(result.get("stock"), 30)
        
        # Test with mixed emoji and misspellings
        command = "🔄 choawal stock update ➡️ 20kg 🍚"
        result = extract_mixed_edit_stock_details(command)
        self.assertEqual(result.get("name"), "चावल")
        self.assertEqual(result.get("stock"), 20)

# For debugging mixed language commands
def debug_mixed_language_commands():
    commands = [
        # Original patterns
        "चीनी का स्टॉक बदलो 5 किलो",
        "आलू स्टॉक अपडेट करें 10 किलो",
        "बदलें स्टॉक साबुन 3",
        "Update stock of आलू to 10 किलो",
        "edit stock of चावल to 20",
        "दाल stock update to 15",
        "update मसाला stock to 8",
        "नमक stock बदलो 7",
        
        # New patterns - emoji rich
        "📦 Update stock of आलू to 10 किलो 🥔",
        "🔄 चावल stock update ➡️ 20kg 🍚",
        
        # New patterns - multi-line
        "Update stock\nof आलू\nto 10 किलो",
        "चावल\nstock update\nto 20kg",
        
        # New patterns - structured formats
        "product: चावल, quantity: 20kg",
        "edit stock: आलू - 10kg",
        "updt stck of चावल with 15 kg"
    ]
    
    for cmd in commands:
        print(f"Command: {cmd}")
        result = extract_mixed_edit_stock_details(cmd)
        print(f"Result: {result}\n")

# For debugging negative stock commands
def debug_negative_stock_commands():
    commands = [
        "edit stock of चावल to -20",
        "चीनी का स्टॉक बदलो -5 किलो"
    ]
    
    for cmd in commands:
        print(f"Command: {cmd}")
        from nlp.mixed_entity_extraction import normalize_mixed_command
        normalized = normalize_mixed_command(cmd)
        print(f"Normalized: {normalized}")
        result = extract_mixed_edit_stock_details(cmd)
        print(f"Result: {result}\n")

if __name__ == "__main__":
    # Run the debug function for negative stock commands
    debug_negative_stock_commands()
    # Run the tests
    unittest.main()