import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from unittest.mock import patch, MagicMock
import datetime

# Import the entity extraction module
from nlp.mixed_entity_extraction import (
    extract_mixed_date_range,
    parse_mixed_date,
    extract_mixed_product_details,
    normalize_mixed_command
)

class TestMixedEntityExtraction(unittest.TestCase):
    """Test cases for the mixed entity extraction module."""
    
    def test_extract_mixed_date_range(self):
        """Test extraction of date ranges from mixed language text."""
        # Test English date ranges
        result = extract_mixed_date_range("Show sales for last week")
        self.assertEqual(result["period"], "last_week")
        
        result = extract_mixed_date_range("Show sales for last month")
        self.assertEqual(result["period"], "last_month")
        
        result = extract_mixed_date_range("Show sales for last 30 days")
        self.assertEqual(result["period"], "last_30_days")
        
        # Test Hindi date ranges
        result = extract_mixed_date_range("पिछले हफ्ते की बिक्री दिखाओ")
        self.assertEqual(result["period"], "last_week")
        
        result = extract_mixed_date_range("पिछले महीने की बिक्री दिखाओ")
        self.assertEqual(result["period"], "last_month")
        
        result = extract_mixed_date_range("पिछले 30 दिनों की बिक्री दिखाओ")
        self.assertEqual(result["period"], "last_30_days")
        
        # Test mixed language date ranges
        result = extract_mixed_date_range("Show sales for पिछले हफ्ते")
        self.assertEqual(result["period"], "last_week")
        
        result = extract_mixed_date_range("पिछले month की sales दिखाओ")
        self.assertEqual(result["period"], "last_month")
        
        # Test custom date ranges with numeric formats
        result = extract_mixed_date_range("Show sales from 01/01/2023 to 31/01/2023")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        self.assertFalse("reversed_dates" in result)  # Dates are in correct order
        
        result = extract_mixed_date_range("01/01/2023 से 31/01/2023 तक की बिक्री दिखाओ")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        self.assertFalse("reversed_dates" in result)  # Dates are in correct order
        
        # Test the failing cases from the bug report
        # Case 1: Natural language date range
        result = extract_mixed_date_range("sales from Jan 1 to Jan 7")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        self.assertFalse("reversed_dates" in result)  # Dates are in correct order
        
        # Case 2: Date range with dash
        result = extract_mixed_date_range("sales 1 Jan – 7 Jan")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        self.assertFalse("reversed_dates" in result)  # Dates are in correct order
        
        # Case 3: Hindi date range with numeric dates
        result = extract_mixed_date_range("01/01/2023 से 07/01/2023 तक की बिक्री")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        self.assertFalse("reversed_dates" in result)  # Dates are in correct order
        
        # Test empty string
        result = extract_mixed_date_range("")
        self.assertEqual(result["period"], "today")  # Default to today
        
        # Test invalid date format
        result = extract_mixed_date_range("Show sales from 31/02/2023 to 01/03/2023")
        # The function should still recognize this as a custom date range attempt
        # even though the date is invalid
        self.assertTrue("error" in result)  # Should have error for invalid date
        
        # Test new enhanced patterns - transliterated forms
        result = extract_mixed_date_range("pichle 5 din ka report dikhao")
        self.assertEqual(result["period"], "last_5_days")
        
        result = extract_mixed_date_range("pichhle 2 hafte ka report")
        self.assertEqual(result["period"], "last_2_weeks")
        
        result = extract_mixed_date_range("past 3 mahine ka data")
        self.assertEqual(result["period"], "last_3_months")
        
        # Test new enhanced patterns - "N days/weeks/months ago" format
        result = extract_mixed_date_range("5 days ago se aaj tak")
        self.assertEqual(result["period"], "last_5_days")
        
        result = extract_mixed_date_range("2 हफ्ते पहले से अब तक")
        self.assertEqual(result["period"], "last_2_weeks")
        
        result = extract_mixed_date_range("3 months पूर्व से today")
        self.assertEqual(result["period"], "last_3_months")
        
        # Test new enhanced patterns - emoji-rich commands
        result = extract_mixed_date_range("📊 Show sales from 📅 1 Jan to 📅 7 Jan 📈")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        
        # Test new enhanced patterns - multi-line commands
        result = extract_mixed_date_range("Show sales\nfrom 1 Jan\nto 7 Jan")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        
        # Test new enhanced patterns - fuzzy date matching without explicit separators
        result = extract_mixed_date_range("Show me data Jan 1 Jan 7")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
    
    def test_parse_mixed_date(self):
        """Test parsing of mixed language date strings."""
        import datetime
        current_year = datetime.datetime.now().year
        
        # Test English date formats
        result, error = parse_mixed_date(f"01/01/{current_year}")
        self.assertIsNone(error)
        self.assertEqual(result.year, current_year)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        
        result, error = parse_mixed_date(f"January 1, {current_year}")
        self.assertIsNone(error)
        self.assertEqual(result.year, current_year)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        
        # Test Hindi date formats
        result, error = parse_mixed_date(f"1 जनवरी {current_year}")
        self.assertIsNone(error)
        self.assertEqual(result.year, current_year)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        
        # Test mixed language date formats
        result, error = parse_mixed_date(f"1 January {current_year}")
        self.assertIsNone(error)
        self.assertEqual(result.year, current_year)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        
        # Test with abbreviated month names
        result, error = parse_mixed_date(f"1 Jan {current_year}")
        self.assertIsNone(error)
        self.assertEqual(result.year, current_year)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        
        # Test formats from the bug report
        # Format: "Jan 1"
        result, error = parse_mixed_date("Jan 1")
        self.assertIsNone(error)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        
        # Format: "1 Jan"
        result, error = parse_mixed_date("1 Jan")
        self.assertIsNone(error)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        
        # Format with ordinal suffix: "1st Jan"
        result, error = parse_mixed_date("1st Jan")
        self.assertIsNone(error)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        
        # Format with dash: "01-01-YYYY"
        result, error = parse_mixed_date(f"01-01-{current_year}")
        self.assertIsNone(error)
        self.assertEqual(result.year, current_year)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
        
        # Format with dot: "01.01.YYYY"
        result, error = parse_mixed_date(f"01.01.{current_year}")
        self.assertIsNone(error)
        self.assertEqual(result.year, current_year)
        self.assertEqual(result.month, 1)
        self.assertEqual(result.day, 1)
    
    def test_extract_mixed_product_details(self):
        """Test extraction of product details from mixed language text."""
        # Test English product details
        result = extract_mixed_product_details("Add rice 5kg ₹50")
        self.assertEqual(result["product"], "rice")
        self.assertEqual(result["quantity"], "5kg")
        self.assertEqual(result["price"], "₹50")
        
        # Test Hindi product details
        result = extract_mixed_product_details("चावल 5 किलो ₹50 जोड़ो")
        self.assertEqual(result["product"], "चावल")
        self.assertEqual(result["quantity"], "5 किलो")
        self.assertEqual(result["price"], "₹50")
        
        # Test mixed language product details
        result = extract_mixed_product_details("Add चावल 5kg ₹50")
        self.assertEqual(result["product"], "चावल")
        self.assertEqual(result["quantity"], "5kg")
        self.assertEqual(result["price"], "₹50")
        
        result = extract_mixed_product_details("चावल add करो 5kg ₹50")
        self.assertEqual(result["product"], "चावल")
        self.assertEqual(result["quantity"], "5kg")
        self.assertEqual(result["price"], "₹50")
    
    def test_normalize_mixed_command(self):
        """Test normalization of mixed language commands."""
        # Test transliteration of Hindi words in Roman script
        result = normalize_mixed_command("chawal stock update karo")
        self.assertIn("चावल", result)  # "chawal" should be transliterated to "चावल"
        
        # Test with mixed script
        result = normalize_mixed_command("चावल stock update karo")
        self.assertIn("चावल", result)  # Should preserve Devanagari script
        
        # Test with numbers and special characters
        result = normalize_mixed_command("chawal 5kg ₹50 add karo")
        self.assertIn("चावल", result)  # "chawal" should be transliterated
        self.assertIn("5kg", result)  # Numbers should be preserved
        self.assertIn("₹50", result)  # Special characters should be preserved
    
    def test_edge_cases(self):
        """Test edge cases for mixed entity extraction."""
        # Test empty string
        result = extract_mixed_date_range("")
        self.assertEqual(result["period"], "today")  # Default to today
        
        # Test invalid date format
        result, error = parse_mixed_date("invalid_date")
        self.assertIsNone(result)  # Should return None for invalid dates
        self.assertIsNotNone(error)  # Should return error information
        self.assertIn("error", error)  # Error should contain an error message
        
        # Test incomplete product details
        result = extract_mixed_product_details("Add rice")
        self.assertIsNone(result)  # Should return None for incomplete details
    
    def test_invalid_dates(self):
        """Test handling of invalid date formats."""
        # Test non-existent date (31st February)
        result, error = parse_mixed_date("31/02/2023")
        self.assertIsNone(result)  # Should return None for invalid dates
        self.assertIsNotNone(error)  # Should return error information
        self.assertIn("Invalid day", error["error"])  # Error should mention invalid day
        
        # Test invalid month
        result, error = parse_mixed_date("15/13/2023")
        self.assertIsNone(result)  # Should return None for invalid dates
        self.assertIsNotNone(error)  # Should return error information
        self.assertIn("Invalid month", error["error"])  # Error should mention invalid month
        
        # Test invalid year
        result, error = parse_mixed_date("15/12/0000")
        self.assertIsNone(result)  # Should return None for invalid dates
        self.assertIsNotNone(error)  # Should return error information
        
        # Test completely malformed date
        result, error = parse_mixed_date("abc/def/ghi")
        self.assertIsNone(result)  # Should return None for invalid dates
        self.assertIsNotNone(error)  # Should return error information
    
    def test_reversed_date_ranges(self):
        """Test handling of reversed date ranges (end date before start date)."""
        # Test reversed date range in English
        result = extract_mixed_date_range("Show sales from 31/01/2023 to 01/01/2023")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        self.assertTrue("reversed_dates" in result)  # Should flag reversed dates
        self.assertTrue(result["reversed_dates"])  # Should be True for reversed dates
        self.assertTrue(result["start_date"] < result["end_date"])  # Dates should be swapped to be in correct order
        
        # Test reversed date range in Hindi
        result = extract_mixed_date_range("31/01/2023 से 01/01/2023 तक की बिक्री दिखाओ")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        self.assertTrue("reversed_dates" in result)  # Should flag reversed dates
        self.assertTrue(result["reversed_dates"])  # Should be True for reversed dates
        self.assertTrue(result["start_date"] < result["end_date"])  # Dates should be swapped to be in correct order
        
        # Test reversed date range with text dates
        result = extract_mixed_date_range("Show sales from 31 Jan to 1 Jan")
        self.assertEqual(result["period"], "custom")
        self.assertTrue("start_date" in result)
        self.assertTrue("end_date" in result)
        self.assertTrue("reversed_dates" in result)  # Should flag reversed dates
        self.assertTrue(result["reversed_dates"])  # Should be True for reversed dates
        self.assertTrue(result["start_date"] < result["end_date"])  # Dates should be swapped to be in correct order

if __name__ == "__main__":
    unittest.main()