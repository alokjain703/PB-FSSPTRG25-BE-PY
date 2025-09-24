# Blog Service Layer
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Session
from src.core.database import Base
from src.core.db_connection import get_db_session
from src.modules.blog.models import BlogPost, Comment, Likes, PostStatus, CommentApprovalStatus
from src.modules.user.models import User
from datetime import datetime
from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from src.modules.blog.schemas import BlogPostCreate, BlogPostUpdate, CommentBase, CommentCreate, CommentUpdate, LikesBase, LikesCreate, LikesUpdate

class BlogService:
    def __init__(self):
        pass

######## BlogPost Methods #########
    async def create_post(self, post_data: BlogPostCreate) -> BlogPost:
        async for db in get_db_session():
            new_post = BlogPost(**post_data.model_dump())
            db.add(new_post)
            await db.commit()
            await db.refresh(new_post)
            return new_post
    
    async def get_post(self, post_id: int) -> Optional[BlogPost]:
        async for db in get_db_session():
            result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
            return result.scalars().first()

    async def update_post(self, post_id: int, post_data: BlogPostUpdate) -> Optional[BlogPost]:
        async for db in get_db_session():
            result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
            existing_post = result.scalars().first()
            if not existing_post:
                return None
            for key, value in post_data.model_dump().items():
                setattr(existing_post, key, value)
            await db.commit()
            await db.refresh(existing_post)
            return existing_post

    async def delete_post(self, post_id: int) -> bool:
        async for db in get_db_session():
            result = await db.execute(select(BlogPost).where(BlogPost.id == post_id))
            existing_post = result.scalars().first()
            if not existing_post:
                return False
            await db.delete(existing_post)
            await db.commit()
            return True
    
    async def list_posts(self, skip: int = 0, limit: int = 10) -> List[BlogPost]:
        async for db in get_db_session():
            result = await db.execute(select(BlogPost).offset(skip).limit(limit))
            return result.scalars().all()
    

######## Comment Methods #########
    async def create_comment(self, comment_data: CommentCreate) -> Comment:
        async for db in get_db_session():
            new_comment = Comment(**comment_data.model_dump())
            db.add(new_comment)
            await db.commit()
            await db.refresh(new_comment)
            return new_comment
    async def get_comment(self, comment_id: int) -> Optional[Comment]:
        async for db in get_db_session():
            result = await db.execute(select(Comment).where(Comment.id == comment_id))
            return result.scalars().first()
    async def update_comment(self, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        async for db in get_db_session():
            result = await db.execute(select(Comment).where(Comment.id == comment_id))
            existing_comment = result.scalars().first()
            if not existing_comment:
                return None
            for key, value in comment_data.model_dump().items():
                setattr(existing_comment, key, value)
            await db.commit()
            await db.refresh(existing_comment)
            return existing_comment
    async def delete_comment(self, comment_id: int) -> bool:
        async for db in get_db_session():
            result = await db.execute(select(Comment).where(Comment.id == comment_id))
            existing_comment = result.scalars().first()
            if not existing_comment:
                return False
            await db.delete(existing_comment)
            await db.commit()
            return True
    async def list_comments(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        async for db in get_db_session():
            result = await db.execute(
                select(Comment).where(Comment.post_id == post_id).offset(skip).limit(limit)
            )
            return result.scalars().all()
    

######## Likes Methods #########
    async def like_post(self, like_data: LikesCreate) -> Likes:
        async for db in get_db_session():
            new_like = Likes(**like_data.model_dump())
            db.add(new_like)
            await db.commit()
            await db.refresh(new_like)
            return new_like
    async def unlike_post(self, post_id: int, user_id: int) -> bool:
        async for db in get_db_session():
            result = await db.execute(
                select(Likes).where(Likes.post_id == post_id, Likes.user_id == user_id)
            )
            existing_like = result.scalars().first()
            if not existing_like:
                return False
            await db.delete(existing_like)
            await db.commit()
            return True
    async def count_likes(self, post_id: int) -> int:
        async for db in get_db_session():
            result = await db.execute(
                select(Likes).where(Likes.post_id == post_id)
            )
            return len(result.scalars().all())
    async def has_liked(self, post_id: int, user_id: int) -> bool:
        async for db in get_db_session():
            result = await db.execute(
                select(Likes).where(Likes.post_id == post_id, Likes.user_id == user_id)
            )
            return result.scalars().first() is not None
    async def list_likes(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Likes]:
        async for db in get_db_session():
            result = await db.execute(
                select(Likes).where(Likes.post_id == post_id).offset(skip).limit(limit)
            )
            return result.scalars().all()


# Create singleton instance
blog_service = BlogService()