from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from src.api.deps import get_db
from src.models.user import User
from src.schemas.user import UserCreate, User as UserResponse, StudentRegister
from src.services.user_service import UserService

router = APIRouter()

@router.post("/", response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserService.create_user(db=db, user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="User already exists")
    return db_user

@router.post("/register/", response_model=dict)
def register_student(student: StudentRegister, db: Session = Depends(get_db)):
    """Register a new student (no password required)"""
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
        combination=student.combination,
        attendance_status=False
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"success": True, "message": "Registration successful", "user_id": new_user.id}

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = UserService.get_user(db=db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.get("/", response_model=list[UserResponse])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = UserService.get_users(db=db, skip=skip, limit=limit)
    return users