# User roles and permissions management routes
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.modules.user import services as user_services
from src.modules.user.schemas import UserCreate, UserSchema
from src.core.db_connection import get_db_session


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
router = APIRouter()

@router.post("/auth/assign-role/", response_model=UserSchema)
async def assign_role_to_user(
    user: UserSchema,
    role: str,
    db: AsyncSession = Depends(get_db_session)
):
    user = await user_services.get_user(db, user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_services.assign_role_to_user(user, role)
    await user_services.update_user(db, user)
    return user

@router.post("/auth/remove-role/", response_model=UserSchema)
async def remove_role_from_user(
    user: UserSchema,
    role: str,
    db: AsyncSession = Depends(get_db_session)
):
    user = await user_services.get_user(db, user.id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user = user_services.remove_role_from_user(user, role)
    await user_services.update_user(db, user)
    return user