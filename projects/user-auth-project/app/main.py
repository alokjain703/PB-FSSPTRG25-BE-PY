from fastapi import FastAPI
from .core.config import settings
app = FastAPI()

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