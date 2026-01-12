from pydantic import BaseModel
from typing import Optional

class VenueBase(BaseModel):
    name: str
    location: str
    capacity: int
    description: Optional[str] = None

class VenueCreate(VenueBase):
    pass

class VenueUpdate(VenueBase):
    pass

class Venue(VenueBase):
    id: int

    class Config:
        orm_mode = True