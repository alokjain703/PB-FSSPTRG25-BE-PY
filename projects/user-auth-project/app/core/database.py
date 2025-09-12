from sqlalchemy import Column, Float, ForeignKey, Table
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
)
class Base(DeclarativeBase):
    pass

class Ticket(Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(nullable=True)
    show: Mapped[str | None]
    user: Mapped[str | None]

class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=False, unique=True)
    email: Mapped[str] = mapped_column(nullable=False, unique=True)
    full_name: Mapped[str | None] = mapped_column(nullable=True)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    disabled: Mapped[int] = mapped_column(default=0)  # 0 for False, 1 for True