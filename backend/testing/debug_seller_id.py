import requests
import json
import logging
import traceback
import sys
import time

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_server_status():
    """Test if the server is running"""
    url = "http://127.0.0.1:8000/"
    try:
        response = requests.get(url, timeout=5)
        logger.info(f"Server status: {response.status_code}")
        logger.info(f"Server response: {response.text[:100]}")
        return response.status_code == 200
    except requests.exceptions.ConnectionError:
        logger.error("Server is not running")
        return False
    except Exception as e:
        logger.error(f"Error checking server status: {str(e)}")
        logger.debug(traceback.format_exc())
        return False

def view_products_schema():
    """View the OpenAPI schema for products endpoint"""
    url = "http://127.0.0.1:8000/openapi.json"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            schema = response.json()
            # Look for product schema
            if 'components' in schema and 'schemas' in schema['components']:
                schemas = schema['components']['schemas']
                for schema_name, schema_def in schemas.items():
                    if 'Product' in schema_name:
                        logger.info(f"Found product schema: {schema_name}")
                        logger.info(json.dumps(schema_def, indent=2))
            
            # Look for product endpoints
            if 'paths' in schema:
                for path, methods in schema['paths'].items():
                    if 'products' in path:
                        logger.info(f"Found product endpoint: {path}")
                        logger.info(json.dumps(methods, indent=2))
            
            return True
        else:
            logger.error(f"Failed to get OpenAPI schema. Status code: {response.status_code}")
            return False
    except Exception as e:
        logger.error(f"Error viewing schema: {str(e)}")
        logger.debug(traceback.format_exc())
        return False

def test_add_product_variations():
    """Test adding a product with different variations of data"""
    url = "http://127.0.0.1:8000/products"
    
    # Test variations
    variations = [
        {
            "name": "With seller_id",
            "data": {
                "product_name": "Test Rice 1",
                "price": 50.0,
                "stock": 20,
                "description": "Test with seller_id",
                "seller_id": 1
            }
        },
        {
            "name": "Without seller_id",
            "data": {
                "product_name": "Test Rice 2",
                "price": 50.0,
                "stock": 20,
                "description": "Test without seller_id"
            }
        },
        {
            "name": "With null seller_id",
            "data": {
                "product_name": "Test Rice 3",
                "price": 50.0,
                "stock": 20,
                "description": "Test with null seller_id",
                "seller_id": None
            }
        }
    ]
    
    results = []
    
    for variation in variations:
        try:
            logger.info(f"\n=== Testing {variation['name']} ===\n")
            logger.info(f"Sending POST request to {url} with data: {variation['data']}")
            
            response = requests.post(
                url, 
                json=variation['data'],
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            # Log the response
            logger.info(f"Response status code: {response.status_code}")
            
            try:
                response_json = response.json()
                logger.info(f"Response JSON: {json.dumps(response_json, indent=2)}")
            except json.JSONDecodeError:
                logger.info(f"Response text: {response.text}")
            
            # Store result
            success = response.status_code in [200, 201]
            results.append({
                "name": variation['name'],
                "success": success,
                "status_code": response.status_code
            })
            
        except Exception as e:
            logger.error(f"Exception occurred: {str(e)}")
            logger.debug(traceback.format_exc())
            results.append({
                "name": variation['name'],
                "success": False,
                "error": str(e)
            })
    
    # Print summary
    logger.info("\n=== Test Summary ===\n")
    for result in results:
        status = "PASSED" if result.get("success", False) else "FAILED"
        logger.info(f"{result['name']}: {status} (Status code: {result.get('status_code', 'N/A')})")
    
    return any(result.get("success", False) for result in results)

if __name__ == "__main__":
    # First check if server is running
    if not test_server_status():
        logger.error("Server is not running. Please start the server first.")
        sys.exit(1)
    
    # View schema to understand the API
    logger.info("\n=== Viewing API Schema ===\n")
    view_products_schema()
    
    # Test adding products with variations
    logger.info("\n=== Testing Product Variations ===\n")
    success = test_add_product_variations()
    
    if not success:
        sys.exit(1)