from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from src.db.session import get_db
from src.models.user import User

def get_user(user_id: int, db: Session = Depends(get_db)) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user

def get_db_session() -> Session:
    db = get_db()
    try:
        yield db
    finally:
        db.close()