from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..db.base import Base

class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)
    venue_id = Column(Integer, ForeignKey('venues.id'))

    venue = relationship("Venue", back_populates="events")

    def __repr__(self):
        return f"<Event(title={self.title}, start_time={self.start_time}, end_time={self.end_time})>"