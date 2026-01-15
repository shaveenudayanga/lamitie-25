from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    index_number = Column(String(50), unique=True, index=True)
    email = Column(String(255), unique=True, index=True)
    mobile_number = Column(String(20), nullable=True)
    combination = Column(String(100), nullable=True)
    attendance_status = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now(), server_default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), server_default=func.now())