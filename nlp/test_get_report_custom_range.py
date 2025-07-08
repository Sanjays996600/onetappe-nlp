import unittest
import sys
import os

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from nlp.intent_handler import parse_command
from nlp.hindi_support import parse_hindi_command
from nlp.command_router import route_command


class TestGetReportCustomRange(unittest.TestCase):
    def test_english_custom_date_range(self):
        # Test English command with custom date range
        command = "Get report from 1 June to 20 June"
        result = parse_command(command)
        
        # Check intent and language
        self.assertEqual(result["intent"], "get_report")
        self.assertEqual(result["language"], "en")
        
        # Check entities
        self.assertIn("start_date", result["entities"])
        self.assertIn("end_date", result["entities"])
        
        # Get current year for comparison
        import datetime
        current_year = datetime.datetime.now().year
        
        # Format expected dates
        expected_start = f"{current_year}-06-01"
        expected_end = f"{current_year}-06-20"
        
        # Check extracted dates
        self.assertEqual(result["entities"]["start_date"], expected_start)
        self.assertEqual(result["entities"]["end_date"], expected_end)
        
        # Test route_command response
        response = route_command(result["intent"], result["entities"], result["language"])
        
        # Check response contains expected elements
        self.assertIn("Sales from 1 June to 20 June", response)
        self.assertIn("Orders:", response)
        self.assertIn("Top product:", response)
    
    def test_english_custom_date_range_between(self):
        # Test English command with "between" format
        command = "Get report between 1st January and 31st January"
        result = parse_command(command)
        
        # Check intent and language
        self.assertEqual(result["intent"], "get_report")
        self.assertEqual(result["language"], "en")
        
        # Check entities
        self.assertIn("start_date", result["entities"])
        self.assertIn("end_date", result["entities"])
        
        # Get current year for comparison
        import datetime
        current_year = datetime.datetime.now().year
        
        # Format expected dates
        expected_start = f"{current_year}-01-01"
        expected_end = f"{current_year}-01-31"
        
        # Check extracted dates
        self.assertEqual(result["entities"]["start_date"], expected_start)
        self.assertEqual(result["entities"]["end_date"], expected_end)
        
        # Test route_command response
        response = route_command(result["intent"], result["entities"], result["language"])
        
        # Check response contains expected elements
        self.assertIn("Sales from 1 January to 31 January", response)
        self.assertIn("Orders:", response)
        self.assertIn("Top product:", response)
    
    def test_hindi_custom_date_range(self):
        # Test Hindi command with custom date range
        command = "1 जून से 20 जून तक की रिपोर्ट दिखाओ"
        result = parse_hindi_command(command)
        
        # Check intent and language
        self.assertEqual(result["intent"], "get_report")
        self.assertEqual(result["language"], "hi")
        
        # Check entities
        self.assertIn("start_date", result["entities"])
        self.assertIn("end_date", result["entities"])
        
        # Get current year for comparison
        import datetime
        current_year = datetime.datetime.now().year
        
        # Format expected dates
        expected_start = f"{current_year}-06-01"
        expected_end = f"{current_year}-06-20"
        
        # Check extracted dates
        self.assertEqual(result["entities"]["start_date"], expected_start)
        self.assertEqual(result["entities"]["end_date"], expected_end)
        
        # Test route_command response
        response = route_command(result["intent"], result["entities"], result["language"])
        
        # Check response contains expected elements
        self.assertIn("1 जून से 20 जून तक की बिक्री", response)
        self.assertIn("ऑर्डर:", response)
        self.assertIn("टॉप प्रोडक्ट:", response)
    
    def test_hindi_custom_date_range_alternate(self):
        # Test Hindi command with alternate format
        command = "रिपोर्ट दिखाओ 1 जनवरी से 31 जनवरी तक"
        result = parse_hindi_command(command)
        
        # Check intent and language
        self.assertEqual(result["intent"], "get_report")
        self.assertEqual(result["language"], "hi")
        
        # Check entities
        self.assertIn("start_date", result["entities"])
        self.assertIn("end_date", result["entities"])
        
        # Get current year for comparison
        import datetime
        current_year = datetime.datetime.now().year
        
        # Format expected dates
        expected_start = f"{current_year}-01-01"
        expected_end = f"{current_year}-01-31"
        
        # Check extracted dates
        self.assertEqual(result["entities"]["start_date"], expected_start)
        self.assertEqual(result["entities"]["end_date"], expected_end)
        
        # Test route_command response
        response = route_command(result["intent"], result["entities"], result["language"])
        
        # Check response contains expected elements
        self.assertIn("1 जनवरी से 31 जनवरी तक की बिक्री", response)
        self.assertIn("ऑर्डर:", response)
        self.assertIn("टॉप प्रोडक्ट:", response)
    
    def test_numeric_date_format(self):
        # Test with numeric date format
        command = "Get report from 01/06 to 20/06"
        result = parse_command(command)
        
        # Check intent and language
        self.assertEqual(result["intent"], "get_report")
        self.assertEqual(result["language"], "en")
        
        # Check entities
        self.assertIn("start_date", result["entities"])
        self.assertIn("end_date", result["entities"])
        
        # Get current year for comparison
        import datetime
        current_year = datetime.datetime.now().year
        
        # Format expected dates
        expected_start = f"{current_year}-06-01"
        expected_end = f"{current_year}-06-20"
        
        # Check extracted dates
        self.assertEqual(result["entities"]["start_date"], expected_start)
        self.assertEqual(result["entities"]["end_date"], expected_end)


if __name__ == "__main__":
    unittest.main()