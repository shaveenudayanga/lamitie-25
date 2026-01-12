from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Venue(Base):
    __tablename__ = 'venues'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    capacity = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)

    def __repr__(self):
        return f"<Venue(name={self.name}, location={self.location}, capacity={self.capacity})>"