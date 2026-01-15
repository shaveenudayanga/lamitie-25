from pydantic import BaseModel, EmailStr
from typing import Optional

class UserBase(BaseModel):
    name: str
    index_number: str
    email: EmailStr
    mobile_number: Optional[str] = None

class UserCreate(UserBase):
    password: str

class StudentRegister(BaseModel):
    name: str
    index_number: str
    email: EmailStr
    mobile_number: Optional[str] = None
    combination: str

class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDB(UserBase):
    hashed_password: str

class User(UserBase):
    id: int
    combination: Optional[str] = None
    mobile_number: Optional[str] = None
    attendance_status: bool

    class Config:
        orm_mode = True