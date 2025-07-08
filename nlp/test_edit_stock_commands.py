import unittest
from nlp.mixed_entity_extraction import extract_mixed_edit_stock_details

class TestEditStockCommands(unittest.TestCase):
    def test_english_edit_stock_commands(self):
        # Test basic English commands
        command1 = "edit stock of rice to 10kg"
        result1 = extract_mixed_edit_stock_details(command1)
        self.assertEqual(result1.get("name"), "rice")
        self.assertEqual(result1.get("stock"), 10)
        
        command2 = "update stock for 5 kg sugar"
        result2 = extract_mixed_edit_stock_details(command2)
        self.assertEqual(result2.get("name"), "sugar")
        self.assertEqual(result2.get("stock"), 5)
        
        command3 = "edit product Aata qty 20"
        result3 = extract_mixed_edit_stock_details(command3)
        self.assertEqual(result3.get("name"), "Aata")
        self.assertEqual(result3.get("stock"), 20)
    
    def test_hindi_edit_stock_commands(self):
        # Test Hindi commands
        command1 = "चीनी का स्टॉक बदलें 3 किलो"
        result1 = extract_mixed_edit_stock_details(command1)
        self.assertEqual(result1.get("name"), "चीनी")
        self.assertEqual(result1.get("stock"), 3)
        
        command2 = "स्टॉक अपडेट करें 12 पीस के लिए नमकीन"
        result2 = extract_mixed_edit_stock_details(command2)
        self.assertEqual(result2.get("name"), "नमकीन")
        self.assertEqual(result2.get("stock"), 12)
    
    def test_mixed_edit_stock_commands(self):
        # Test mixed language commands
        command1 = "update rice स्टॉक to 15"
        result1 = extract_mixed_edit_stock_details(command1)
        self.assertEqual(result1.get("name"), "rice")
        self.assertEqual(result1.get("stock"), 15)
        
        command2 = "चावल stock बदलें to 8 kg"
        result2 = extract_mixed_edit_stock_details(command2)
        self.assertEqual(result2.get("name"), "चावल")
        self.assertEqual(result2.get("stock"), 8)
    
    def test_complex_edit_stock_commands(self):
        # Test more complex cases
        command1 = "update the stock of 2kg sugar to 7kg"
        result1 = extract_mixed_edit_stock_details(command1)
        self.assertEqual(result1.get("name"), "sugar")
        self.assertEqual(result1.get("stock"), 7)
        
        command2 = "edit 5 kg aata stock to 10"
        result2 = extract_mixed_edit_stock_details(command2)
        self.assertEqual(result2.get("name"), "aata")
        self.assertEqual(result2.get("stock"), 10)

if __name__ == "__main__":
    unittest.main()