from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schemas.registration import RegistrationCreate, RegistrationResponse
from src.services.registration_service import RegistrationService
from src.api.deps import get_db

router = APIRouter()

@router.post("/registrations/", response_model=RegistrationResponse)
async def create_registration(
    registration: RegistrationCreate,
    db: Session = Depends(get_db)
):
    try:
        registration_service = RegistrationService(db)
        new_registration = await registration_service.create_registration(registration)
        return new_registration
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))