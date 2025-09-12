from pydantic import BaseModel, Field
from typing import Optional

class UserSchema(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None

class UserInDB(UserSchema):
    hashed_password: str

class UserCreate(BaseModel):
    username: str = Field(..., example="johndoe")
    email: str = Field(..., example="johndoe@example.com")
    full_name: str = Field(..., example="John Doe")
    password: str = Field(..., example="password123")