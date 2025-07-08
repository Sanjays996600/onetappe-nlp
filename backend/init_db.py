import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to path

from models.base import Base, engine, DATABASE_URL

def init_db():
    # Print database connection information
    print(f"Using database: {DATABASE_URL}")
    print(f"Engine URL: {engine.url}")
    
    # Create all tables in the database
    Base.metadata.create_all(bind=engine)
    print("Database tables created successfully!")
    
    # List all tables created
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in database: {tables}")

if __name__ == "__main__":
    init_db()