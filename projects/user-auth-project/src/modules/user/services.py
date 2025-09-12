# User services
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.modules.user.models import User
from src.modules.user.schemas import UserSchema
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Function to get user by username
async def get_user(session: AsyncSession, username: str) -> UserSchema | None:
    result = await session.execute(select(User).where(User.username == username))
    user = result.scalars().first() 
    if user:
        return UserSchema(
            id=user.id,
            username=user.username,
            email=user.email,
            full_name=user.full_name,
            disabled=bool(user.disabled)
        )
    return None
# Function to create a new user
async def create_user(session: AsyncSession, username: str, email: str, full_name: str, password: str) -> UserSchema:
    hashed_password = pwd_context.hash(password)
    new_user = User(
        username=username,
        email=email,
        full_name=full_name,
        hashed_password=hashed_password,
        disabled=0
    )
    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)
    return UserSchema(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        full_name=new_user.full_name,
        disabled=bool(new_user.disabled)
    )