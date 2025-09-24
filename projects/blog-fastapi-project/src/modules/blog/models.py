# BlogPost model based on SQLAlchemy
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum as SQLEnum
from src.core.database import Base
from sqlalchemy.orm import  Mapped, mapped_column, relationship
from src.modules.user.models import User

# Define enums
class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    PENDING_REVIEW = "pending_review"

class CommentApprovalStatus(int, Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2

# mapped_column is the modern, recommended approach introduced in SQLAlchemy 2.0. It provides:

# Better Type Hints: Works seamlessly with Python type annotations
# Declarative Mapping: More explicit and cleaner syntax
# Better IDE Support: Enhanced autocompletion and type checking
# Future-Proof: This is the direction SQLAlchemy is moving toward
class BlogPost(Base):
    __tablename__ = "blog_posts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    excerpt: Mapped[str | None] = mapped_column(String(200))
    tags: Mapped[str] = mapped_column(String(255), default="[]")
    status: Mapped[PostStatus] = mapped_column(SQLEnum(PostStatus), default=PostStatus.DRAFT)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    category: Mapped[str | None] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)

    def __repr__(self):
        return f"<BlogPost(title={self.title}, status={self.status})>"
    
class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    approved: Mapped[CommentApprovalStatus] = mapped_column(SQLEnum(CommentApprovalStatus), default=CommentApprovalStatus.PENDING)

    def __repr__(self):
        return f"<Comment(author_name={self.author_name}, post_id={self.post_id})>"
    
class Likes (Base):
    __tablename__ = "likes"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("blog_posts.id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Likes(user_id={self.user_id}, post_id={self.post_id})>"

# class Category(Base):
#     __tablename__ = "categories"

#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String(100), unique=True, nullable=False)
#     description = Column(Text)

#     def __repr__(self):
#         return f"<Category(name={self.name})>"
