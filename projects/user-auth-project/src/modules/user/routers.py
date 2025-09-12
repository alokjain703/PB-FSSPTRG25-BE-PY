# user routers
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user import services as user_services
from src.modules.user.schemas import UserCreate, UserSchema
from src.core.db_connection import get_db_session

router = APIRouter()

# create user router
@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    return await user_services.create_user(db, **user.dict())

@router.get("/users/{username}", response_model=UserSchema)
async def read_user(username: str, db: AsyncSession = Depends(get_db_session)):
    db_user = await user_services.get_user(db, username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user




