from fastapi import APIRouter, Request
import httpx

router = APIRouter()

import os
from dotenv import load_dotenv

load_dotenv()

PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from parser import parse_command
from database import get_db
from models.base import Product, Order

router = APIRouter()

from fastapi import HTTPException
from models.base import Product

@router.post("/")
async def whatsapp_webhook(payload: dict, db: Session = Depends(get_db)):
    message = payload.get("message", "")
    result = parse_command(message)
    # Just log or return for now
    action = result.get("action")
    return handle_action(action, db)


def handle_action(action: str, db: Session):
    if action == "create_product":
        # Use parsed data from the result dictionary
        name = result.get("data", {}).get("name", "Test")
        price = result.get("data", {}).get("price", 0.0)
        stock = result.get("data", {}).get("stock", 0)
        new_product = Product(name=name, price=price, stock=stock)
        db.add(new_product)
        db.commit()
        return {"reply": "✅ Product '" + name + "' has been added with price \u20b950" + str(price) + " and stock " + str(stock) + "."}
    elif action == "delete_product":
        product_id = result.get("data", {}).get("product_id")
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"reply": "❌ Product not found."}
        db.delete(product)
        db.commit()
        return {"reply": f"🗑️ Product with ID {product_id} deleted successfully."}
    elif action == "get_orders":
        # Example order fetching logic
        orders = db.query(Order).all()
        if not orders:
            return {"reply": "📦 No orders found."}
        orders_lines = []
        for idx, o in enumerate(orders, start=1):
            orders_lines.append(f"{idx}. Product: {o.product_name}, Qty: {o.quantity}")
        orders_text = "\n".join(orders_lines)
        return {"reply": f"📦 Orders:\n{orders_text}"}
    elif action == "view_inventory":
        current_user_email = result.get("user_email")
        products = db.query(Product).filter(Product.seller_id == current_user_email).all()
        inventory_list = [f"{p.name}: {p.stock} units" for p in products]
        reply = "\n".join(inventory_list) if inventory_list else "Inventory is empty."
        return {"reply": reply}
    elif action == "update_inventory":
        product_id = result.get("product_id")
        stock = result.get("stock")
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {"reply": "❌ Product not found."}
        product.stock = stock
        db.commit()
        return {"reply": f"📦 Stock for Product ID {product_id} updated to {stock} units."}
    else:
        return {"reply": "❓ Sorry, I didn\u2019t understand that command. Try 'add product' or 'view orders'."}
@router.get("/webhook")
async def verify_webhook(request: Request):
    params = dict(request.query_params)
    if (
        params.get("hub.mode") == "subscribe" and
        params.get("hub.verify_token") == "onetappe123"
    ):
        return int(params.get("hub.challenge"))
    return {"status": "unauthorized"}

    # Handle buyer selection
    if text.startswith("Reply "):
        selection = text.split("Reply ")[1].strip()
        if selection.isdigit():
            selected_seller = sellers[int(selection) - 1]
            reply_text = "Select time: 10AM / 12PM / 4PM"
            await send_whatsapp_message(sender, reply_text)
            return {"status": "time slot requested"}

    # Handle time slot selection
    if text in ["10AM", "12PM", "4PM"]:
        create_booking(sender, selected_seller['id'], text, "today")
        reply_text = f"Booking confirmed for {selected_seller['name']} at {text}."
        await send_whatsapp_message(sender, reply_text)
        # Notify seller
        seller_message = f"New booking: {sender} at {text}."
        await send_whatsapp_message(selected_seller['contact'], seller_message)
        return {"status": "booking confirmed"}

# Simple in-memory state management for demonstration purposes
user_states = {}

async def handle_message(sender, text):
    state = user_states.get(sender, "")

    # Handle seller registration
    if text.lower() == "register":
        user_states[sender] = "awaiting shop name"
        reply_text = "What’s your shop name?"
        await send_whatsapp_message(sender, reply_text)
        return {"status": "awaiting shop name"}

    if state == "awaiting shop name":
        shop_name = text.strip()
        user_states[sender] = "awaiting service"
        reply_text = "Which service you offer?"
        await send_whatsapp_message(sender, reply_text)
        return {"status": "awaiting service", "shop_name": shop_name}

    if state == "awaiting service":
        service = text.strip()
        user_states[sender] = "awaiting pincode"
        reply_text = "Enter Pincode"
        await send_whatsapp_message(sender, reply_text)
        return {"status": "awaiting pincode", "service": service}

    if state == "awaiting pincode":
        pincode = text.strip()
        user_states[sender] = "awaiting hours"
        reply_text = "What’s your working hours?"
        await send_whatsapp_message(sender, reply_text)
        return {"status": "awaiting hours", "pincode": pincode}

    if state == "awaiting hours":
        hours = text.strip()
        # Validate and save to database
        if not validate_seller(shop_name, service, pincode, hours):
            reply_text = "Invalid input or duplicate entry. Please try again."
            await send_whatsapp_message(sender, reply_text)
            return {"status": "registration failed"}
        save_seller(shop_name, service, pincode, hours)
        reply_text = "Registration successful!"
        await send_whatsapp_message(sender, reply_text)
        user_states.pop(sender, None)  # Clear state after successful registration
        return {"status": "registration successful"}
