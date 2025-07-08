import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))  # Add parent directory to path

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool

from models.base import Base
from backend.main import app
from backend.database import get_db

# Create in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def test_db():
    # Create the tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session for testing
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
    # Drop the tables after the test
    Base.metadata.drop_all(bind=engine)

# Override the get_db dependency
@pytest.fixture(scope="function")
def override_get_db(test_db):
    def _get_test_db():
        try:
            yield test_db
        finally:
            pass
    return _get_test_db

@pytest.fixture(scope="function")
def client(override_get_db):
    # Override the get_db dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create a test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Reset the dependency override
    app.dependency_overrides = {}