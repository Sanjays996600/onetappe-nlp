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
TEST_USERS = [
    {"username": "test_admin", "password": "admin123", "role": "admin"},
    {"username": "test_seller", "password": "seller123", "role": "seller"},
    {"username": "test_user", "password": "user123", "role": "user"}
]

class AuthenticationTester:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.tokens = {}
        self.headers = {"Content-Type": "application/json"}
    
    def test_login_valid(self, username: str, password: str, role: str) -> bool:
        """Test login with valid credentials"""
        url = f"{self.base_url}/login"
        data = {"username": username, "password": password}
        
        try:
            logger.info(f"Testing login with valid credentials for {role} user")
            response = requests.post(
                url,
                json=data,
                headers=self.headers,
                timeout=TIMEOUT
            )
            
            logger.info(f"Response status code: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.debug(f"Response JSON: {json.dumps(response_json, indent=2)}")
                
                if "access_token" in response_json:
                    self.tokens[role] = response_json["access_token"]
                    logger.info(f"Received token for {role} user")
                    return True
                else:
                    logger.error("No token in response")
                    return False
            except json.JSONDecodeError:
                logger.info(f"Response text: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Exception during login: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def test_login_invalid(self) -> bool:
        """Test login with invalid credentials"""
        url = f"{self.base_url}/login"
        data = {"username": "invalid_user", "password": "invalid_password"}
        
        try:
            logger.info("Testing login with invalid credentials")
            response = requests.post(
                url,
                json=data,
                headers=self.headers,
                timeout=TIMEOUT
            )
            
            logger.info(f"Response status code: {response.status_code}")
            
            # Should get 401 Unauthorized
            return response.status_code == 401
        except Exception as e:
            logger.error(f"Exception during invalid login test: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def test_protected_endpoint(self, endpoint: str, role: str, expected_status: int) -> bool:
        """Test accessing a protected endpoint with a specific role"""
        url = f"{self.base_url}{endpoint}"
        
        if role not in self.tokens:
            logger.error(f"No token available for {role} role")
            return False
        
        headers = self.headers.copy()
        headers["Authorization"] = f"Bearer {self.tokens[role]}"
        
        try:
            logger.info(f"Testing access to {endpoint} with {role} role")
            response = requests.get(
                url,
                headers=headers,
                timeout=TIMEOUT
            )
            
            logger.info(f"Response status code: {response.status_code}")
            
            return response.status_code == expected_status
        except Exception as e:
            logger.error(f"Exception during protected endpoint test: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def test_token_expiration(self, role: str) -> bool:
        """Test token expiration (if applicable)"""
        # This test is optional and depends on the token expiration time
        # For testing purposes, we'll just log a message
        logger.info("Token expiration test is not implemented")
        return True
    
    def run_all_tests(self) -> bool:
        """Run all authentication tests"""
        try:
            # Test valid logins for all roles
            login_results = []
            for user in TEST_USERS:
                result = self.test_login_valid(user["username"], user["password"], user["role"])
                login_results.append((f"login_{user['role']}", result))
            
            # Test invalid login
            invalid_login_result = self.test_login_invalid()
            
            # Test protected endpoints
            endpoint_tests = [
                # (endpoint, role, expected_status)
                ("/admin-only", "admin", 200),  # Admin should have access
                ("/admin-only", "seller", 403),  # Seller should be forbidden
                ("/admin-only", "user", 403),    # User should be forbidden
                ("/seller/dashboard", "seller", 200),  # Seller should have access
                ("/seller/dashboard", "user", 403)    # User should be forbidden
            ]
            
            endpoint_results = []
            for endpoint, role, expected_status in endpoint_tests:
                if role in self.tokens:  # Only test if we have a token for this role
                    result = self.test_protected_endpoint(endpoint, role, expected_status)
                    endpoint_results.append((f"{role}_access_{endpoint}", result))
            
            # Combine all results
            all_results = dict(login_results + [("invalid_login", invalid_login_result)] + endpoint_results)
            
            # Print summary
            logger.info("\n=== Test Summary ===\n")
            for test_name, result in all_results.items():
                logger.info(f"{test_name}: {'PASSED' if result else 'FAILED'}")
            
            # Return overall result
            return all(all_results.values())
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
    
    # Run authentication tests
    tester = AuthenticationTester()
    success = tester.run_all_tests()
    
    sys.exit(0 if success else 1)