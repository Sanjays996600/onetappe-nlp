#!/usr/bin/env python3
"""
Test suite for the test prioritization framework.

This script tests the functionality of the test prioritization framework,
including the TestPrioritizer class, priority calculation, and test suite generation.
"""

import os
import sys
import json
import unittest
import tempfile
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).resolve().parent))

# Import the modules to test
from prioritize_test_cases import TestPrioritizer, RISK_WEIGHTS, EFFICIENCY_WEIGHTS


class TestPrioritizationFrameworkTestCase(unittest.TestCase):
    """Test case for the test prioritization framework."""

    def setUp(self):
        """Set up test fixtures."""
        # Sample test cases for testing
        self.sample_test_cases = {
            "test_product_listing": {
                "file": "test_product_api_suite.py",
                "function": "test_product_listing",
                "category": "product",
                "description": "Test product listing API",
                "business_impact": 5,  # High impact
                "failure_probability": 3,  # Medium probability
                "execution_time": 2.5,  # 2.5 seconds
                "code_coverage": 4,  # Good coverage
            },
            "test_user_login": {
                "file": "test_authentication.py",
                "function": "test_user_login",
                "category": "authentication",
                "description": "Test user login functionality",
                "business_impact": 5,  # High impact
                "failure_probability": 4,  # High probability
                "execution_time": 1.5,  # 1.5 seconds
                "code_coverage": 3,  # Medium coverage
            },
            "test_seller_dashboard_access": {
                "file": "test_seller_dashboard.py",
                "function": "test_seller_dashboard_access",
                "category": "seller_dashboard",
                "description": "Test seller dashboard access",
                "business_impact": 4,  # Medium-high impact
                "failure_probability": 2,  # Low-medium probability
                "execution_time": 3.0,  # 3 seconds
                "code_coverage": 3,  # Medium coverage
            },
            "test_product_search_performance": {
                "file": "performance_test.py",
                "function": "test_product_search_performance",
                "category": "performance",
                "description": "Test product search performance",
                "business_impact": 3,  # Medium impact
                "failure_probability": 2,  # Low-medium probability
                "execution_time": 5.0,  # 5 seconds
                "code_coverage": 2,  # Low-medium coverage
            },
            "test_sql_injection": {
                "file": "security_test.py",
                "function": "test_sql_injection",
                "category": "security",
                "description": "Test SQL injection prevention",
                "business_impact": 5,  # High impact
                "failure_probability": 1,  # Low probability
                "execution_time": 4.0,  # 4 seconds
                "code_coverage": 2,  # Low-medium coverage
            },
        }

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
            },
            "test_product_search_performance": {
                "last_execution": "2023-06-15T10:39:30",
                "result": "pass",
                "execution_count": 30,
                "failure_count": 8,
                "recent_results": ["pass", "fail", "fail", "pass", "pass"]
            },
            "test_sql_injection": {
                "last_execution": "2023-06-15T10:43:30",
                "result": "pass",
                "execution_count": 25,
                "failure_count": 0,
                "recent_results": ["pass", "pass", "pass", "pass", "pass"]
            },
        }

        # Create a TestPrioritizer instance
        self.prioritizer = TestPrioritizer(
            test_cases=self.sample_test_cases,
            test_history=self.sample_test_history
        )

    def test_risk_score_calculation(self):
        """Test risk score calculation."""
        # Calculate risk score for test_user_login
        test_case = self.sample_test_cases["test_user_login"]
        risk_score = self.prioritizer._calculate_risk_score(test_case)

        # Expected risk score calculation
        expected_score = (
            test_case["business_impact"] * RISK_WEIGHTS["business_impact"] +
            test_case["failure_probability"] * RISK_WEIGHTS["failure_probability"]
        ) / sum(RISK_WEIGHTS.values())

        self.assertAlmostEqual(risk_score, expected_score, places=2)

    def test_efficiency_score_calculation(self):
        """Test efficiency score calculation."""
        # Calculate efficiency score for test_user_login
        test_case = self.sample_test_cases["test_user_login"]
        efficiency_score = self.prioritizer._calculate_efficiency_score(test_case)

        # Expected efficiency score calculation
        # Note: execution_time is inverted (1/time) for efficiency
        expected_score = (
            (1 / test_case["execution_time"]) * EFFICIENCY_WEIGHTS["execution_time"] +
            test_case["code_coverage"] * EFFICIENCY_WEIGHTS["code_coverage"]
        ) / sum(EFFICIENCY_WEIGHTS.values())

        self.assertAlmostEqual(efficiency_score, expected_score, places=2)

    def test_prioritization(self):
        """Test test case prioritization."""
        # Prioritize test cases
        prioritized_tests = self.prioritizer.prioritize_tests()

        # Check that all test cases are included
        self.assertEqual(len(prioritized_tests), len(self.sample_test_cases))

        # Check that test cases are sorted by priority score (descending)
        for i in range(len(prioritized_tests) - 1):
            self.assertGreaterEqual(
                prioritized_tests[i]["priority_score"],
                prioritized_tests[i + 1]["priority_score"]
            )

    def test_priority_level_assignment(self):
        """Test priority level assignment."""
        # Prioritize test cases
        prioritized_tests = self.prioritizer.prioritize_tests()

        # Check that all test cases have a priority level
        for test in prioritized_tests:
            self.assertIn("priority_level", test)
            self.assertIn(test["priority_level"], ["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low"])

    def test_generate_test_suite(self):
        """Test test suite generation."""
        # Prioritize test cases
        self.prioritizer.prioritize_tests()

        # Generate test suite with a time budget of 10 seconds
        test_suite = self.prioritizer.generate_test_suite(time_budget=10)

        # Calculate total execution time
        total_time = sum(self.sample_test_cases[test["function"]]["execution_time"] for test in test_suite)

        # Check that the test suite fits within the time budget
        self.assertLessEqual(total_time, 10)

    def test_generate_test_suite_with_categories(self):
        """Test test suite generation with category filtering."""
        # Prioritize test cases
        self.prioritizer.prioritize_tests()

        # Generate test suite with category filtering
        test_suite = self.prioritizer.generate_test_suite(
            time_budget=20,
            categories=["product", "authentication"]
        )

        # Check that all tests in the suite belong to the specified categories
        for test in test_suite:
            test_case = self.sample_test_cases[test["function"]]
            self.assertIn(test_case["category"], ["product", "authentication"])

    def test_generate_test_suite_with_priority_levels(self):
        """Test test suite generation with priority level filtering."""
        # Prioritize test cases
        self.prioritizer.prioritize_tests()

        # Generate test suite with priority level filtering
        test_suite = self.prioritizer.generate_test_suite(
            time_budget=20,
            priority_levels=["P1 - Critical", "P2 - High"]
        )

        # Check that all tests in the suite have the specified priority levels
        for test in test_suite:
            self.assertIn(test["priority_level"], ["P1 - Critical", "P2 - High"])

    def test_save_and_load(self):
        """Test saving and loading test cases and history."""
        # Create temporary files for test cases and history
        with tempfile.NamedTemporaryFile(delete=False, suffix=".json") as test_cases_file, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".json") as test_history_file:
            test_cases_path = test_cases_file.name
            test_history_path = test_history_file.name

        try:
            # Prioritize test cases
            self.prioritizer.prioritize_tests()

            # Save test cases and history
            self.prioritizer.save_prioritized_tests(test_cases_path)
            self.prioritizer.save_test_history(test_history_path)

            # Create a new TestPrioritizer instance and load the saved files
            new_prioritizer = TestPrioritizer()
            new_prioritizer.load_test_cases(test_cases_path)
            new_prioritizer.load_test_history(test_history_path)

            # Check that the loaded test cases and history match the original
            self.assertEqual(len(new_prioritizer.test_cases), len(self.prioritizer.test_cases))
            self.assertEqual(len(new_prioritizer.test_history), len(self.prioritizer.test_history))

            # Check a specific test case
            test_name = "test_user_login"
            self.assertEqual(
                new_prioritizer.test_cases[test_name]["business_impact"],
                self.prioritizer.test_cases[test_name]["business_impact"]
            )

            # Check a specific test history entry
            self.assertEqual(
                new_prioritizer.test_history[test_name]["failure_count"],
                self.prioritizer.test_history[test_name]["failure_count"]
            )

        finally:
            # Clean up temporary files
            for path in [test_cases_path, test_history_path]:
                if os.path.exists(path):
                    os.unlink(path)


if __name__ == "__main__":
    unittest.main()