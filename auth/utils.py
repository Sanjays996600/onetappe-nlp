# New function to send WhatsApp message
async def send_whatsapp_message(sender, reply_text):
    url = f"https://graph.facebook.com/v15.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": sender,
        "text": {"body": reply_text}
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload)

    return response.status_code == 200


import sqlite3

# Function to find matching sellers from SQLite database

def find_sellers(category: str, pincode: str):
    conn = sqlite3.connect('sellers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, category, pincode FROM sellers WHERE category = ? AND pincode = ?', (category, pincode))
    rows = cursor.fetchall()
    conn.close()
    sellers = []
    for row in rows:
        sellers.append({"id": row[0], "name": row[1], "category": row[2], "pincode": row[3]})
    return sellers

import re

# Function to extract category and pincode from buyer message

def extract_category_pincode(message: str):
    category_pattern = r"(electrician|plumber|salon|repair|cleaning|carpenter)"
    pincode_pattern = r"\b(\d{6})\b"
    category_match = re.search(category_pattern, message, re.IGNORECASE)
    pincode_match = re.search(pincode_pattern, message)
    category = category_match.group(1).lower() if category_match else None
    pincode = pincode_match.group(1) if pincode_match else None
    return category, pincode


# Function to create a booking in the database
def create_booking(buyer: str, seller_id: int, slot: str, time: str):
    conn = sqlite3.connect('sellers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO bookings (buyer, seller_id, slot, time) VALUES (?, ?, ?, ?)', (buyer, seller_id, slot, time))
    conn.commit()
    conn.close()

# Validate seller inputs
def validate_seller(shop_name: str, service: str, pincode: str, hours: str) -> bool:
    # Check for duplicates and validate inputs
    conn = sqlite3.connect('sellers.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM sellers WHERE name = ? AND service = ? AND pincode = ?', (shop_name, service, pincode))
    result = cursor.fetchone()
    conn.close()
    if result:
        return False
    # Additional validation logic can be added here
    return True

# Save seller to database
def save_seller(shop_name: str, service: str, pincode: str, hours: str):
    conn = sqlite3.connect('sellers.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO sellers (name, service, pincode, business_hours) VALUES (?, ?, ?, ?)', (shop_name, service, pincode, hours))
    conn.commit()
    conn.close()

import os
from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY", "your-default-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Password verification

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# JWT token creation

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Read secret key from environment

def get_secret_key() -> str:
    return SECRET_KEY