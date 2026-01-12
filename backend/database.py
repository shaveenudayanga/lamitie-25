"""
=============================================================================
DATABASE CONNECTION MODULE
=============================================================================
This file handles the connection to our MySQL database using SQLAlchemy.

What is SQLAlchemy?
- It's a Python library that helps us talk to databases
- We're using "async" mode which means our app can handle multiple 
  requests at the same time without waiting (faster performance!)

What is aiomysql?
- It's the driver that lets Python connect to MySQL asynchronously
=============================================================================
"""

import os
from dotenv import load_dotenv
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

# Load environment variables from .env file
# This reads the .env file and makes those variables available
load_dotenv()

# Get the database URL from environment variables
# This keeps our password safe and not in the code
DATABASE_URL = os.getenv("DB_URL")

# Validate that DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError(
        "DATABASE_URL is not set! Please check your .env file. "
        "It should look like: DB_URL=mysql+aiomysql://user:pass@host:port/dbname"
    )

# Create the database engine
# Think of this as the "connection manager" to our database
# - echo=False: Don't print all SQL queries to console (set True for debugging)
# - pool_size=5: Keep 5 connections ready for use
# - max_overflow=10: Allow up to 10 extra connections if needed
# - pool_pre_ping=True: Test connections before using them (important for remote DBs)
# - pool_recycle=300: Recycle connections every 5 minutes (prevents stale connections)
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)

# Create a session factory
# Sessions are like "conversations" with the database
# Each API request will get its own session
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,  # Keep data accessible after commit
)


# Base class for all our database models (tables)
# All models will inherit from this class
class Base(DeclarativeBase):
    """
    Base class for SQLAlchemy models.
    All database tables/models inherit from this.
    """
    pass


async def init_db():
    """
    Initialize the database by creating all tables.
    
    This function:
    1. Connects to the database
    2. Creates all tables defined in our models
    3. Should be called when the app starts
    
    Note: This won't delete existing data, it only creates 
    tables if they don't exist.
    """
    async with engine.begin() as conn:
        # Import models here to ensure they're registered with Base
        from models import Student  # noqa: F401
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """
    Dependency function to get a database session.
    
    This is used by FastAPI to provide a database session
    to each API endpoint that needs it.
    
    How it works:
    1. Creates a new session
    2. Gives it to the API endpoint to use
    3. Automatically closes it when done (even if there's an error)
    
    Usage in endpoints:
        async def my_endpoint(db: AsyncSession = Depends(get_db)):
            # Use db here
    """
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
