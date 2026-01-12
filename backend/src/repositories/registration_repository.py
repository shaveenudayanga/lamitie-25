from sqlalchemy.orm import Session
from src.models.registration import Registration
from src.schemas.registration import RegistrationCreate, RegistrationUpdate
from typing import List, Optional

class RegistrationRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_registration(self, registration: RegistrationCreate) -> Registration:
        db_registration = Registration(**registration.dict())
        self.db.add(db_registration)
        self.db.commit()
        self.db.refresh(db_registration)
        return db_registration

    def get_registration(self, registration_id: int) -> Optional[Registration]:
        return self.db.query(Registration).filter(Registration.id == registration_id).first()

    def get_registrations(self, skip: int = 0, limit: int = 100) -> List[Registration]:
        return self.db.query(Registration).offset(skip).limit(limit).all()

    def update_registration(self, registration_id: int, registration: RegistrationUpdate) -> Optional[Registration]:
        db_registration = self.get_registration(registration_id)
        if db_registration:
            for key, value in registration.dict(exclude_unset=True).items():
                setattr(db_registration, key, value)
            self.db.commit()
            self.db.refresh(db_registration)
            return db_registration
        return None

    def delete_registration(self, registration_id: int) -> Optional[Registration]:
        db_registration = self.get_registration(registration_id)
        if db_registration:
            self.db.delete(db_registration)
            self.db.commit()
            return db_registration
        return None