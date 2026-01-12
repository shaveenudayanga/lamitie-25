from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.venue import Venue
from src.schemas.venue import VenueCreate, VenueUpdate
from src.core.exceptions import NotFoundException

class VenueRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_venue(self, venue: VenueCreate) -> Venue:
        db_venue = Venue(**venue.dict())
        self.db.add(db_venue)
        self.db.commit()
        self.db.refresh(db_venue)
        return db_venue

    def get_venue(self, venue_id: int) -> Venue:
        venue = self.db.query(Venue).filter(Venue.id == venue_id).first()
        if not venue:
            raise NotFoundException(f"Venue with id {venue_id} not found")
        return venue

    def get_venues(self, skip: int = 0, limit: int = 10) -> List[Venue]:
        return self.db.query(Venue).offset(skip).limit(limit).all()

    def update_venue(self, venue_id: int, venue_data: VenueUpdate) -> Venue:
        venue = self.get_venue(venue_id)
        for key, value in venue_data.dict(exclude_unset=True).items():
            setattr(venue, key, value)
        self.db.commit()
        self.db.refresh(venue)
        return venue

    def delete_venue(self, venue_id: int) -> None:
        venue = self.get_venue(venue_id)
        self.db.delete(venue)
        self.db.commit()