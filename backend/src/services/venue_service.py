from sqlalchemy.orm import Session
from typing import List
from src.models.venue import Venue
from src.schemas.venue import VenueCreate, VenueUpdate
from src.repositories.venue_repository import VenueRepository
from src.core.exceptions import NotFoundException

class VenueService:
    def __init__(self, db: Session):
        self.db = db
        self.venue_repository = VenueRepository(db)

    def create_venue(self, venue_data: VenueCreate) -> Venue:
        return self.venue_repository.create(venue_data)

    def get_venue(self, venue_id: int) -> Venue:
        venue = self.venue_repository.get(venue_id)
        if not venue:
            raise NotFoundException(f"Venue with id {venue_id} not found")
        return venue

    def update_venue(self, venue_id: int, venue_data: VenueUpdate) -> Venue:
        venue = self.get_venue(venue_id)
        return self.venue_repository.update(venue, venue_data)

    def delete_venue(self, venue_id: int) -> None:
        venue = self.get_venue(venue_id)
        self.venue_repository.delete(venue)

    def list_venues(self) -> List[Venue]:
        return self.venue_repository.list_all()