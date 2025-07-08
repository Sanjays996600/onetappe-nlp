import unittest
import sys
import os
import pytz
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from typing import Optional
import re

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.reports import get_date_range, IST_TZ
from OneTappeProject.nlp.mixed_entity_extraction import parse_mixed_date, extract_mixed_date_range


class TestMultilingualReports(unittest.TestCase):
    """
    Test multilingual support for reports API, focusing on date parsing and range extraction
    for both English and Hindi languages, as well as mixed language inputs.
    """
    
    def test_hindi_date_parsing(self):
        """
        Test parsing of Hindi date formats using the parse_mixed_date function.
        """
        # Get current year for testing
        current_year = datetime.now().year
        
        # Test Hindi month names
        test_cases = [
            # Format: Hindi date string, expected month, expected day
            (f"1 जनवरी {current_year}", 1, 1),
            (f"15 फरवरी {current_year}", 2, 15),
            (f"31 मार्च {current_year}", 3, 31),
            (f"10 अप्रैल {current_year}", 4, 10),
            (f"20 मई {current_year}", 5, 20),
            (f"30 जून {current_year}", 6, 30),
            (f"5 जुलाई {current_year}", 7, 5),
            (f"25 अगस्त {current_year}", 8, 25),
            (f"15 सितंबर {current_year}", 9, 15),
            (f"10 अक्टूबर {current_year}", 10, 10),
            (f"11 नवंबर {current_year}", 11, 11),
            (f"25 दिसंबर {current_year}", 12, 25),
        ]
        
        for date_str, expected_month, expected_day in test_cases:
            parsed_date = parse_mixed_date(date_str)
            self.assertIsNotNone(parsed_date, f"Failed to parse Hindi date: {date_str}")
            self.assertEqual(parsed_date.month, expected_month)
            self.assertEqual(parsed_date.day, expected_day)
            self.assertEqual(parsed_date.year, current_year)
    
    def test_transliterated_hindi_date_parsing(self):
        """
        Test parsing of transliterated Hindi (Hinglish) date formats.
        """
        current_year = datetime.now().year
        
        # Test transliterated Hindi month names
        test_cases = [
            # Format: Transliterated Hindi date string, expected month, expected day
            (f"1 janvari {current_year}", 1, 1),
            (f"15 farvari {current_year}", 2, 15),
            (f"31 march {current_year}", 3, 31),
            (f"10 april {current_year}", 4, 10),
            (f"20 mai {current_year}", 5, 20),
            (f"30 june {current_year}", 6, 30),
            (f"5 july {current_year}", 7, 5),
            (f"25 august {current_year}", 8, 25),
            (f"15 september {current_year}", 9, 15),
            (f"10 october {current_year}", 10, 10),
            (f"11 november {current_year}", 11, 11),
            (f"25 december {current_year}", 12, 25),
        ]
        
        for date_str, expected_month, expected_day in test_cases:
            parsed_date = parse_mixed_date(date_str)
            self.assertIsNotNone(parsed_date, f"Failed to parse transliterated Hindi date: {date_str}")
            self.assertEqual(parsed_date.month, expected_month)
            self.assertEqual(parsed_date.day, expected_day)
            self.assertEqual(parsed_date.year, current_year)
    
    def test_mixed_language_date_parsing(self):
        """
        Test parsing of mixed language date formats (Hindi-English hybrid).
        """
        current_year = datetime.now().year
        
        # Test mixed language date formats
        test_cases = [
            # Format: Mixed language date string, expected month, expected day
            (f"1 जनवरी {current_year}", 1, 1),  # Hindi month
            (f"15 February {current_year}", 2, 15),  # English month
            (f"31 मार्च {current_year}", 3, 31),  # Hindi month
            (f"10 April {current_year}", 4, 10),  # English month
            (f"जनवरी 1 {current_year}", 1, 1),  # Hindi month first
            (f"February 15 {current_year}", 2, 15),  # English month first
        ]
        
        for date_str, expected_month, expected_day in test_cases:
            parsed_date = parse_mixed_date(date_str)
            self.assertIsNotNone(parsed_date, f"Failed to parse mixed language date: {date_str}")
            self.assertEqual(parsed_date.month, expected_month)
            self.assertEqual(parsed_date.day, expected_day)
            self.assertEqual(parsed_date.year, current_year)
    
    def test_mixed_date_range_extraction(self):
        """
        Test extraction of date ranges from mixed language commands.
        """
        test_cases = [
            # Format: Command, expected period
            ("आज का report दिखाओ", "today"),
            ("कल के orders", "yesterday"),
            ("इस हफ्ते का report", "week"),
            ("इस महीने का report", "month"),
            ("पिछले 7 दिन का report", "last_7_days"),
            ("last 10 दिनों का report", "last_10_days"),
            ("pichhle hafte ka report", "last_week"),
            ("पिछले महीने का report", "last_month"),
            ("सभी orders दिखाओ", "all"),
            ("Show report from 1 जनवरी to 31 जनवरी", "custom"),
            ("1 January से 31 January तक का report", "custom"),
        ]
        
        for command, expected_period in test_cases:
            result = extract_mixed_date_range(command)
            self.assertIsNotNone(result, f"Failed to extract date range from: {command}")
            if expected_period == "custom":
                self.assertEqual(result.get("range", ""), expected_period)
            else:
                self.assertEqual(result.get("period", ""), expected_period)
    
    def test_get_date_range_with_hindi_input(self):
        """
        Test that get_date_range correctly handles Hindi date range inputs.
        
        This test simulates the integration of the mixed_entity_extraction module
        with the reports API by manually extracting the date range and then passing
        it to get_date_range.
        """
        # Test cases with Hindi commands and expected date ranges
        test_cases = [
            ("आज का report", "today"),
            ("इस हफ्ते का report", "this-week"),
            ("इस महीने का report", "this-month"),
            ("1 जनवरी से 31 जनवरी तक का report", "2023-01-01,2023-01-31"),  # Custom date range
        ]
        
        for command, expected_range in test_cases:
            # For custom date range, we need to extract the dates and format them
            if "से" in command and "तक" in command:
                # Extract dates using regex (simplified for test)
                match = re.search(r'(\d+)\s+([^\s]+)\s+से\s+(\d+)\s+([^\s]+)\s+तक', command)
                if match:
                    day1, month1, day2, month2 = match.groups()
                    # Map Hindi month names to numbers (simplified)
                    month_map = {
                        "जनवरी": "01", "फरवरी": "02", "मार्च": "03", "अप्रैल": "04",
                        "मई": "05", "जून": "06", "जुलाई": "07", "अगस्त": "08",
                        "सितंबर": "09", "अक्टूबर": "10", "नवंबर": "11", "दिसंबर": "12"
                    }
                    # Format as YYYY-MM-DD,YYYY-MM-DD
                    formatted_range = f"2023-{month_map.get(month1, '01')}-{day1:0>2},2023-{month_map.get(month2, '01')}-{day2:0>2}"
                    start_date, end_date = get_date_range(formatted_range)
                else:
                    # Fallback to today if parsing fails
                    start_date, end_date = get_date_range("today")
            else:
                # Map Hindi time periods to English
                period_map = {
                    "आज": "today",
                    "इस हफ्ते": "this-week",
                    "इस महीने": "this-month"
                }
                # Find the matching period
                for hindi_period, english_period in period_map.items():
                    if hindi_period in command:
                        start_date, end_date = get_date_range(english_period)
                        break
                else:
                    # Fallback to today if no match
                    start_date, end_date = get_date_range("today")
            
            # Verify that dates are in UTC
            self.assertEqual(start_date.tzinfo, pytz.UTC)
            self.assertEqual(end_date.tzinfo, pytz.UTC)
            
            # For predefined ranges, verify the correct range is used
            if expected_range == "today":
                # Today should be from 00:00:00 to 23:59:59.999999
                today_ist = datetime.now(IST_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
                expected_start = today_ist.astimezone(pytz.UTC)
                expected_end = (today_ist + timedelta(days=1) - timedelta(microseconds=1)).astimezone(pytz.UTC)
                
                self.assertEqual(start_date.date(), expected_start.date())
                self.assertEqual(end_date.date(), expected_end.date())


if __name__ == "__main__":
    unittest.main()