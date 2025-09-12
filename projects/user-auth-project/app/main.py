from fastapi import FastAPI
from .core.config import settings
from contextlib import asynccontextmanager
from app.core.db_connection import get_db_session, get_engine
from app.core.database import Base

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

# for testing purpose
@app.get("/info")
async def info():
    return {
        "app_name": settings.app_name,
        "database_url": settings.database_url,
        "debug_mode": settings.debug_mode,
    }