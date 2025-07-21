import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import api
from app.models import get_session
from app.auth.models import User, UserRole

@pytest.fixture
def test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    return engine

@pytest.fixture
def client(test_db):
    def get_test_session():
        with test_db.connect() as conn:
            yield conn
    
    api.dependency_overrides[get_session] = get_test_session
    return TestClient(api)

def test_register_user(client):
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123",
        "full_name": "Test User"
    }
    
    response = client.post("/auth/register", json=user_data)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == user_data["email"]
    assert data["username"] == user_data["username"]

def test_login_user(client):
    # First register a user
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "testpassword123"
    }
    client.post("/auth/register", json=user_data)
    
    # Then try to login
    login_data = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer" 