# Blog Service Layer
from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import Session
from src.core.database import Base
from src.modules.blog.models import BlogPost, Comment, Likes, PostStatus, CommentApprovalStatus
from src.modules.user.models import User
from datetime import datetime
from typing import List, Optional
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert as pg_insert
from src.modules.blog.schemas import BlogPostCreate, BlogPostUpdate, CommentBase, CommentCreate, CommentUpdate, LikesBase, LikesCreate, LikesUpdate

class BlogService:
    def __init__(self, db: AsyncSession):
        self.db = db

######## BlogPost Methods #########
    async def create_post(self, post_data: BlogPostCreate) -> BlogPost:
        new_post = BlogPost(**post_data.model_dump())
        self.db.add(new_post)
        await self.db.commit()
        await self.db.refresh(new_post)
        return new_post
    
    async def get_post(self, post_id: int) -> Optional[BlogPost]:
        result = await self.db.execute(select(BlogPost).where(BlogPost.id == post_id))
        return result.scalars().first()

    async def update_post(self, post_id: int, post_data: BlogPostUpdate) -> Optional[BlogPost]:
        existing_post = await self.get_post(post_id)
        if not existing_post:
            return None
        for key, value in post_data.model_dump().items():
            setattr(existing_post, key, value)
        await self.db.commit()
        await self.db.refresh(existing_post)
        return existing_post

    async def delete_post(self, post_id: int) -> bool:
        existing_post = await self.get_post(post_id)
        if not existing_post:
            return False
        await self.db.delete(existing_post)
        await self.db.commit()
        return True
    
    async def list_posts(self, skip: int = 0, limit: int = 10) -> List[BlogPost]:
        result = await self.db.execute(select(BlogPost).offset(skip).limit(limit))
        return result.scalars().all()
    

######## Comment Methods #########
    async def create_comment(self, comment_data: CommentCreate) -> Comment:
        new_comment = Comment(**comment_data.model_dump())
        self.db.add(new_comment)
        await self.db.commit()
        await self.db.refresh(new_comment)
        return new_comment
    async def get_comment(self, comment_id: int) -> Optional[Comment]:
        result = await self.db.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalars().first()
    async def update_comment(self, comment_id: int, comment_data: CommentUpdate) -> Optional[Comment]:
        existing_comment = await self.get_comment(comment_id)
        if not existing_comment:
            return None
        for key, value in comment_data.model_dump().items():
            setattr(existing_comment, key, value)
        await self.db.commit()
        await self.db.refresh(existing_comment)
        return existing_comment
    async def delete_comment(self, comment_id: int) -> bool:
        existing_comment = await self.get_comment(comment_id)
        if not existing_comment:
            return False
        await self.db.delete(existing_comment)
        await self.db.commit()
        return True
    async def list_comments(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Comment]:
        result = await self.db.execute(
            select(Comment).where(Comment.post_id == post_id).offset(skip).limit(limit)
        )
        return result.scalars().all()
    

######## Likes Methods #########
    async def like_post(self, like_data: LikesCreate) -> Likes:
        new_like = Likes(**like_data.model_dump())
        self.db.add(new_like)
        await self.db.commit()
        await self.db.refresh(new_like)
        return new_like
    async def unlike_post(self, post_id: int, user_id: int) -> bool:
        result = await self.db.execute(
            select(Likes).where(Likes.post_id == post_id, Likes.user_id == user_id)
        )
        existing_like = result.scalars().first()
        if not existing_like:
            return False
        await self.db.delete(existing_like)
        await self.db.commit()
        return True
    async def count_likes(self, post_id: int) -> int:
        result = await self.db.execute(
            select(Likes).where(Likes.post_id == post_id)
        )
        return result.scalars().count()
    async def has_liked(self, post_id: int, user_id: int) -> bool:
        result = await self.db.execute(
            select(Likes).where(Likes.post_id == post_id, Likes.user_id == user_id)
        )
        return result.scalars().first() is not None
    async def list_likes(self, post_id: int, skip: int = 0, limit: int = 10) -> List[Likes]:
        result = await self.db.execute(
            select(Likes).where(Likes.post_id == post_id).offset(skip).limit(limit)
        )
        return result.scalars().all()
    
    
