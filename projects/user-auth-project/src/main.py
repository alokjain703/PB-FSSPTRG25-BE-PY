from fastapi import FastAPI
from .core.config import settings
from contextlib import asynccontextmanager
from src.core.db_connection import get_db_session, get_engine
from src.core.database import Base
# import user model
from src.modules.user import models as user_models

#import routers 
from src.modules.user.routers import router as user_router
from src.modules.auth.routers import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
    await engine.dispose()
app = FastAPI(lifespan=lifespan)



@app.get("/")
def read_root():
    return {"Hello": "World"}

# include routers with prefix and tags
app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(auth_router, prefix="/auth", tags=["auth"])

# for testing purpose
@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "database_url": settings.database_url,
        "debug_mode": settings.debug_mode,
    }