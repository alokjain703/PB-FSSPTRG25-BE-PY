# Database Connection Configuration

## Overview
Your FastAPI project now supports multiple database environments with separate database files for testing and development.

## Database Files
- **Development**: `test-db/database.db` 
- **Test**: `test-db/database-test.db`
- **Production**: `test-db/database.db` (same as development for now)

## Configuration Methods

### Method 1: Environment Variable (Recommended)
Set the `FASTAPI_ENV` environment variable to control which database is used:

```bash
# Development (default)
export FASTAPI_ENV=development
# or just leave unset

# Test environment  
export FASTAPI_ENV=test

# Production
export FASTAPI_ENV=production
```

### Method 2: Direct Function Usage
Use the dedicated test database functions directly:

```python
from src.core.db_connection import get_test_db_session

async def my_test_function():
    async for db in get_test_db_session():
        # This always uses database-test.db
        pass
```

## How It Works

### Updated `db_connection.py`
```python
def get_database_url():
    """Get database URL based on environment"""
    env = os.getenv("FASTAPI_ENV", "development")
    
    if env == "test":
        return "sqlite+aiosqlite:///test-db/database-test.db"
    else:
        return "sqlite+aiosqlite:///test-db/database.db"
```

### Test Configuration
The test file automatically:
1. Sets `FASTAPI_ENV=test` 
2. Creates database tables if they don't exist
3. Cleans up data between tests

## Usage Examples

### Running Tests with Test Database
```bash
# Automatic (test file sets environment)
python -m pytest tests/

# Manual environment setting
FASTAPI_ENV=test python -m pytest tests/
```

### Running Application in Different Environments
```bash
# Development
python -m src.main

# Test mode
FASTAPI_ENV=test python -m src.main  

# Production
FASTAPI_ENV=production python -m src.main
```

## Benefits
1. **Isolation**: Tests don't interfere with development data
2. **Flexibility**: Easy switching between environments
3. **Safety**: Production and development databases are separate
4. **Clean Tests**: Automatic database cleanup between tests

## Database Structure
```
test-db/
├── database.db      # Development & Production
└── database-test.db # Testing
```

## Next Steps
Consider adding:
- PostgreSQL for production
- Docker environment support
- Database migration scripts
- Environment-specific configurations in separate files