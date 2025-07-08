#!/usr/bin/env python3
"""
Test Data Generator for OneTappe API

This script generates realistic test data for the OneTappe API, including:
- Users (customers and sellers)
- Products with various attributes
- Orders with line items
- Reviews and ratings

The generated data can be used for testing the API endpoints, performance testing,
and populating the database with realistic data for development and testing.
"""

import os
import sys
import json
import random
import datetime
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("test_data_generation.log")
    ]
)
logger = logging.getLogger("test_data_generator")

# Configuration
OUTPUT_DIR = "test_data"
USERS_FILE = os.path.join(OUTPUT_DIR, "users.json")
PRODUCTS_FILE = os.path.join(OUTPUT_DIR, "products.json")
ORDERS_FILE = os.path.join(OUTPUT_DIR, "orders.json")
REVIEWS_FILE = os.path.join(OUTPUT_DIR, "reviews.json")
SQL_FILE = os.path.join(OUTPUT_DIR, "test_data.sql")

# Sample data for generating realistic test data
FIRST_NAMES = [
    "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
    "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Dorothy", "Kevin", "Carol", "Brian", "Amanda", "George", "Melissa"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller", "Wilson",
    "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White", "Harris", "Martin",
    "Thompson", "Garcia", "Martinez", "Robinson", "Clark", "Rodriguez", "Lewis", "Lee",
    "Walker", "Hall", "Allen", "Young", "Hernandez", "King", "Wright", "Lopez",
    "Hill", "Scott", "Green", "Adams", "Baker", "Gonzalez", "Nelson", "Carter",
    "Mitchell", "Perez", "Roberts", "Turner", "Phillips", "Campbell", "Parker", "Evans"
]

PRODUCT_ADJECTIVES = [
    "Premium", "Deluxe", "Luxury", "Essential", "Basic", "Advanced", "Professional",
    "Elegant", "Classic", "Modern", "Vintage", "Sleek", "Compact", "Portable", "Wireless",
    "Smart", "Digital", "Analog", "Organic", "Natural", "Handcrafted", "Artisanal",
    "Eco-friendly", "Sustainable", "Biodegradable", "Recycled", "Innovative", "Revolutionary",
    "High-performance", "Energy-efficient", "Waterproof", "Shockproof", "Durable", "Lightweight"
]

PRODUCT_NOUNS = [
    "Headphones", "Speakers", "Smartphone", "Laptop", "Tablet", "Camera", "Watch",
    "Sunglasses", "Backpack", "Wallet", "Purse", "Shoes", "Sneakers", "T-shirt", "Jeans",
    "Jacket", "Sweater", "Dress", "Skirt", "Pants", "Hat", "Gloves", "Scarf", "Socks",
    "Umbrella", "Water Bottle", "Coffee Mug", "Notebook", "Pen", "Pencil", "Desk Lamp",
    "Chair", "Table", "Bookshelf", "Sofa", "Bed", "Pillow", "Blanket", "Towel", "Rug"
]

PRODUCT_CATEGORIES = [
    "Electronics", "Clothing", "Accessories", "Home & Kitchen", "Books", "Sports & Outdoors",
    "Beauty & Personal Care", "Health & Wellness", "Toys & Games", "Automotive", "Pet Supplies",
    "Office Products", "Grocery", "Baby", "Jewelry", "Tools & Home Improvement", "Garden & Outdoor"
]

PRODUCT_DESCRIPTIONS = [
    "Perfect for everyday use. This {product} is designed with comfort and functionality in mind.",
    "Elevate your experience with our {product}. Crafted with premium materials for lasting quality.",
    "Introducing the next generation of {product}. Innovative features meet sleek design.",
    "Discover the difference with our {product}. Unmatched performance and reliability.",
    "Meet your new favorite {product}. Versatile, stylish, and built to last.",
    "Experience luxury with our signature {product}. The perfect blend of form and function.",
    "Designed for the modern lifestyle, our {product} combines style with practicality.",
    "Upgrade your daily routine with our {product}. Thoughtfully designed for maximum convenience.",
    "Simplify your life with our {product}. Intuitive design meets exceptional quality.",
    "Stand out from the crowd with our unique {product}. A statement piece for the discerning customer."
]

ORDER_STATUSES = ["Pending", "Processing", "Shipped", "Delivered", "Cancelled"]

PAYMENT_METHODS = ["Credit Card", "PayPal", "Apple Pay", "Google Pay", "Bank Transfer"]

REVIEW_COMMENTS = [
    "Absolutely love this product! Exceeded my expectations in every way.",
    "Good quality for the price. Would recommend to others looking for a budget option.",
    "Decent product but took longer than expected to arrive.",
    "Not as described. Disappointed with the quality.",
    "Average product. Nothing special but gets the job done.",
    "Excellent customer service when I had questions about this item.",
    "Perfect fit for what I needed. Very satisfied with my purchase.",
    "The product works well but the instructions were confusing.",
    "Great value for money. Will definitely buy again.",
    "Had to return due to a defect, but the return process was smooth.",
    "This is exactly what I was looking for. Very happy with my purchase.",
    "The quality exceeded my expectations. Highly recommend!",
    "Shipping was fast and the product arrived in perfect condition.",
    "Not quite what I expected, but still a good product overall.",
    "Amazing product! Will definitely be ordering more in the future."
]


def ensure_output_dir():
    """Ensure the output directory exists."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def generate_users(num_users, num_sellers):
    """Generate user data with a mix of customers and sellers."""
    logger.info(f"Generating {num_users} users ({num_sellers} sellers)...")
    
    users = []
    
    # Generate sellers first to ensure we have enough
    for i in range(1, num_sellers + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
        email = f"{username}@example.com"
        
        user = {
            "id": i,
            "username": username,
            "email": email,
            "password": "password123",  # In a real system, this would be hashed
            "first_name": first_name,
            "last_name": last_name,
            "role": "seller",
            "created_at": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))).isoformat(),
            "seller_info": {
                "store_name": f"{last_name}'s {random.choice(['Shop', 'Store', 'Emporium', 'Boutique', 'Market'])}",
                "description": f"Quality products from {first_name} {last_name}.",
                "rating": round(random.uniform(3.5, 5.0), 1),
                "total_sales": random.randint(10, 1000)
            }
        }
        
        users.append(user)
    
    # Generate regular customers
    for i in range(num_sellers + 1, num_users + 1):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        username = f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 999)}"
        email = f"{username}@example.com"
        
        user = {
            "id": i,
            "username": username,
            "email": email,
            "password": "password123",  # In a real system, this would be hashed
            "first_name": first_name,
            "last_name": last_name,
            "role": "customer",
            "created_at": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 365))).isoformat(),
            "customer_info": {
                "shipping_address": f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Maple', 'Cedar', 'Pine'])} St, {random.choice(['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'])}, {random.choice(['NY', 'CA', 'IL', 'TX', 'AZ'])} {random.randint(10000, 99999)}",
                "phone": f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
            }
        }
        
        users.append(user)
    
    return users


def generate_products(num_products, sellers):
    """Generate product data for the given sellers."""
    logger.info(f"Generating {num_products} products...")
    
    products = []
    seller_ids = [seller["id"] for seller in sellers]
    
    for i in range(1, num_products + 1):
        adjective = random.choice(PRODUCT_ADJECTIVES)
        noun = random.choice(PRODUCT_NOUNS)
        product_name = f"{adjective} {noun}"
        category = random.choice(PRODUCT_CATEGORIES)
        price = round(random.uniform(9.99, 999.99), 2)
        stock = random.randint(0, 100)
        seller_id = random.choice(seller_ids)
        description = random.choice(PRODUCT_DESCRIPTIONS).format(product=noun.lower())
        
        product = {
            "id": i,
            "product_name": product_name,
            "price": price,
            "stock": stock,
            "description": description,
            "category": category,
            "seller_id": seller_id,
            "created_at": (datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 180))).isoformat(),
            "updated_at": (datetime.datetime.now() - datetime.timedelta(days=random.randint(0, 30))).isoformat(),
            "image_url": f"https://example.com/images/products/{i}.jpg",
            "rating": round(random.uniform(1.0, 5.0), 1),
            "num_ratings": random.randint(0, 100)
        }
        
        products.append(product)
    
    return products


def generate_orders(num_orders, customers, products):
    """Generate order data for the given customers and products."""
    logger.info(f"Generating {num_orders} orders...")
    
    orders = []
    customer_ids = [customer["id"] for customer in customers]
    product_ids = [product["id"] for product in products]
    
    for i in range(1, num_orders + 1):
        customer_id = random.choice(customer_ids)
        status = random.choice(ORDER_STATUSES)
        payment_method = random.choice(PAYMENT_METHODS)
        
        # Generate order date based on status
        if status == "Delivered":
            days_ago = random.randint(7, 90)
        elif status == "Shipped":
            days_ago = random.randint(3, 7)
        elif status == "Processing":
            days_ago = random.randint(1, 3)
        elif status == "Pending":
            days_ago = random.randint(0, 1)
        else:  # Cancelled
            days_ago = random.randint(1, 30)
        
        order_date = (datetime.datetime.now() - datetime.timedelta(days=days_ago)).isoformat()
        
        # Generate line items (products in the order)
        num_items = random.randint(1, 5)
        line_items = []
        total_amount = 0
        
        # Ensure no duplicate products in the same order
        order_product_ids = random.sample(product_ids, num_items)
        
        for product_id in order_product_ids:
            product = next((p for p in products if p["id"] == product_id), None)
            if product:
                quantity = random.randint(1, 3)
                price = product["price"]
                line_total = price * quantity
                total_amount += line_total
                
                line_item = {
                    "product_id": product_id,
                    "product_name": product["product_name"],
                    "quantity": quantity,
                    "price": price,
                    "line_total": line_total
                }
                
                line_items.append(line_item)
        
        # Apply random discount
        discount = 0
        if random.random() < 0.3:  # 30% chance of discount
            discount_percent = random.choice([5, 10, 15, 20])
            discount = round(total_amount * (discount_percent / 100), 2)
        
        # Calculate final amount
        final_amount = total_amount - discount
        
        # Add shipping info
        shipping_fee = 0 if final_amount > 50 else 5.99  # Free shipping over $50
        final_amount += shipping_fee
        
        order = {
            "id": i,
            "customer_id": customer_id,
            "order_date": order_date,
            "status": status,
            "payment_method": payment_method,
            "line_items": line_items,
            "subtotal": total_amount,
            "discount": discount,
            "shipping_fee": shipping_fee,
            "total_amount": final_amount,
            "shipping_address": next((c["customer_info"]["shipping_address"] for c in customers if c["id"] == customer_id), "")
        }
        
        # Add tracking info for shipped/delivered orders
        if status in ["Shipped", "Delivered"]:
            order["tracking_number"] = f"TRK{random.randint(1000000, 9999999)}"
            order["shipping_carrier"] = random.choice(["FedEx", "UPS", "USPS", "DHL"])
        
        orders.append(order)
    
    return orders


def generate_reviews(orders, products, customers):
    """Generate review data based on delivered orders."""
    logger.info("Generating reviews for delivered orders...")
    
    reviews = []
    review_id = 1
    
    for order in orders:
        if order["status"] == "Delivered":
            customer_id = order["customer_id"]
            
            # Not all customers leave reviews
            if random.random() < 0.7:  # 70% chance of leaving a review
                for line_item in order["line_items"]:
                    product_id = line_item["product_id"]
                    
                    # Not all products in an order get reviewed
                    if random.random() < 0.8:  # 80% chance of reviewing each product
                        rating = random.randint(1, 5)
                        comment = random.choice(REVIEW_COMMENTS)
                        
                        # Calculate review date (after order date)
                        order_date = datetime.datetime.fromisoformat(order["order_date"])
                        days_after_order = random.randint(3, 14)  # Review 3-14 days after delivery
                        review_date = (order_date + datetime.timedelta(days=days_after_order)).isoformat()
                        
                        review = {
                            "id": review_id,
                            "product_id": product_id,
                            "customer_id": customer_id,
                            "order_id": order["id"],
                            "rating": rating,
                            "comment": comment,
                            "review_date": review_date,
                            "helpful_votes": random.randint(0, 20)
                        }
                        
                        reviews.append(review)
                        review_id += 1
    
    return reviews


def update_product_ratings(products, reviews):
    """Update product ratings based on reviews."""
    logger.info("Updating product ratings based on reviews...")
    
    # Group reviews by product_id
    product_reviews = {}
    for review in reviews:
        product_id = review["product_id"]
        if product_id not in product_reviews:
            product_reviews[product_id] = []
        product_reviews[product_id].append(review)
    
    # Update product ratings
    for product in products:
        product_id = product["id"]
        if product_id in product_reviews:
            product_ratings = [review["rating"] for review in product_reviews[product_id]]
            product["rating"] = round(sum(product_ratings) / len(product_ratings), 1)
            product["num_ratings"] = len(product_ratings)
    
    return products


def generate_sql_script(users, products, orders, reviews):
    """Generate SQL script to insert the test data into the database."""
    logger.info("Generating SQL script...")
    
    sql = "-- OneTappe API Test Data\n"
    sql += "-- Generated on " + datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
    
    # Insert users
    sql += "-- Users\n"
    for user in users:
        sql += f"INSERT INTO users (id, username, email, password, first_name, last_name, role, created_at) VALUES "
        sql += f"({user['id']}, '{user['username']}', '{user['email']}', '{user['password']}', '{user['first_name']}', '{user['last_name']}', '{user['role']}', '{user['created_at']}');\n"
    
    sql += "\n"
    
    # Insert seller info
    sql += "-- Seller Info\n"
    for user in users:
        if user["role"] == "seller":
            seller_info = user["seller_info"]
            sql += f"INSERT INTO seller_info (seller_id, store_name, description, rating, total_sales) VALUES "
            sql += f"({user['id']}, '{seller_info['store_name']}', '{seller_info['description']}', {seller_info['rating']}, {seller_info['total_sales']});\n"
    
    sql += "\n"
    
    # Insert customer info
    sql += "-- Customer Info\n"
    for user in users:
        if user["role"] == "customer":
            customer_info = user["customer_info"]
            sql += f"INSERT INTO customer_info (customer_id, shipping_address, phone) VALUES "
            sql += f"({user['id']}, '{customer_info['shipping_address']}', '{customer_info['phone']}');\n"
    
    sql += "\n"
    
    # Insert products
    sql += "-- Products\n"
    for product in products:
        sql += f"INSERT INTO products (id, product_name, price, stock, description, category, seller_id, created_at, updated_at, image_url, rating, num_ratings) VALUES "
        sql += f"({product['id']}, '{product['product_name']}', {product['price']}, {product['stock']}, '{product['description']}', '{product['category']}', {product['seller_id']}, '{product['created_at']}', '{product['updated_at']}', '{product['image_url']}', {product['rating']}, {product['num_ratings']});\n"
    
    sql += "\n"
    
    # Insert orders
    sql += "-- Orders\n"
    for order in orders:
        sql += f"INSERT INTO orders (id, customer_id, order_date, status, payment_method, subtotal, discount, shipping_fee, total_amount, shipping_address) VALUES "
        sql += f"({order['id']}, {order['customer_id']}, '{order['order_date']}', '{order['status']}', '{order['payment_method']}', {order['subtotal']}, {order['discount']}, {order['shipping_fee']}, {order['total_amount']}, '{order['shipping_address']}');\n"
        
        if order["status"] in ["Shipped", "Delivered"] and "tracking_number" in order:
            sql += f"UPDATE orders SET tracking_number = '{order['tracking_number']}', shipping_carrier = '{order['shipping_carrier']}' WHERE id = {order['id']};\n"
    
    sql += "\n"
    
    # Insert order items
    sql += "-- Order Items\n"
    for order in orders:
        for item in order["line_items"]:
            sql += f"INSERT INTO order_items (order_id, product_id, product_name, quantity, price, line_total) VALUES "
            sql += f"({order['id']}, {item['product_id']}, '{item['product_name']}', {item['quantity']}, {item['price']}, {item['line_total']});\n"
    
    sql += "\n"
    
    # Insert reviews
    sql += "-- Reviews\n"
    for review in reviews:
        sql += f"INSERT INTO reviews (id, product_id, customer_id, order_id, rating, comment, review_date, helpful_votes) VALUES "
        sql += f"({review['id']}, {review['product_id']}, {review['customer_id']}, {review['order_id']}, {review['rating']}, '{review['comment']}', '{review['review_date']}', {review['helpful_votes']});\n"
    
    return sql


def save_data_to_files(users, products, orders, reviews, sql):
    """Save the generated data to JSON and SQL files."""
    logger.info("Saving data to files...")
    
    # Save users
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)
    
    # Save products
    with open(PRODUCTS_FILE, "w") as f:
        json.dump(products, f, indent=2)
    
    # Save orders
    with open(ORDERS_FILE, "w") as f:
        json.dump(orders, f, indent=2)
    
    # Save reviews
    with open(REVIEWS_FILE, "w") as f:
        json.dump(reviews, f, indent=2)
    
    # Save SQL script
    with open(SQL_FILE, "w") as f:
        f.write(sql)
    
    logger.info(f"Data saved to {OUTPUT_DIR} directory")


def main():
    """Main function to generate test data."""
    parser = argparse.ArgumentParser(description="Generate test data for OneTappe API")
    parser.add_argument("--users", type=int, default=50, help="Number of users to generate (default: 50)")
    parser.add_argument("--sellers", type=int, default=10, help="Number of sellers to generate (default: 10)")
    parser.add_argument("--products", type=int, default=100, help="Number of products to generate (default: 100)")
    parser.add_argument("--orders", type=int, default=200, help="Number of orders to generate (default: 200)")
    args = parser.parse_args()
    
    # Ensure output directory exists
    ensure_output_dir()
    
    # Generate data
    users = generate_users(args.users, args.sellers)
    sellers = [user for user in users if user["role"] == "seller"]
    customers = [user for user in users if user["role"] == "customer"]
    
    products = generate_products(args.products, sellers)
    orders = generate_orders(args.orders, customers, products)
    reviews = generate_reviews(orders, products, customers)
    
    # Update product ratings based on reviews
    products = update_product_ratings(products, reviews)
    
    # Generate SQL script
    sql = generate_sql_script(users, products, orders, reviews)
    
    # Save data to files
    save_data_to_files(users, products, orders, reviews, sql)
    
    # Print summary
    logger.info("Test data generation complete!")
    logger.info(f"Generated {len(users)} users ({len(sellers)} sellers, {len(customers)} customers)")
    logger.info(f"Generated {len(products)} products")
    logger.info(f"Generated {len(orders)} orders")
    logger.info(f"Generated {len(reviews)} reviews")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())