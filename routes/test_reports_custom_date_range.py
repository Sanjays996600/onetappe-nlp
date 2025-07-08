import unittest
import sys
import os
import pytz
import asyncio
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.reports import get_date_range, IST_TZ


class TestReportsCustomDateRange(unittest.TestCase):
    def test_get_date_range_predefined(self):
        """Test predefined date ranges (today, this-week, this-month)"""
        # Test 'today' range
        start_date, end_date = get_date_range("today")
        
        # Convert back to IST for comparison
        start_date_ist = start_date.astimezone(IST_TZ)
        end_date_ist = end_date.astimezone(IST_TZ)
        
        # Get current time in IST
        ist_now = datetime.now(pytz.UTC).astimezone(IST_TZ)
        today = ist_now.replace(hour=0, minute=0, second=0, microsecond=0)
        
        # Check that start date is today at 00:00:00 IST
        self.assertEqual(start_date_ist.year, today.year)
        self.assertEqual(start_date_ist.month, today.month)
        self.assertEqual(start_date_ist.day, today.day)
        self.assertEqual(start_date_ist.hour, 0)
        self.assertEqual(start_date_ist.minute, 0)
        self.assertEqual(start_date_ist.second, 0)
        
        # Check that end date is today at 23:59:59.999999 IST
        self.assertEqual(end_date_ist.year, today.year)
        self.assertEqual(end_date_ist.month, today.month)
        self.assertEqual(end_date_ist.day, today.day)
        self.assertEqual(end_date_ist.hour, 23)
        self.assertEqual(end_date_ist.minute, 59)
        self.assertEqual(end_date_ist.second, 59)
        
        # Test 'this-week' range
        start_date, end_date = get_date_range("this-week")
        
        # Convert back to IST for comparison
        start_date_ist = start_date.astimezone(IST_TZ)
        end_date_ist = end_date.astimezone(IST_TZ)
        
        # Start date should be Monday of current week at 00:00:00 IST
        monday = today - timedelta(days=today.weekday())
        self.assertEqual(start_date_ist.year, monday.year)
        self.assertEqual(start_date_ist.month, monday.month)
        self.assertEqual(start_date_ist.day, monday.day)
        self.assertEqual(start_date_ist.hour, 0)
        self.assertEqual(start_date_ist.minute, 0)
        self.assertEqual(start_date_ist.second, 0)
        
        # End date should be Sunday of current week at 23:59:59.999999 IST
        sunday = monday + timedelta(days=6)
        self.assertEqual(end_date_ist.year, sunday.year)
        self.assertEqual(end_date_ist.month, sunday.month)
        self.assertEqual(end_date_ist.day, sunday.day)
        self.assertEqual(end_date_ist.hour, 23)
        self.assertEqual(end_date_ist.minute, 59)
        self.assertEqual(end_date_ist.second, 59)
    
    def test_get_date_range_custom_format(self):
        """Test custom date range in the format 'YYYY-MM-DD,YYYY-MM-DD'"""
        # Test with a valid custom date range
        start_date, end_date = get_date_range("2023-06-01,2023-06-30")
        
        # Verify start date (in UTC)
        self.assertEqual(start_date.year, 2023)
        self.assertEqual(start_date.month, 6)
        self.assertEqual(start_date.day, 1)
        self.assertEqual(start_date.hour, 0)
        self.assertEqual(start_date.minute, 0)
        self.assertEqual(start_date.second, 0)
        self.assertEqual(start_date.tzinfo, pytz.UTC)
        
        # Verify end date (in UTC) - should be end of day
        self.assertEqual(end_date.year, 2023)
        self.assertEqual(end_date.month, 6)
        self.assertEqual(end_date.day, 30)
        self.assertEqual(end_date.hour, 23)
        self.assertEqual(end_date.minute, 59)
        self.assertEqual(end_date.second, 59)
        self.assertEqual(end_date.tzinfo, pytz.UTC)
    
    def test_custom_date_range_direct(self):
        """Test custom date range handling directly in the get_date_range function"""
        # Test with a custom date range string
        custom_range = "2023-06-01,2023-06-30"
        start_date, end_date = get_date_range(custom_range)
        
        # Verify start date
        self.assertEqual(start_date.year, 2023)
        self.assertEqual(start_date.month, 6)
        self.assertEqual(start_date.day, 1)
        self.assertEqual(start_date.hour, 0)
        self.assertEqual(start_date.minute, 0)
        self.assertEqual(start_date.second, 0)
        
        # Verify end date (should be end of day)
        self.assertEqual(end_date.year, 2023)
        self.assertEqual(end_date.month, 6)
        self.assertEqual(end_date.day, 30)
        self.assertEqual(end_date.hour, 23)
        self.assertEqual(end_date.minute, 59)
        self.assertEqual(end_date.second, 59)


if __name__ == "__main__":
    unittest.main()