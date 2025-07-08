# OneTappe API Testing Suite

## Overview

This directory contains a comprehensive testing suite for the OneTappe API, focusing on product management, authentication, and seller dashboard functionality. The tests are designed to validate API endpoints, error handling, input validation, and security aspects of the application.

## Test Structure

### Test Files

- **test_product_api_suite.py**: Comprehensive test suite for product API endpoints
- **test_api_pytest.py**: Pytest-based test suite for structured testing
- **debug_seller_id.py**: Specific tests for seller_id handling in product creation
- **test_authentication.py**: Tests for authentication endpoints and role-based access
- **test_seller_dashboard.py**: Tests for seller dashboard functionality
- **run_tests.py**: Script to run all test suites

### Test Plan

The **test_plan.md** file contains a detailed testing strategy, including:

- Test categories and test cases
- Expected results
- Test data
- Reporting guidelines

## Running Tests

### Prerequisites

1. Python 3.6+
2. Required packages: `requests`, `pytest`
3. OneTappe API server (can be started automatically by the test runner)

### Installation

```bash
# Install required packages
pip install requests pytest
```

### Running All Tests

```bash
python run_tests.py --test all
```

### Running Specific Test Suites

```bash
# Run product API tests
python run_tests.py --test product

# Run authentication tests
python run_tests.py --test auth

# Run seller dashboard tests
python run_tests.py --test seller

# Run pytest-based tests
python run_tests.py --test pytest
```

### Running Tests with Existing Server

If the API server is already running, use the `--no-server` flag:

```bash
python run_tests.py --test all --no-server
```

## Test Reports

Test results are logged to the console with detailed information about each test case. The logs include:

- Request details
- Response status codes
- Response bodies
- Error messages (if any)

## Debugging

For debugging specific issues, use the dedicated debug scripts:

```bash
# Debug seller_id issues
python debug_seller_id.py
```

## Known Issues

1. **Seller ID Handling**: The product creation endpoint may return a 500 error if `seller_id` is not provided or is null.

## Contributing

When adding new tests:

1. Follow the existing test structure
2. Include proper error handling and logging
3. Update the test plan document
4. Ensure tests can run both independently and as part of the suite

## Best Practices

- Always check if the server is running before executing tests
- Clean up test data after tests complete
- Use descriptive test names and logging
- Handle exceptions properly to avoid test failures due to infrastructure issues