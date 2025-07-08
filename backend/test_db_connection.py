from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

load_dotenv()
db_url = os.getenv("DATABASE_URL")
engine = create_engine(db_url)

try:
    with engine.connect() as conn:
        print("✅ PostgreSQL connected successfully")
except Exception as e:
    print("❌ Failed to connect:", e)