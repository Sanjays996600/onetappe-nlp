#!/usr/bin/env python3
"""
Run Prioritized Tests for OneTappe API

This script integrates the test prioritization framework with the test runner.
It prioritizes tests based on risk and importance, then executes them in priority order.
"""

import os
import sys
import json
import time
import logging
import argparse
import subprocess
from datetime import datetime
from pathlib import Path

# Import the test prioritizer
sys.path.append(str(Path(__file__).resolve().parent))
from prioritize_test_cases import TestPrioritizer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("prioritized_test_run.log")
    ]
)
logger = logging.getLogger("run_prioritized_tests")

# Constants
BASE_DIR = Path(__file__).resolve().parent
SERVER_SCRIPT = BASE_DIR / "../run_app.py"
TEST_CASES_FILE = BASE_DIR / "test_cases.json"
TEST_HISTORY_FILE = BASE_DIR / "test_history.json"
TEST_RESULTS_FILE = BASE_DIR / "test_results.json"
TEST_REPORT_FILE = BASE_DIR / "prioritized_test_report.md"

# Test script mapping
TEST_SCRIPTS = {
    "product_api": BASE_DIR / "test_api_pytest.py",
    "authentication": BASE_DIR / "test_authentication.py",
    "seller_dashboard": BASE_DIR / "test_seller_dashboard.py",
    "security": BASE_DIR / "security_test.py",
    "performance": BASE_DIR / "performance_test.py"
}


class PrioritizedTestRunner:
    """Runs tests in prioritized order."""
    
    def __init__(self, time_budget=None, categories=None, priority_levels=None):
        """Initialize with optional filters."""
        self.time_budget = time_budget  # in seconds
        self.categories = categories or []  # list of categories to include
        self.priority_levels = priority_levels or []  # list of priority levels to include
        self.server_process = None
        self.test_results = {}
    
    def start_server(self):
        """Start the FastAPI server."""
        logger.info("Starting FastAPI server...")
        try:
            self.server_process = subprocess.Popen(
                [sys.executable, str(SERVER_SCRIPT)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            # Wait for server to start
            time.sleep(2)
            logger.info("Server started successfully")
            return True
        except Exception as e:
            logger.error(f"Failed to start server: {e}")
            return False
    
    def stop_server(self):
        """Stop the FastAPI server."""
        if self.server_process:
            logger.info("Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
            logger.info("Server stopped")
    
    def check_server_status(self):
        """Check if the server is running."""
        if not self.server_process:
            return False
        
        return self.server_process.poll() is None
    
    def prioritize_tests(self):
        """Prioritize tests using the TestPrioritizer."""
        logger.info("Prioritizing tests...")
        
        prioritizer = TestPrioritizer()
        prioritizer.load_test_cases(TEST_CASES_FILE)
        prioritizer.load_test_history(TEST_HISTORY_FILE)
        prioritizer.prioritize_tests()
        
        # Generate test suite based on filters
        if self.time_budget:
            # Generate a test suite based on time budget
            test_suite = []
            
            # If categories are specified, generate a suite for each category
            if self.categories:
                remaining_time = self.time_budget
                for category in self.categories:
                    category_time = remaining_time / len(self.categories)
                    category_tests = prioritizer.generate_test_suite(
                        time_budget=category_time,
                        category=category
                    )
                    test_suite.extend(category_tests)
                    remaining_time -= sum(test.get("execution_time", 0) for test in category_tests)
            else:
                # Generate a suite with all categories
                test_suite = prioritizer.generate_test_suite(
                    time_budget=self.time_budget
                )
        else:
            # Use all prioritized tests
            test_suite = prioritizer.prioritized_tests
        
        # Filter by priority levels if specified
        if self.priority_levels:
            test_suite = [test for test in test_suite if test.get("priority_level") in self.priority_levels]
        
        # Filter by categories if specified and time_budget not used
        if self.categories and not self.time_budget:
            test_suite = [test for test in test_suite if test.get("category") in self.categories]
        
        logger.info(f"Generated test suite with {len(test_suite)} tests")
        return test_suite
    
    def run_test(self, test_case):
        """Run a single test case."""
        test_id = test_case.get("id")
        category = test_case.get("category")
        name = test_case.get("name")
        
        logger.info(f"Running test {test_id}: {name} (Category: {category})")
        
        # Get the appropriate test script for this category
        test_script = TEST_SCRIPTS.get(category)
        if not test_script or not os.path.exists(test_script):
            logger.warning(f"No test script found for category: {category}")
            return {
                "id": test_id,
                "name": name,
                "category": category,
                "result": "skip",
                "message": f"No test script found for category: {category}",
                "execution_time": 0
            }
        
        # Prepare test-specific arguments
        test_args = [sys.executable, str(test_script)]
        
        # Add test-specific arguments if needed
        if "test_id" in test_case:
            test_args.extend(["--test-id", test_id])
        
        # Run the test
        start_time = time.time()
        try:
            process = subprocess.run(
                test_args,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300  # 5-minute timeout
            )
            
            execution_time = time.time() - start_time
            
            # Parse the output to determine if the test passed or failed
            if process.returncode == 0:
                result = "pass"
                message = "Test passed successfully"
            else:
                result = "fail"
                message = process.stderr or "Test failed with unknown error"
            
            return {
                "id": test_id,
                "name": name,
                "category": category,
                "result": result,
                "message": message,
                "execution_time": execution_time,
                "stdout": process.stdout,
                "stderr": process.stderr,
                "return_code": process.returncode
            }
        except subprocess.TimeoutExpired:
            execution_time = time.time() - start_time
            return {
                "id": test_id,
                "name": name,
                "category": category,
                "result": "timeout",
                "message": "Test execution timed out after 5 minutes",
                "execution_time": execution_time
            }
        except Exception as e:
            execution_time = time.time() - start_time
            return {
                "id": test_id,
                "name": name,
                "category": category,
                "result": "error",
                "message": str(e),
                "execution_time": execution_time
            }
    
    def run_tests(self, test_suite):
        """Run all tests in the test suite."""
        logger.info(f"Running {len(test_suite)} tests...")
        
        # Start the server if it's not already running
        if not self.check_server_status():
            if not self.start_server():
                logger.error("Failed to start server. Cannot run tests.")
                return {}
        
        # Run each test in the suite
        results = {}
        for test_case in test_suite:
            test_id = test_case.get("id")
            result = self.run_test(test_case)
            results[test_id] = result
        
        self.test_results = results
        return results
    
    def update_test_history(self, results):
        """Update test history with new results."""
        logger.info("Updating test history...")
        
        # Load existing history
        history = {}
        if os.path.exists(TEST_HISTORY_FILE):
            try:
                with open(TEST_HISTORY_FILE, "r") as f:
                    history = json.load(f)
            except Exception as e:
                logger.error(f"Error loading test history: {e}")
        
        # Update history with new results
        for test_id, result in results.items():
            if test_id not in history:
                history[test_id] = {
                    "execution_count": 0,
                    "failure_count": 0,
                    "recent_results": []
                }
            
            # Update execution count
            history[test_id]["execution_count"] = history[test_id].get("execution_count", 0) + 1
            
            # Update last execution timestamp
            history[test_id]["last_execution"] = datetime.now().isoformat()
            
            # Update last result
            test_result = result.get("result")
            history[test_id]["last_result"] = test_result
            
            # Update failure count
            if test_result in ["fail", "error", "timeout"]:
                history[test_id]["failure_count"] = history[test_id].get("failure_count", 0) + 1
            
            # Update recent results
            recent_results = history[test_id].get("recent_results", [])
            recent_results.insert(0, test_result)
            history[test_id]["recent_results"] = recent_results[:5]  # Keep only the 5 most recent results
        
        # Save updated history
        try:
            os.makedirs(os.path.dirname(TEST_HISTORY_FILE), exist_ok=True)
            with open(TEST_HISTORY_FILE, "w") as f:
                json.dump(history, f, indent=2)
            logger.info(f"Updated test history saved to {TEST_HISTORY_FILE}")
        except Exception as e:
            logger.error(f"Error saving test history: {e}")
    
    def save_test_results(self, results, file_path=TEST_RESULTS_FILE):
        """Save test results to a JSON file."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w") as f:
                json.dump(results, f, indent=2)
            logger.info(f"Test results saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving test results: {e}")
    
    def generate_report(self, results, test_suite, file_path=TEST_REPORT_FILE):
        """Generate a Markdown report of test results."""
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "w") as f:
                f.write("# Prioritized Test Execution Report\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                # Summary
                f.write("## Summary\n\n")
                
                total_tests = len(results)
                passed_tests = sum(1 for r in results.values() if r.get("result") == "pass")
                failed_tests = sum(1 for r in results.values() if r.get("result") == "fail")
                error_tests = sum(1 for r in results.values() if r.get("result") in ["error", "timeout"])
                skipped_tests = sum(1 for r in results.values() if r.get("result") == "skip")
                
                pass_rate = (passed_tests / total_tests) * 100 if total_tests > 0 else 0
                
                f.write(f"**Total Tests:** {total_tests}\n\n")
                f.write(f"**Pass Rate:** {pass_rate:.1f}%\n\n")
                
                f.write("| Result | Count | Percentage |\n")
                f.write("|--------|-------|------------|\n")
                f.write(f"| ✅ Passed | {passed_tests} | {(passed_tests / total_tests) * 100:.1f}% |\n")
                f.write(f"| ❌ Failed | {failed_tests} | {(failed_tests / total_tests) * 100:.1f}% |\n")
                f.write(f"| ⚠️ Error | {error_tests} | {(error_tests / total_tests) * 100:.1f}% |\n")
                f.write(f"| ⏭️ Skipped | {skipped_tests} | {(skipped_tests / total_tests) * 100:.1f}% |\n\n")
                
                # Results by category
                f.write("## Results by Category\n\n")
                
                categories = {}
                for test_id, result in results.items():
                    category = result.get("category", "unknown")
                    if category not in categories:
                        categories[category] = {
                            "total": 0,
                            "passed": 0,
                            "failed": 0,
                            "error": 0,
                            "skipped": 0
                        }
                    
                    categories[category]["total"] += 1
                    
                    test_result = result.get("result")
                    if test_result == "pass":
                        categories[category]["passed"] += 1
                    elif test_result == "fail":
                        categories[category]["failed"] += 1
                    elif test_result in ["error", "timeout"]:
                        categories[category]["error"] += 1
                    elif test_result == "skip":
                        categories[category]["skipped"] += 1
                
                f.write("| Category | Total | Passed | Failed | Error | Skipped | Pass Rate |\n")
                f.write("|----------|-------|--------|--------|-------|---------|-----------|\n")
                
                for category, stats in sorted(categories.items()):
                    pass_rate = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
                    f.write(f"| {category} | {stats['total']} | {stats['passed']} | {stats['failed']} | {stats['error']} | {stats['skipped']} | {pass_rate:.1f}% |\n")
                
                f.write("\n")
                
                # Results by priority level
                f.write("## Results by Priority Level\n\n")
                
                priority_levels = {}
                for test_case in test_suite:
                    test_id = test_case.get("id")
                    if test_id in results:
                        priority_level = test_case.get("priority_level", "unknown")
                        if priority_level not in priority_levels:
                            priority_levels[priority_level] = {
                                "total": 0,
                                "passed": 0,
                                "failed": 0,
                                "error": 0,
                                "skipped": 0
                            }
                        
                        priority_levels[priority_level]["total"] += 1
                        
                        test_result = results[test_id].get("result")
                        if test_result == "pass":
                            priority_levels[priority_level]["passed"] += 1
                        elif test_result == "fail":
                            priority_levels[priority_level]["failed"] += 1
                        elif test_result in ["error", "timeout"]:
                            priority_levels[priority_level]["error"] += 1
                        elif test_result == "skip":
                            priority_levels[priority_level]["skipped"] += 1
                
                f.write("| Priority Level | Total | Passed | Failed | Error | Skipped | Pass Rate |\n")
                f.write("|---------------|-------|--------|--------|-------|---------|-----------|\n")
                
                for level in ["P1 - Critical", "P2 - High", "P3 - Medium", "P4 - Low", "unknown"]:
                    if level in priority_levels:
                        stats = priority_levels[level]
                        pass_rate = (stats["passed"] / stats["total"]) * 100 if stats["total"] > 0 else 0
                        f.write(f"| {level} | {stats['total']} | {stats['passed']} | {stats['failed']} | {stats['error']} | {stats['skipped']} | {pass_rate:.1f}% |\n")
                
                f.write("\n")
                
                # Detailed test results
                f.write("## Detailed Test Results\n\n")
                
                # Group by result
                for result_type, emoji in [("fail", "❌"), ("error", "⚠️"), ("timeout", "⏱️"), ("pass", "✅"), ("skip", "⏭️")]:
                    result_tests = [(test_id, result) for test_id, result in results.items() if result.get("result") == result_type]
                    
                    if result_tests:
                        if result_type == "fail":
                            f.write("### Failed Tests\n\n")
                        elif result_type == "error" or result_type == "timeout":
                            f.write("### Tests with Errors\n\n")
                        elif result_type == "pass":
                            f.write("### Passed Tests\n\n")
                        elif result_type == "skip":
                            f.write("### Skipped Tests\n\n")
                        
                        for test_id, result in result_tests:
                            f.write(f"#### {emoji} {test_id}: {result.get('name', '')}\n\n")
                            f.write(f"**Category:** {result.get('category', '')}\n\n")
                            f.write(f"**Execution Time:** {result.get('execution_time', 0):.2f} seconds\n\n")
                            
                            if result_type in ["fail", "error", "timeout"]:
                                f.write(f"**Error Message:**\n```\n{result.get('message', '')}\n```\n\n")
                                
                                if "stderr" in result and result["stderr"]:
                                    f.write(f"**Standard Error:**\n```\n{result['stderr'][:500]}{'...' if len(result['stderr']) > 500 else ''}\n```\n\n")
                            
                            f.write("\n")
                
                # Recommendations
                f.write("## Recommendations\n\n")
                
                # Add recommendations based on test results
                if failed_tests > 0:
                    f.write("### Critical Issues\n\n")
                    
                    # List failed critical tests
                    critical_fails = []
                    for test_case in test_suite:
                        test_id = test_case.get("id")
                        if test_id in results and results[test_id].get("result") == "fail" and test_case.get("priority_level") == "P1 - Critical":
                            critical_fails.append((test_id, test_case.get("name", ""), test_case.get("category", "")))
                    
                    if critical_fails:
                        f.write("The following critical tests failed and should be addressed immediately:\n\n")
                        for test_id, name, category in critical_fails:
                            f.write(f"- **{test_id}**: {name} ({category})\n")
                        f.write("\n")
                    
                    # Check for common failure patterns
                    if any("seller_id" in results[test_id].get("message", "").lower() for test_id in results if results[test_id].get("result") == "fail"):
                        f.write("- **seller_id Issues**: Multiple tests are failing due to seller_id validation problems. Review the seller_id handling in the API.\n\n")
                    
                    if any("token" in results[test_id].get("message", "").lower() or "auth" in results[test_id].get("message", "").lower() for test_id in results if results[test_id].get("result") == "fail"):
                        f.write("- **Authentication Issues**: Tests are failing due to authentication or token validation problems. Review the authentication flow.\n\n")
                
                f.write("### General Recommendations\n\n")
                f.write("1. **Address Failed Tests**: Prioritize fixing failed tests, especially those with high priority levels.\n")
                f.write("2. **Improve Test Coverage**: Consider adding more tests for areas with low coverage.\n")
                f.write("3. **Optimize Test Performance**: Some tests are taking longer than expected to execute.\n")
                
                # Execution summary
                f.write("## Execution Summary\n\n")
                
                total_execution_time = sum(result.get("execution_time", 0) for result in results.values())
                avg_execution_time = total_execution_time / len(results) if results else 0
                
                f.write(f"**Total Execution Time:** {total_execution_time:.2f} seconds\n\n")
                f.write(f"**Average Test Execution Time:** {avg_execution_time:.2f} seconds\n\n")
                
                # Slowest tests
                slowest_tests = sorted([(test_id, result) for test_id, result in results.items()], key=lambda x: x[1].get("execution_time", 0), reverse=True)[:5]
                
                if slowest_tests:
                    f.write("**Slowest Tests:**\n\n")
                    f.write("| Test ID | Name | Category | Execution Time (s) |\n")
                    f.write("|---------|------|----------|-------------------|\n")
                    
                    for test_id, result in slowest_tests:
                        f.write(f"| {test_id} | {result.get('name', '')} | {result.get('category', '')} | {result.get('execution_time', 0):.2f} |\n")
            
            logger.info(f"Test report generated: {file_path}")
            return True
        except Exception as e:
            logger.error(f"Error generating test report: {e}")
            return False


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run prioritized tests for OneTappe API")
    parser.add_argument("--time-budget", type=int, help="Time budget for test execution in seconds")
    parser.add_argument("--categories", type=str, help="Comma-separated list of test categories to include")
    parser.add_argument("--priority-levels", type=str, help="Comma-separated list of priority levels to include (e.g., 'P1 - Critical,P2 - High')")
    parser.add_argument("--no-server", action="store_true", help="Don't start the server (assume it's already running)")
    parser.add_argument("--results-file", type=str, default=TEST_RESULTS_FILE, help="Path to save test results")
    parser.add_argument("--report-file", type=str, default=TEST_REPORT_FILE, help="Path to save test report")
    args = parser.parse_args()
    
    # Parse categories and priority levels
    categories = args.categories.split(",") if args.categories else []
    priority_levels = args.priority_levels.split(",") if args.priority_levels else []
    
    # Create and run the test runner
    runner = PrioritizedTestRunner(
        time_budget=args.time_budget,
        categories=categories,
        priority_levels=priority_levels
    )
    
    # Start server if needed
    if not args.no_server and not runner.check_server_status():
        if not runner.start_server():
            logger.error("Failed to start server. Exiting.")
            return 1
    
    try:
        # Prioritize tests
        test_suite = runner.prioritize_tests()
        
        # Run tests
        results = runner.run_tests(test_suite)
        
        # Update test history
        runner.update_test_history(results)
        
        # Save test results
        runner.save_test_results(results, args.results_file)
        
        # Generate report
        runner.generate_report(results, test_suite, args.report_file)
        
        # Print summary
        total_tests = len(results)
        passed_tests = sum(1 for r in results.values() if r.get("result") == "pass")
        failed_tests = sum(1 for r in results.values() if r.get("result") == "fail")
        error_tests = sum(1 for r in results.values() if r.get("result") in ["error", "timeout"])
        
        logger.info(f"Test execution complete: {passed_tests}/{total_tests} tests passed")
        if failed_tests > 0 or error_tests > 0:
            logger.warning(f"Failed tests: {failed_tests}, Tests with errors: {error_tests}")
            return 1
        
        return 0
    finally:
        # Stop server if we started it
        if not args.no_server:
            runner.stop_server()


if __name__ == "__main__":
    sys.exit(main())