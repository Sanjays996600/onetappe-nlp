import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from models.base import SessionLocal
    print("Successfully imported SessionLocal")
except Exception as e:
    print(f"Error importing SessionLocal: {e}")