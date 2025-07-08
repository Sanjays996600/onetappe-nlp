import pytest
import requests
import time
import os
import sys
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "http://127.0.0.1:8000"
SERVER_SCRIPT = "../run_app.py"

@pytest.fixture(scope="session")
def server():
    """Start and stop the server for the test session"""
    # Check if server is already running
    try:
        response = requests.get(f"{BASE_URL}/", timeout=2)
        if response.status_code == 200:
            logger.info("Server is already running")
            yield BASE_URL
            return
    except requests.exceptions.ConnectionError:
        pass
    
    # Start server
    logger.info("Starting server...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    run_app_path = os.path.join(os.path.dirname(script_dir), "run_app.py")
    
    server_process = subprocess.Popen(
        [sys.executable, run_app_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    max_retries = 5
    for i in range(max_retries):
        try:
            time.sleep(2)  # Give the server time to start
            response = requests.get(f"{BASE_URL}/", timeout=2)
            if response.status_code == 200:
                logger.info("Server started successfully")
                break
        except requests.exceptions.ConnectionError:
            if i == max_retries - 1:
                logger.error("Failed to start server")
                server_process.terminate()
                pytest.fail("Could not start server")
    
    yield BASE_URL
    
    # Stop server
    logger.info("Stopping server...")
    server_process.terminate()
    server_process.wait()

@pytest.fixture
def api_client(server):
    """Return a session for making API requests"""
    session = requests.Session()
    session.headers.update({"Content-Type": "application/json"})
    return session

@pytest.fixture
def auth_headers(api_client):
    """Get authentication headers for API requests"""
    # This is a placeholder - in a real test, you would authenticate and get a token
    # For now, we'll just return empty headers
    return {}

@pytest.fixture
def test_product():
    """Return test product data"""
    return {
        "product_name": "Test Product",
        "price": 50.0,
        "stock": 20,
        "description": "Test product for pytest",
        "seller_id": 1
    }