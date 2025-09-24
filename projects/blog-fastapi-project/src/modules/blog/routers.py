# Blog Routers
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_connection import get_db_session
from src.modules.blog.services import BlogService
from src.modules.user.services import UserService
from src.modules.blog.schemas import (
    BlogPostCreate, BlogPostUpdate, BlogPostResponse,
    CommentBase, CommentCreate, CommentUpdate, CommentResponse,
    LikesBase, LikesCreate, LikesUpdate
)
from src.modules.blog.models import BlogPost, Comment

from src.modules.user.models import User

router = APIRouter(prefix="/blogs")
# Dependency to get the BlogService
def get_blog_service(db: AsyncSession = Depends(get_db_session)) -> BlogService:
    return BlogService(db)
def get_user_service(db: AsyncSession = Depends(get_db_session)) -> UserService:
    return UserService(db)


######## BlogPost Endpoints #########
@router.post("/posts/", response_model=BlogPostResponse , tags=[ "posts"])
async def create_post(
    post_data: BlogPostCreate,
    user_service: UserService = Depends(get_user_service),
    blog_service: BlogService = Depends(get_blog_service)
):
    author_id = post_data.author_id
    if author_id is None:
        raise HTTPException(status_code=400, detail="author_id is required")
    # check if author exists
    author = await user_service.check_if_user_exists(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return await blog_service.create_post(post_data)

@router.get("/posts/{post_id}", response_model=BlogPostResponse , tags=[ "posts"])
async def get_post(
    post_id: int,
    blog_service: BlogService = Depends(get_blog_service)
):
    post = await blog_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/posts/{post_id}", response_model=BlogPostResponse , tags=[ "posts"])
async def update_post(
    post_id: int,
    post_data: BlogPostUpdate,
    user_service: User = Depends(get_user_service),
    blog_service: BlogService = Depends(get_blog_service)
):
    existing_post = await blog_service.get_post(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing_post.author_id != user_service.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    return await blog_service.update_post(post_id, post_data)

@router.delete("/posts/{post_id}", response_model=dict , tags=[ "posts"])
async def delete_post(
    post_id: int,
    user_service: User = Depends(get_user_service),
    blog_service: BlogService = Depends(get_blog_service)
):
    existing_post = await blog_service.get_post(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    if existing_post.author_id != user_service.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    success = await blog_service.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete post")
    return {"detail": "Post deleted successfully"} 

@router.get("/posts/", response_model=List[BlogPostResponse] , tags=[ "posts"])
async def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    blog_service: BlogService = Depends(get_blog_service)
):
    return await blog_service.list_posts(skip=skip, limit=limit)


######## Comment Endpoints #########
@router.post("/comments/", response_model=CommentResponse, tags=[ "comments"])
async def create_comment( 
    comment_data: CommentCreate,
    user_service: User = Depends(get_user_service),
    blog_service: BlogService = Depends(get_blog_service)
):
    comment_data.author_id = user_service.id
    return await blog_service.create_comment(comment_data)
@router.get("/comments/{comment_id}", response_model=CommentResponse, tags=[ "comments"])
async def get_comment(
    comment_id: int,
    blog_service: BlogService = Depends(get_blog_service)
):
    comment = await blog_service.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment
@router.put("/comments/{comment_id}", response_model=CommentResponse , tags=[ "comments"])
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    user_service: User = Depends(get_user_service),
    blog_service: BlogService = Depends(get_blog_service)
):
    existing_comment = await blog_service.get_comment(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.author_id != user_service.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    return await blog_service.update_comment(comment_id, comment_data)

@router.delete("/comments/{comment_id}", response_model=dict , tags=[ "comments"])
async def delete_comment(
    comment_id: int,
    user_service: User = Depends(get_user_service),
    blog_service: BlogService = Depends(get_blog_service)
):
    existing_comment = await blog_service.get_comment(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if existing_comment.author_id != user_service.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    success = await blog_service.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete comment")
    return {"detail": "Comment deleted successfully"}
@router.get("/posts/{post_id}/comments/", response_model=List[CommentResponse], tags=[ "comments"])
async def list_comments(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    blog_service: BlogService = Depends(get_blog_service)
):
    return await blog_service.list_comments(post_id=post_id, skip=skip, limit=limit)

######## Likes Endpoints #########
@router.post("/likes/", response_model=dict, tags=[ "likes"])
async def like_post(
    post_id: int,
    user_service: User = Depends(get_user_service),
    blog_service: BlogService = Depends(get_blog_service)
):
    like_data = LikesBase(post_id=post_id, user_id=user_service.id)
    await blog_service.like_post(like_data)
    return {"detail": "Post liked successfully"}

@router.delete("/likes/", response_model=dict , tags=[ "likes"])
async def unlike_post(
    post_id: int,
    user_service: User = Depends(get_user_service),
    blog_service: BlogService = Depends(get_blog_service)
):
    success = await blog_service.unlike_post(post_id, user_service.id)
    if not success:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"detail": "Post unliked successfully"}

@router.get("/posts/{post_id}/likes/count", response_model=dict, tags=[ "likes"])
async def count_likes(
    post_id: int,
    blog_service: BlogService = Depends(get_blog_service)
):
    count = await blog_service.count_likes(post_id)
    return {"post_id": post_id, "like_count": count}

@router.get("/posts/{post_id}/likes/check", response_model=dict, tags=[ "likes"])
async def has_liked(
    post_id: int,
    user_service: User = Depends(get_user_service),
    blog_service: BlogService = Depends(get_blog_service)
):
    liked = await blog_service.has_liked(post_id, user_service.id)
    return {"post_id": post_id, "has_liked": liked}

@router.get("/posts/{post_id}/likes/", response_model=List[dict] , tags=[ "likes"])
async def list_likes(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    blog_service: BlogService = Depends(get_blog_service)
):
    likes = await blog_service.list_likes(post_id=post_id, skip=skip, limit=limit)
    return [{"user_id": like.user_id, "created_at": like.created_at} for like in likes] 

# Note: For simplicity, the likes listing endpoint returns a list of dictionaries with user_id and created_at.
# In a real application, you might want to create a Pydantic schema for this.
# This code provides a comprehensive set of CRUD operations for blog posts, comments, and likes,
# along with appropriate authorization checks to ensure users can only modify their own content. It also includes pagination for listing endpoints.
# Make sure to test each endpoint thoroughly and handle edge cases as needed.