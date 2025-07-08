#!/usr/bin/env python3
"""
Test Runner for Multilingual NLP Tests

This script runs all the test cases for the multilingual NLP system
and generates a comprehensive test report.
"""

import sys
import os
import unittest
import time
import json
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import test modules
from test_multilingual_parser import TestMultilingualParser
from test_language_detection import TestLanguageDetection
from test_mixed_entity_extraction import TestMixedEntityExtraction

def generate_test_report(test_results, execution_time):
    """
    Generate a markdown report from test results.
    
    Args:
        test_results: TestResult object from unittest
        execution_time: Total execution time in seconds
    
    Returns:
        String containing the markdown report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate statistics
    total_tests = test_results.testsRun
    failures = len(test_results.failures)
    errors = len(test_results.errors)
    skipped = len(test_results.skipped)
    passed = total_tests - failures - errors - skipped
    success_rate = (passed / total_tests) * 100 if total_tests > 0 else 0
    
    # Generate report header
    report = f"# Multilingual NLP Test Report\n\n"
    report += f"**Generated:** {timestamp}\n\n"
    report += f"**Execution Time:** {execution_time:.2f} seconds\n\n"
    
    # Generate summary table
    report += f"## Summary\n\n"
    report += f"| Metric | Value |\n"
    report += f"|--------|-------|\n"
    report += f"| Total Tests | {total_tests} |\n"
    report += f"| Passed | {passed} |\n"
    report += f"| Failed | {failures} |\n"
    report += f"| Errors | {errors} |\n"
    report += f"| Skipped | {skipped} |\n"
    report += f"| Success Rate | {success_rate:.2f}% |\n\n"
    
    # Generate failures section if any
    if failures > 0:
        report += f"## Failures\n\n"
        for i, (test, traceback) in enumerate(test_results.failures, 1):
            report += f"### {i}. {test}\n\n"
            report += f"```\n{traceback}\n```\n\n"
    
    # Generate errors section if any
    if errors > 0:
        report += f"## Errors\n\n"
        for i, (test, traceback) in enumerate(test_results.errors, 1):
            report += f"### {i}. {test}\n\n"
            report += f"```\n{traceback}\n```\n\n"
    
    return report

def save_report(report, filename="nlp_test_report.md"):
    """
    Save the test report to a file.
    
    Args:
        report: String containing the markdown report
        filename: Name of the file to save the report to
    """
    # Create reports directory if it doesn't exist
    os.makedirs("reports", exist_ok=True)
    
    # Save report to file
    with open(os.path.join("reports", filename), "w", encoding="utf-8") as f:
        f.write(report)

def run_tests():
    """
    Run all the test cases and generate a report.
    """
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_suite.addTest(unittest.makeSuite(TestMultilingualParser))
    test_suite.addTest(unittest.makeSuite(TestLanguageDetection))
    test_suite.addTest(unittest.makeSuite(TestMixedEntityExtraction))
    
    # Run tests
    start_time = time.time()
    test_runner = unittest.TextTestRunner(verbosity=2)
    test_results = test_runner.run(test_suite)
    execution_time = time.time() - start_time
    
    # Generate and save report
    report = generate_test_report(test_results, execution_time)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    save_report(report, f"nlp_test_report_{timestamp}.md")
    
    # Return success status (True if all tests passed)
    return test_results.wasSuccessful()

def main():
    """
    Main function.
    """
    print("Running Multilingual NLP Tests...")
    success = run_tests()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()