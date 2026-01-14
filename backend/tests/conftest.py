from fastapi import FastAPI
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.db.session import get_db
from src.config.settings import settings

@pytest.fixture(scope="session")
def db_session():
    engine = create_engine(settings.db_url)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture
def db():
    db = db_session()
    yield db
    db.close()

@pytest.fixture
def client():
    app = FastAPI()
    app.dependency_overrides[get_db] = lambda: db_session()
    with TestClient(app) as client:
        yield client