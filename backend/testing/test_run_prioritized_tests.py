#!/usr/bin/env python3
"""
Test suite for the run_prioritized_tests.py script.

This script tests the functionality of the run_prioritized_tests.py script,
including test suite execution, history updates, and report generation.
"""

import os
import sys
import json
import unittest
import tempfile
from unittest.mock import patch, MagicMock
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).resolve().parent))

# Import the modules to test
from run_prioritized_tests import (
    run_test, run_test_suite, update_test_history,
    save_test_results, generate_test_report
)


class RunPrioritizedTestsTestCase(unittest.TestCase):
    """Test case for the run_prioritized_tests.py script."""

    def setUp(self):
        """Set up test fixtures."""
        # Sample test suite for testing
        self.sample_test_suite = [
            {
                "function": "test_product_listing",
                "file": "test_product_api_suite.py",
                "category": "product",
                "priority_level": "P1 - Critical",
                "priority_score": 4.8
            },
            {
                "function": "test_user_login",
                "file": "test_authentication.py",
                "category": "authentication",
                "priority_level": "P1 - Critical",
                "priority_score": 4.7
            },
            {
                "function": "test_seller_dashboard_access",
                "file": "test_seller_dashboard.py",
                "category": "seller_dashboard",
                "priority_level": "P2 - High",
                "priority_score": 3.9
            }
        ]

        # Sample test history
        self.sample_test_history = {
            "test_product_listing": {
                "last_execution": "2023-06-15T10:30:00",
                "result": "pass",
                "execution_count": 50,
                "failure_count": 2,
                "recent_results": ["pass", "pass", "pass", "pass", "pass"]
            },
            "test_user_login": {
                "last_execution": "2023-06-15T10:31:30",
                "result": "fail",
                "execution_count": 50,
                "failure_count": 5,
                "recent_results": ["fail", "pass", "pass", "fail", "pass"]
            },
            "test_seller_dashboard_access": {
                "last_execution": "2023-06-15T10:34:30",
                "result": "pass",
                "execution_count": 45,
                "failure_count": 1,
                "recent_results": ["pass", "pass", "pass", "pass", "fail"]
            }
        }

    @patch("subprocess.run")
    def test_run_test(self, mock_run):
        """Test running a single test."""
        # Mock subprocess.run to return a successful result
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Test passed"
        mock_process.stderr = ""
        mock_run.return_value = mock_process

        # Run a test
        test = self.sample_test_suite[0]
        result = run_test(test, timeout=10)

        # Check that subprocess.run was called with the correct arguments
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(kwargs["timeout"], 10)

        # Check the result
        self.assertEqual(result["function"], test["function"])
        self.assertEqual(result["file"], test["file"])
        self.assertEqual(result["category"], test["category"])
        self.assertEqual(result["priority_level"], test["priority_level"])
        self.assertEqual(result["outcome"], "pass")
        self.assertGreaterEqual(result["execution_time"], 0)

    @patch("run_prioritized_tests.run_test")
    def test_run_test_suite(self, mock_run_test):
        """Test running a test suite."""
        # Mock run_test to return test results
        def mock_run_test_impl(test, timeout=10):
            return {
                "function": test["function"],
                "file": test["file"],
                "category": test["category"],
                "priority_level": test["priority_level"],
                "outcome": "pass" if test["function"] != "test_user_login" else "fail",
                "execution_time": 1.0,
                "output": "Test output",
                "error": ""
            }
        
        mock_run_test.side_effect = mock_run_test_impl

        # Run the test suite
        results = run_test_suite(self.sample_test_suite, no_server=True, timeout=10)

        # Check that run_test was called for each test
        self.assertEqual(mock_run_test.call_count, len(self.sample_test_suite))

        # Check the results
        self.assertEqual(len(results), len(self.sample_test_suite))
        self.assertEqual(results[0]["function"], self.sample_test_suite[0]["function"])
        self.assertEqual(results[0]["outcome"], "pass")
        self.assertEqual(results[1]["function"], self.sample_test_suite[1]["function"])
        self.assertEqual(results[1]["outcome"], "fail")

    def test_update_test_history(self):
        """Test updating test history."""
        # Create a temporary file for test history
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as test_history_file:
            test_history_path = test_history_file.name

        try:
            # Write sample test history to the file
            with open(test_history_path, "w") as f:
                json.dump(self.sample_test_history, f)

            # Create test results
            test_results = [
                {
                    "function": "test_product_listing",
                    "file": "test_product_api_suite.py",
                    "category": "product",
                    "priority_level": "P1 - Critical",
                    "outcome": "pass",
                    "execution_time": 2.5,
                    "output": "Test output",
                    "error": ""
                },
                {
                    "function": "test_user_login",
                    "file": "test_authentication.py",
                    "category": "authentication",
                    "priority_level": "P1 - Critical",
                    "outcome": "fail",
                    "execution_time": 1.5,
                    "output": "Test output",
                    "error": "Test failed"
                }
            ]

            # Update test history
            update_test_history(test_results, test_history_path)

            # Load the updated test history
            with open(test_history_path, "r") as f:
                updated_history = json.load(f)

            # Check that the history was updated correctly
            self.assertEqual(updated_history["test_product_listing"]["result"], "pass")
            self.assertEqual(updated_history["test_product_listing"]["execution_count"], 51)
            self.assertEqual(updated_history["test_product_listing"]["failure_count"], 2)
            self.assertEqual(updated_history["test_product_listing"]["recent_results"][0], "pass")

            self.assertEqual(updated_history["test_user_login"]["result"], "fail")
            self.assertEqual(updated_history["test_user_login"]["execution_count"], 51)
            self.assertEqual(updated_history["test_user_login"]["failure_count"], 6)
            self.assertEqual(updated_history["test_user_login"]["recent_results"][0], "fail")

        finally:
            # Clean up temporary file
            if os.path.exists(test_history_path):
                os.unlink(test_history_path)

    def test_save_test_results(self):
        """Test saving test results."""
        # Create a temporary file for test results
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as test_results_file:
            test_results_path = test_results_file.name

        try:
            # Create test results
            test_results = [
                {
                    "function": "test_product_listing",
                    "file": "test_product_api_suite.py",
                    "category": "product",
                    "priority_level": "P1 - Critical",
                    "outcome": "pass",
                    "execution_time": 2.5,
                    "output": "Test output",
                    "error": ""
                },
                {
                    "function": "test_user_login",
                    "file": "test_authentication.py",
                    "category": "authentication",
                    "priority_level": "P1 - Critical",
                    "outcome": "fail",
                    "execution_time": 1.5,
                    "output": "Test output",
                    "error": "Test failed"
                }
            ]

            # Save test results
            save_test_results(test_results, test_results_path)

            # Load the saved test results
            with open(test_results_path, "r") as f:
                saved_results = json.load(f)

            # Check that the results were saved correctly
            self.assertEqual(len(saved_results), len(test_results))
            self.assertEqual(saved_results[0]["function"], test_results[0]["function"])
            self.assertEqual(saved_results[0]["outcome"], test_results[0]["outcome"])
            self.assertEqual(saved_results[1]["function"], test_results[1]["function"])
            self.assertEqual(saved_results[1]["outcome"], test_results[1]["outcome"])

        finally:
            # Clean up temporary file
            if os.path.exists(test_results_path):
                os.unlink(test_results_path)

    def test_generate_test_report(self):
        """Test generating a test report."""
        # Create a temporary file for the test report
        with tempfile.NamedTemporaryFile(delete=False, suffix=".md") as test_report_file:
            test_report_path = test_report_file.name

        try:
            # Create test results
            test_results = [
                {
                    "function": "test_product_listing",
                    "file": "test_product_api_suite.py",
                    "category": "product",
                    "priority_level": "P1 - Critical",
                    "outcome": "pass",
                    "execution_time": 2.5,
                    "output": "Test output",
                    "error": ""
                },
                {
                    "function": "test_user_login",
                    "file": "test_authentication.py",
                    "category": "authentication",
                    "priority_level": "P1 - Critical",
                    "outcome": "fail",
                    "execution_time": 1.5,
                    "output": "Test output",
                    "error": "Test failed"
                },
                {
                    "function": "test_seller_dashboard_access",
                    "file": "test_seller_dashboard.py",
                    "category": "seller_dashboard",
                    "priority_level": "P2 - High",
                    "outcome": "error",
                    "execution_time": 3.0,
                    "output": "Test output",
                    "error": "Test error"
                }
            ]

            # Generate test report
            generate_test_report(test_results, test_report_path)

            # Check that the report was generated
            self.assertTrue(os.path.exists(test_report_path))

            # Read the report content
            with open(test_report_path, "r") as f:
                report_content = f.read()

            # Check that the report contains expected sections
            self.assertIn("# Prioritized Test Report", report_content)
            self.assertIn("## Summary", report_content)
            self.assertIn("## Results by Outcome", report_content)
            self.assertIn("### Failed Tests", report_content)
            self.assertIn("### Error Tests", report_content)
            self.assertIn("### Passed Tests", report_content)
            self.assertIn("## Results by Category", report_content)
            self.assertIn("### Product", report_content)
            self.assertIn("### Authentication", report_content)
            self.assertIn("### Seller Dashboard", report_content)
            self.assertIn("## Results by Priority Level", report_content)
            self.assertIn("### P1 - Critical", report_content)
            self.assertIn("### P2 - High", report_content)
            self.assertIn("## Recommendations", report_content)
            self.assertIn("## Execution Time", report_content)

        finally:
            # Clean up temporary file
            if os.path.exists(test_report_path):
                os.unlink(test_report_path)


if __name__ == "__main__":
    unittest.main()