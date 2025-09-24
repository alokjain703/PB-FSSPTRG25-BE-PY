from sqlalchemy import Column, Integer, String
from src.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String, index=True)
    disabled = Column(Integer, default=0)   # 0 for False, 1 for True
    username = Column(String, unique=True, index=True)