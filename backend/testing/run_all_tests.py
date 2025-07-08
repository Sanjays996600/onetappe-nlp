#!/usr/bin/env python3
"""
Comprehensive Test Runner for OneTappe API

This script automates the execution of all test types and generates a comprehensive test report.
It includes:
- Starting and stopping the FastAPI server
- Running functional tests (API endpoints)
- Running performance tests
- Running security tests
- Running load tests
- Generating test coverage reports
- Compiling all results into a comprehensive test report
"""

import os
import sys
import time
import json
import argparse
import logging
import subprocess
import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("all_tests.log")
    ]
)
logger = logging.getLogger("run_all_tests")

# Constants
BASE_DIR = Path(__file__).resolve().parent
SERVER_SCRIPT = BASE_DIR.parent / "run_app.py"
REPORTS_DIR = BASE_DIR / "reports"
TEST_DATA_DIR = BASE_DIR / "test_data"

# Test scripts
TEST_PRODUCT_API = BASE_DIR / "test_product_api_suite.py"
TEST_AUTHENTICATION = BASE_DIR / "test_authentication.py"
TEST_SELLER_DASHBOARD = BASE_DIR / "test_seller_dashboard.py"
TEST_API_PYTEST = BASE_DIR / "test_api_pytest.py"
PERFORMANCE_TEST = BASE_DIR / "performance_test.py"
SECURITY_TEST = BASE_DIR / "security_test.py"
LOAD_TEST = BASE_DIR / "load_test.py"
GENERATE_COVERAGE = BASE_DIR / "generate_coverage_report.py"
GENERATE_REPORT = BASE_DIR / "generate_comprehensive_report.py"
GENERATE_TEST_DATA = BASE_DIR / "generate_test_data.py"
RUN_PRIORITIZED_TESTS = BASE_DIR / "run_prioritized_tests.py"

# Server process
server_process = None


def ensure_directories():
    """Ensure necessary directories exist."""
    os.makedirs(REPORTS_DIR, exist_ok=True)
    os.makedirs(TEST_DATA_DIR, exist_ok=True)


def start_server():
    """Start the FastAPI server."""
    global server_process
    
    logger.info("Starting FastAPI server...")
    
    try:
        # Start the server as a subprocess
        server_process = subprocess.Popen(
            [sys.executable, str(SERVER_SCRIPT)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Wait for the server to start
        time.sleep(2)
        
        # Check if the server is running
        if server_process.poll() is not None:
            stdout, stderr = server_process.communicate()
            logger.error(f"Failed to start server: {stderr}")
            return False
        
        # Check if the server is responding
        response = subprocess.run(
            ["curl", "-s", "http://127.0.0.1:8000/"],
            capture_output=True,
            text=True
        )
        
        if response.returncode != 0:
            logger.warning("Server started but not responding to requests yet. Waiting...")
            time.sleep(3)  # Wait a bit longer
            
            # Check again
            response = subprocess.run(
                ["curl", "-s", "http://127.0.0.1:8000/"],
                capture_output=True,
                text=True
            )
            
            if response.returncode != 0:
                logger.error("Server is not responding to requests")
                return False
        
        logger.info("FastAPI server started successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error starting server: {e}")
        return False


def stop_server():
    """Stop the FastAPI server."""
    global server_process
    
    if server_process is not None:
        logger.info("Stopping FastAPI server...")
        
        try:
            # Try to terminate gracefully
            server_process.terminate()
            server_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            # Force kill if it doesn't terminate
            logger.warning("Server did not terminate gracefully, forcing kill...")
            server_process.kill()
        
        server_process = None
        logger.info("FastAPI server stopped")


def check_server_status():
    """Check if the server is running and responding."""
    try:
        response = subprocess.run(
            ["curl", "-s", "http://127.0.0.1:8000/"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        return response.returncode == 0
    except Exception:
        return False


def generate_test_data(users=50, sellers=10, products=100, orders=200):
    """Generate test data for the API."""
    logger.info("Generating test data...")
    
    try:
        result = subprocess.run(
            [
                sys.executable, 
                str(GENERATE_TEST_DATA),
                "--users", str(users),
                "--sellers", str(sellers),
                "--products", str(products),
                "--orders", str(orders)
            ],
            capture_output=True,
            text=True
        )
        
        if result.returncode != 0:
            logger.error(f"Failed to generate test data: {result.stderr}")
            return False
        
        logger.info("Test data generated successfully")
        return True
    
    except Exception as e:
        logger.error(f"Error generating test data: {e}")
        return False


def run_functional_tests():
    """Run functional API tests."""
    logger.info("Running functional API tests...")
    results = {}
    
    # Run product API tests
    logger.info("Running product API tests...")
    try:
        result = subprocess.run(
            [sys.executable, str(TEST_PRODUCT_API)],
            capture_output=True,
            text=True
        )
        
        results["product_api"] = {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
        
        if result.returncode == 0:
            logger.info("Product API tests completed successfully")
        else:
            logger.error(f"Product API tests failed: {result.stderr}")
    
    except Exception as e:
        logger.error(f"Error running product API tests: {e}")
        results["product_api"] = {
            "success": False,
            "output": "",
            "error": str(e)
        }
    
    # Run authentication tests
    logger.info("Running authentication tests...")
    try:
        result = subprocess.run(
            [sys.executable, str(TEST_AUTHENTICATION)],
            capture_output=True,
            text=True
        )
        
        results["authentication"] = {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
        
        if result.returncode == 0:
            logger.info("Authentication tests completed successfully")
        else:
            logger.error(f"Authentication tests failed: {result.stderr}")
    
    except Exception as e:
        logger.error(f"Error running authentication tests: {e}")
        results["authentication"] = {
            "success": False,
            "output": "",
            "error": str(e)
        }
    
    # Run seller dashboard tests
    logger.info("Running seller dashboard tests...")
    try:
        result = subprocess.run(
            [sys.executable, str(TEST_SELLER_DASHBOARD)],
            capture_output=True,
            text=True
        )
        
        results["seller_dashboard"] = {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
        
        if result.returncode == 0:
            logger.info("Seller dashboard tests completed successfully")
        else:
            logger.error(f"Seller dashboard tests failed: {result.stderr}")
    
    except Exception as e:
        logger.error(f"Error running seller dashboard tests: {e}")
        results["seller_dashboard"] = {
            "success": False,
            "output": "",
            "error": str(e)
        }
    
    # Run pytest tests
    logger.info("Running pytest tests...")
    try:
        result = subprocess.run(
            ["pytest", "-v", str(TEST_API_PYTEST)],
            capture_output=True,
            text=True
        )
        
        results["pytest"] = {
            "success": result.returncode == 0,
            "output": result.stdout,
            "error": result.stderr
        }
        
        if result.returncode == 0:
            logger.info("Pytest tests completed successfully")
        else:
            logger.error(f"Pytest tests failed: {result.stderr}")
    
    except Exception as e:
        logger.error(f"Error running pytest tests: {e}")
        results["pytest"] = {
            "success": False,
            "output": "",
            "error": str(e)
        }
    
    # Save results to file
    with open(REPORTS_DIR / "functional_test_results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results


def run_performance_tests():
    """Run performance tests."""
    logger.info("Running performance tests...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(PERFORMANCE_TEST)],
            capture_output=True,
            text=True
        )
        
        success = result.returncode == 0
        
        if success:
            logger.info("Performance tests completed successfully")
        else:
            logger.error(f"Performance tests failed: {result.stderr}")
        
        return {
            "success": success,
            "output": result.stdout,
            "error": result.stderr
        }
    
    except Exception as e:
        logger.error(f"Error running performance tests: {e}")
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


def run_security_tests():
    """Run security tests."""
    logger.info("Running security tests...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(SECURITY_TEST)],
            capture_output=True,
            text=True
        )
        
        success = result.returncode == 0
        
        if success:
            logger.info("Security tests completed successfully")
        else:
            logger.error(f"Security tests failed: {result.stderr}")
        
        return {
            "success": success,
            "output": result.stdout,
            "error": result.stderr
        }
    
    except Exception as e:
        logger.error(f"Error running security tests: {e}")
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


def run_load_tests(duration=60, users=10, spawn_rate=1):
    """Run load tests."""
    logger.info(f"Running load tests with {users} users for {duration} seconds...")
    
    try:
        # Set environment variables for Locust
        env = os.environ.copy()
        env["LOCUST_USERS"] = str(users)
        env["LOCUST_SPAWN_RATE"] = str(spawn_rate)
        env["LOCUST_RUN_TIME"] = f"{duration}s"
        
        result = subprocess.run(
            [
                "locust",
                "-f", str(LOAD_TEST),
                "--headless",
                "--host=http://127.0.0.1:8000"
            ],
            capture_output=True,
            text=True,
            env=env
        )
        
        success = result.returncode == 0
        
        if success:
            logger.info("Load tests completed successfully")
        else:
            logger.error(f"Load tests failed: {result.stderr}")
        
        return {
            "success": success,
            "output": result.stdout,
            "error": result.stderr
        }
    
    except Exception as e:
        logger.error(f"Error running load tests: {e}")
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


def generate_coverage_report():
    """Generate test coverage report."""
    logger.info("Generating test coverage report...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(GENERATE_COVERAGE)],
            capture_output=True,
            text=True
        )
        
        success = result.returncode == 0
        
        if success:
            logger.info("Coverage report generated successfully")
        else:
            logger.error(f"Failed to generate coverage report: {result.stderr}")
        
        return {
            "success": success,
            "output": result.stdout,
            "error": result.stderr
        }
    
    except Exception as e:
        logger.error(f"Error generating coverage report: {e}")
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


def generate_comprehensive_report():
    """Generate comprehensive test report."""
    logger.info("Generating comprehensive test report...")
    
    try:
        result = subprocess.run(
            [sys.executable, str(GENERATE_REPORT)],
            capture_output=True,
            text=True
        )
        
        success = result.returncode == 0
        
        if success:
            logger.info("Comprehensive report generated successfully")
        else:
            logger.error(f"Failed to generate comprehensive report: {result.stderr}")
        
        return {
            "success": success,
            "output": result.stdout,
            "error": result.stderr
        }
    
    except Exception as e:
        logger.error(f"Error generating comprehensive report: {e}")
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


def run_prioritized_tests(args):
    """Run prioritized tests based on risk and importance."""
    logger.info("Running prioritized tests...")
    
    try:
        # Build command arguments
        cmd_args = [sys.executable, str(RUN_PRIORITIZED_TESTS)]
        
        # Add time budget if specified
        if args.prioritized_time_budget:
            cmd_args.extend(["--time-budget", str(args.prioritized_time_budget)])
        
        # Add categories if specified
        if args.prioritized_categories:
            cmd_args.extend(["--categories", args.prioritized_categories])
        
        # Add priority levels if specified
        if args.prioritized_levels:
            cmd_args.extend(["--priority-levels", args.prioritized_levels])
        
        # Add no-server flag if server is already running
        if check_server_status():
            cmd_args.append("--no-server")
        
        # Run the prioritized tests
        result = subprocess.run(
            cmd_args,
            capture_output=True,
            text=True
        )
        
        success = result.returncode == 0
        
        if success:
            logger.info("Prioritized tests completed successfully")
            
            # Check if report was generated
            report_path = BASE_DIR / "prioritized_test_report.md"
            if os.path.exists(report_path):
                logger.info(f"Prioritized test report available at: {report_path}")
        else:
            logger.error(f"Prioritized tests failed: {result.stderr}")
        
        return {
            "success": success,
            "output": result.stdout,
            "error": result.stderr
        }
    
    except Exception as e:
        logger.error(f"Error running prioritized tests: {e}")
        return {
            "success": False,
            "output": "",
            "error": str(e)
        }


def run_all_tests(args):
    """Run all tests and generate reports."""
    start_time = datetime.datetime.now()
    logger.info(f"Starting test run at {start_time}")
    
    # Ensure directories exist
    ensure_directories()
    
    # Generate test data if requested
    if args.generate_data:
        if not generate_test_data(
            users=args.users,
            sellers=args.sellers,
            products=args.products,
            orders=args.orders
        ):
            logger.error("Failed to generate test data, aborting test run")
            return False
    
    # Start the server if it's not already running
    server_started_by_us = False
    if not check_server_status():
        server_started_by_us = start_server()
        if not server_started_by_us:
            logger.error("Failed to start server, aborting test run")
            return False
    
    try:
        # Run prioritized tests if requested
        if args.prioritized:
            prioritized_results = run_prioritized_tests(args)
            logger.info(f"Prioritized tests completed: {'Success' if prioritized_results['success'] else 'Failure'}")
        
        # Run functional tests
        if args.functional:
            functional_results = run_functional_tests()
            logger.info(f"Functional tests completed with {sum(1 for r in functional_results.values() if r['success'])} successes and {sum(1 for r in functional_results.values() if not r['success'])} failures")
        
        # Run performance tests
        if args.performance:
            performance_results = run_performance_tests()
            logger.info(f"Performance tests completed: {'Success' if performance_results['success'] else 'Failure'}")
        
        # Run security tests
        if args.security:
            security_results = run_security_tests()
            logger.info(f"Security tests completed: {'Success' if security_results['success'] else 'Failure'}")
        
        # Run load tests
        if args.load:
            load_results = run_load_tests(
                duration=args.load_duration,
                users=args.load_users,
                spawn_rate=args.load_spawn_rate
            )
            logger.info(f"Load tests completed: {'Success' if load_results['success'] else 'Failure'}")
        
        # Generate coverage report
        if args.coverage:
            coverage_results = generate_coverage_report()
            logger.info(f"Coverage report generation: {'Success' if coverage_results['success'] else 'Failure'}")
        
        # Generate comprehensive report
        if args.report:
            report_results = generate_comprehensive_report()
            logger.info(f"Comprehensive report generation: {'Success' if report_results['success'] else 'Failure'}")
            
            if report_results['success']:
                report_path = REPORTS_DIR / "comprehensive_report.md"
                if os.path.exists(report_path):
                    logger.info(f"Comprehensive report available at: {report_path}")
        
        end_time = datetime.datetime.now()
        duration = end_time - start_time
        logger.info(f"Test run completed at {end_time} (Duration: {duration})")
        
        return True
    
    finally:
        # Stop the server if we started it
        if server_started_by_us:
            stop_server()


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Run all tests for OneTappe API")
    
    # Test selection options
    parser.add_argument("--all", action="store_true", help="Run all tests")
    parser.add_argument("--functional", action="store_true", help="Run functional tests")
    parser.add_argument("--performance", action="store_true", help="Run performance tests")
    parser.add_argument("--security", action="store_true", help="Run security tests")
    parser.add_argument("--load", action="store_true", help="Run load tests")
    parser.add_argument("--coverage", action="store_true", help="Generate coverage report")
    parser.add_argument("--report", action="store_true", help="Generate comprehensive report")
    parser.add_argument("--prioritized", action="store_true", help="Run prioritized tests based on risk and importance")
    
    # Test data options
    parser.add_argument("--generate-data", action="store_true", help="Generate test data")
    parser.add_argument("--users", type=int, default=50, help="Number of users to generate (default: 50)")
    parser.add_argument("--sellers", type=int, default=10, help="Number of sellers to generate (default: 10)")
    parser.add_argument("--products", type=int, default=100, help="Number of products to generate (default: 100)")
    parser.add_argument("--orders", type=int, default=200, help="Number of orders to generate (default: 200)")
    
    # Load test options
    parser.add_argument("--load-duration", type=int, default=60, help="Duration of load test in seconds (default: 60)")
    parser.add_argument("--load-users", type=int, default=10, help="Number of users for load test (default: 10)")
    parser.add_argument("--load-spawn-rate", type=int, default=1, help="User spawn rate for load test (default: 1)")
    
    # Prioritized test options
    parser.add_argument("--prioritized-time-budget", type=int, help="Time budget for prioritized tests in seconds")
    parser.add_argument("--prioritized-categories", type=str, help="Comma-separated list of test categories for prioritized tests")
    parser.add_argument("--prioritized-levels", type=str, help="Comma-separated list of priority levels for prioritized tests (e.g., 'P1 - Critical,P2 - High')")
    
    args = parser.parse_args()
    
    # If --all is specified, run all tests
    if args.all:
        args.functional = True
        args.performance = True
        args.security = True
        args.load = True
        args.coverage = True
        args.report = True
        args.prioritized = True
    
    # If no tests are specified, run functional tests by default
    if not any([args.functional, args.performance, args.security, args.load, args.coverage, args.report, args.prioritized]):
        args.functional = True
    
    # Run the tests
    success = run_all_tests(args)
    
    return 0 if success else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        logger.info("Test run interrupted by user")
        stop_server()  # Ensure server is stopped
        sys.exit(130)  # 130 is the standard exit code for SIGINT