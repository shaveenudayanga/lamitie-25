from sqlalchemy.orm import Session
from fastapi import HTTPException
from ..models.registration import Registration
from ..repositories.registration_repository import RegistrationRepository
from ..schemas.registration import RegistrationCreate, RegistrationResponse
from ..utils.helpers import generate_qr_code, send_email

class RegistrationService:
    def __init__(self, db: Session):
        self.db = db
        self.registration_repository = RegistrationRepository(db)

    def create_registration(self, registration_data: RegistrationCreate) -> RegistrationResponse:
        existing_registration = self.registration_repository.get_by_email(registration_data.email)
        if existing_registration:
            raise HTTPException(status_code=400, detail="Email already registered")

        registration = Registration(**registration_data.dict())
        self.registration_repository.create(registration)

        qr_code = generate_qr_code(registration.id)
        send_email(registration.email, qr_code)

        return RegistrationResponse.from_orm(registration)

    def get_registration(self, registration_id: int) -> RegistrationResponse:
        registration = self.registration_repository.get_by_id(registration_id)
        if not registration:
            raise HTTPException(status_code=404, detail="Registration not found")
        return RegistrationResponse.from_orm(registration)