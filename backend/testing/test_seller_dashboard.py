import requests
import json
import logging
import traceback
import sys
import time
from typing import Dict, Any, Optional

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 10

# Test credentials
TEST_SELLER = {
    "username": "test_seller",
    "password": "password123"
}

class SellerDashboardTester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.token = None
        self.headers = {"Content-Type": "application/json"}
    
    def login(self, username: str, password: str) -> bool:
        """Login and get authentication token"""
        url = f"{self.base_url}/login"
        data = {"username": username, "password": password}
        
        try:
            logger.info(f"Logging in as {username}")
            response = requests.post(
                url,
                json=data,
                headers=self.headers,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if "access_token" in response_data:
                    self.token = response_data["access_token"]
                    self.headers["Authorization"] = f"Bearer {self.token}"
                    logger.info("Login successful")
                    return True
                else:
                    logger.error("No token in response")
                    return False
            else:
                logger.error(f"Login failed with status code {response.status_code}")
                logger.error(f"Response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Exception during login: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def test_dashboard_access(self) -> bool:
        """Test accessing the seller dashboard"""
        url = f"{self.base_url}/seller/dashboard"
        
        try:
            logger.info("Testing dashboard access")
            response = requests.get(
                url,
                headers=self.headers,
                timeout=TIMEOUT
            )
            
            logger.info(f"Response status code: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.info(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                logger.info(f"Response text: {response.text}")
            
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Exception during dashboard access: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def test_orders_access(self) -> bool:
        """Test accessing the seller orders"""
        url = f"{self.base_url}/seller/orders"
        
        try:
            logger.info("Testing orders access")
            response = requests.get(
                url,
                headers=self.headers,
                timeout=TIMEOUT
            )
            
            logger.info(f"Response status code: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.info(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                logger.info(f"Response text: {response.text}")
            
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Exception during orders access: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def test_inventory_access(self) -> bool:
        """Test accessing the seller inventory"""
        url = f"{self.base_url}/seller/inventory"
        
        try:
            logger.info("Testing inventory access")
            response = requests.get(
                url,
                headers=self.headers,
                timeout=TIMEOUT
            )
            
            logger.info(f"Response status code: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.info(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                logger.info(f"Response text: {response.text}")
            
            return response.status_code == 200
        except Exception as e:
            logger.error(f"Exception during inventory access: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def test_unauthorized_access(self) -> bool:
        """Test accessing endpoints without authentication"""
        endpoints = [
            "/seller/dashboard",
            "/seller/orders",
            "/seller/inventory",
            "/admin-only"
        ]
        
        results = []
        
        # Save current headers and remove authorization
        original_headers = self.headers.copy()
        if "Authorization" in self.headers:
            del self.headers["Authorization"]
        
        for endpoint in endpoints:
            url = f"{self.base_url}{endpoint}"
            try:
                logger.info(f"Testing unauthorized access to {endpoint}")
                response = requests.get(
                    url,
                    headers=self.headers,
                    timeout=TIMEOUT
                )
                
                logger.info(f"Response status code: {response.status_code}")
                
                # Should get 401 Unauthorized
                results.append(response.status_code == 401)
            except Exception as e:
                logger.error(f"Exception during unauthorized access test: {str(e)}")
                results.append(False)
        
        # Restore original headers
        self.headers = original_headers
        
        # All tests should pass (all endpoints should return 401)
        return all(results)
    
    def run_all_tests(self) -> bool:
        """Run all seller dashboard tests"""
        try:
            # First try to login
            if not self.login(TEST_SELLER["username"], TEST_SELLER["password"]):
                logger.warning("Login failed, continuing with tests but they may fail")
            
            # Run tests
            results = {
                "dashboard_access": self.test_dashboard_access(),
                "orders_access": self.test_orders_access(),
                "inventory_access": self.test_inventory_access(),
                "unauthorized_access": self.test_unauthorized_access()
            }
            
            # Print summary
            logger.info("\n=== Test Summary ===\n")
            for test_name, result in results.items():
                logger.info(f"{test_name}: {'PASSED' if result else 'FAILED'}")
            
            # Return overall result
            return all(results.values())
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}")
            logger.debug(traceback.format_exc())
            return False

def test_server_status():
    """Test if the server is running"""
    url = f"{BASE_URL}/"
    try:
        response = requests.get(url, timeout=5)
        logger.info(f"Server status: {response.status_code}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        logger.error("Server is not running")
        return False
    except Exception as e:
        logger.error(f"Error checking server status: {str(e)}")
        return False

if __name__ == "__main__":
    # First check if server is running
    if not test_server_status():
        logger.error("Server is not running. Please start the server first.")
        sys.exit(1)
    
    # Run seller dashboard tests
    tester = SellerDashboardTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)