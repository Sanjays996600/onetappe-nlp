#!/usr/bin/env python3
"""
Demo script for the test prioritization framework.

This script demonstrates how to use the test prioritization framework
to prioritize and run tests for the OneTappe API.
"""

import os
import sys
import json
import argparse
import datetime
import logging
from pathlib import Path

# Add parent directory to path to import modules
sys.path.append(str(Path(__file__).resolve().parent))

# Import the modules
from prioritize_test_cases import TestPrioritizer
from run_prioritized_tests import run_test_suite, update_test_history

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger("demo_test_prioritization")

# Constants
BASE_DIR = Path(__file__).resolve().parent
TEST_CASES_FILE = BASE_DIR / "test_data" / "test_cases.json"
TEST_HISTORY_FILE = BASE_DIR / "test_data" / "test_history.json"
RESULTS_FILE = BASE_DIR / "reports" / "demo_prioritized_test_results.json"
REPORT_FILE = BASE_DIR / "reports" / "demo_prioritized_test_report.md"


def ensure_directories():
    """Ensure necessary directories exist."""
    os.makedirs(BASE_DIR / "test_data", exist_ok=True)
    os.makedirs(BASE_DIR / "reports", exist_ok=True)


def generate_sample_data():
    """Generate sample test cases and history data."""
    from prioritize_test_cases import SAMPLE_TEST_CASES, SAMPLE_TEST_HISTORY
    
    # Save sample test cases
    with open(TEST_CASES_FILE, "w") as f:
        json.dump(SAMPLE_TEST_CASES, f, indent=2)
    
    # Save sample test history
    with open(TEST_HISTORY_FILE, "w") as f:
        json.dump(SAMPLE_TEST_HISTORY, f, indent=2)
    
    logger.info(f"Generated sample test data in {TEST_CASES_FILE} and {TEST_HISTORY_FILE}")


def demo_prioritization(args):
    """Demonstrate test prioritization."""
    # Create a TestPrioritizer instance
    prioritizer = TestPrioritizer()
    
    # Load test cases and history
    prioritizer.load_test_cases(TEST_CASES_FILE)
    prioritizer.load_test_history(TEST_HISTORY_FILE)
    
    # Prioritize tests
    prioritized_tests = prioritizer.prioritize_tests()
    
    # Print prioritized tests
    logger.info("Prioritized tests:")
    for i, test in enumerate(prioritized_tests, 1):
        logger.info(
            f"{i}. {test['function']} - {test['priority_level']} - "
            f"Score: {test['priority_score']:.2f} - "
            f"Category: {test['category']}"
        )
    
    # Generate test suite based on time budget and filters
    test_suite = prioritizer.generate_test_suite(
        time_budget=args.time_budget,
        categories=args.categories.split(",") if args.categories else None,
        priority_levels=args.priority_levels.split(",") if args.priority_levels else None
    )
    
    # Print selected test suite
    logger.info("\nSelected test suite:")
    total_time = 0
    for i, test in enumerate(test_suite, 1):
        test_case = prioritizer.test_cases[test["function"]]
        execution_time = test_case["execution_time"]
        total_time += execution_time
        logger.info(
            f"{i}. {test['function']} - {test['priority_level']} - "
            f"Execution time: {execution_time:.1f}s - "
            f"Category: {test_case['category']}"
        )
    
    logger.info(f"\nTotal execution time: {total_time:.1f}s (Budget: {args.time_budget}s)")
    
    # Save prioritized tests
    if args.save:
        output_file = BASE_DIR / "reports" / "prioritized_tests.json"
        prioritizer.save_prioritized_tests(output_file)
        logger.info(f"Saved prioritized tests to {output_file}")
        
        # Export to other formats
        csv_file = BASE_DIR / "reports" / "prioritized_tests.csv"
        md_file = BASE_DIR / "reports" / "prioritized_tests.md"
        prioritizer.export_to_csv(csv_file)
        prioritizer.export_to_markdown(md_file)
        logger.info(f"Exported prioritized tests to {csv_file} and {md_file}")
    
    # Run tests if requested
    if args.run:
        logger.info("\nRunning test suite...")
        
        # Run the test suite
        results = run_test_suite(test_suite, no_server=True, timeout=args.timeout)
        
        # Update test history
        update_test_history(results, TEST_HISTORY_FILE)
        
        # Save results
        with open(RESULTS_FILE, "w") as f:
            json.dump(results, f, indent=2)
        
        # Print summary
        total_tests = len(results)
        passed = sum(1 for r in results if r["outcome"] == "pass")
        failed = sum(1 for r in results if r["outcome"] == "fail")
        errors = sum(1 for r in results if r["outcome"] == "error")
        timeouts = sum(1 for r in results if r["outcome"] == "timeout")
        skipped = sum(1 for r in results if r["outcome"] == "skip")
        
        logger.info(f"\nTest results summary:")
        logger.info(f"Total tests: {total_tests}")
        logger.info(f"Passed: {passed}")
        logger.info(f"Failed: {failed}")
        logger.info(f"Errors: {errors}")
        logger.info(f"Timeouts: {timeouts}")
        logger.info(f"Skipped: {skipped}")
        
        # Generate report
        from run_prioritized_tests import generate_test_report
        generate_test_report(results, REPORT_FILE)
        logger.info(f"\nGenerated test report at {REPORT_FILE}")


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Demo for test prioritization framework")
    
    # Options
    parser.add_argument("--generate-data", action="store_true", help="Generate sample test data")
    parser.add_argument("--time-budget", type=int, default=30, help="Time budget for test suite in seconds (default: 30)")
    parser.add_argument("--categories", type=str, help="Comma-separated list of test categories to include")
    parser.add_argument("--priority-levels", type=str, help="Comma-separated list of priority levels to include")
    parser.add_argument("--save", action="store_true", help="Save prioritized tests to files")
    parser.add_argument("--run", action="store_true", help="Run the selected test suite")
    parser.add_argument("--timeout", type=int, default=10, help="Timeout for individual tests in seconds (default: 10)")
    
    args = parser.parse_args()
    
    # Ensure directories exist
    ensure_directories()
    
    # Generate sample data if requested
    if args.generate_data:
        generate_sample_data()
    
    # Demo prioritization
    demo_prioritization(args)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())