#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
import logging
import time
import requests

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "http://127.0.0.1:8000"
SERVER_SCRIPT = "../run_app.py"  # Updated path to run_app.py

def check_server_status():
    """Check if the server is running"""
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        return False
    except Exception as e:
        logger.error(f"Error checking server status: {str(e)}")
        return False

def start_server():
    """Start the FastAPI server"""
    if check_server_status():
        logger.info("Server is already running")
        return None
    
    try:
        logger.info("Starting server...")
        server_process = subprocess.Popen(
            [sys.executable, SERVER_SCRIPT],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Wait for server to start
        max_retries = 5
        for i in range(max_retries):
            time.sleep(2)  # Give the server time to start
            if check_server_status():
                logger.info("Server started successfully")
                return server_process
        
        logger.error("Failed to start server")
        server_process.terminate()
        return None
    except Exception as e:
        logger.error(f"Error starting server: {str(e)}")
        return None

def stop_server(server_process):
    """Stop the FastAPI server"""
    if server_process:
        logger.info("Stopping server...")
        server_process.terminate()
        server_process.wait()
        logger.info("Server stopped")

def run_test(test_script):
    """Run a test script and return success status"""
    logger.info(f"Running test: {test_script}")
    result = subprocess.run([sys.executable, test_script], capture_output=True, text=True)
    
    # Log output
    if result.stdout:
        logger.info(f"Test output:\n{result.stdout}")
    if result.stderr:
        logger.error(f"Test errors:\n{result.stderr}")
    
    return result.returncode == 0

def run_pytest(test_script=None):
    """Run pytest with optional specific test script"""
    cmd = [sys.executable, "-m", "pytest", "-xvs"]
    if test_script:
        cmd.append(test_script)
    
    logger.info(f"Running pytest: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    # Log output
    if result.stdout:
        logger.info(f"Pytest output:\n{result.stdout}")
    if result.stderr:
        logger.error(f"Pytest errors:\n{result.stderr}")
    
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description="Run API tests")
    parser.add_argument("--test", choices=["all", "product", "auth", "seller", "pytest"], default="all",
                        help="Which test suite to run")
    parser.add_argument("--no-server", action="store_true", help="Don't start/stop the server")
    args = parser.parse_args()
    
    # Get script directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Define test scripts
    test_scripts = {
        "product": "test_product_api_suite.py",
        "auth": "test_authentication.py",
        "seller": "test_seller_dashboard.py",
        "pytest": "test_api_pytest.py"
    }
    
    # Start server if needed
    server_process = None
    if not args.no_server and not check_server_status():
        server_process = start_server()
        if not server_process:
            logger.error("Failed to start server. Exiting.")
            return 1
    
    try:
        results = {}
        
        if args.test == "all":
            # Run all test scripts
            for test_name, test_script in test_scripts.items():
                if test_name == "pytest":
                    results[test_name] = run_pytest()
                else:
                    results[test_name] = run_test(test_script)
        elif args.test == "pytest":
            # Run pytest
            results[args.test] = run_pytest()
        else:
            # Run specific test script
            results[args.test] = run_test(test_scripts[args.test])
        
        # Print summary
        logger.info("\n=== Test Summary ===\n")
        for test_name, result in results.items():
            logger.info(f"{test_name}: {'PASSED' if result else 'FAILED'}")
        
        # Return overall result
        return 0 if all(results.values()) else 1
    finally:
        # Stop server if we started it
        if server_process:
            stop_server(server_process)

if __name__ == "__main__":
    sys.exit(main())