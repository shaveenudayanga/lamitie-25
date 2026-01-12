"""
=============================================================================
LAMITIE 2025 - UNIVERSITY EVENT MANAGEMENT SYSTEM
=============================================================================
Main Application Entry Point

This is the heart of our backend system. It handles:
1. Student registration with QR code generation
2. Attendance tracking via QR code scanning
3. Email notifications with event invitations

Tech Stack:
- FastAPI: Modern, fast web framework for building APIs
- SQLAlchemy (Async): Database ORM for MySQL
- Pydantic V2: Data validation
- fastapi-mail: Email sending
- qrcode: QR code generation

API Endpoints:
- POST /register: Register a new student
- POST /scan: Mark attendance by scanning QR code
- GET /health: Health check endpoint
- GET /students: List all students (admin only, for testing)

Author: Lamitie 2025 Development Team
=============================================================================
"""

import os
from contextlib import asynccontextmanager
from dotenv import load_dotenv

from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

# Import our modules
from database import init_db, get_db
from models import Student
from schemas import (
    RegistrationRequest,
    RegistrationResponse,
    ScanRequest,
    ScanResponse,
    StudentResponse,
    ErrorResponse,
)
from email_utils import send_invitation_email

# Load environment variables from .env file
load_dotenv()


# =============================================================================
# APPLICATION LIFECYCLE
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application startup and shutdown events.
    
    On Startup:
    - Initialize database connection
    - Create tables if they don't exist
    
    On Shutdown:
    - Clean up resources
    """
    # Startup
    print("🚀 Starting Lamitie 2025 Backend...")
    print("📦 Initializing database...")
    await init_db()
    print("✅ Database initialized successfully!")
    print("🌐 Server is ready to accept connections")
    
    yield  # Application runs here
    
    # Shutdown
    print("👋 Shutting down Lamitie 2025 Backend...")


# =============================================================================
# APPLICATION CONFIGURATION
# =============================================================================

# Create the FastAPI application instance
app = FastAPI(
    title="Lamitie 2025 API",
    description="""
    🎉 **University Event Management System**
    
    This API handles student registration and attendance tracking 
    for the Lamitie 2025 cultural festival.
    
    ## Features
    - 📝 **Registration**: Students can register and receive QR code invitations
    - 📱 **Attendance**: Scan QR codes to mark attendance at the event
    - ✉️ **Email Notifications**: Automated email with QR code attachment
    
    ## Quick Start
    1. Register a student via `POST /register`
    2. Student receives email with QR code
    3. On event day, scan QR code via `POST /scan`
    """,
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",      # Swagger UI at /docs
    redoc_url="/redoc",    # ReDoc at /redoc
)

# =============================================================================
# CORS MIDDLEWARE
# =============================================================================
# CORS (Cross-Origin Resource Sharing) allows our React frontend
# to communicate with this backend API.
# Without this, browsers would block requests from localhost:5173

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Vite dev server (React)
        "http://127.0.0.1:5173",      # Alternative localhost
        "http://localhost:3000",       # Alternative React port
    ],
    allow_credentials=True,            # Allow cookies
    allow_methods=["*"],               # Allow all HTTP methods
    allow_headers=["*"],               # Allow all headers
)


# =============================================================================
# API ENDPOINTS
# =============================================================================

@app.get(
    "/",
    tags=["General"],
    summary="Welcome endpoint",
)
async def root():
    """
    Welcome endpoint - returns basic API information.
    
    Use this to verify the API is running.
    """
    return {
        "message": "Welcome to Lamitie 2025 API! 🎉",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
    }


@app.get(
    "/health",
    tags=["General"],
    summary="Health check",
)
async def health_check(db: AsyncSession = Depends(get_db)):
    """
    Health check endpoint - verifies API and database are working.
    
    Returns:
        - status: "healthy" if everything is working
        - database: "connected" if database is accessible
    """
    try:
        # Try a simple database query
        await db.execute(select(1))
        db_status = "connected"
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "service": "Lamitie 2025 API",
    }


# =============================================================================
# REGISTRATION ENDPOINT
# =============================================================================

@app.post(
    "/register",
    response_model=RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Registration"],
    summary="Register a new student",
    responses={
        201: {"description": "Student registered successfully"},
        400: {"model": ErrorResponse, "description": "Invalid input data"},
        409: {"model": ErrorResponse, "description": "Student already registered"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
async def register_student(
    registration: RegistrationRequest,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new student for Lamitie 2025.
    
    This endpoint:
    1. Validates the input data
    2. Creates a new student record in the database
    3. Sends an email with QR code (in background)
    4. Returns success response immediately
    
    The email is sent as a background task so the API responds instantly
    without waiting for the email to be delivered.
    
    **Request Body:**
    - `name`: Student's full name
    - `index_number`: Unique student ID (used in QR code)
    - `email`: Email address for invitation
    - `combination`: Subject combination
    
    **Returns:**
    - Success message with student details
    - Email is sent in background
    
    **Errors:**
    - 409: Student with this index number already exists
    - 400: Invalid input data
    """
    try:
        # Step 1: Create a new Student object
        new_student = Student(
            name=registration.name,
            index_number=registration.index_number,
            email=registration.email,
            combination=registration.combination,
            attendance_status=False,  # Not attended yet
        )
        
        # Step 2: Add to database and commit
        db.add(new_student)
        await db.commit()
        await db.refresh(new_student)  # Get the auto-generated ID
        
        # Step 3: Schedule email to be sent in background
        # This allows the API to respond immediately while
        # the email is being sent asynchronously
        background_tasks.add_task(
            send_invitation_email,
            recipient_email=registration.email,
            student_name=registration.name,
            index_number=registration.index_number,
        )
        
        # Step 4: Return success response
        return RegistrationResponse(
            success=True,
            message=(
                f"Registration successful! 🎉 "
                f"An invitation email with your QR code has been sent to {registration.email}"
            ),
            student=StudentResponse.model_validate(new_student),
        )
        
    except IntegrityError:
        # This happens when index_number already exists (unique constraint)
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={
                "success": False,
                "error": "A student with this index number is already registered",
                "detail": f"Index number '{registration.index_number}' is already in use",
            },
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": "An unexpected error occurred",
                "detail": str(e),
            },
        )


# =============================================================================
# ATTENDANCE/SCAN ENDPOINT
# =============================================================================

@app.post(
    "/scan",
    response_model=ScanResponse,
    tags=["Attendance"],
    summary="Scan QR code for attendance",
    responses={
        200: {"description": "Attendance recorded successfully"},
        404: {"model": ErrorResponse, "description": "Student not found"},
        500: {"model": ErrorResponse, "description": "Server error"},
    },
)
async def scan_attendance(
    scan_data: ScanRequest,
    db: AsyncSession = Depends(get_db),
):
    """
    Mark a student's attendance by scanning their QR code.
    
    This endpoint is called when a QR code is scanned at the event venue.
    The QR code contains the student's index_number.
    
    **What happens:**
    1. Look up the student by index_number
    2. If found, mark attendance_status as True
    3. Return success with student's name
    
    **Request Body:**
    - `index_number`: The index number extracted from QR code
    
    **Returns:**
    - Student's name (for welcome message at entry)
    - Whether they were already scanned
    
    **Errors:**
    - 404: No student found with this index number
    """
    try:
        # Step 1: Find the student by index number
        query = select(Student).where(Student.index_number == scan_data.index_number)
        result = await db.execute(query)
        student = result.scalar_one_or_none()
        
        # Step 2: Check if student exists
        if not student:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error": "Student not found",
                    "detail": f"No student registered with index number: {scan_data.index_number}",
                },
            )
        
        # Step 3: Check if already scanned
        already_scanned = student.attendance_status
        
        # Step 4: Update attendance status to True
        if not already_scanned:
            student.attendance_status = True
            await db.commit()
        
        # Step 5: Return appropriate response
        if already_scanned:
            return ScanResponse(
                success=True,
                message=f"Hello again, {student.name}! You've already checked in. Enjoy the event! 🎉",
                student_name=student.name,
                already_scanned=True,
            )
        else:
            return ScanResponse(
                success=True,
                message=f"Welcome, {student.name}! 🎉 Your attendance has been recorded. Have a great time!",
                student_name=student.name,
                already_scanned=False,
            )
            
    except HTTPException:
        raise  # Re-raise HTTP exceptions as-is
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": "An unexpected error occurred",
                "detail": str(e),
            },
        )


# =============================================================================
# ADMIN/DEBUG ENDPOINTS
# =============================================================================

@app.get(
    "/students",
    response_model=list[StudentResponse],
    tags=["Admin"],
    summary="List all students (Admin only)",
)
async def list_students(db: AsyncSession = Depends(get_db)):
    """
    Get a list of all registered students.
    
    **Note:** This endpoint is for admin/testing purposes.
    In production, you should add authentication.
    
    Returns:
        List of all students with their details
    """
    query = select(Student).order_by(Student.created_at.desc())
    result = await db.execute(query)
    students = result.scalars().all()
    
    return [StudentResponse.model_validate(s) for s in students]


@app.get(
    "/students/{index_number}",
    response_model=StudentResponse,
    tags=["Admin"],
    summary="Get student by index number",
    responses={
        200: {"description": "Student found"},
        404: {"model": ErrorResponse, "description": "Student not found"},
    },
)
async def get_student(
    index_number: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Get a specific student's details by their index number.
    
    **Note:** This endpoint is for admin/testing purposes.
    
    Args:
        index_number: The student's unique index number
        
    Returns:
        Student details if found
    """
    query = select(Student).where(Student.index_number == index_number)
    result = await db.execute(query)
    student = result.scalar_one_or_none()
    
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "error": "Student not found",
                "detail": f"No student with index number: {index_number}",
            },
        )
    
    return StudentResponse.model_validate(student)


# =============================================================================
# EXCEPTION HANDLERS
# =============================================================================

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler for unhandled errors.
    
    This catches any exception that isn't explicitly handled
    and returns a clean error response instead of crashing.
    """
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "error": "Internal server error",
            "detail": str(exc) if os.getenv("DEBUG", "False").lower() == "true" else None,
        },
    )


# =============================================================================
# MAIN ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    # Run the server
    # Host 0.0.0.0 allows connections from any IP (needed for Docker)
    # Port 8000 is the default for FastAPI
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # Auto-reload on code changes (dev only)
    )
