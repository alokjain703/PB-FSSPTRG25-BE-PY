# FSSPTRG25-BE-PY
Fullstack specialization Training 2025 Backend Python Public Repo

# Getting Started
- app/: Contains the core application logic.
- main.py: The entry point of your FastAPI application, where you initialize the FastAPI instance and include your API routers.
- core/: Holds core functionalities like configuration (config.py), security utilities (security.py), and common dependencies (dependencies.py).
- db/: Handles database-related operations, including session management (session.py) and base classes for models (base.py).
- schemas/: Defines Pydantic models used for request and response data validation and serialization (e.g., user.py, blog.py).
- models.py: SQLAlchemy or ORM models specific to the module.
- crud/: Contains Create, Read, Update, Delete (CRUD) operations for your database models (e.g., user.py, blog.py).
- api/: Organizes your API endpoints, potentially by version (e.g., v1/).
- v1/endpoints/: Holds the actual FastAPI APIRouter instances for different resources (e.g., user.py, blog.py).
- v1/api.py: Aggregates all routers for a specific API version.
- modules/: This is where you define your distinct application modules (e.g., user, blog). Each module can contain:
- routers.py: Module-specific APIRouter instances.
services.py: Business logic and operations related to the module.
- tests/: Contains unit and integration tests for your application.
- .env: Stores environment variables for configuration.
- requirements.txt: Lists all project dependencies.
- alembic/: Contains files related to database migrations using Alembic.

