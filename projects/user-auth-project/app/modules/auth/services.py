# Auth services
# create_access_token function to create JWT tokens
from datetime import datetime, timedelta
from jose import JWTError, jwt
from app.core.config import settings

# create_access_token function to create JWT tokens
def create_access_token(data: dict, expires_delta: timedelta | None = None):
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