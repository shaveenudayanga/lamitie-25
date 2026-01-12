from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.models.user import User
from src.schemas.user import UserCreate
from src.db.session import get_db
from sqlalchemy.orm import Session
import pytest

app = FastAPI()

# Dependency override for testing
@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = next(get_db())):
    return db.query(User).filter(User.id == user_id).first()

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

def test_create_user(client):
    response = client.post("/users/", json={"name": "John Doe", "index_number": "123456", "email": "john@example.com"})
    assert response.status_code == 201
    assert response.json()["name"] == "John Doe"

def test_read_user(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_read_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"