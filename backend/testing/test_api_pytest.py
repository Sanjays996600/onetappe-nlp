import pytest
import requests
import json
import logging
import time
import os
import sys
import subprocess
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 10

# Test data
TEST_PRODUCT = {
    "product_name": "Test Rice",
    "price": 50.0,
    "stock": 20,
    "description": "Test product for pytest",
    "seller_id": 1
}

TEST_USER = {
    "username": "test_user",
    "password": "password123"
}

# Fixture for server management
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
    run_app_path = os.path.join(script_dir, "run_app.py")
    
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

# Fixture for product creation
@pytest.fixture
def created_product(server):
    """Create a test product and return its data"""
    url = f"{BASE_URL}/products"
    response = requests.post(
        url,
        json=TEST_PRODUCT,
        headers={"Content-Type": "application/json"},
        timeout=TIMEOUT
    )
    
    if response.status_code != 201:
        pytest.skip(f"Could not create test product: {response.text}")
    
    product_data = response.json()
    yield product_data
    
    # Cleanup: Delete the product
    if 'id' in product_data:
        try:
            requests.delete(f"{BASE_URL}/products/{product_data['id']}", timeout=TIMEOUT)
        except Exception as e:
            logger.warning(f"Failed to delete test product: {str(e)}")

# Test cases

def test_server_health(server):
    """Test if the server is healthy"""
    response = requests.get(f"{server}/", timeout=TIMEOUT)
    assert response.status_code == 200
    assert "message" in response.json()

class TestProductAPI:
    """Tests for the Product API endpoints"""
    
    def test_get_products(self, server):
        """Test getting all products"""
        response = requests.get(f"{server}/products", timeout=TIMEOUT)
        assert response.status_code == 200
        assert isinstance(response.json(), list)
    
    def test_add_product(self, server):
        """Test adding a new product"""
        response = requests.post(
            f"{server}/products",
            json=TEST_PRODUCT,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["product_name"] == TEST_PRODUCT["product_name"]
        
        # Cleanup
        if "id" in data:
            requests.delete(f"{server}/products/{data['id']}", timeout=TIMEOUT)
    
    def test_get_product_by_id(self, server, created_product):
        """Test getting a product by ID"""
        product_id = created_product["id"]
        response = requests.get(f"{server}/products/{product_id}", timeout=TIMEOUT)
        assert response.status_code == 200
        assert response.json()["id"] == product_id
    
    def test_update_product(self, server, created_product):
        """Test updating a product"""
        product_id = created_product["id"]
        updated_data = {
            "product_name": "Updated Rice",
            "price": 55.0,
            "stock": 25,
            "description": "Updated test product",
            "seller_id": created_product.get("seller_id", 1)
        }
        
        response = requests.put(
            f"{server}/products/{product_id}",
            json=updated_data,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        assert data["product_name"] == updated_data["product_name"]
        assert data["price"] == updated_data["price"]
    
    def test_delete_product(self, server):
        """Test deleting a product"""
        # First create a product to delete
        response = requests.post(
            f"{server}/products",
            json=TEST_PRODUCT,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code == 201
        product_id = response.json()["id"]
        
        # Now delete it
        response = requests.delete(f"{server}/products/{product_id}", timeout=TIMEOUT)
        assert response.status_code == 200
        
        # Verify it's gone
        response = requests.get(f"{server}/products/{product_id}", timeout=TIMEOUT)
        assert response.status_code == 404
    
    def test_add_product_without_seller_id(self, server):
        """Test adding a product without seller_id"""
        product_data = TEST_PRODUCT.copy()
        if "seller_id" in product_data:
            del product_data["seller_id"]
        
        response = requests.post(
            f"{server}/products",
            json=product_data,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        
        # This test might fail if the API requires seller_id
        # We're documenting the current behavior
        logger.info(f"Response status for product without seller_id: {response.status_code}")
        logger.info(f"Response body: {response.text}")
        
        # Cleanup if product was created
        try:
            data = response.json()
            if "id" in data:
                requests.delete(f"{server}/products/{data['id']}", timeout=TIMEOUT)
        except:
            pass

class TestInputValidation:
    """Tests for input validation"""
    
    def test_add_product_with_invalid_price(self, server):
        """Test adding a product with invalid price"""
        invalid_product = TEST_PRODUCT.copy()
        invalid_product["price"] = -10  # Negative price
        
        response = requests.post(
            f"{server}/products",
            json=invalid_product,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code == 422  # Unprocessable Entity
    
    def test_add_product_with_empty_name(self, server):
        """Test adding a product with empty name"""
        invalid_product = TEST_PRODUCT.copy()
        invalid_product["product_name"] = ""  # Empty name
        
        response = requests.post(
            f"{server}/products",
            json=invalid_product,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code == 422  # Unprocessable Entity

class TestErrorHandling:
    """Tests for error handling"""
    
    def test_get_nonexistent_product(self, server):
        """Test getting a product that doesn't exist"""
        response = requests.get(f"{server}/products/99999", timeout=TIMEOUT)
        assert response.status_code == 404  # Not Found
    
    def test_update_nonexistent_product(self, server):
        """Test updating a product that doesn't exist"""
        response = requests.put(
            f"{server}/products/99999",
            json=TEST_PRODUCT,
            headers={"Content-Type": "application/json"},
            timeout=TIMEOUT
        )
        assert response.status_code == 404  # Not Found
    
    def test_delete_nonexistent_product(self, server):
        """Test deleting a product that doesn't exist"""
        response = requests.delete(f"{server}/products/99999", timeout=TIMEOUT)
        assert response.status_code == 404  # Not Found

if __name__ == "__main__":
    # Run pytest with specific options
    pytest.main(['-xvs', __file__])