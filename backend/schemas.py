"""
=============================================================================
PYDANTIC SCHEMAS MODULE
=============================================================================
This file defines the data validation schemas using Pydantic V2.

What are Schemas?
- Schemas define the structure of data going in and out of our API
- They automatically validate that incoming data is correct
- They generate clear error messages if data is invalid
- They also help generate API documentation

Types of Schemas:
1. Request Schemas: What data the API expects to receive
2. Response Schemas: What data the API sends back
=============================================================================
"""

from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# =============================================================================
# REGISTRATION SCHEMAS
# =============================================================================

class RegistrationRequest(BaseModel):
    """
    Schema for the POST /register endpoint.
    
    This defines what data a student must provide to register.
    If any field is missing or invalid, the API will return an error.
    
    Example Request Body:
    {
        "name": "John Doe",
        "index_number": "2024CS001",
        "email": "john.doe@university.edu",
        "combination": "Physical Science"
    }
    """
    
    # Student's full name (required)
    # min_length ensures they can't submit an empty name
    name: str = Field(
        ...,  # ... means this field is required
        min_length=2,
        max_length=255,
        description="Student's full name",
        examples=["John Doe"]
    )
    
    # Unique index number (required)
    # This will be encoded in the QR code
    index_number: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="Unique student index number",
        examples=["2024CS001"]
    )
    
    # Email address (required)
    # EmailStr automatically validates email format
    email: EmailStr = Field(
        ...,
        description="Student's email address for sending invitation",
        examples=["john.doe@university.edu"]
    )
    
    # Mobile number (optional)
    # For contact purposes
    mobile_number: str | None = Field(
        default=None,
        max_length=20,
        description="Student's mobile phone number",
        examples=["0771234567"]
    )
    
    # Subject combination (required)
    combination: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Student's subject combination",
        examples=["Physical Science", "Biological Science", "Commerce"]
    )


class RegistrationResponse(BaseModel):
    """
    Schema for the response from POST /register.
    
    This is what the API sends back after a successful registration.
    
    Example Response:
    {
        "success": true,
        "message": "Registration successful! Check your email for the QR code invitation.",
        "student": {
            "id": 1,
            "name": "John Doe",
            "index_number": "2024CS001",
            "email": "john.doe@university.edu",
            "combination": "Physical Science",
            "attendance_status": false,
            "created_at": "2025-01-13T10:30:00"
        }
    }
    """
    
    success: bool = Field(
        ...,
        description="Whether the registration was successful"
    )
    
    message: str = Field(
        ...,
        description="A human-readable message about the result"
    )
    
    student: "StudentResponse" = Field(
        ...,
        description="The registered student's details"
    )


# =============================================================================
# ATTENDANCE/SCAN SCHEMAS
# =============================================================================

class ScanRequest(BaseModel):
    """
    Schema for the POST /scan endpoint.
    
    This is used when scanning a student's QR code at the event.
    The QR code contains the index_number.
    
    Example Request Body:
    {
        "index_number": "2024CS001"
    }
    """
    
    index_number: str = Field(
        ...,
        min_length=3,
        max_length=50,
        description="The index number from the scanned QR code",
        examples=["2024CS001"]
    )


class ScanResponse(BaseModel):
    """
    Schema for the response from POST /scan.
    
    This is what the scanning device/app receives after a successful scan.
    
    Example Response:
    {
        "success": true,
        "message": "Welcome, John Doe! Your attendance has been recorded.",
        "student_name": "John Doe",
        "already_scanned": false
    }
    """
    
    success: bool = Field(
        ...,
        description="Whether the scan was successful"
    )
    
    message: str = Field(
        ...,
        description="A human-readable message about the result"
    )
    
    student_name: str = Field(
        ...,
        description="The name of the student who was scanned"
    )
    
    already_scanned: bool = Field(
        default=False,
        description="True if this student was already marked as attended"
    )


# =============================================================================
# STUDENT SCHEMAS
# =============================================================================

class StudentResponse(BaseModel):
    """
    Schema representing a student's full details in responses.
    
    This is used when returning student information from the API.
    """
    
    # Enable ORM mode to work with SQLAlchemy models
    model_config = ConfigDict(from_attributes=True)
    
    id: int = Field(
        ...,
        description="Unique database ID"
    )
    
    name: str = Field(
        ...,
        description="Student's full name"
    )
    
    index_number: str = Field(
        ...,
        description="Unique student index number"
    )
    
    email: EmailStr = Field(
        ...,
        description="Student's email address"
    )
    
    mobile_number: str | None = Field(
        default=None,
        description="Student's mobile phone number"
    )
    
    combination: str = Field(
        ...,
        description="Student's subject combination"
    )
    
    attendance_status: bool = Field(
        ...,
        description="Whether the student has attended the event"
    )
    
    created_at: datetime = Field(
        ...,
        description="When the student registered"
    )


# =============================================================================
# ERROR SCHEMAS
# =============================================================================

class ErrorResponse(BaseModel):
    """
    Schema for error responses.
    
    Used when something goes wrong (validation error, not found, etc.)
    
    Example:
    {
        "success": false,
        "error": "Student with this index number already exists",
        "detail": "Duplicate index_number: 2024CS001"
    }
    """
    
    success: bool = Field(
        default=False,
        description="Always false for error responses"
    )
    
    error: str = Field(
        ...,
        description="Error message"
    )
    
    detail: str | None = Field(
        default=None,
        description="Additional error details (optional)"
    )
