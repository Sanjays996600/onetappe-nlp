#!/usr/bin/env python3
"""
Test Data Validator for OneTappe API

This script validates test data to ensure it meets the requirements and constraints
of the OneTappe API. It checks for:
- Data integrity and consistency
- Required fields and data types
- Business logic constraints
- Edge cases and boundary values

The validator can be used to check both generated test data and actual database data.
"""

import os
import sys
import json
import argparse
import logging
from pathlib import Path
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("data_validation.log")
    ]
)
logger = logging.getLogger("test_data_validator")

# Constants
TEST_DATA_DIR = "test_data"
USERS_FILE = os.path.join(TEST_DATA_DIR, "users.json")
PRODUCTS_FILE = os.path.join(TEST_DATA_DIR, "products.json")
ORDERS_FILE = os.path.join(TEST_DATA_DIR, "orders.json")
REVIEWS_FILE = os.path.join(TEST_DATA_DIR, "reviews.json")
VALIDATION_REPORT_FILE = os.path.join(TEST_DATA_DIR, "validation_report.md")


class ValidationError(Exception):
    """Exception raised for validation errors."""
    pass


class TestDataValidator:
    """Validator for OneTappe API test data."""
    
    def __init__(self, data_dir=TEST_DATA_DIR):
        """Initialize the validator with the data directory."""
        self.data_dir = data_dir
        self.users_file = os.path.join(data_dir, "users.json")
        self.products_file = os.path.join(data_dir, "products.json")
        self.orders_file = os.path.join(data_dir, "orders.json")
        self.reviews_file = os.path.join(data_dir, "reviews.json")
        
        self.users = []
        self.products = []
        self.orders = []
        self.reviews = []
        
        self.validation_results = {
            "users": {"passed": 0, "failed": 0, "warnings": 0, "errors": []},
            "products": {"passed": 0, "failed": 0, "warnings": 0, "errors": []},
            "orders": {"passed": 0, "failed": 0, "warnings": 0, "errors": []},
            "reviews": {"passed": 0, "failed": 0, "warnings": 0, "errors": []},
            "relationships": {"passed": 0, "failed": 0, "warnings": 0, "errors": []}
        }
    
    def load_data(self):
        """Load test data from JSON files."""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, "r") as f:
                    self.users = json.load(f)
                logger.info(f"Loaded {len(self.users)} users from {self.users_file}")
            else:
                logger.warning(f"Users file not found: {self.users_file}")
            
            if os.path.exists(self.products_file):
                with open(self.products_file, "r") as f:
                    self.products = json.load(f)
                logger.info(f"Loaded {len(self.products)} products from {self.products_file}")
            else:
                logger.warning(f"Products file not found: {self.products_file}")
            
            if os.path.exists(self.orders_file):
                with open(self.orders_file, "r") as f:
                    self.orders = json.load(f)
                logger.info(f"Loaded {len(self.orders)} orders from {self.orders_file}")
            else:
                logger.warning(f"Orders file not found: {self.orders_file}")
            
            if os.path.exists(self.reviews_file):
                with open(self.reviews_file, "r") as f:
                    self.reviews = json.load(f)
                logger.info(f"Loaded {len(self.reviews)} reviews from {self.reviews_file}")
            else:
                logger.warning(f"Reviews file not found: {self.reviews_file}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error loading test data: {e}")
            return False
    
    def validate_users(self):
        """Validate user data."""
        logger.info("Validating user data...")
        
        for user in self.users:
            try:
                # Check required fields
                required_fields = ["id", "username", "email", "password", "first_name", "last_name", "role"]
                for field in required_fields:
                    if field not in user:
                        raise ValidationError(f"Missing required field: {field}")
                
                # Check data types
                if not isinstance(user["id"], int):
                    raise ValidationError(f"User ID must be an integer: {user['id']}")
                
                if not isinstance(user["username"], str):
                    raise ValidationError(f"Username must be a string: {user['username']}")
                
                if not isinstance(user["email"], str):
                    raise ValidationError(f"Email must be a string: {user['email']}")
                
                # Check email format (basic check)
                if "@" not in user["email"] or "." not in user["email"]:
                    raise ValidationError(f"Invalid email format: {user['email']}")
                
                # Check role
                if user["role"] not in ["customer", "seller", "admin"]:
                    raise ValidationError(f"Invalid role: {user['role']}")
                
                # Check role-specific fields
                if user["role"] == "seller" and "seller_info" not in user:
                    raise ValidationError(f"Seller user missing seller_info: {user['id']}")
                
                if user["role"] == "customer" and "customer_info" not in user:
                    raise ValidationError(f"Customer user missing customer_info: {user['id']}")
                
                # Check seller_info fields
                if user["role"] == "seller":
                    seller_info = user["seller_info"]
                    seller_required_fields = ["store_name", "description", "rating", "total_sales"]
                    for field in seller_required_fields:
                        if field not in seller_info:
                            raise ValidationError(f"Missing required seller_info field: {field}")
                    
                    # Check rating range
                    if not (0 <= seller_info["rating"] <= 5):
                        raise ValidationError(f"Seller rating must be between 0 and 5: {seller_info['rating']}")
                
                # Check customer_info fields
                if user["role"] == "customer":
                    customer_info = user["customer_info"]
                    customer_required_fields = ["shipping_address", "phone"]
                    for field in customer_required_fields:
                        if field not in customer_info:
                            raise ValidationError(f"Missing required customer_info field: {field}")
                
                self.validation_results["users"]["passed"] += 1
            
            except ValidationError as e:
                self.validation_results["users"]["failed"] += 1
                error = {"id": user.get("id", "unknown"), "error": str(e)}
                self.validation_results["users"]["errors"].append(error)
                logger.error(f"User validation error: {error}")
            
            except Exception as e:
                self.validation_results["users"]["failed"] += 1
                error = {"id": user.get("id", "unknown"), "error": f"Unexpected error: {str(e)}"}
                self.validation_results["users"]["errors"].append(error)
                logger.error(f"User validation error: {error}")
        
        logger.info(f"User validation complete: {self.validation_results['users']['passed']} passed, {self.validation_results['users']['failed']} failed")
    
    def validate_products(self):
        """Validate product data."""
        logger.info("Validating product data...")
        
        seller_ids = [user["id"] for user in self.users if user["role"] == "seller"]
        
        for product in self.products:
            try:
                # Check required fields
                required_fields = ["id", "product_name", "price", "stock", "description", "category", "seller_id"]
                for field in required_fields:
                    if field not in product:
                        raise ValidationError(f"Missing required field: {field}")
                
                # Check data types
                if not isinstance(product["id"], int):
                    raise ValidationError(f"Product ID must be an integer: {product['id']}")
                
                if not isinstance(product["product_name"], str):
                    raise ValidationError(f"Product name must be a string: {product['product_name']}")
                
                if not isinstance(product["price"], (int, float)):
                    raise ValidationError(f"Price must be a number: {product['price']}")
                
                if not isinstance(product["stock"], int):
                    raise ValidationError(f"Stock must be an integer: {product['stock']}")
                
                # Check value constraints
                if product["price"] < 0:
                    raise ValidationError(f"Price cannot be negative: {product['price']}")
                
                if product["stock"] < 0:
                    raise ValidationError(f"Stock cannot be negative: {product['stock']}")
                
                # Check seller_id exists
                if product["seller_id"] not in seller_ids:
                    raise ValidationError(f"Invalid seller_id: {product['seller_id']}")
                
                # Check rating range if present
                if "rating" in product and not (0 <= product["rating"] <= 5):
                    raise ValidationError(f"Product rating must be between 0 and 5: {product['rating']}")
                
                self.validation_results["products"]["passed"] += 1
            
            except ValidationError as e:
                self.validation_results["products"]["failed"] += 1
                error = {"id": product.get("id", "unknown"), "error": str(e)}
                self.validation_results["products"]["errors"].append(error)
                logger.error(f"Product validation error: {error}")
            
            except Exception as e:
                self.validation_results["products"]["failed"] += 1
                error = {"id": product.get("id", "unknown"), "error": f"Unexpected error: {str(e)}"}
                self.validation_results["products"]["errors"].append(error)
                logger.error(f"Product validation error: {error}")
        
        logger.info(f"Product validation complete: {self.validation_results['products']['passed']} passed, {self.validation_results['products']['failed']} failed")
    
    def validate_orders(self):
        """Validate order data."""
        logger.info("Validating order data...")
        
        customer_ids = [user["id"] for user in self.users if user["role"] == "customer"]
        product_ids = [product["id"] for product in self.products]
        
        for order in self.orders:
            try:
                # Check required fields
                required_fields = ["id", "customer_id", "order_date", "status", "payment_method", "line_items", "total_amount"]
                for field in required_fields:
                    if field not in order:
                        raise ValidationError(f"Missing required field: {field}")
                
                # Check data types
                if not isinstance(order["id"], int):
                    raise ValidationError(f"Order ID must be an integer: {order['id']}")
                
                if not isinstance(order["customer_id"], int):
                    raise ValidationError(f"Customer ID must be an integer: {order['customer_id']}")
                
                if not isinstance(order["line_items"], list):
                    raise ValidationError(f"Line items must be a list: {order['id']}")
                
                # Check customer_id exists
                if order["customer_id"] not in customer_ids:
                    raise ValidationError(f"Invalid customer_id: {order['customer_id']}")
                
                # Check status
                valid_statuses = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]
                if order["status"] not in valid_statuses:
                    raise ValidationError(f"Invalid order status: {order['status']}")
                
                # Check line items
                if len(order["line_items"]) == 0:
                    raise ValidationError(f"Order must have at least one line item: {order['id']}")
                
                total = 0
                for item in order["line_items"]:
                    # Check required fields
                    item_required_fields = ["product_id", "product_name", "quantity", "price", "line_total"]
                    for field in item_required_fields:
                        if field not in item:
                            raise ValidationError(f"Missing required line item field: {field}")
                    
                    # Check product_id exists
                    if item["product_id"] not in product_ids:
                        raise ValidationError(f"Invalid product_id in line item: {item['product_id']}")
                    
                    # Check quantity
                    if not isinstance(item["quantity"], int) or item["quantity"] <= 0:
                        raise ValidationError(f"Line item quantity must be a positive integer: {item['quantity']}")
                    
                    # Check price
                    if not isinstance(item["price"], (int, float)) or item["price"] < 0:
                        raise ValidationError(f"Line item price must be a non-negative number: {item['price']}")
                    
                    # Check line_total calculation
                    expected_line_total = item["quantity"] * item["price"]
                    if abs(item["line_total"] - expected_line_total) > 0.01:  # Allow small floating-point differences
                        raise ValidationError(f"Line item total incorrect: {item['line_total']} != {expected_line_total}")
                    
                    total += item["line_total"]
                
                # Check subtotal calculation
                if "subtotal" in order:
                    if abs(order["subtotal"] - total) > 0.01:  # Allow small floating-point differences
                        raise ValidationError(f"Order subtotal incorrect: {order['subtotal']} != {total}")
                
                # Check total_amount calculation
                expected_total = total
                if "discount" in order:
                    expected_total -= order["discount"]
                if "shipping_fee" in order:
                    expected_total += order["shipping_fee"]
                
                if abs(order["total_amount"] - expected_total) > 0.01:  # Allow small floating-point differences
                    raise ValidationError(f"Order total_amount incorrect: {order['total_amount']} != {expected_total}")
                
                # Check tracking info for shipped/delivered orders
                if order["status"] in ["Shipped", "Delivered"]:
                    if "tracking_number" not in order:
                        self.validation_results["orders"]["warnings"] += 1
                        logger.warning(f"Shipped/delivered order missing tracking number: {order['id']}")
                
                self.validation_results["orders"]["passed"] += 1
            
            except ValidationError as e:
                self.validation_results["orders"]["failed"] += 1
                error = {"id": order.get("id", "unknown"), "error": str(e)}
                self.validation_results["orders"]["errors"].append(error)
                logger.error(f"Order validation error: {error}")
            
            except Exception as e:
                self.validation_results["orders"]["failed"] += 1
                error = {"id": order.get("id", "unknown"), "error": f"Unexpected error: {str(e)}"}
                self.validation_results["orders"]["errors"].append(error)
                logger.error(f"Order validation error: {error}")
        
        logger.info(f"Order validation complete: {self.validation_results['orders']['passed']} passed, {self.validation_results['orders']['failed']} failed, {self.validation_results['orders']['warnings']} warnings")
    
    def validate_reviews(self):
        """Validate review data."""
        logger.info("Validating review data...")
        
        customer_ids = [user["id"] for user in self.users if user["role"] == "customer"]
        product_ids = [product["id"] for product in self.products]
        order_ids = [order["id"] for order in self.orders]
        
        for review in self.reviews:
            try:
                # Check required fields
                required_fields = ["id", "product_id", "customer_id", "rating", "comment", "review_date"]
                for field in required_fields:
                    if field not in review:
                        raise ValidationError(f"Missing required field: {field}")
                
                # Check data types
                if not isinstance(review["id"], int):
                    raise ValidationError(f"Review ID must be an integer: {review['id']}")
                
                if not isinstance(review["product_id"], int):
                    raise ValidationError(f"Product ID must be an integer: {review['product_id']}")
                
                if not isinstance(review["customer_id"], int):
                    raise ValidationError(f"Customer ID must be an integer: {review['customer_id']}")
                
                if not isinstance(review["rating"], int):
                    raise ValidationError(f"Rating must be an integer: {review['rating']}")
                
                # Check value constraints
                if not (1 <= review["rating"] <= 5):
                    raise ValidationError(f"Rating must be between 1 and 5: {review['rating']}")
                
                # Check references exist
                if review["product_id"] not in product_ids:
                    raise ValidationError(f"Invalid product_id: {review['product_id']}")
                
                if review["customer_id"] not in customer_ids:
                    raise ValidationError(f"Invalid customer_id: {review['customer_id']}")
                
                if "order_id" in review and review["order_id"] not in order_ids:
                    raise ValidationError(f"Invalid order_id: {review['order_id']}")
                
                self.validation_results["reviews"]["passed"] += 1
            
            except ValidationError as e:
                self.validation_results["reviews"]["failed"] += 1
                error = {"id": review.get("id", "unknown"), "error": str(e)}
                self.validation_results["reviews"]["errors"].append(error)
                logger.error(f"Review validation error: {error}")
            
            except Exception as e:
                self.validation_results["reviews"]["failed"] += 1
                error = {"id": review.get("id", "unknown"), "error": f"Unexpected error: {str(e)}"}
                self.validation_results["reviews"]["errors"].append(error)
                logger.error(f"Review validation error: {error}")
        
        logger.info(f"Review validation complete: {self.validation_results['reviews']['passed']} passed, {self.validation_results['reviews']['failed']} failed")
    
    def validate_relationships(self):
        """Validate relationships between entities."""
        logger.info("Validating relationships between entities...")
        
        try:
            # Check that all products have valid sellers
            seller_ids = [user["id"] for user in self.users if user["role"] == "seller"]
            products_with_invalid_sellers = [p for p in self.products if p["seller_id"] not in seller_ids]
            
            if products_with_invalid_sellers:
                for product in products_with_invalid_sellers:
                    error = {"type": "product_seller", "id": product["id"], "error": f"Product has invalid seller_id: {product['seller_id']}"}
                    self.validation_results["relationships"]["errors"].append(error)
                    self.validation_results["relationships"]["failed"] += 1
            
            # Check that all orders have valid customers
            customer_ids = [user["id"] for user in self.users if user["role"] == "customer"]
            orders_with_invalid_customers = [o for o in self.orders if o["customer_id"] not in customer_ids]
            
            if orders_with_invalid_customers:
                for order in orders_with_invalid_customers:
                    error = {"type": "order_customer", "id": order["id"], "error": f"Order has invalid customer_id: {order['customer_id']}"}
                    self.validation_results["relationships"]["errors"].append(error)
                    self.validation_results["relationships"]["failed"] += 1
            
            # Check that all order line items have valid products
            product_ids = [p["id"] for p in self.products]
            for order in self.orders:
                for item in order["line_items"]:
                    if item["product_id"] not in product_ids:
                        error = {"type": "order_item_product", "id": order["id"], "error": f"Order line item has invalid product_id: {item['product_id']}"}
                        self.validation_results["relationships"]["errors"].append(error)
                        self.validation_results["relationships"]["failed"] += 1
            
            # Check that all reviews have valid products and customers
            reviews_with_invalid_products = [r for r in self.reviews if r["product_id"] not in product_ids]
            reviews_with_invalid_customers = [r for r in self.reviews if r["customer_id"] not in customer_ids]
            
            if reviews_with_invalid_products:
                for review in reviews_with_invalid_products:
                    error = {"type": "review_product", "id": review["id"], "error": f"Review has invalid product_id: {review['product_id']}"}
                    self.validation_results["relationships"]["errors"].append(error)
                    self.validation_results["relationships"]["failed"] += 1
            
            if reviews_with_invalid_customers:
                for review in reviews_with_invalid_customers:
                    error = {"type": "review_customer", "id": review["id"], "error": f"Review has invalid customer_id: {review['customer_id']}"}
                    self.validation_results["relationships"]["errors"].append(error)
                    self.validation_results["relationships"]["failed"] += 1
            
            # Check that all reviews with order_id have valid orders
            order_ids = [o["id"] for o in self.orders]
            reviews_with_invalid_orders = [r for r in self.reviews if "order_id" in r and r["order_id"] not in order_ids]
            
            if reviews_with_invalid_orders:
                for review in reviews_with_invalid_orders:
                    error = {"type": "review_order", "id": review["id"], "error": f"Review has invalid order_id: {review['order_id']}"}
                    self.validation_results["relationships"]["errors"].append(error)
                    self.validation_results["relationships"]["failed"] += 1
            
            # If no errors, all relationships passed
            if self.validation_results["relationships"]["failed"] == 0:
                self.validation_results["relationships"]["passed"] = 1
            
            logger.info(f"Relationship validation complete: {self.validation_results['relationships']['passed']} passed, {self.validation_results['relationships']['failed']} failed")
        
        except Exception as e:
            logger.error(f"Error validating relationships: {e}")
            self.validation_results["relationships"]["failed"] += 1
            self.validation_results["relationships"]["errors"].append({"type": "general", "error": str(e)})
    
    def validate_all(self):
        """Validate all test data."""
        if not self.load_data():
            return False
        
        self.validate_users()
        self.validate_products()
        self.validate_orders()
        self.validate_reviews()
        self.validate_relationships()
        
        return True
    
    def generate_report(self):
        """Generate a validation report in Markdown format."""
        logger.info("Generating validation report...")
        
        # Calculate overall statistics
        total_passed = sum(self.validation_results[entity]["passed"] for entity in self.validation_results)
        total_failed = sum(self.validation_results[entity]["failed"] for entity in self.validation_results)
        total_warnings = sum(self.validation_results[entity]["warnings"] for entity in self.validation_results)
        
        # Create report
        report = "# Test Data Validation Report\n\n"
        report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # Summary
        report += "## Summary\n\n"
        report += "| Entity | Passed | Failed | Warnings |\n"
        report += "|--------|--------|--------|----------|\n"
        
        for entity in self.validation_results:
            passed = self.validation_results[entity]["passed"]
            failed = self.validation_results[entity]["failed"]
            warnings = self.validation_results[entity]["warnings"]
            report += f"| {entity.capitalize()} | {passed} | {failed} | {warnings} |\n"
        
        report += f"| **Total** | **{total_passed}** | **{total_failed}** | **{total_warnings}** |\n\n"
        
        # Overall result
        if total_failed == 0:
            if total_warnings == 0:
                report += "**Overall Result:** ✅ PASS - All validation checks passed successfully.\n\n"
            else:
                report += "**Overall Result:** ⚠️ PASS WITH WARNINGS - All validation checks passed but with warnings.\n\n"
        else:
            report += "**Overall Result:** ❌ FAIL - Some validation checks failed.\n\n"
        
        # Detailed results
        report += "## Detailed Results\n\n"
        
        for entity in self.validation_results:
            report += f"### {entity.capitalize()}\n\n"
            
            if self.validation_results[entity]["failed"] == 0 and self.validation_results[entity]["warnings"] == 0:
                report += "✅ All validation checks passed.\n\n"
            else:
                # Errors
                if self.validation_results[entity]["errors"]:
                    report += "#### Errors\n\n"
                    report += "| ID | Error |\n"
                    report += "|-----|-------|\n"
                    
                    for error in self.validation_results[entity]["errors"]:
                        if "type" in error:  # Relationship error
                            report += f"| {error['id']} | [{error['type']}] {error['error']} |\n"
                        else:  # Entity error
                            report += f"| {error['id']} | {error['error']} |\n"
                    
                    report += "\n"
        
        # Recommendations
        report += "## Recommendations\n\n"
        
        if total_failed > 0:
            report += "1. Fix all validation errors before using this test data.\n"
            report += "2. Pay special attention to relationship errors, as they can cause cascading failures.\n"
        
        if total_warnings > 0:
            report += "3. Review warnings to ensure the test data meets all business requirements.\n"
        
        report += "4. Consider adding more edge cases to test boundary conditions.\n"
        report += "5. Ensure test data covers all possible scenarios for thorough testing.\n\n"
        
        # Save report
        os.makedirs(os.path.dirname(VALIDATION_REPORT_FILE), exist_ok=True)
        with open(VALIDATION_REPORT_FILE, "w") as f:
            f.write(report)
        
        logger.info(f"Validation report saved to {VALIDATION_REPORT_FILE}")
        
        return report


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Validate test data for OneTappe API")
    parser.add_argument("--data-dir", type=str, default=TEST_DATA_DIR, help="Directory containing test data files")
    parser.add_argument("--report", type=str, default=VALIDATION_REPORT_FILE, help="Path to save validation report")
    args = parser.parse_args()
    
    validator = TestDataValidator(args.data_dir)
    
    if validator.validate_all():
        validator.generate_report()
        
        # Print summary
        total_passed = sum(validator.validation_results[entity]["passed"] for entity in validator.validation_results)
        total_failed = sum(validator.validation_results[entity]["failed"] for entity in validator.validation_results)
        total_warnings = sum(validator.validation_results[entity]["warnings"] for entity in validator.validation_results)
        
        logger.info(f"Validation complete: {total_passed} passed, {total_failed} failed, {total_warnings} warnings")
        
        if total_failed > 0:
            logger.error("Validation failed! See the report for details.")
            return 1
        elif total_warnings > 0:
            logger.warning("Validation passed with warnings. See the report for details.")
            return 0
        else:
            logger.info("Validation passed successfully!")
            return 0
    else:
        logger.error("Failed to load test data")
        return 1


if __name__ == "__main__":
    sys.exit(main())