import os
from sqlalchemy.ext.asyncio import (
    create_async_engine, AsyncSession,
)
from sqlalchemy.orm import sessionmaker

def get_database_url():
    """Get database URL based on environment"""
    env = os.getenv("FASTAPI_ENV", "development")
    
    if env == "test":
        return "sqlite+aiosqlite:///test-db/database-test.db"
    else:
        return "sqlite+aiosqlite:///test-db/database.db"

def get_engine():
    database_url = get_database_url()
    echo = os.getenv("FASTAPI_ENV") != "production"  # Only echo in dev/test
    return create_async_engine(database_url, echo=echo)
# Dynamic session creation to respect environment changes
def get_session_local():
    """Get a fresh sessionmaker with current environment settings"""
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine(),
        class_=AsyncSession,
    )

async def get_db_session():
    """Get database session that respects current environment"""
    SessionLocal = get_session_local()
    async with SessionLocal() as session:
        yield session

#########  Test-specific database connection #########
def get_test_engine():
    """Get engine specifically for testing with database-test.db"""
    return create_async_engine(
        "sqlite+aiosqlite:///test-db/database-test.db", 
        echo=True
    )

def get_test_session_local():
    """Get a fresh test sessionmaker"""
    return sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_test_engine(),
        class_=AsyncSession,
    )

async def get_test_db_session():
    """Get database session specifically for testing"""
    TestSessionLocal = get_test_session_local()
    async with TestSessionLocal() as session:
        yield session