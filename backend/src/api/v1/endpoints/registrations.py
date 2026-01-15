from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.schemas.registration import RegistrationCreate, RegistrationResponse
from src.services.registration_service import RegistrationService
from src.models.user import User
from src.api.deps import get_db
from pydantic import BaseModel

router = APIRouter()

class ScanRequest(BaseModel):
    index_number: str

@router.post("/", response_model=RegistrationResponse)
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

@router.post("/scan/", response_model=dict)
async def scan_attendance(scan: ScanRequest, db: Session = Depends(get_db)):
    """Mark student attendance by scanning QR code or manual entry"""
    user = db.query(User).filter(User.index_number == scan.index_number).first()
    
    if not user:
        raise HTTPException(
            status_code=404, 
            detail={"detail": f"Student with index {scan.index_number} not found"}
        )
    
    if user.attendance_status:
        return {
            "success": False,
            "message": f"{user.name} has already been checked in!",
            "student_name": user.name,
            "already_checked_in": True
        }
    
    # Mark attendance
    user.attendance_status = True
    db.commit()
    db.refresh(user)
    
    return {
        "success": True,
        "message": f"Welcome, {user.name}! Access Granted.",
        "student_name": user.name,
        "already_checked_in": False
    }