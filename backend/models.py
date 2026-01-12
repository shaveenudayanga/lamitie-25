"""
=============================================================================
DATABASE MODELS MODULE
=============================================================================
This file defines the structure of our database tables using SQLAlchemy ORM.

What is a Model?
- A model is a Python class that represents a database table
- Each attribute of the class becomes a column in the table
- SQLAlchemy handles converting between Python objects and database rows

The Student model stores:
- Student's personal info (name, email, index number)
- Their subject combination
- Registration timestamp
- Whether they attended the event
=============================================================================
"""

from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from database import Base


class Student(Base):
    """
    Student Model - Represents the 'students' table in the database.
    
    This table stores all registered students for Lamitie 2025.
    Each row represents one student registration.
    
    Table Name: students
    
    Columns:
    - id: Auto-generated unique identifier
    - name: Student's full name
    - index_number: Unique student ID (used for QR code)
    - email: Student's email address
    - combination: Subject combination (e.g., "Physical Science")
    - attendance_status: Has the student arrived at the event?
    - created_at: When did they register?
    """
    
    # Name of the table in the database
    __tablename__ = "students"
    
    # ==========================================================================
    # COLUMN DEFINITIONS
    # ==========================================================================
    
    # Primary Key: Auto-incrementing unique ID for each student
    # Example: 1, 2, 3, 4...
    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        comment="Unique identifier for the student"
    )
    
    # Student's full name
    # Example: "John Doe"
    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Student's full name"
    )
    
    # Unique index number - used for QR code generation
    # This must be unique across all students
    # Example: "2024CS001"
    index_number: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,  # Creates an index for faster lookups
        comment="Unique student index number (used in QR code)"
    )
    
    # Student's email address for sending invitations
    # Example: "john.doe@university.edu"
    email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Student's email address"
    )
    
    # Subject combination the student is enrolled in
    # Example: "Physical Science", "Biological Science", "Commerce"
    combination: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Student's subject combination"
    )
    
    # Attendance status - Did the student show up on event day?
    # Default is False (not attended yet)
    # Changes to True when they scan their QR code at the event
    attendance_status: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        comment="Whether student has attended the event"
    )
    
    # Timestamp of when the student registered
    # Automatically set to current time when record is created
    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
        comment="Registration timestamp"
    )
    
    def __repr__(self) -> str:
        """
        String representation of the Student object.
        Useful for debugging and logging.
        
        Example output: <Student(id=1, name='John Doe', index='2024CS001')>
        """
        return f"<Student(id={self.id}, name='{self.name}', index='{self.index_number}')>"
