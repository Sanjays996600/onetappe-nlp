#!/usr/bin/env python3
"""
Inventory Report Test Data Generator

This script generates test data for inventory report testing with various
scenarios like normal stock, low stock, out of stock, and different inventory sizes.
"""

import json
import random
import os
import sys
import argparse
from datetime import datetime

# Add parent directory to path to import modules if needed
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Product categories
CATEGORIES = [
    "Electronics", "Clothing", "Food", "Beverages", "Household", 
    "Beauty", "Toys", "Stationery", "Sports", "Furniture"
]

# Product name templates by category
PRODUCT_TEMPLATES = {
    "Electronics": ["Smartphone", "Laptop", "Headphones", "Charger", "Power Bank", "Speaker", "Camera", "Tablet"],
    "Clothing": ["T-shirt", "Jeans", "Dress", "Shirt", "Jacket", "Socks", "Hat", "Scarf"],
    "Food": ["Rice", "Flour", "Sugar", "Salt", "Spices", "Noodles", "Biscuits", "Chips"],
    "Beverages": ["Water", "Soda", "Juice", "Tea", "Coffee", "Energy Drink", "Milk", "Smoothie"],
    "Household": ["Soap", "Detergent", "Cleaner", "Tissue", "Towel", "Broom", "Mop", "Bucket"],
    "Beauty": ["Shampoo", "Conditioner", "Lotion", "Cream", "Perfume", "Makeup", "Lipstick", "Nail Polish"],
    "Toys": ["Doll", "Car", "Puzzle", "Board Game", "Action Figure", "Stuffed Animal", "Building Blocks", "Remote Control"],
    "Stationery": ["Pen", "Pencil", "Notebook", "Paper", "Eraser", "Ruler", "Stapler", "Scissors"],
    "Sports": ["Ball", "Bat", "Racket", "Gloves", "Shoes", "Jersey", "Helmet", "Knee Pad"],
    "Furniture": ["Chair", "Table", "Bed", "Sofa", "Cabinet", "Shelf", "Desk", "Stool"]
}

# Adjectives to make product names more varied
ADJECTIVES = [
    "Premium", "Deluxe", "Basic", "Advanced", "Professional", "Standard", 
    "Classic", "Modern", "Vintage", "Eco-friendly", "Luxury", "Budget", 
    "Compact", "Portable", "Heavy-duty", "Lightweight", "All-purpose", "Specialized"
]

# Brands to make product names more varied
BRANDS = [
    "TechPro", "EcoLife", "HomeStyle", "FreshFoods", "SportMax", 
    "BeautyGlow", "KidsFun", "OfficeSupply", "ComfortZone", "NatureCraft"
]

def generate_product(product_id, stock_scenario="random"):
    """
    Generate a single product with random attributes
    
    Args:
        product_id: Unique identifier for the product
        stock_scenario: One of "normal", "low", "out", or "random"
    
    Returns:
        Dictionary containing product data
    """
    category = random.choice(CATEGORIES)
    product_type = random.choice(PRODUCT_TEMPLATES[category])
    adjective = random.choice(ADJECTIVES)
    brand = random.choice(BRANDS)
    
    # Create product name with some variation
    name_format = random.choice([
        "{brand} {adjective} {product_type}",
        "{adjective} {product_type} by {brand}",
        "{brand} {product_type}",
        "{adjective} {product_type}"
    ])
    name = name_format.format(brand=brand, adjective=adjective, product_type=product_type)
    
    # Set price between 10 and 5000
    price = round(random.uniform(10, 5000), 2)
    
    # Set low stock threshold between 5 and 20
    low_stock_threshold = random.randint(5, 20)
    
    # Set stock based on scenario
    if stock_scenario == "normal":
        stock = random.randint(low_stock_threshold + 1, low_stock_threshold * 5)
    elif stock_scenario == "low":
        stock = random.randint(1, low_stock_threshold)
    elif stock_scenario == "out":
        stock = 0
    else:  # random
        scenario = random.choice(["normal", "low", "out"])
        if scenario == "normal":
            stock = random.randint(low_stock_threshold + 1, low_stock_threshold * 5)
        elif scenario == "low":
            stock = random.randint(1, low_stock_threshold)
        else:  # out
            stock = 0
    
    return {
        "id": str(product_id),
        "name": name,
        "price": price,
        "stock": stock,
        "category": category,
        "low_stock_threshold": low_stock_threshold
    }

def generate_seller(seller_id="test_seller"):
    """
    Generate seller information
    
    Args:
        seller_id: Unique identifier for the seller
    
    Returns:
        Dictionary containing seller data
    """
    business_names = [
        "Sunrise Traders", "Global Mart", "City Superstore", "Family Shop",
        "Quick Bazaar", "Metro Retail", "Village Store", "Urban Market"
    ]
    
    seller_names = [
        "Raj Kumar", "Priya Sharma", "Amit Singh", "Neha Patel",
        "Sanjay Gupta", "Anita Desai", "Vikram Mehta", "Sunita Verma"
    ]
    
    return {
        "id": seller_id,
        "name": random.choice(seller_names),
        "business_name": random.choice(business_names),
        "phone": "+91" + ''.join([str(random.randint(0, 9)) for _ in range(10)])
    }

def generate_inventory_data(num_products=50, normal_pct=60, low_pct=30, out_pct=10):
    """
    Generate inventory data with specified distribution of stock levels
    
    Args:
        num_products: Total number of products to generate
        normal_pct: Percentage of products with normal stock
        low_pct: Percentage of products with low stock
        out_pct: Percentage of products out of stock
    
    Returns:
        Dictionary containing products and seller information
    """
    # Calculate number of products in each category
    normal_count = int(num_products * normal_pct / 100)
    low_count = int(num_products * low_pct / 100)
    out_count = num_products - normal_count - low_count
    
    products = []
    product_id = 1
    
    # Generate normal stock products
    for _ in range(normal_count):
        products.append(generate_product(product_id, "normal"))
        product_id += 1
    
    # Generate low stock products
    for _ in range(low_count):
        products.append(generate_product(product_id, "low"))
        product_id += 1
    
    # Generate out of stock products
    for _ in range(out_count):
        products.append(generate_product(product_id, "out"))
        product_id += 1
    
    # Shuffle products to randomize order
    random.shuffle(products)
    
    # Generate seller information
    seller = generate_seller()
    
    return {
        "products": products,
        "seller": seller
    }

def save_to_json(data, filename):
    """
    Save data to JSON file
    
    Args:
        data: Data to save
        filename: Output filename
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Generate test data for inventory report testing")
    parser.add_argument(
        "--size", type=str, default="medium",
        choices=["small", "medium", "large", "xlarge"],
        help="Size of inventory to generate (small=10, medium=50, large=200, xlarge=1000)"
    )
    parser.add_argument(
        "--normal", type=int, default=60,
        help="Percentage of products with normal stock (default: 60)"
    )
    parser.add_argument(
        "--low", type=int, default=30,
        help="Percentage of products with low stock (default: 30)"
    )
    parser.add_argument(
        "--out", type=int, default=10,
        help="Percentage of products out of stock (default: 10)"
    )
    parser.add_argument(
        "--output", type=str, default="inventory_test_data.json",
        help="Output filename (default: inventory_test_data.json)"
    )
    
    args = parser.parse_args()
    
    # Set number of products based on size
    size_map = {
        "small": 10,
        "medium": 50,
        "large": 200,
        "xlarge": 1000
    }
    num_products = size_map[args.size]
    
    # Validate percentages
    total_pct = args.normal + args.low + args.out
    if total_pct != 100:
        print(f"Warning: Percentages sum to {total_pct}, not 100. Adjusting...")
        args.normal = int(args.normal * 100 / total_pct)
        args.low = int(args.low * 100 / total_pct)
        args.out = 100 - args.normal - args.low
    
    # Generate data
    data = generate_inventory_data(
        num_products=num_products,
        normal_pct=args.normal,
        low_pct=args.low,
        out_pct=args.out
    )
    
    # Add metadata
    data["metadata"] = {
        "generated_at": datetime.now().isoformat(),
        "size": args.size,
        "num_products": num_products,
        "normal_pct": args.normal,
        "low_pct": args.low,
        "out_pct": args.out
    }
    
    # Save to file
    save_to_json(data, args.output)
    
    # Print summary
    print(f"Generated {num_products} products:")
    print(f"  - Normal stock: {args.normal}%")
    print(f"  - Low stock: {args.low}%")
    print(f"  - Out of stock: {args.out}%")

if __name__ == "__main__":
    main()