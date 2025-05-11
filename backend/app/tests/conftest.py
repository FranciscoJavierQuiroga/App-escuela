import asyncio
import os
import pytest
from sqlmodel import SQLModel, Session
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import StaticPool

from app.main import app
from app.database.session import get_session
from app.models.user import User, UserRole
from app.auth.token import get_password_hash

# Use an in-memory SQLite database for testing
TEST_DATABASE_URL = "sqlite:///./test.db"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def test_db():
    # Create the test database
    engine = create_async_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    
    # Create all tables
    SQLModel.metadata.create_all(engine)
    
    # Override the dependency
    def override_get_session():
        with Session(engine) as session:
            yield session
    
    app.dependency_overrides[get_session] = override_get_session
    
    yield engine
    
    # Clean up
    SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def test_client(test_db):
    with TestClient(app) as client:
        yield client

@pytest.fixture(scope="function")
async def admin_user(test_db):
    async with Session(test_db) as session:
        # Create admin user for testing
        admin = User(
            email="admin@test.com",
            first_name="Test",
            last_name="Admin",
            role=UserRole.ADMIN,
            hashed_password=get_password_hash("testpassword")
        )
        
        session.add(admin)
        await session.commit()
        await session.refresh(admin)
        
        yield admin

@pytest.fixture(scope="function")
async def teacher_user(test_db):
    async with Session(test_db) as session:
        # Create teacher user for testing
        teacher = User(
            email="teacher@test.com",
            first_name="Test",
            last_name="Teacher",
            role=UserRole.TEACHER,
            hashed_password=get_password_hash("testpassword")
        )
        
        session.add(teacher)
        await session.commit()
        await session.refresh(teacher)
        
        yield teacher

@pytest.fixture(scope="function")
async def student_user(test_db):
    async with Session(test_db) as session:
        # Create student user for testing
        student = User(
            email="student@test.com",
            first_name="Test",
            last_name="Student",
            role=UserRole.STUDENT,
            hashed_password=get_password_hash("testpassword")
        )
        
        session.add(student)
        await session.commit()
        await session.refresh(student)
        
        yield student