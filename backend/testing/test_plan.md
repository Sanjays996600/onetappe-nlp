# OneTappe API Testing Plan

## Overview
This document outlines the testing strategy for the OneTappe API, focusing on product management endpoints and seller dashboard functionality.

## Test Environment
- Local development environment
- FastAPI backend running on http://127.0.0.1:8000
- Python test scripts for automated testing

## Test Categories

### 1. API Endpoint Testing

#### 1.1 Product Management

| Test Case ID | Description | Method | Endpoint | Expected Result |
|--------------|-------------|--------|----------|----------------|
| PROD-001 | Get all products | GET | /products | 200 OK with product list |
| PROD-002 | Get product by ID | GET | /products/{id} | 200 OK with product details |
| PROD-003 | Add new product | POST | /products | 201 Created with product details |
| PROD-004 | Update product | PUT | /products/{id} | 200 OK with updated product |
| PROD-005 | Delete product | DELETE | /products/{id} | 200 OK with success message |
| PROD-006 | Add product with invalid data | POST | /products | 422 Unprocessable Entity |
| PROD-007 | Get non-existent product | GET | /products/{invalid_id} | 404 Not Found |

#### 1.2 Authentication

| Test Case ID | Description | Method | Endpoint | Expected Result |
|--------------|-------------|--------|----------|----------------|
| AUTH-001 | Login with valid credentials | POST | /login | 200 OK with token |
| AUTH-002 | Login with invalid credentials | POST | /login | 401 Unauthorized |
| AUTH-003 | Access protected endpoint with valid token | GET | /admin-only | 200 OK |
| AUTH-004 | Access protected endpoint with invalid token | GET | /admin-only | 401 Unauthorized |

#### 1.3 Seller Dashboard

| Test Case ID | Description | Method | Endpoint | Expected Result |
|--------------|-------------|--------|----------|----------------|
| SELL-001 | Get seller dashboard | GET | /seller/dashboard | 200 OK with dashboard data |
| SELL-002 | Get seller orders | GET | /seller/orders | 200 OK with orders list |
| SELL-003 | Get seller inventory | GET | /seller/inventory | 200 OK with inventory list |

### 2. Integration Testing

| Test Case ID | Description | Expected Result |
|--------------|-------------|----------------|
| INT-001 | Add product and verify it appears in inventory | Product added and visible in inventory |
| INT-002 | Update product and verify changes in inventory | Product updated and changes reflected in inventory |
| INT-003 | Delete product and verify removal from inventory | Product deleted and removed from inventory |

### 3. Security Testing

| Test Case ID | Description | Expected Result |
|--------------|-------------|----------------|
| SEC-001 | Access seller endpoints without authentication | 401 Unauthorized |
| SEC-002 | Access admin endpoints with seller token | 403 Forbidden |
| SEC-003 | Input validation for SQL injection | 422 Unprocessable Entity or sanitized input |

### 4. Performance Testing

| Test Case ID | Description | Expected Result |
|--------------|-------------|----------------|
| PERF-001 | Response time for product listing | < 500ms |
| PERF-002 | Response time for dashboard data | < 1000ms |
| PERF-003 | Concurrent API requests | All requests handled without errors |

## Test Data

### Sample Product Data
```json
{
  "product_name": "Test Rice",
  "price": 50.0,
  "stock": 20,
  "description": "Test product for API testing",
  "seller_id": 1
}
```

### Sample User Credentials
```json
{
  "username": "test_seller",
  "password": "password123"
}
```

## Test Scripts

1. `test_product_api_suite.py` - Comprehensive test suite for product API
2. `debug_seller_id.py` - Specific tests for seller_id handling
3. `test_authentication.py` - Tests for authentication endpoints
4. `test_seller_dashboard.py` - Tests for seller dashboard functionality

## Known Issues

1. **Seller ID Handling**: The product creation endpoint currently has issues with the `seller_id` field. The API may return a 500 error if `seller_id` is not provided or is null.

## Test Execution

### Prerequisites
1. Server is running on http://127.0.0.1:8000
2. Database is initialized with test data
3. Required Python packages are installed:
   - requests
   - pytest (for automated tests)

### Running Tests
```bash
# Run all tests
python -m pytest

# Run specific test file
python test_product_api_suite.py

# Run with detailed logging
python debug_seller_id.py
```

## Reporting

Test results will be documented with:
- Test case ID
- Pass/Fail status
- Error messages (if applicable)
- Response times
- Screenshots (for UI tests)

## Continuous Integration

Tests should be integrated into the CI pipeline to run automatically on code changes.