import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from models.user import User, UserRole
from models.base import SessionLocal
from passlib.context import CryptContext
import uuid

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def seed_test_user():
    db = SessionLocal()
    test_email = "test_user@example.com"
    existing_user = db.query(User).filter(User.email == test_email).first()
    if existing_user:
        print(f"User {test_email} already exists. Skipping creation.")
        return

    user = User(
        id=str(uuid.uuid4()),
        email=test_email,
        hashed_password=get_password_hash("test123"),
        is_active=True,
        is_superuser=False,
        role=UserRole.seller
    )
    db.add(user)
    db.commit()
    print(f"✅ Test user created: {test_email} / test123")


if __name__ == "__main__":
    seed_test_user()