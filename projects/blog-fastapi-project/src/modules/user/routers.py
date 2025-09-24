# user routers
from fastapi import APIRouter, HTTPException, status
from src.modules.user.schemas import UserCreate, UserSchema, UserUpdate
from src.modules.user.services import user_service

router = APIRouter()
# create user router
@router.post("/users/", response_model=UserSchema)
# send error message if unique constraint or any other error occurs

async def create_user(user: UserCreate):
    try:
        return await user_service.create_user(**user.dict())
    except Exception as e:
        # suppress hashed password in error message
        detail = str(e)
        if "hashed_password" in detail:
            detail = detail.replace("hashed_password", "****")
        raise HTTPException(status_code=400, detail=detail)

#get all users 
@router.get("/user/all-users", response_model=list[UserSchema])
async def read_users(skip: int = 0, limit: int = 100):
    users = await user_service.get_all_users(skip=skip, limit=limit)
    return users

@router.get("/users/{username}", response_model=UserSchema)
async def read_user(username: str):
    db_user = await user_service.get_user(username)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Update User for user with user_id in route params
@router.put("/users/{user_id}", response_model=UserSchema)
async def update_user(user_id: int, user: UserUpdate):
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
async def delete_user(user_id: int):
    success = await user_service.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return { "detail": "User deleted"}


