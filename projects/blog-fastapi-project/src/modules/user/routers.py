# user routers
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user import services as user_services
from src.modules.user.schemas import UserCreate, UserSchema, UserUpdate
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

# Update User for user with user_id in route params
@router.get("/users/{user_id}", response_model=UserSchema)
async def update_user( user_id: int, user: UserUpdate, db: AsyncSession = Depends(get_db_session)):
    updated_user = await user_services.update_user(
        db,
        user_id=user_id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        password=user.password,
        disabled=user.disabled
    )
    if updated_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

# Delete User by Id
@router.delete("/users/{user_id}", status_code=200)
async def delete_user( user_id: int, db: AsyncSession = Depends(get_db_session )):
    success = await user_services.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return { "detail": "User deleted"}


