from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    index_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    attendance_status = Column(Boolean, default=False)