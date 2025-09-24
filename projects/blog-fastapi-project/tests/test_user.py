# Python unit test to test user services
import os

# CRITICAL: Set test environment BEFORE any imports that might use the database
os.environ["FASTAPI_ENV"] = "test"
print("Environment set to test for unit tests:", os.environ["FASTAPI_ENV"])

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.modules.user import services as user_services
from src.modules.user.models import User
from src.modules.user.schemas import UserSchema
from src.core.db_connection import get_db_session
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest_asyncio.fixture(autouse=True)
async def clean_database():
    """Clean up database before each test"""
    # Import here to avoid circular imports
    from src.core.database import Base
    from src.core.db_connection import get_engine
    
    # Create tables if they don't exist (for test database)
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    # Cleanup before test
    async for db in get_db_session():
        # Delete all test users
        result = await db.execute(select(User))
        users = result.scalars().all()
        for user in users:
            await db.delete(user)
        await db.commit()
    
    yield  # Run the test
    
    # Cleanup after test (optional, but good practice)
    async for db in get_db_session():
        result = await db.execute(select(User))
        users = result.scalars().all()
        for user in users:
            await db.delete(user)
        await db.commit()

@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    async for session in get_db_session():
        yield session
        await session.close()

@pytest_asyncio.fixture
async def user_service() -> user_services.UserService:
    return user_services.UserService()
@pytest.mark.asyncio
async def test_create_user( user_service: user_services.UserService):
    username = "testuser1"
    email = "testuser1@example.com"
    full_name = "Test User 1"
    password = "password123"
    user = await user_service.create_user(username, email, full_name, password)
    assert user
    assert user.username == username
    assert user.email == email
    assert user.full_name == full_name
    assert user.disabled == False  # SQLite stores as 0/1 # New users should be enabled by default
    # Verify password is hashed
    async for db in get_db_session():
        result = await db.execute(select(User).where(User.id == user.id))
        db_user = result.scalars().first()
        assert db_user is not None
        assert pwd_context.verify(password, db_user.hashed_password)
@pytest.mark.asyncio
async def test_get_user( user_service: user_services.UserService):
    # First, create a user to fetch
    username = "fetchuser1"
    email = "fetchuser1@example.com"
    full_name = "Fetch User 1"
    password = "password123"
    user = await user_service.create_user(username, email, full_name, password)
    assert user
    assert user.username == username
    assert user.email == email
    assert user.full_name == full_name
    assert user.disabled == False  # SQLite stores as 0/1 # New users should be enabled by default
    # Verify password is hashed
    async for db in get_db_session():
        result = await db.execute(select(User).where(User.id == user.id))
        db_user = result.scalars().first()
        assert db_user is not None
        assert pwd_context.verify(password, db_user.hashed_password)
    # Now, fetch the user by username
    fetched_user = await user_service.get_user(username)
    assert fetched_user is not None
    assert fetched_user.username == username
    assert fetched_user.email == email
    assert fetched_user.full_name == full_name
    assert user.disabled == False  # SQLite stores as 0/1
@pytest.mark.asyncio
async def test_get_all_users( user_service: user_services.UserService):
    # Create multiple users
    users_data = [
        ("Testuser2", "user1@example.com", "User One", "password123"),
        ("Testuser3", "user2@example.com", "User Two", "password123"),
        ("Testuser4", "user3@example.com", "User Three", "password123"),
    ]
    for username, email, full_name, password in users_data:
        user = await user_service.create_user(username, email, full_name, password)
        assert user
        assert user.username == username
        assert user.email == email
        assert user.full_name == full_name
        assert user.disabled == False  # SQLite stores as 0/1
    # Now, fetch all users
    all_users = await user_service.get_all_users()
    assert all_users is not None
    assert len(all_users) == len(users_data)
    for user, (username, email, full_name, password) in zip(all_users, users_data):
        assert user.username == username
        assert user.email == email
        assert user.full_name == full_name
        assert user.disabled == False  # SQLite stores as 0/1
@pytest.mark.asyncio
async def test_update_user(user_service: user_services.UserService):
    # First, create a user to update
    username = "Testupdateuser"
    email = "Testupdateuser@example.com"
    full_name = "Test Update User"
    password = "password123"
    user = await user_service.create_user(username, email, full_name, password)
    assert user
    assert user.username == username
    assert user.email == email
    assert user.full_name == full_name
    assert user.disabled == False  # SQLite stores as 0/1
    # Now, update the user's information
    new_email = "new_updateuser@example.com"
    new_full_name = "New Update User"
    updated_user = await user_service.update_user(user.id, email=new_email, full_name=new_full_name)
    assert updated_user
    assert updated_user.id == user.id
    assert updated_user.email == new_email
    assert updated_user.full_name == new_full_name
    assert user.disabled == False  # SQLite stores as 0/1
    # Verify password remains unchanged
    async for db in get_db_session():
        result = await db.execute(select(User).where(User.id == user.id))
        db_user = result.scalars().first()
        assert db_user is not None
        assert pwd_context.verify(password, db_user.hashed_password)
@pytest.mark.asyncio
async def test_delete_user( user_service: user_services.UserService):
    # First, create a user to delete
    username = "Testdeleteuser"
    email = "Testdeleteuser@example.com"
    full_name = "Test Delete User"
    password = "password123"
    user = await user_service.create_user(username, email, full_name, password)
    assert user
    assert user.username == username
    assert user.email == email
    assert user.full_name == full_name
    assert user.disabled == False  # SQLite stores as 0/1
    # Now, delete the user
    deletion_result = await user_service.delete_user(user.id)
    assert deletion_result is True  # delete_user returns boolean
    # Verify user is actually deleted
    async for db in get_db_session():
        result = await db.execute(select(User).where(User.id == user.id))
        db_user = result.scalars().first()
        assert db_user is None
@pytest.mark.asyncio
async def test_check_if_user_exists( user_service: user_services.UserService):
    # First, create a user to check
    username = "Testexistuser"
    email = "Testexistuser@example.com" # Corrected email
    full_name = "Test Exist User"
    password = "password123"
    user = await user_service.create_user(username, email, full_name, password)
    assert user
    assert user.username == username
    assert user.email == email
    assert user.full_name == full_name
    assert user.disabled == False  # SQLite stores as 0/1
    # Now, check if the user exists
    existing_user = await user_service.check_if_user_exists(user.id)
    assert existing_user is not None
    assert existing_user.id == user.id
    assert existing_user.username == username
    assert existing_user.email == email
    assert existing_user.full_name == full_name
    assert existing_user.disabled == False  # SQLite stores as 0/1, not True/False
    # Check for a non-existing user
    non_existing_user = await user_service.check_if_user_exists(99999) # Assuming this ID doesn't exist
    assert non_existing_user is None

# Note: Database cleanup is handled automatically by the clean_database fixture

# how to run the tests
# install pytest and pytest-asyncio if not already installed
# pip3 install pytest pytest-asyncio
# pytest tests/test_user.py --asyncio-mode=auto --maxfail=1 --disable-warnings -q
# pytest tests/test_user.py --asyncio-mode=auto -v
