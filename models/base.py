from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv
import sys

# Get the project root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Load environment variables from the backend .env file
load_dotenv(os.path.join(project_root, 'backend', '.env'))
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if we're using SQLite (for testing) or PostgreSQL (for production)
if DATABASE_URL.startswith('sqlite'):
    engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
else:
    engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

from sqlalchemy import Column, Integer, String, DateTime

from datetime import datetime, timezone
from sqlalchemy import ForeignKey, Float

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    product = Column(String, nullable=False)
    buyer = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Inventory(Base):
    __tablename__ = "inventory"
    item_id = Column(Integer, primary_key=True, index=True)
    stock_count = Column(Integer, nullable=False)
    threshold = Column(Integer, nullable=False)

class Seller(Base):
    __tablename__ = "sellers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    service = Column(String)
    pincode = Column(String)
    hours = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    seller_id = Column(Integer, ForeignKey("sellers.id"))
    name = Column(String, nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    stock = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))