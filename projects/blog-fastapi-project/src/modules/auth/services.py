# Auth services
# create_access_token function to create JWT tokens
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings
from src.modules.user.models import User
from src.modules.user.services import get_user
from sqlalchemy.ext.asyncio import AsyncSession

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    # create_access_token function to create JWT tokens
    def create_access_token(self, data: dict, expires_delta: timedelta | None = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
        return encoded_jwt

    # decode_access_token function to decode JWT tokens
    def decode_access_token(token: str):
        try:
            payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
            return payload
        except JWTError:
            return None
    
    # def decode_access_token(
    #     token: str, session: Session
    # ) -> User | None:
    #     try:
    #         payload = jwt.decode(
    #             token, settings.secret_key, algorithms=[settings.algorithm]
    #         )
    #         username: str = payload.get("sub")
    #     except JWTError:
    #         return
    #     if not username:
    #         return
    #     user = get_user(session, username)
    #     return user

    # add user roles and permissions management functions here
    # e.g., assign_role_to_user, check_user_permission, etc.

    def assign_role_to_user(user: User, role: str):
        user.roles.append(role)
        return user

    def remove_role_from_user(user: User, role: str):
        if role in user.roles:
            user.roles.remove(role)
        return user

    def check_user_permission(user: User, permission: str) -> bool:
        return permission in user.permissions