import os
from dotenv import load_dotenv

print("Current working directory:", os.getcwd())
load_dotenv()
print("DATABASE_URL:", os.getenv("DATABASE_URL"))