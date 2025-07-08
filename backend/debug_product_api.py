import requests
import json
import logging
import traceback
import sys

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_server_status():
    """Test if the server is running"""
    url = "http://127.0.0.1:8000/"
    try:
        response = requests.get(url, timeout=5)
        logger.info(f"Server status: {response.status_code}")
        logger.info(f"Server response: {response.text}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        logger.error("Server is not running")
        return False

def test_add_product_with_seller_id():
    """Test adding a product with seller_id via the API"""
    url = "http://127.0.0.1:8000/products"
    
    # Test data with seller_id
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
        logger.debug(f"Request headers: Content-Type: application/json")
        
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

if __name__ == "__main__":
    # First check if server is running
    if not test_server_status():
        logger.error("Server is not running. Please start the server first.")
        sys.exit(1)
    
    # Test adding a product with seller_id
    logger.info("\n=== Testing Add Product With Seller ID ===\n")
    add_result = test_add_product_with_seller_id()
    
    # Summary
    logger.info("\n=== Test Summary ===\n")
    logger.info(f"Add Product Test: {'PASSED' if add_result else 'FAILED'}")
    
    if not add_result:
        sys.exit(1)