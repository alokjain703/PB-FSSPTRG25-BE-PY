# user routers
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user import services as user_services
from src.modules.user.schemas import UserCreate, UserSchema, UserUpdate
from src.core.db_connection import get_db_session
from src.modules.user.services import UserService

router = APIRouter()

def get_user_service(db: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(db)
# create user router
@router.post("/users/", response_model=UserSchema)
async def create_user(user: UserCreate, user_service: UserService = Depends(get_user_service)):
    return await user_service.create_user(**user.dict())

#get all users 
@router.get("/user/all-users", response_model=list[UserSchema])
async def read_users(skip: int = 0, limit: int = 100, user_service: UserService = Depends(get_user_service)):
    users = await user_service.get_all_users(skip=skip, limit=limit)
    return users

@router.get("/users/{username}", response_model=UserSchema)
async def read_user(username: str, user_service: UserService = Depends(get_user_service)):
    db_user = await user_service.get_user(username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update User for user with user_id in route params
@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserUpdate, user_service: UserService = Depends(get_user_service)):
    updated_user = await user_service.update_user(
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
async def delete_user(user_id: int, user_service: UserService = Depends(get_user_service)):
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return { "detail": "User deleted"}


