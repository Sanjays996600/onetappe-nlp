import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.base import Base, engine

Base.metadata.create_all(bind=engine)

print("Orders and Inventory tables created successfully.")