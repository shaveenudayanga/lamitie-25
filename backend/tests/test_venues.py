import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.models.venue import Venue
from src.db.session import get_db

@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

@pytest.fixture
def db_session():
    db = next(get_db())
    yield db

def test_create_venue(client, db_session):
    response = client.post("/api/v1/venues/", json={"name": "Conference Hall", "capacity": 200})
    assert response.status_code == 201
    assert response.json()["name"] == "Conference Hall"

def test_get_venue(client, db_session):
    response = client.get("/api/v1/venues/1")
    assert response.status_code == 200
    assert "name" in response.json()

def test_update_venue(client, db_session):
    response = client.put("/api/v1/venues/1", json={"name": "Updated Hall", "capacity": 250})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Hall"

def test_delete_venue(client, db_session):
    response = client.delete("/api/v1/venues/1")
    assert response.status_code == 204

def test_get_nonexistent_venue(client, db_session):
    response = client.get("/api/v1/venues/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Venue not found"