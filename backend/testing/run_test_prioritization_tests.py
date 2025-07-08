#!/usr/bin/env python3
"""
Script to run all test cases for the test prioritization framework.

This script runs all the test cases for the test prioritization framework,
including tests for the TestPrioritizer class, run_prioritized_tests.py,
and the integration with run_all_tests.py.
"""

import os
import sys
import unittest
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("run_test_prioritization_tests")

# Constants
BASE_DIR = Path(__file__).resolve().parent
TEST_PRIORITIZATION_FRAMEWORK_TEST = BASE_DIR / "test_prioritization_framework.py"
RUN_PRIORITIZED_TESTS_TEST = BASE_DIR / "test_run_prioritized_tests.py"
RUN_ALL_TESTS_INTEGRATION_TEST = BASE_DIR / "test_run_all_tests_integration.py"


def run_test_suite(test_script):
    """Run a test suite."""
    logger.info(f"Running test suite: {test_script}")
    
    # Run the test script
    result = os.system(f"{sys.executable} {test_script}")
    
    # Check the result
    if result == 0:
        logger.info(f"Test suite passed: {test_script}")
        return True
    else:
        logger.error(f"Test suite failed: {test_script}")
        return False


def run_all_test_suites():
    """Run all test suites."""
    # List of test scripts to run
    test_scripts = [
        TEST_PRIORITIZATION_FRAMEWORK_TEST,
        RUN_PRIORITIZED_TESTS_TEST,
        RUN_ALL_TESTS_INTEGRATION_TEST
    ]
    
    # Run each test suite
    results = {}
    for test_script in test_scripts:
        if os.path.exists(test_script):
            results[test_script.name] = run_test_suite(test_script)
        else:
            logger.warning(f"Test script not found: {test_script}")
            results[test_script.name] = False
    
    # Print summary
    logger.info("\nTest results summary:")
    for test_script, success in results.items():
        logger.info(f"{test_script}: {'PASS' if success else 'FAIL'}")
    
    # Return True if all tests passed, False otherwise
    return all(results.values())


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run all test cases for the test prioritization framework")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Run all test suites
    success = run_all_test_suites()
    
    # Return exit code
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())