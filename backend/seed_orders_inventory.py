import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import SessionLocal, Order, Inventory
import uuid
from datetime import datetime

# Create a new database session
session = SessionLocal()

try:
    # Insert dummy orders
    orders = [
        Order(id=uuid.uuid4().int % 100000, product="Milk", buyer="Ramesh", quantity=2, date=datetime.utcnow()),
        Order(id=uuid.uuid4().int % 100000, product="Laptop", buyer="John", quantity=1, date=datetime.utcnow()),
        Order(id=uuid.uuid4().int % 100000, product="Mixer", buyer="Ali", quantity=3, date=datetime.utcnow())
    ]

    # Insert dummy inventory
    inventory_items = [
        Inventory(item_id=uuid.uuid4().int % 100000, stock_count=10, threshold=5),
        Inventory(item_id=uuid.uuid4().int % 100000, stock_count=15, threshold=7),
        Inventory(item_id=uuid.uuid4().int % 100000, stock_count=5, threshold=2)
    ]

    # Add all to the session
    session.add_all(orders + inventory_items)
    session.commit()
    print("Seeded 3 orders and 3 inventory items successfully.")
except Exception as e:
    session.rollback()
    print(f"An error occurred: {e}")
finally:
    session.close()