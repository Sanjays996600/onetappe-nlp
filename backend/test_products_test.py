import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from main import app
from auth.jwt import create_access_token

import pytest
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_products_unauthorized():
    response = client.get("/seller/products")
    assert response.status_code == 401

def test_get_products_authorized():
    token = create_access_token({"sub": "test_user@example.com", "role": "seller"})  # Generate a valid test token with role
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/seller/products", headers=headers)
    print("Token used:", token)
    print("Response status:", response.status_code)
    print("Response body:", response.text)
    assert response.status_code == 200

def test_delete_product_authorized():
    token = create_access_token({"sub": "test_user@example.com", "role": "seller"})
    headers = {"Authorization": f"Bearer {token}"}

    # First, create a product to delete
    product_data = {"name": "Test Product", "price": 10.0, "stock": 5}
    create_response = client.post("/seller/products/", json=product_data, headers=headers)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Now, delete the product
    delete_response = client.delete(f"/seller/products/{product_id}", headers=headers)
    assert delete_response.status_code == 200 or delete_response.status_code == 204

    # Verify deletion
    get_response = client.get("/seller/products/", headers=headers)
    products = get_response.json()
    assert all(p["id"] != product_id for p in products)

def test_view_inventory_authorized():
    token = create_access_token({"sub": "test_user@example.com", "role": "seller"})
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/inventory/", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_update_stock_authorized():
    token = create_access_token({"sub": "test_user@example.com", "role": "seller"})
    headers = {"Authorization": f"Bearer {token}"}

    # Create a product first
    product_data = {"name": "Stock Test Product", "price": 15.0, "stock": 10}
    create_response = client.post("/seller/products/", json=product_data, headers=headers)
    assert create_response.status_code == 201
    product_id = create_response.json()["id"]

    # Update stock
    update_data = {"product_id": product_id, "stock": 30}
    update_response = client.post("/inventory/update", json=update_data, headers=headers)
    assert update_response.status_code == 200
    assert f"Stock for Product ID {product_id} updated to 30 units." in update_response.json().get("reply", "")


def test_update_stock_invalid_product():
    token = create_access_token({"sub": "test_user@example.com", "role": "seller"})
    headers = {"Authorization": f"Bearer {token}"}
    update_data = {"product_id": 999999, "stock": 30}
    update_response = client.post("/inventory/update", json=update_data, headers=headers)
    assert update_response.status_code == 404
    assert update_response.json().get("detail") == "Product not found"

# Additional tests can be added here