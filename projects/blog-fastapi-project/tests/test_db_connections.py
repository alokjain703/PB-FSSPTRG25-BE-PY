#!/usr/bin/env python3
"""
Test script to demonstrate different database connections
"""
import os
import asyncio
from src.core.db_connection import get_database_url, get_db_session, get_test_db_session

async def test_connections():
    print("=== Database Connection Test ===\n")
    
    # Test 1: Default (development) environment
    print("1. Default environment:")
    print(f"   Database URL: {get_database_url()}")
    
    # Test 2: Test environment
    print("\n2. Test environment:")
    os.environ["FASTAPI_ENV"] = "test"
    print(f"   Database URL: {get_database_url()}")
    
    # Test 3: Production environment
    print("\n3. Production environment:")
    os.environ["FASTAPI_ENV"] = "production"
    print(f"   Database URL: {get_database_url()}")
    
    # Reset to test environment for demonstration
    os.environ["FASTAPI_ENV"] = "test"
    
    print("\n=== Testing Database Sessions ===")
    
    # Test regular session (will use test DB because FASTAPI_ENV=test)
    print("\n4. Regular session (using environment-based URL):")
    async for db in get_db_session():
        print(f"   Connected to database session")
        break
    
    # Test dedicated test session
    print("\n5. Dedicated test session:")
    async for db in get_test_db_session():
        print(f"   Connected to test database session")
        break
    
    print("\n✅ All database connections working!")

if __name__ == "__main__":
    asyncio.run(test_connections())