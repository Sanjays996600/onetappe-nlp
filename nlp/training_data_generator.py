#!/usr/bin/env python3
"""
Training Data Generator for Multilingual NLP Model

This script generates training data for the multilingual NLP model,
creating examples in both English and Hindi for various intents.
"""

import json
import random
import os
from datetime import datetime, timedelta

# Define templates for generating training data
ENGLISH_TEMPLATES = {
    "get_inventory": [
        "Show me my inventory",
        "What's in my inventory?",
        "Check inventory",
        "Show inventory status",
        "List all products in inventory",
        "What products do I have?",
        "Display my current stock",
        "Show me what I have in stock",
        "Inventory check",
        "What items are in my inventory?"
    ],
    "get_low_stock": [
        "Show low stock items",
        "Which products are running low?",
        "List items below {threshold} units",
        "Show products with stock below {threshold}",
        "What's running out of stock?",
        "Check which items need restocking",
        "Show me products with low inventory",
        "Which items have less than {threshold} units?",
        "Display products that need reordering",
        "What products are below threshold of {threshold}?"
    ],
    "get_report": [
        "Generate a report for {time_range}",
        "Show me sales report for {time_range}",
        "Get {time_range} report",
        "I need a report from {start_date} to {end_date}",
        "Show business performance for {time_range}",
        "Generate analytics for {time_range}",
        "Show me the numbers for {time_range}",
        "Get me a report between {start_date} and {end_date}",
        "Sales data for {time_range}",
        "Show performance metrics for {time_range}"
    ],
    "get_top_products": [
        "Show top {limit} products for {time_range}",
        "What are my best selling items for {time_range}?",
        "List top {limit} selling products",
        "Show best performers for {time_range}",
        "Which {limit} products sold the most in {time_range}?",
        "Top {limit} items for {time_range}",
        "Show me my {limit} most popular products",
        "Which products are selling best in {time_range}?",
        "Display top {limit} items by sales",
        "What are the {limit} most popular items in {time_range}?"
    ],
    "get_customer_data": [
        "Show customer data for {time_range}",
        "Get customer insights for {time_range}",
        "Show me customer analytics",
        "Customer report for {time_range}",
        "Show top {limit} customers",
        "Who are my best customers in {time_range}?",
        "Display customer statistics for {time_range}",
        "Show customer purchase history",
        "Get me customer data from {time_range}",
        "Customer buying patterns for {time_range}"
    ],
    "add_product": [
        "Add new product {product_name} price {price} stock {stock}",
        "Create product {product_name} with price {price} and quantity {stock}",
        "Add {product_name} to inventory, price: {price}, quantity: {stock}",
        "New product: {product_name}, {price} rupees, {stock} units",
        "Create new item {product_name} costing {price} with {stock} in stock",
        "Add {product_name} priced at {price} with initial stock of {stock}",
        "Create inventory item: {product_name}, price: {price}, stock: {stock}",
        "New product {product_name} with {stock} units at {price} each",
        "Add {product_name} to my products, price {price}, quantity {stock}",
        "Create {product_name} with {stock} units at {price} per unit"
    ],
    "edit_stock": [
        "Update {product_name} stock to {stock}",
        "Change {product_name} quantity to {stock}",
        "Set {product_name} inventory to {stock} units",
        "Adjust {product_name} stock to {stock}",
        "{product_name} new stock is {stock}",
        "Update inventory of {product_name} to {stock}",
        "Change stock level of {product_name} to {stock}",
        "Set {product_name} stock level to {stock} units",
        "Make {product_name} stock {stock}",
        "{product_name} stock update to {stock}"
    ],
    "get_orders": [
        "Show orders for {time_range}",
        "Get {time_range} orders",
        "Show me order history for {time_range}",
        "List all orders from {time_range}",
        "Display orders received in {time_range}",
        "Show me sales orders for {time_range}",
        "Get order data for {time_range}",
        "Show customer orders from {time_range}",
        "List orders between {start_date} and {end_date}",
        "Show me what was ordered in {time_range}"
    ],
    "search_product": [
        "Search for {product_name}",
        "Find {product_name} in inventory",
        "Look up {product_name}",
        "Do we have {product_name} in stock?",
        "Check if {product_name} is available",
        "Find product {product_name}",
        "Search inventory for {product_name}",
        "Is {product_name} in stock?",
        "Look for {product_name} in my products",
        "Check stock for {product_name}"
    ]
}

HINDI_TEMPLATES = {
    "get_inventory": [
        "मेरा इन्वेंटरी दिखाओ",
        "स्टॉक की जानकारी दो",
        "इन्वेंटरी चेक करो",
        "मेरे पास क्या स्टॉक है?",
        "सभी प्रोडक्ट्स दिखाओ",
        "मेरे पास कौन से प्रोडक्ट हैं?",
        "वर्तमान स्टॉक दिखाओ",
        "मेरे पास क्या है?",
        "इन्वेंटरी स्टेटस",
        "स्टॉक में क्या है?"
    ],
    "get_low_stock": [
        "कम स्टॉक वाले आइटम दिखाओ",
        "कौन से प्रोडक्ट कम हो रहे हैं?",
        "{threshold} से कम यूनिट वाले आइटम दिखाओ",
        "{threshold} से कम स्टॉक वाले प्रोडक्ट दिखाओ",
        "कौन सा स्टॉक खत्म हो रहा है?",
        "किन आइटम को रिस्टॉक करने की जरूरत है?",
        "कम इन्वेंटरी वाले प्रोडक्ट दिखाओ",
        "किन आइटम के {threshold} से कम यूनिट हैं?",
        "वो प्रोडक्ट दिखाओ जिन्हें फिर से ऑर्डर करने की जरूरत है",
        "कौन से प्रोडक्ट {threshold} से नीचे हैं?"
    ],
    "get_report": [
        "{time_range} का रिपोर्ट जनरेट करो",
        "{time_range} का सेल्स रिपोर्ट दिखाओ",
        "{time_range} का रिपोर्ट दो",
        "{start_date} से {end_date} तक का रिपोर्ट चाहिए",
        "{time_range} का बिज़नेस परफॉरमेंस दिखाओ",
        "{time_range} का एनालिटिक्स जनरेट करो",
        "{time_range} के नंबर्स दिखाओ",
        "{start_date} और {end_date} के बीच का रिपोर्ट दो",
        "{time_range} का सेल्स डेटा",
        "{time_range} का परफॉरमेंस मेट्रिक्स दिखाओ"
    ],
    "get_top_products": [
        "{time_range} के टॉप {limit} प्रोडक्ट दिखाओ",
        "{time_range} में मेरे बेस्ट सेलिंग आइटम कौन से हैं?",
        "टॉप {limit} सेलिंग प्रोडक्ट्स की लिस्ट दो",
        "{time_range} के बेस्ट परफॉर्मर्स दिखाओ",
        "{time_range} में कौन से {limit} प्रोडक्ट्स सबसे ज्यादा बिके?",
        "{time_range} के टॉप {limit} आइटम",
        "मेरे {limit} सबसे लोकप्रिय प्रोडक्ट्स दिखाओ",
        "{time_range} में कौन से प्रोडक्ट्स सबसे अच्छे बिक रहे हैं?",
        "सेल्स के हिसाब से टॉप {limit} आइटम दिखाओ",
        "{time_range} में {limit} सबसे लोकप्रिय आइटम कौन से हैं?"
    ],
    "get_customer_data": [
        "{time_range} का कस्टमर डेटा दिखाओ",
        "{time_range} के कस्टमर इनसाइट्स दो",
        "कस्टमर एनालिटिक्स दिखाओ",
        "{time_range} का कस्टमर रिपोर्ट",
        "टॉप {limit} कस्टमर्स दिखाओ",
        "{time_range} में मेरे बेस्ट कस्टमर्स कौन हैं?",
        "{time_range} के कस्टमर स्टैटिस्टिक्स दिखाओ",
        "कस्टमर खरीदारी हिस्ट्री दिखाओ",
        "{time_range} का कस्टमर डेटा दो",
        "{time_range} के कस्टमर खरीदारी पैटर्न दिखाओ"
    ],
    "add_product": [
        "नया प्रोडक्ट {product_name} कीमत {price} स्टॉक {stock} जोड़ो",
        "{product_name} प्रोडक्ट बनाओ कीमत {price} और मात्रा {stock}",
        "{product_name} को इन्वेंटरी में जोड़ो, कीमत: {price}, मात्रा: {stock}",
        "नया प्रोडक्ट: {product_name}, {price} रुपये, {stock} यूनिट्स",
        "नया आइटम {product_name} कीमत {price} के साथ {stock} स्टॉक में बनाओ",
        "{product_name} जोड़ो कीमत {price} के साथ {stock} की शुरुआती स्टॉक",
        "इन्वेंटरी आइटम बनाओ: {product_name}, कीमत: {price}, स्टॉक: {stock}",
        "नया प्रोडक्ट {product_name} {stock} यूनिट्स के साथ {price} प्रति यूनिट",
        "{product_name} को मेरे प्रोडक्ट्स में जोड़ो, कीमत {price}, मात्रा {stock}",
        "{product_name} बनाओ {stock} यूनिट्स के साथ {price} प्रति यूनिट"
    ],
    "edit_stock": [
        "{product_name} का स्टॉक {stock} अपडेट करो",
        "{product_name} की मात्रा {stock} करो",
        "{product_name} का इन्वेंटरी {stock} यूनिट्स सेट करो",
        "{product_name} का स्टॉक {stock} एडजस्ट करो",
        "{product_name} का नया स्टॉक {stock} है",
        "{product_name} का इन्वेंटरी {stock} अपडेट करो",
        "{product_name} का स्टॉक लेवल {stock} करो",
        "{product_name} का स्टॉक लेवल {stock} यूनिट्स सेट करो",
        "{product_name} का स्टॉक {stock} करो",
        "{product_name} स्टॉक अपडेट {stock} करो"
    ],
    "get_orders": [
        "{time_range} के ऑर्डर्स दिखाओ",
        "{time_range} के ऑर्डर्स दो",
        "{time_range} का ऑर्डर हिस्ट्री दिखाओ",
        "{time_range} के सभी ऑर्डर्स की लिस्ट दो",
        "{time_range} में प्राप्त ऑर्डर्स दिखाओ",
        "{time_range} के सेल्स ऑर्डर्स दिखाओ",
        "{time_range} का ऑर्डर डेटा दो",
        "{time_range} के कस्टमर ऑर्डर्स दिखाओ",
        "{start_date} और {end_date} के बीच के ऑर्डर्स की लिस्ट दो",
        "{time_range} में क्या ऑर्डर किया गया था दिखाओ"
    ],
    "search_product": [
        "{product_name} के लिए सर्च करो",
        "इन्वेंटरी में {product_name} ढूंढो",
        "{product_name} लुक अप करो",
        "क्या हमारे पास {product_name} स्टॉक में है?",
        "चेक करो कि {product_name} उपलब्ध है",
        "प्रोडक्ट {product_name} ढूंढो",
        "इन्वेंटरी में {product_name} सर्च करो",
        "क्या {product_name} स्टॉक में है?",
        "मेरे प्रोडक्ट्स में {product_name} ढूंढो",
        "{product_name} के लिए स्टॉक चेक करो"
    ]
}

# Define placeholder values for templates
PRODUCT_NAMES_EN = [
    "Rice", "Wheat", "Sugar", "Salt", "Oil", "Milk", "Coffee", "Tea", 
    "Flour", "Soap", "Shampoo", "Toothpaste", "Biscuits", "Chips", 
    "Chocolate", "Bread", "Butter", "Cheese", "Eggs", "Chicken"
]

PRODUCT_NAMES_HI = [
    "चावल", "गेहूं", "चीनी", "नमक", "तेल", "दूध", "कॉफी", "चाय", 
    "आटा", "साबुन", "शैम्पू", "टूथपेस्ट", "बिस्कुट", "चिप्स", 
    "चॉकलेट", "ब्रेड", "मक्खन", "पनीर", "अंडे", "चिकन"
]

PRICE_RANGE = [10, 20, 25, 30, 40, 50, 75, 100, 150, 200, 250, 300, 500]
STOCK_RANGE = [5, 10, 15, 20, 25, 30, 40, 50, 75, 100, 150, 200]
THRESHOLD_RANGE = [5, 10, 15, 20, 25, 30]
LIMIT_RANGE = [3, 5, 10, 15, 20]

TIME_RANGES_EN = [
    "today", "yesterday", "this week", "last week", "this month", "last month",
    "this year", "last year", "last 7 days", "last 30 days", "last 90 days"
]

TIME_RANGES_HI = [
    "आज", "कल", "इस हफ्ते", "पिछले हफ्ते", "इस महीने", "पिछले महीने",
    "इस साल", "पिछले साल", "पिछले 7 दिन", "पिछले 30 दिन", "पिछले 90 दिन"
]

# Generate date ranges
def generate_date_range():
    today = datetime.now()
    start_date = (today - timedelta(days=random.randint(10, 60))).strftime("%d/%m/%Y")
    end_date = (today - timedelta(days=random.randint(0, 9))).strftime("%d/%m/%Y")
    return start_date, end_date

# Generate training data
def generate_training_data(num_samples_per_intent=50):
    training_data = []
    
    # Generate English examples
    for intent, templates in ENGLISH_TEMPLATES.items():
        for _ in range(num_samples_per_intent):
            template = random.choice(templates)
            
            # Replace placeholders based on intent
            if "{product_name}" in template:
                template = template.replace("{product_name}", random.choice(PRODUCT_NAMES_EN))
            
            if "{price}" in template:
                template = template.replace("{price}", str(random.choice(PRICE_RANGE)))
            
            if "{stock}" in template:
                template = template.replace("{stock}", str(random.choice(STOCK_RANGE)))
            
            if "{threshold}" in template:
                template = template.replace("{threshold}", str(random.choice(THRESHOLD_RANGE)))
            
            if "{limit}" in template:
                template = template.replace("{limit}", str(random.choice(LIMIT_RANGE)))
            
            if "{time_range}" in template:
                template = template.replace("{time_range}", random.choice(TIME_RANGES_EN))
            
            if "{start_date}" in template and "{end_date}" in template:
                start_date, end_date = generate_date_range()
                template = template.replace("{start_date}", start_date)
                template = template.replace("{end_date}", end_date)
            
            training_data.append({
                "text": template,
                "intent": intent,
                "language": "en"
            })
    
    # Generate Hindi examples
    for intent, templates in HINDI_TEMPLATES.items():
        for _ in range(num_samples_per_intent):
            template = random.choice(templates)
            
            # Replace placeholders based on intent
            if "{product_name}" in template:
                template = template.replace("{product_name}", random.choice(PRODUCT_NAMES_HI))
            
            if "{price}" in template:
                template = template.replace("{price}", str(random.choice(PRICE_RANGE)))
            
            if "{stock}" in template:
                template = template.replace("{stock}", str(random.choice(STOCK_RANGE)))
            
            if "{threshold}" in template:
                template = template.replace("{threshold}", str(random.choice(THRESHOLD_RANGE)))
            
            if "{limit}" in template:
                template = template.replace("{limit}", str(random.choice(LIMIT_RANGE)))
            
            if "{time_range}" in template:
                template = template.replace("{time_range}", random.choice(TIME_RANGES_HI))
            
            if "{start_date}" in template and "{end_date}" in template:
                start_date, end_date = generate_date_range()
                template = template.replace("{start_date}", start_date)
                template = template.replace("{end_date}", end_date)
            
            training_data.append({
                "text": template,
                "intent": intent,
                "language": "hi"
            })
    
    # Generate mixed language examples (20% of total)
    num_mixed_samples = int(len(training_data) * 0.2)
    mixed_data = []
    
    for _ in range(num_mixed_samples):
        # Select a random English and Hindi example with the same intent
        en_examples = [ex for ex in training_data if ex["language"] == "en"]
        hi_examples = [ex for ex in training_data if ex["language"] == "hi"]
        
        en_example = random.choice(en_examples)
        matching_hi_examples = [ex for ex in hi_examples if ex["intent"] == en_example["intent"]]
        
        if matching_hi_examples:
            hi_example = random.choice(matching_hi_examples)
            
            # Create mixed language by combining parts
            en_words = en_example["text"].split()
            hi_words = hi_example["text"].split()
            
            # Mix strategy 1: Take first half from one language, second half from another
            if random.random() < 0.5:
                en_split = len(en_words) // 2
                hi_split = len(hi_words) // 2
                
                if random.random() < 0.5:
                    mixed_text = " ".join(en_words[:en_split] + hi_words[hi_split:])
                else:
                    mixed_text = " ".join(hi_words[:hi_split] + en_words[en_split:])
            # Mix strategy 2: Replace key entities (like product names, numbers)
            else:
                if en_example["intent"] in ["add_product", "edit_stock", "search_product"]:
                    # For product-related intents, swap product names
                    for en_prod in PRODUCT_NAMES_EN:
                        if en_prod in en_example["text"]:
                            hi_prod = random.choice(PRODUCT_NAMES_HI)
                            mixed_text = en_example["text"].replace(en_prod, hi_prod)
                            break
                    else:
                        # If no product name found, use strategy 1
                        en_split = len(en_words) // 2
                        hi_split = len(hi_words) // 2
                        mixed_text = " ".join(en_words[:en_split] + hi_words[hi_split:])
                else:
                    # For other intents, mix random words
                    mixed_words = []
                    for i in range(max(len(en_words), len(hi_words))):
                        if i < len(en_words) and i < len(hi_words):
                            word = random.choice([en_words[i], hi_words[i]])
                            mixed_words.append(word)
                        elif i < len(en_words):
                            mixed_words.append(en_words[i])
                        else:
                            mixed_words.append(hi_words[i])
                    
                    mixed_text = " ".join(mixed_words)
            
            mixed_data.append({
                "text": mixed_text,
                "intent": en_example["intent"],
                "language": "mixed"
            })
    
    # Add mixed examples to training data
    training_data.extend(mixed_data)
    
    # Shuffle the data
    random.shuffle(training_data)
    
    return training_data

# Split data into training and testing sets
def split_data(data, train_ratio=0.8):
    random.shuffle(data)
    split_idx = int(len(data) * train_ratio)
    return data[:split_idx], data[split_idx:]

# Save data to JSON files
def save_data(train_data, test_data, output_dir="./data"):
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save training data
    with open(os.path.join(output_dir, "training_data.json"), "w", encoding="utf-8") as f:
        json.dump(train_data, f, ensure_ascii=False, indent=2)
    
    # Save testing data
    with open(os.path.join(output_dir, "testing_data.json"), "w", encoding="utf-8") as f:
        json.dump(test_data, f, ensure_ascii=False, indent=2)
    
    print(f"Saved {len(train_data)} training examples and {len(test_data)} testing examples")

# Main function
def main():
    # Set random seed for reproducibility
    random.seed(42)
    
    # Generate data
    print("Generating training data...")
    data = generate_training_data(num_samples_per_intent=50)
    
    # Split into training and testing sets
    train_data, test_data = split_data(data)
    
    # Print statistics
    print(f"Total examples: {len(data)}")
    print(f"Training examples: {len(train_data)}")
    print(f"Testing examples: {len(test_data)}")
    
    # Count examples by intent and language
    intent_counts = {}
    language_counts = {"en": 0, "hi": 0, "mixed": 0}
    
    for example in data:
        intent = example["intent"]
        language = example["language"]
        
        if intent not in intent_counts:
            intent_counts[intent] = 0
        intent_counts[intent] += 1
        language_counts[language] += 1
    
    print("\nIntent distribution:")
    for intent, count in intent_counts.items():
        print(f"{intent}: {count} examples ({count/len(data)*100:.1f}%)")
    
    print("\nLanguage distribution:")
    for language, count in language_counts.items():
        print(f"{language}: {count} examples ({count/len(data)*100:.1f}%)")
    
    # Save data
    save_data(train_data, test_data)

if __name__ == "__main__":
    main()