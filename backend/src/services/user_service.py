from sqlalchemy.orm import Session
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate
from src.core.exceptions import UserNotFoundException

class UserService:
    def __init__(self, db: Session):
        self.db = db

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        db_user = User(**user.dict())
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def get_user(db: Session, user_id: int) -> User:
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise UserNotFoundException(f"User with id {user_id} not found")
        return user

    @staticmethod
    def get_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return db.query(User).offset(skip).limit(limit).all()

    @staticmethod
    def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User:
        user = UserService.get_user(db, user_id)
        for key, value in user_update.dict(exclude_unset=True).items():
            setattr(user, key, value)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int) -> None:
        user = UserService.get_user(db, user_id)
        db.delete(user)
        db.commit()