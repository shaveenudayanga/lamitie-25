from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
from src.api.deps import get_db, get_current_admin
from src.models.user import User
from src.schemas.user import UserCreate, User as UserResponse, StudentRegister
from src.services.user_service import UserService
import asyncio
import sys
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import email function from the root email_utils module
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
from email_utils import send_invitation_email

router = APIRouter()

def send_email_sync(recipient_email: str, student_name: str, index_number: str):
    """Synchronous wrapper for async email function"""
    logger.info(f"🚀 Starting email send to {recipient_email}")
    try:
        result = asyncio.run(
            send_invitation_email(
                recipient_email=recipient_email,
                student_name=student_name,
                index_number=index_number
            )
        )
        logger.info(f"✅ Email send completed: {result}")
        return result
    except Exception as e:
        logger.error(f"❌ Error sending email: {e}")
        import traceback
        traceback.print_exc()
        return False

@router.post("/", response_model=UserResponse)
def create_user(
    user: UserCreate, 
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)  # Protected: requires auth
):
    db_user = UserService.create_user(db=db, user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user

@router.post("/register/", response_model=dict)
async def register_student(
    student: StudentRegister, 
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)  # Protected: requires auth
):
    """Register a new student (no password required) and send invitation email"""
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == student.email) | (User.index_number == student.index_number)
    ).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="User with this email or index number already exists")
    
    # Create new user
    new_user = User(
        name=student.name,
        index_number=student.index_number,
        email=student.email,
        mobile_number=student.mobile_number,
        combination=student.combination,
        attendance_status=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Send invitation email in background using sync wrapper
    background_tasks.add_task(
        send_email_sync,
        recipient_email=student.email,
        student_name=student.name,
        index_number=student.index_number,
    )
    
    return {
        "success": True, 
        "message": f"Registration successful! An invitation email has been sent to {student.email}",
        "user_id": new_user.id
    }

@router.get("/index/{index_number}", response_model=UserResponse)
def read_user_by_index(
    index_number: str, 
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)  # Protected: requires auth
):
    """Get user by index number (e.g., AS2023359)"""
    db_user = db.query(User).filter(User.index_number == index_number).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with index number {index_number} not found")
    return db_user

@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int, 
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)  # Protected: requires auth
):
    db_user = UserService.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db),
    admin: dict = Depends(get_current_admin)  # Protected: requires auth
):
    users = UserService.get_users(db=db, skip=skip, limit=limit)
    return users