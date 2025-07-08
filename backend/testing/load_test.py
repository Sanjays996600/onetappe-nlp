#!/usr/bin/env python3
"""
Load Testing Script for OneTappe API

This script performs load testing on the OneTappe API using Locust.
It simulates multiple users accessing the API simultaneously and
measures response times, failure rates, and throughput.

Requirements:
- locust (pip install locust)

Usage:
- Run this script directly to start the Locust web interface
- Access the web interface at http://localhost:8089
- Set the number of users, spawn rate, and host in the web interface

Alternatively, run in headless mode:
- locust -f load_test.py --headless -u 100 -r 10 -t 30s --host=http://127.0.0.1:8000
"""

import os
import sys
import json
import time
import random
import logging
from pathlib import Path

try:
    from locust import HttpUser, task, between, events
except ImportError:
    print("Locust is not installed. Please install it using 'pip install locust'")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("load_test.log")
    ]
)
logger = logging.getLogger("load_test")

# Test data
TEST_PRODUCTS = [
    {
        "product_name": "Load Test Product 1",
        "price": 99.99,
        "stock": 100,
        "description": "Product created during load testing 1",
        "seller_id": 1
    },
    {
        "product_name": "Load Test Product 2",
        "price": 149.99,
        "stock": 50,
        "description": "Product created during load testing 2",
        "seller_id": 1
    },
    {
        "product_name": "Load Test Product 3",
        "price": 199.99,
        "stock": 25,
        "description": "Product created during load testing 3",
        "seller_id": 1
    },
]

TEST_USERS = [
    {"username": "test_user1", "password": "password123"},
    {"username": "test_user2", "password": "password123"},
    {"username": "test_user3", "password": "password123"},
]

# Store created product IDs for later use
created_product_ids = []


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when the test is starting"""
    logger.info("Load test is starting")


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when the test is stopping"""
    logger.info("Load test is stopping")
    
    # Generate summary report
    if environment.stats.total.num_requests > 0:
        logger.info("Load Test Summary:")
        logger.info(f"Total Requests: {environment.stats.total.num_requests}")
        logger.info(f"Total Failures: {environment.stats.total.num_failures}")
        logger.info(f"Failure Rate: {environment.stats.total.fail_ratio * 100:.2f}%")
        logger.info(f"Median Response Time: {environment.stats.total.median_response_time} ms")
        logger.info(f"95th Percentile Response Time: {environment.stats.total.get_response_time_percentile(0.95)} ms")
        logger.info(f"Requests Per Second: {environment.stats.total.current_rps}")


class ProductAPIUser(HttpUser):
    """Simulates a user interacting with the Product API"""
    
    # Wait between 1 and 5 seconds between tasks
    wait_time = between(1, 5)
    
    def on_start(self):
        """Called when a user starts"""
        # Try to log in
        if TEST_USERS:
            user = random.choice(TEST_USERS)
            try:
                response = self.client.post("/login", json=user)
                if response.status_code == 200:
                    token = response.json().get("access_token")
                    if token:
                        self.client.headers["Authorization"] = f"Bearer {token}"
                        logger.debug(f"User logged in: {user['username']}")
            except Exception as e:
                logger.error(f"Login failed: {str(e)}")
    
    @task(3)
    def get_all_products(self):
        """Get all products (high frequency task)"""
        with self.client.get("/products", name="Get All Products", catch_response=True) as response:
            if response.status_code == 200:
                products = response.json()
                if isinstance(products, list):
                    # Store product IDs for other tasks
                    product_ids = [p.get("id") for p in products if p.get("id")]
                    if product_ids:
                        global created_product_ids
                        created_product_ids.extend([pid for pid in product_ids if pid not in created_product_ids])
            else:
                response.failure(f"Failed to get products: {response.status_code}")
    
    @task(2)
    def get_product_by_id(self):
        """Get a specific product by ID (medium frequency task)"""
        # Use created product IDs if available, otherwise use a default ID
        product_id = random.choice(created_product_ids) if created_product_ids else 1
        
        with self.client.get(f"/products/{product_id}", name="Get Product by ID", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get product {product_id}: {response.status_code}")
    
    @task(1)
    def add_product(self):
        """Add a new product (low frequency task)"""
        # Create a unique product for each request
        product = random.choice(TEST_PRODUCTS).copy()
        product["product_name"] = f"{product['product_name']} {int(time.time())}"
        
        with self.client.post("/products", json=product, name="Add Product", catch_response=True) as response:
            if response.status_code == 200:
                new_product = response.json()
                if new_product and "id" in new_product:
                    product_id = new_product["id"]
                    if product_id not in created_product_ids:
                        created_product_ids.append(product_id)
            else:
                response.failure(f"Failed to add product: {response.status_code}")
    
    @task(1)
    def update_product(self):
        """Update an existing product (low frequency task)"""
        if not created_product_ids:
            return
        
        product_id = random.choice(created_product_ids)
        update_data = {
            "price": round(random.uniform(10, 1000), 2),
            "stock": random.randint(1, 100)
        }
        
        with self.client.put(f"/products/{product_id}", json=update_data, name="Update Product", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to update product {product_id}: {response.status_code}")
    
    @task(1)
    def search_products(self):
        """Search for products (low frequency task)"""
        search_terms = ["Test", "Product", "Load", "API"]
        search_term = random.choice(search_terms)
        
        with self.client.get(f"/products/search?q={search_term}", name="Search Products", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to search products: {response.status_code}")


class AuthenticationUser(HttpUser):
    """Simulates a user performing authentication operations"""
    
    # Wait between 5 and 15 seconds between tasks
    wait_time = between(5, 15)
    
    @task(3)
    def login(self):
        """Attempt to log in (high frequency task)"""
        if TEST_USERS:
            user = random.choice(TEST_USERS)
            with self.client.post("/login", json=user, name="Login", catch_response=True) as response:
                if response.status_code == 200:
                    data = response.json()
                    if "access_token" not in data:
                        response.failure("Login response missing access token")
                else:
                    response.failure(f"Login failed: {response.status_code}")
    
    @task(1)
    def invalid_login(self):
        """Attempt to log in with invalid credentials (low frequency task)"""
        invalid_user = {
            "username": f"invalid_user_{random.randint(1000, 9999)}",
            "password": "wrong_password"
        }
        
        with self.client.post("/login", json=invalid_user, name="Invalid Login", catch_response=True) as response:
            # This should fail with 401, so we mark it as success if it does
            if response.status_code == 401:
                response.success()
            else:
                response.failure(f"Expected 401, got {response.status_code}")


class SellerDashboardUser(HttpUser):
    """Simulates a seller using the dashboard"""
    
    # Wait between 3 and 8 seconds between tasks
    wait_time = between(3, 8)
    
    def on_start(self):
        """Called when a user starts"""
        # Log in as a seller
        if TEST_USERS:
            user = random.choice(TEST_USERS)
            try:
                response = self.client.post("/login", json=user)
                if response.status_code == 200:
                    token = response.json().get("access_token")
                    if token:
                        self.client.headers["Authorization"] = f"Bearer {token}"
                        logger.debug(f"Seller logged in: {user['username']}")
            except Exception as e:
                logger.error(f"Seller login failed: {str(e)}")
    
    @task(3)
    def get_seller_products(self):
        """Get products for the seller (high frequency task)"""
        with self.client.get("/seller/products", name="Get Seller Products", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get seller products: {response.status_code}")
    
    @task(2)
    def get_seller_orders(self):
        """Get orders for the seller (medium frequency task)"""
        with self.client.get("/seller/orders", name="Get Seller Orders", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get seller orders: {response.status_code}")
    
    @task(1)
    def get_seller_dashboard(self):
        """Get seller dashboard data (low frequency task)"""
        with self.client.get("/seller/dashboard", name="Get Seller Dashboard", catch_response=True) as response:
            if response.status_code != 200:
                response.failure(f"Failed to get seller dashboard: {response.status_code}")


def ensure_server_running():
    """Ensure the API server is running."""
    import requests
    
    try:
        response = requests.get("http://127.0.0.1:8000/")
        return response.status_code < 500
    except requests.RequestException:
        logger.warning("API server is not running. Starting server...")
        
        # Start the server in a separate process
        server_script = Path("../run_app.py").resolve()
        if not server_script.exists():
            logger.error(f"Server script not found at {server_script}")
            return False
        
        import subprocess
        subprocess.Popen([sys.executable, str(server_script)], 
                        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Wait for server to start
        for _ in range(10):
            time.sleep(1)
            try:
                response = requests.get("http://127.0.0.1:8000/")
                if response.status_code < 500:
                    logger.info("Server started successfully.")
                    return True
            except requests.RequestException:
                pass
        
        logger.error("Failed to start server.")
        return False


if __name__ == "__main__":
    # Check if server is running
    if not ensure_server_running():
        logger.error("Cannot run load tests without a running server.")
        sys.exit(1)
    
    # If running directly, start Locust
    # This allows the script to be imported without starting Locust
    from locust.env import Environment
    from locust.stats import stats_printer, stats_history
    from locust.log import setup_logging
    import gevent
    
    # Check if running with command line arguments
    if len(sys.argv) > 1:
        # Let Locust handle command line arguments
        from locust.main import main
        main()
    else:
        # Start Locust web interface
        setup_logging("INFO", None)
        
        # Create a local environment
        env = Environment(user_classes=[ProductAPIUser, AuthenticationUser, SellerDashboardUser])
        env.create_local_runner()
        
        # Start a WebUI instance
        env.create_web_ui("127.0.0.1", 8089)
        
        # Start a greenlet that periodically outputs the current stats
        gevent.spawn(stats_printer(env.stats))
        
        # Start a greenlet that saves current stats to history
        gevent.spawn(stats_history, env.runner)
        
        # Start the test
        env.runner.greenlet.join()