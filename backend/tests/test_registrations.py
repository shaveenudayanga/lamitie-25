from fastapi.testclient import TestClient
from src.main import app
from src.schemas.registration import RegistrationCreate, RegistrationResponse

client = TestClient(app)

def test_register_user():
    registration_data = RegistrationCreate(
        name="John Doe",
        index_number="123456",
        email="john.doe@example.com"
    )
    response = client.post("/api/v1/registrations/", json=registration_data.dict())
    assert response.status_code == 201
    assert response.json()["email"] == registration_data.email

def test_register_user_invalid_email():
    registration_data = RegistrationCreate(
        name="Jane Doe",
        index_number="654321",
        email="invalid-email"
    )
    response = client.post("/api/v1/registrations/", json=registration_data.dict())
    assert response.status_code == 422

def test_register_user_duplicate():
    registration_data = RegistrationCreate(
        name="John Doe",
        index_number="123456",
        email="john.doe@example.com"
    )
    response = client.post("/api/v1/registrations/", json=registration_data.dict())
    assert response.status_code == 400
    assert "already registered" in response.json()["detail"]