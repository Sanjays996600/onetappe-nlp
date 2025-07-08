import requests
import json
import logging
import traceback
import sys
import time
import os
import subprocess

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ProductAPITester:
    def __init__(self, base_url="http://127.0.0.1:8000"):
        self.base_url = base_url
        self.server_process = None
        self.product_id = None
    
    def start_server(self):
        """Start the FastAPI server"""
        try:
            logger.info("Starting server...")
            # Get the absolute path to run_app.py
            script_dir = os.path.dirname(os.path.abspath(__file__))
            run_app_path = os.path.join(script_dir, "run_app.py")
            
            # Start the server as a subprocess
            self.server_process = subprocess.Popen(
                [sys.executable, run_app_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Wait for server to start
            logger.info("Waiting for server to start...")
            time.sleep(5)  # Give the server time to start
            
            # Check if server is running
            if self.check_server_status():
                logger.info("Server started successfully")
                return True
            else:
                logger.error("Failed to start server")
                self.stop_server()
                return False
        except Exception as e:
            logger.error(f"Error starting server: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def stop_server(self):
        """Stop the FastAPI server"""
        if self.server_process:
            logger.info("Stopping server...")
            self.server_process.terminate()
            self.server_process.wait()
            self.server_process = None
            logger.info("Server stopped")
    
    def check_server_status(self):
        """Check if the server is running"""
        url = f"{self.base_url}/"
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
    
    def test_add_product(self):
        """Test adding a product via the API"""
        url = f"{self.base_url}/products"
        
        # Test data
        product_data = {
            "product_name": "Test Rice",
            "price": 50.0,
            "stock": 20,
            "description": "Test product added via API",
            "seller_id": 1  # Adding seller_id explicitly
        }
        
        try:
            # Make the POST request
            logger.info(f"Sending POST request to {url} with data: {product_data}")
            
            response = requests.post(
                url, 
                json=product_data,
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # Log the response
            logger.info(f"Response status code: {response.status_code}")
            logger.debug(f"Response headers: {response.headers}")
            
            try:
                response_json = response.json()
                logger.info(f"Response JSON: {json.dumps(response_json, indent=2)}")
                
                # Store product ID for later tests
                if response.status_code == 201 and 'id' in response_json:
                    self.product_id = response_json['id']
                
            except json.JSONDecodeError:
                logger.info(f"Response text: {response.text}")
            
            # Check if the request was successful
            if response.status_code == 201:
                logger.info("Product added successfully!")
                return True
            else:
                logger.error(f"Failed to add product. Status code: {response.status_code}")
                if response.text:
                    logger.error(f"Error response: {response.text}")
                return False
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
        except requests.exceptions.Timeout as e:
            logger.error(f"Request timed out: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def test_get_products(self):
        """Test getting all products via the API"""
        url = f"{self.base_url}/products"
        
        try:
            # Make the GET request
            logger.info(f"Sending GET request to {url}")
            
            response = requests.get(
                url,
                timeout=10
            )
            
            # Log the response
            logger.info(f"Response status code: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.info(f"Found {len(response_json)} products")
                logger.debug(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                logger.info(f"Response text: {response.text}")
            
            # Check if the request was successful
            if response.status_code == 200:
                logger.info("Products retrieved successfully!")
                return True
            else:
                logger.error(f"Failed to get products. Status code: {response.status_code}")
                if response.text:
                    logger.error(f"Error response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def test_get_product_by_id(self):
        """Test getting a specific product by ID"""
        if not self.product_id:
            logger.error("No product ID available. Add a product first.")
            return False
        
        url = f"{self.base_url}/products/{self.product_id}"
        
        try:
            # Make the GET request
            logger.info(f"Sending GET request to {url}")
            
            response = requests.get(
                url,
                timeout=10
            )
            
            # Log the response
            logger.info(f"Response status code: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.info(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                logger.info(f"Response text: {response.text}")
            
            # Check if the request was successful
            if response.status_code == 200:
                logger.info("Product retrieved successfully!")
                return True
            else:
                logger.error(f"Failed to get product. Status code: {response.status_code}")
                if response.text:
                    logger.error(f"Error response: {response.text}")
                return False
        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
    
    def run_all_tests(self):
        """Run all API tests"""
        try:
            # Start server if not already running
            server_started_by_us = False
            if not self.check_server_status():
                server_started_by_us = self.start_server()
                if not server_started_by_us:
                    logger.error("Cannot run tests without a running server")
                    return False
            
            # Run tests
            results = {
                "add_product": self.test_add_product(),
                "get_products": self.test_get_products(),
                "get_product_by_id": self.test_get_product_by_id()
            }
            
            # Print summary
            logger.info("\n=== Test Summary ===\n")
            for test_name, result in results.items():
                logger.info(f"{test_name}: {'PASSED' if result else 'FAILED'}")
            
            # Stop server if we started it
            if server_started_by_us:
                self.stop_server()
            
            # Return overall result
            return all(results.values())
        except Exception as e:
            logger.error(f"Error running tests: {str(e)}")
            logger.debug(traceback.format_exc())
            return False
        finally:
            # Ensure server is stopped if we started it
            if 'server_started_by_us' in locals() and server_started_by_us and self.server_process:
                self.stop_server()

if __name__ == "__main__":
    tester = ProductAPITester()
    success = tester.run_all_tests()
    sys.exit(0 if success else 1)