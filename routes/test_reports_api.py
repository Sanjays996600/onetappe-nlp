import unittest
import sys
import os
import pytz
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock, AsyncMock
import asyncio
from typing import Optional

# Add parent directory to path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.reports import get_date_range, IST_TZ


class TestDateRangeFunction(unittest.TestCase):
    
    def test_get_date_range_today(self):
        """Test that get_date_range correctly handles 'today' range"""
        # Get today's date in IST
        today_ist = datetime.now(IST_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
        expected_start = today_ist
        expected_end = today_ist + timedelta(days=1) - timedelta(microseconds=1)
        
        # Convert to UTC for comparison
        expected_start_utc = expected_start.astimezone(pytz.UTC)
        expected_end_utc = expected_end.astimezone(pytz.UTC)
        
        # Call the function
        start_date, end_date = get_date_range("today")
        
        # Verify the dates
        self.assertEqual(start_date.date(), expected_start_utc.date())
        self.assertEqual(end_date.date(), expected_end_utc.date())
        self.assertEqual(start_date.tzinfo, pytz.UTC)
        self.assertEqual(end_date.tzinfo, pytz.UTC)
    
    def test_get_date_range_yesterday(self):
        """Test that get_date_range correctly handles 'yesterday' range"""
        # Get today's date in IST
        today_ist = datetime.now(IST_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
        # Yesterday
        yesterday_ist = today_ist - timedelta(days=1)
        expected_start = yesterday_ist
        expected_end = yesterday_ist + timedelta(days=1) - timedelta(microseconds=1)
        
        # Convert to UTC for comparison
        expected_start_utc = expected_start.astimezone(pytz.UTC)
        expected_end_utc = expected_end.astimezone(pytz.UTC)
        
        # Call the function
        start_date, end_date = get_date_range("yesterday")
        
        # Verify the dates
        self.assertEqual(start_date.date(), expected_start_utc.date())
        self.assertEqual(end_date.date(), expected_end_utc.date())
        self.assertEqual(start_date.tzinfo, pytz.UTC)
        self.assertEqual(end_date.tzinfo, pytz.UTC)
    
    def test_get_date_range_this_week(self):
        """Test that get_date_range correctly handles 'this-week' range"""
        # Get today's date in IST
        today_ist = datetime.now(IST_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
        # Start of week (Monday)
        start_of_week = today_ist - timedelta(days=today_ist.weekday())
        # End of week (Sunday)
        end_of_week = start_of_week + timedelta(days=7) - timedelta(microseconds=1)
        
        # Convert to UTC for comparison
        expected_start_utc = start_of_week.astimezone(pytz.UTC)
        expected_end_utc = end_of_week.astimezone(pytz.UTC)
        
        # Call the function
        start_date, end_date = get_date_range("this-week")
        
        # Verify the dates
        self.assertEqual(start_date.date(), expected_start_utc.date())
        self.assertEqual(end_date.date(), expected_end_utc.date())
        self.assertEqual(start_date.tzinfo, pytz.UTC)
        self.assertEqual(end_date.tzinfo, pytz.UTC)
    
    def test_get_date_range_this_month(self):
        """Test that get_date_range correctly handles 'this-month' range"""
        # Get today's date in IST
        today_ist = datetime.now(IST_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
        # Start of month
        start_of_month = today_ist.replace(day=1)
        # End of month
        if today_ist.month == 12:
            end_of_month = today_ist.replace(year=today_ist.year+1, month=1, day=1) - timedelta(microseconds=1)
        else:
            end_of_month = today_ist.replace(month=today_ist.month+1, day=1) - timedelta(microseconds=1)
        
        # Convert to UTC for comparison
        expected_start_utc = start_of_month.astimezone(pytz.UTC)
        expected_end_utc = end_of_month.astimezone(pytz.UTC)
        
        # Call the function
        start_date, end_date = get_date_range("this-month")
        
        # Verify the dates
        self.assertEqual(start_date.date(), expected_start_utc.date())
        self.assertEqual(end_date.date(), expected_end_utc.date())
        self.assertEqual(start_date.tzinfo, pytz.UTC)
        self.assertEqual(end_date.tzinfo, pytz.UTC)
    
    def test_get_date_range_custom(self):
        """Test that get_date_range correctly handles custom date range"""
        # Define a custom date range
        custom_range = "2023-06-01,2023-06-30"
        
        # Call the function
        start_date, end_date = get_date_range(custom_range)
        
        # Verify the dates are in UTC
        self.assertEqual(start_date.tzinfo, pytz.UTC)
        self.assertEqual(end_date.tzinfo, pytz.UTC)
        
        # The function parses dates directly in UTC, not IST
        # So 2023-06-01 in the string becomes 2023-06-01 00:00:00 UTC
        self.assertEqual(start_date.year, 2023)
        self.assertEqual(start_date.month, 6)
        self.assertEqual(start_date.day, 1)
        self.assertEqual(start_date.hour, 0)
        self.assertEqual(start_date.minute, 0)
        self.assertEqual(start_date.second, 0)
        
        # End date should be set to end of day
        self.assertEqual(end_date.year, 2023)
        self.assertEqual(end_date.month, 6)
        self.assertEqual(end_date.day, 30)
        self.assertEqual(end_date.hour, 23)
        self.assertEqual(end_date.minute, 59)
        self.assertEqual(end_date.second, 59)
        self.assertEqual(end_date.microsecond, 999999)
    
    def test_get_date_range_invalid_format(self):
        """Test that get_date_range handles invalid date formats gracefully"""
        # Invalid format should default to today
        today_ist = datetime.now(IST_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
        expected_start = today_ist
        expected_end = today_ist + timedelta(days=1) - timedelta(microseconds=1)
        
        # Convert to UTC for comparison
        expected_start_utc = expected_start.astimezone(pytz.UTC)
        expected_end_utc = expected_end.astimezone(pytz.UTC)
        
        # Call the function with invalid format
        start_date, end_date = get_date_range("invalid-format")
        
        # Verify the dates default to today
        self.assertEqual(start_date.date(), expected_start_utc.date())
        self.assertEqual(end_date.date(), expected_end_utc.date())
        
    def test_get_date_range_invalid_custom_format(self):
        """Test that get_date_range handles invalid custom date formats gracefully"""
        # Invalid custom format should default to today
        today_ist = datetime.now(IST_TZ).replace(hour=0, minute=0, second=0, microsecond=0)
        expected_start = today_ist
        expected_end = today_ist + timedelta(days=1) - timedelta(microseconds=1)
        
        # Convert to UTC for comparison
        expected_start_utc = expected_start.astimezone(pytz.UTC)
        expected_end_utc = expected_end.astimezone(pytz.UTC)
        
        # Call the function with invalid custom format
        start_date, end_date = get_date_range("2023-06-01,invalid-date")
        
        # Verify the dates default to today
        self.assertEqual(start_date.date(), expected_start_utc.date())
        self.assertEqual(end_date.date(), expected_end_utc.date())


if __name__ == "__main__":
    unittest.main()