from pydantic import BaseModel
from typing import Optional

class RegistrationCreate(BaseModel):
    user_id: int
    event_id: int
    qr_code: Optional[str] = None

class RegistrationResponse(BaseModel):
    id: int
    user_id: int
    event_id: int
    qr_code: Optional[str] = None

    class Config:
        orm_mode = True