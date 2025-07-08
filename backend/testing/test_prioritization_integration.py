#!/usr/bin/env python3
"""
Test suite for the integration of the test prioritization framework with the existing test suite.

This script tests the integration of the test prioritization framework with the existing test suite,
including the ability to prioritize and run tests from the existing test suite.
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
from prioritize_test_cases import TestPrioritizer
from run_prioritized_tests import run_test_suite


class TestPrioritizationIntegrationTestCase(unittest.TestCase):
    """Test case for the integration of the test prioritization framework with the existing test suite."""

    def setUp(self):
        """Set up test fixtures."""
        # Create a TestPrioritizer instance with sample data
        self.prioritizer = TestPrioritizer()
        
        # Sample test cases for the existing test suite
        self.sample_test_cases = {
            "test_product_listing": {
                "file": "test_product_api_suite.py",
                "function": "test_product_listing",
                "category": "product",
                "description": "Test product listing API",
                "business_impact": 5,
                "failure_probability": 3,
                "execution_time": 2.5,
                "code_coverage": 4
            },
            "test_product_detail": {
                "file": "test_product_api_suite.py",
                "function": "test_product_detail",
                "category": "product",
                "description": "Test product detail API",
                "business_impact": 4,
                "failure_probability": 2,
                "execution_time": 2.0,
                "code_coverage": 3
            },
            "test_user_login": {
                "file": "test_authentication.py",
                "function": "test_user_login",
                "category": "authentication",
                "description": "Test user login functionality",
                "business_impact": 5,
                "failure_probability": 4,
                "execution_time": 1.5,
                "code_coverage": 3
            },
            "test_user_registration": {
                "file": "test_authentication.py",
                "function": "test_user_registration",
                "category": "authentication",
                "description": "Test user registration functionality",
                "business_impact": 4,
                "failure_probability": 3,
                "execution_time": 2.0,
                "code_coverage": 3
            },
            "test_seller_dashboard_access": {
                "file": "test_seller_dashboard.py",
                "function": "test_seller_dashboard_access",
                "category": "seller_dashboard",
                "description": "Test seller dashboard access",
                "business_impact": 4,
                "failure_probability": 2,
                "execution_time": 3.0,
                "code_coverage": 3
            },
            "test_seller_product_management": {
                "file": "test_seller_dashboard.py",
                "function": "test_seller_product_management",
                "category": "seller_dashboard",
                "description": "Test seller product management",
                "business_impact": 4,
                "failure_probability": 3,
                "execution_time": 3.5,
                "code_coverage": 4
            },
            "test_product_search_performance": {
                "file": "performance_test.py",
                "function": "test_product_search_performance",
                "category": "performance",
                "description": "Test product search performance",
                "business_impact": 3,
                "failure_probability": 2,
                "execution_time": 5.0,
                "code_coverage": 2
            },
            "test_checkout_performance": {
                "file": "performance_test.py",
                "function": "test_checkout_performance",
                "category": "performance",
                "description": "Test checkout performance",
                "business_impact": 4,
                "failure_probability": 3,
                "execution_time": 6.0,
                "code_coverage": 3
            },
            "test_sql_injection": {
                "file": "security_test.py",
                "function": "test_sql_injection",
                "category": "security",
                "description": "Test SQL injection prevention",
                "business_impact": 5,
                "failure_probability": 1,
                "execution_time": 4.0,
                "code_coverage": 2
            },
            "test_xss_prevention": {
                "file": "security_test.py",
                "function": "test_xss_prevention",
                "category": "security",
                "description": "Test XSS prevention",
                "business_impact": 5,
                "failure_probability": 2,
                "execution_time": 3.5,
                "code_coverage": 2
            }
        }
        
        # Set the test cases in the prioritizer
        self.prioritizer.test_cases = self.sample_test_cases

    def test_prioritization_with_existing_test_suite(self):
        """Test prioritization with the existing test suite."""
        # Prioritize the test cases
        prioritized_tests = self.prioritizer.prioritize_tests()
        
        # Check that all test cases are included
        self.assertEqual(len(prioritized_tests), len(self.sample_test_cases))
        
        # Check that test cases are sorted by priority score (descending)
        for i in range(len(prioritized_tests) - 1):
            self.assertGreaterEqual(
                prioritized_tests[i]["priority_score"],
                prioritized_tests[i + 1]["priority_score"]
            )
        
        # Check that high business impact tests are prioritized
        high_impact_tests = [t for t in prioritized_tests if self.sample_test_cases[t["function"]]["business_impact"] >= 5]
        for test in high_impact_tests:
            self.assertIn(test["priority_level"], ["P1 - Critical", "P2 - High"])

    def test_generate_test_suite_with_time_budget(self):
        """Test generating a test suite with a time budget."""
        # Prioritize the test cases
        self.prioritizer.prioritize_tests()
        
        # Generate a test suite with a time budget of 10 seconds
        test_suite = self.prioritizer.generate_test_suite(time_budget=10)
        
        # Calculate the total execution time
        total_time = sum(self.sample_test_cases[test["function"]]["execution_time"] for test in test_suite)
        
        # Check that the test suite fits within the time budget
        self.assertLessEqual(total_time, 10)
        
        # Check that the test suite includes the highest priority tests
        prioritized_tests = self.prioritizer.prioritize_tests()
        highest_priority_test = prioritized_tests[0]["function"]
        self.assertIn(highest_priority_test, [test["function"] for test in test_suite])

    def test_generate_test_suite_with_categories(self):
        """Test generating a test suite with specific categories."""
        # Prioritize the test cases
        self.prioritizer.prioritize_tests()
        
        # Generate a test suite with specific categories
        categories = ["product", "authentication"]
        test_suite = self.prioritizer.generate_test_suite(categories=categories)
        
        # Check that all tests in the suite belong to the specified categories
        for test in test_suite:
            test_case = self.sample_test_cases[test["function"]]
            self.assertIn(test_case["category"], categories)
        
        # Check that all tests from the specified categories are included
        category_tests = [name for name, test in self.sample_test_cases.items() if test["category"] in categories]
        self.assertEqual(len(test_suite), len(category_tests))

    def test_generate_test_suite_with_priority_levels(self):
        """Test generating a test suite with specific priority levels."""
        # Prioritize the test cases
        self.prioritizer.prioritize_tests()
        
        # Generate a test suite with specific priority levels
        priority_levels = ["P1 - Critical", "P2 - High"]
        test_suite = self.prioritizer.generate_test_suite(priority_levels=priority_levels)
        
        # Check that all tests in the suite have the specified priority levels
        for test in test_suite:
            self.assertIn(test["priority_level"], priority_levels)

    @patch("subprocess.run")
    def test_run_test_suite_integration(self, mock_run):
        """Test running a test suite with the existing test suite."""
        # Mock subprocess.run to return successful results
        mock_process = MagicMock()
        mock_process.returncode = 0
        mock_process.stdout = "Test passed"
        mock_process.stderr = ""
        mock_run.return_value = mock_process
        
        # Prioritize the test cases
        self.prioritizer.prioritize_tests()
        
        # Generate a test suite with a time budget of 10 seconds
        test_suite = self.prioritizer.generate_test_suite(time_budget=10)
        
        # Run the test suite
        results = run_test_suite(test_suite, no_server=True, timeout=10)
        
        # Check that subprocess.run was called for each test
        self.assertEqual(mock_run.call_count, len(test_suite))
        
        # Check that the results include all tests in the suite
        self.assertEqual(len(results), len(test_suite))
        
        # Check that all tests passed
        for result in results:
            self.assertEqual(result["outcome"], "pass")

    def test_export_to_formats(self):
        """Test exporting prioritized tests to different formats."""
        # Prioritize the test cases
        self.prioritizer.prioritize_tests()
        
        # Create temporary files for export
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as json_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as csv_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".md") as md_file:
            json_path = json_file.name
            csv_path = csv_file.name
            md_path = md_file.name
        
        try:
            # Export to different formats
            self.prioritizer.save_prioritized_tests(json_path)
            self.prioritizer.export_to_csv(csv_path)
            self.prioritizer.export_to_markdown(md_path)
            
            # Check that the files were created
            self.assertTrue(os.path.exists(json_path))
            self.assertTrue(os.path.exists(csv_path))
            self.assertTrue(os.path.exists(md_path))
            
            # Check the JSON file content
            with open(json_path, "r") as f:
                json_content = json.load(f)
                self.assertEqual(len(json_content), len(self.sample_test_cases))
            
            # Check the CSV file content
            with open(csv_path, "r") as f:
                csv_content = f.read()
                self.assertIn("function,file,category,priority_level,priority_score", csv_content)
                for test_name in self.sample_test_cases.keys():
                    self.assertIn(test_name, csv_content)
            
            # Check the Markdown file content
            with open(md_path, "r") as f:
                md_content = f.read()
                self.assertIn("# Prioritized Test Cases", md_content)
                self.assertIn("## Summary", md_content)
                self.assertIn("## Tests by Priority Level", md_content)
                self.assertIn("## Tests by Category", md_content)
                for test_name in self.sample_test_cases.keys():
                    self.assertIn(test_name, md_content)
        
        finally:
            # Clean up temporary files
            for path in [json_path, csv_path, md_path]:
                if os.path.exists(path):
                    os.unlink(path)


if __name__ == "__main__":
    unittest.main()