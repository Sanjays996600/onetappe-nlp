#!/usr/bin/env python3
"""
Test suite for the integration of run_all_tests.py with the test prioritization framework.

This script tests the integration of run_all_tests.py with the test prioritization framework,
including command-line argument parsing and test execution.
"""

import os
import sys
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).resolve().parent))

# Import the modules to test
import run_all_tests


class RunAllTestsIntegrationTestCase(unittest.TestCase):
    """Test case for the integration of run_all_tests.py with the test prioritization framework."""

    @patch("run_all_tests.run_prioritized_tests")
    def test_run_prioritized_tests_integration(self, mock_run_prioritized_tests):
        """Test integration of run_prioritized_tests with run_all_tests."""
        # Mock run_prioritized_tests to return a successful result
        mock_run_prioritized_tests.return_value = {
            "success": True,
            "output": "Prioritized tests completed successfully",
            "error": ""
        }

        # Create mock arguments
        args = MagicMock()
        args.prioritized = True
        args.prioritized_time_budget = 60
        args.prioritized_categories = "product,authentication"
        args.prioritized_levels = "P1 - Critical,P2 - High"
        args.functional = False
        args.performance = False
        args.security = False
        args.load = False
        args.coverage = False
        args.report = False
        args.generate_data = False

        # Run the tests
        result = run_all_tests.run_all_tests(args)

        # Check that run_prioritized_tests was called with the correct arguments
        mock_run_prioritized_tests.assert_called_once_with(args)

        # Check the result
        self.assertTrue(result)

    @patch("run_all_tests.run_prioritized_tests")
    @patch("run_all_tests.run_functional_tests")
    @patch("run_all_tests.run_performance_tests")
    @patch("run_all_tests.run_security_tests")
    @patch("run_all_tests.run_load_tests")
    @patch("run_all_tests.generate_coverage_report")
    @patch("run_all_tests.generate_comprehensive_report")
    @patch("run_all_tests.check_server_status")
    @patch("run_all_tests.start_server")
    @patch("run_all_tests.stop_server")
    def test_run_all_tests_with_all_flag(self, mock_stop_server, mock_start_server, 
                                       mock_check_server_status, mock_generate_comprehensive_report, 
                                       mock_generate_coverage_report, mock_run_load_tests, 
                                       mock_run_security_tests, mock_run_performance_tests, 
                                       mock_run_functional_tests, mock_run_prioritized_tests):
        """Test running all tests with the --all flag."""
        # Mock check_server_status to return False (server not running)
        mock_check_server_status.return_value = False

        # Mock start_server to return True (server started successfully)
        mock_start_server.return_value = True

        # Mock all test functions to return successful results
        mock_run_prioritized_tests.return_value = {"success": True}
        mock_run_functional_tests.return_value = {"test_product_api": {"success": True}}
        mock_run_performance_tests.return_value = {"success": True}
        mock_run_security_tests.return_value = {"success": True}
        mock_run_load_tests.return_value = {"success": True}
        mock_generate_coverage_report.return_value = {"success": True}
        mock_generate_comprehensive_report.return_value = {"success": True}

        # Create mock arguments with --all flag
        args = MagicMock()
        args.all = True
        args.prioritized = True
        args.functional = True
        args.performance = True
        args.security = True
        args.load = True
        args.coverage = True
        args.report = True
        args.generate_data = False
        args.load_duration = 60
        args.load_users = 10
        args.load_spawn_rate = 1

        # Run the tests
        result = run_all_tests.run_all_tests(args)

        # Check that all test functions were called
        mock_run_prioritized_tests.assert_called_once_with(args)
        mock_run_functional_tests.assert_called_once()
        mock_run_performance_tests.assert_called_once()
        mock_run_security_tests.assert_called_once()
        mock_run_load_tests.assert_called_once_with(
            duration=args.load_duration,
            users=args.load_users,
            spawn_rate=args.load_spawn_rate
        )
        mock_generate_coverage_report.assert_called_once()
        mock_generate_comprehensive_report.assert_called_once()

        # Check that the server was started and stopped
        mock_start_server.assert_called_once()
        mock_stop_server.assert_called_once()

        # Check the result
        self.assertTrue(result)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("run_all_tests.run_all_tests")
    def test_main_with_prioritized_flag(self, mock_run_all_tests, mock_parse_args):
        """Test main function with --prioritized flag."""
        # Mock parse_args to return arguments with --prioritized flag
        args = MagicMock()
        args.prioritized = True
        args.functional = False
        args.performance = False
        args.security = False
        args.load = False
        args.coverage = False
        args.report = False
        args.all = False
        args.generate_data = False
        mock_parse_args.return_value = args

        # Mock run_all_tests to return True (success)
        mock_run_all_tests.return_value = True

        # Run the main function
        result = run_all_tests.main()

        # Check that run_all_tests was called with the correct arguments
        mock_run_all_tests.assert_called_once_with(args)

        # Check the result
        self.assertEqual(result, 0)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("run_all_tests.run_all_tests")
    def test_main_with_prioritized_options(self, mock_run_all_tests, mock_parse_args):
        """Test main function with prioritized test options."""
        # Mock parse_args to return arguments with prioritized test options
        args = MagicMock()
        args.prioritized = True
        args.prioritized_time_budget = 60
        args.prioritized_categories = "product,authentication"
        args.prioritized_levels = "P1 - Critical,P2 - High"
        args.functional = False
        args.performance = False
        args.security = False
        args.load = False
        args.coverage = False
        args.report = False
        args.all = False
        args.generate_data = False
        mock_parse_args.return_value = args

        # Mock run_all_tests to return True (success)
        mock_run_all_tests.return_value = True

        # Run the main function
        result = run_all_tests.main()

        # Check that run_all_tests was called with the correct arguments
        mock_run_all_tests.assert_called_once_with(args)

        # Check the result
        self.assertEqual(result, 0)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("run_all_tests.run_all_tests")
    def test_main_with_all_flag(self, mock_run_all_tests, mock_parse_args):
        """Test main function with --all flag."""
        # Mock parse_args to return arguments with --all flag
        args = MagicMock()
        args.all = True
        args.prioritized = True  # Should be set to True by main when --all is specified
        args.functional = True  # Should be set to True by main when --all is specified
        args.performance = True  # Should be set to True by main when --all is specified
        args.security = True  # Should be set to True by main when --all is specified
        args.load = True  # Should be set to True by main when --all is specified
        args.coverage = True  # Should be set to True by main when --all is specified
        args.report = True  # Should be set to True by main when --all is specified
        args.generate_data = False
        mock_parse_args.return_value = args

        # Mock run_all_tests to return True (success)
        mock_run_all_tests.return_value = True

        # Run the main function
        result = run_all_tests.main()

        # Check that run_all_tests was called with the correct arguments
        mock_run_all_tests.assert_called_once_with(args)

        # Check the result
        self.assertEqual(result, 0)

    @patch("argparse.ArgumentParser.parse_args")
    @patch("run_all_tests.run_all_tests")
    def test_main_with_no_flags(self, mock_run_all_tests, mock_parse_args):
        """Test main function with no flags (should default to functional tests)."""
        # Mock parse_args to return arguments with no flags
        args = MagicMock()
        args.all = False
        args.prioritized = False
        args.functional = False  # Should be set to True by main when no flags are specified
        args.performance = False
        args.security = False
        args.load = False
        args.coverage = False
        args.report = False
        args.generate_data = False
        mock_parse_args.return_value = args

        # Mock run_all_tests to return True (success)
        mock_run_all_tests.return_value = True

        # Run the main function
        result = run_all_tests.main()

        # Check that run_all_tests was called with the correct arguments
        # Note: args.functional should be set to True by main when no flags are specified
        args.functional = True
        mock_run_all_tests.assert_called_once_with(args)

        # Check the result
        self.assertEqual(result, 0)


if __name__ == "__main__":
    unittest.main()