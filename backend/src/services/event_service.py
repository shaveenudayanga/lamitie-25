from sqlalchemy.orm import Session
from typing import List
from src.models.event import Event
from src.schemas.event import EventCreate, EventUpdate
from src.core.exceptions import NotFoundException

class EventService:
    def __init__(self, db: Session):
        self.db = db

    def create_event(self, event_data: EventCreate) -> Event:
        event = Event(**event_data.dict())
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def get_event(self, event_id: int) -> Event:
        event = self.db.query(Event).filter(Event.id == event_id).first()
        if not event:
            raise NotFoundException(f"Event with id {event_id} not found")
        return event

    def update_event(self, event_id: int, event_data: EventUpdate) -> Event:
        event = self.get_event(event_id)
        for key, value in event_data.dict(exclude_unset=True).items():
            setattr(event, key, value)
        self.db.commit()
        self.db.refresh(event)
        return event

    def delete_event(self, event_id: int) -> None:
        event = self.get_event(event_id)
        self.db.delete(event)
        self.db.commit()

    def get_all_events(self) -> List[Event]:
        return self.db.query(Event).all()