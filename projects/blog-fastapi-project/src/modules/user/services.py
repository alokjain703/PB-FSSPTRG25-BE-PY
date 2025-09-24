# User services
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.modules.user.models import User
from src.modules.user.schemas import UserSchema
from passlib.context import CryptContext
from src.core.db_connection import get_db_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# Function to get user by username
class UserService:
    def __init__(self):
        pass
    
    async def get_user(self, username: str) -> UserSchema | None:
        """Get a single user by username"""
        async for db in get_db_session():
            result = await db.execute(select(User).where(User.username == username))
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

    async def get_all_users(self, skip: int = 0, limit: int = 100) -> list[UserSchema]:
        """Get multiple users with pagination"""
        
        async for db in get_db_session():
            result = await db.execute(select(User).offset(skip).limit(limit))
            users = result.scalars().all()
            return [
                UserSchema(
                    id=user.id,
                    username=user.username,
                    email=user.email,
                    full_name=user.full_name,
                    disabled=bool(user.disabled)
                ) for user in users
            ]

    async def create_user(self, username: str, email: str, full_name: str, password: str) -> UserSchema:
        """Create a new user"""
        
        async for db in get_db_session():
            hashed_password = pwd_context.hash(password)
            new_user = User(
                username=username,
                email=email,
                full_name=full_name,
                hashed_password=hashed_password,
                disabled=0
            )
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            return UserSchema(
                id=new_user.id,
                username=new_user.username,
                email=new_user.email,
                full_name=new_user.full_name,
                disabled=bool(new_user.disabled)
            )

    async def update_user(
        self,
        user_id: int,
        username: str = None,
        email: str = None,
        full_name: str = None,
        password: str = None,
        disabled: bool = None
    ) -> UserSchema | None:
        """Update an existing user"""
        
        async for db in get_db_session():
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()
            if not user:
                return None

            if username is not None:
                user.username = username
            if email is not None:
                user.email = email
            if full_name is not None:
                user.full_name = full_name
            if password is not None:
                user.hashed_password = pwd_context.hash(password)
            if disabled is not None:
                user.disabled = int(disabled)
            
            await db.commit()
            await db.refresh(user)
            return UserSchema(
                id=user.id,
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                disabled=bool(user.disabled)
            )

    async def delete_user(self, user_id: int) -> bool:
        """Delete a user by ID"""
        
        async for db in get_db_session():
            result = await db.execute(select(User).where(User.id == user_id))
            user = result.scalars().first()
            if not user:
                return False
            await db.delete(user)
            await db.commit()
            return True

    async def check_if_user_exists(self, user_id: int) -> User | None:
        """Check if a user exists by ID"""
        async for db in get_db_session():
            result = await db.execute(select(User).where(User.id == user_id))
            return result.scalars().first()
        async for db in get_db_session():
            result = await db.execute(select(User).where(User.id == user_id))
            return result.scalars().first()


# Create singleton instance
user_service = UserService()
    
