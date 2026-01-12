from sqlalchemy.orm import Session
from typing import List, Optional
from src.models.event import Event
from src.schemas.event import EventCreate, EventUpdate

class EventRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_event(self, event_id: int) -> Optional[Event]:
        return self.db.query(Event).filter(Event.id == event_id).first()

    def get_events(self, skip: int = 0, limit: int = 100) -> List[Event]:
        return self.db.query(Event).offset(skip).limit(limit).all()

    def create_event(self, event: EventCreate) -> Event:
        db_event = Event(**event.dict())
        self.db.add(db_event)
        self.db.commit()
        self.db.refresh(db_event)
        return db_event

    def update_event(self, event_id: int, event: EventUpdate) -> Optional[Event]:
        db_event = self.get_event(event_id)
        if db_event:
            for key, value in event.dict(exclude_unset=True).items():
                setattr(db_event, key, value)
            self.db.commit()
            self.db.refresh(db_event)
            return db_event
        return None

    def delete_event(self, event_id: int) -> Optional[Event]:
        db_event = self.get_event(event_id)
        if db_event:
            self.db.delete(db_event)
            self.db.commit()
            return db_event
        return None