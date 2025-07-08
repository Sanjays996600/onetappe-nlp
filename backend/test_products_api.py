import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to path

import pytest
from fastapi.testclient import TestClient
from backend.main import app

def test_create_product_success(client):
    """Test successful product creation"""
    # Test data
    product_data = {
        "product_name": "Test Product",
        "price": 99.99,
        "stock": 50,
        "description": "This is a test product"
    }
    
    # Make request
    response = client.post("/products/", json=product_data)
    
    # Assertions
    assert response.status_code == 201
    assert response.json()["success"] == True
    assert "product_id" in response.json()

def test_create_product_validation_error(client):
    """Test validation errors for product creation"""
    # Test cases with invalid data
    test_cases = [
        # Empty product name
        {
            "product_name": "",
            "price": 99.99,
            "stock": 50,
            "description": "Test product"
        },
        # Negative price
        {
            "product_name": "Test Product",
            "price": -10.0,
            "stock": 50,
            "description": "Test product"
        },
        # Negative stock
        {
            "product_name": "Test Product",
            "price": 99.99,
            "stock": -5,
            "description": "Test product"
        },
        # Description too long (over 300 chars)
        {
            "product_name": "Test Product",
            "price": 99.99,
            "stock": 50,
            "description": "A" * 301
        }
    ]
    
    for test_case in test_cases:
        response = client.post("/products/", json=test_case)
        assert response.status_code == 422, f"Expected validation error for {test_case}"

def test_create_product_missing_fields(client):
    """Test missing required fields"""
    # Missing product_name
    response = client.post("/products/", json={
        "price": 99.99,
        "stock": 50
    })
    assert response.status_code == 422
    
    # Missing price
    response = client.post("/products/", json={
        "product_name": "Test Product",
        "stock": 50
    })
    assert response.status_code == 422
    
    # Missing stock
    response = client.post("/products/", json={
        "product_name": "Test Product",
        "price": 99.99
    })
    assert response.status_code == 422

if __name__ == "__main__":
    pytest.main(['-xvs', __file__])