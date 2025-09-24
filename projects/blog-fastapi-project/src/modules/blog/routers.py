# Blog Routers
from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from src.modules.blog.services import blog_service
from src.modules.user.services import user_service
from src.modules.blog.schemas import (
    BlogPostCreate, BlogPostUpdate, BlogPostResponse,
    CommentBase, CommentCreate, CommentUpdate, CommentResponse,
    LikesBase, LikesCreate, LikesUpdate
)

router = APIRouter(prefix="/blogs")

######## BlogPost Endpoints #########
@router.post("/posts/", response_model=BlogPostResponse, tags=["posts"])
async def create_post(post_data: BlogPostCreate):
    author_id = post_data.author_id
    if author_id is None:
        raise HTTPException(status_code=400, detail="author_id is required")
    
    # Check if author exists
    author = await user_service.check_if_user_exists(author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    
    return await blog_service.create_post(post_data)

@router.get("/posts/{post_id}", response_model=BlogPostResponse, tags=["posts"])
async def get_post(post_id: int):
    post = await blog_service.get_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.put("/posts/{post_id}", response_model=BlogPostResponse, tags=["posts"])
async def update_post(
    post_id: int,
    post_data: BlogPostUpdate,
    current_user_id: int  # TODO: Replace with proper authentication dependency
):
    existing_post = await blog_service.get_post(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Authorization check
    if existing_post.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    return await blog_service.update_post(post_id, post_data)

@router.delete("/posts/{post_id}", response_model=dict, tags=["posts"])
async def delete_post(
    post_id: int,
    current_user_id: int  # TODO: Replace with proper authentication dependency
):
    existing_post = await blog_service.get_post(post_id)
    if not existing_post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # Authorization check
    if existing_post.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    success = await blog_service.delete_post(post_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete post")
    
    return {"detail": "Post deleted successfully"}

@router.get("/posts/", response_model=List[BlogPostResponse], tags=["posts"])
async def list_posts(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return await blog_service.list_posts(skip=skip, limit=limit)

######## Comment Endpoints #########
@router.post("/comments/", response_model=CommentResponse, tags=["comments"])
async def create_comment(
    comment_data: CommentCreate,
    current_user_id: int  # TODO: Replace with proper authentication dependency
):
    # Set the author_id from the authenticated user
    comment_data.author_id = current_user_id
    return await blog_service.create_comment(comment_data)

@router.get("/comments/{comment_id}", response_model=CommentResponse, tags=["comments"])
async def get_comment(comment_id: int):
    comment = await blog_service.get_comment(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.put("/comments/{comment_id}", response_model=CommentResponse, tags=["comments"])
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    current_user_id: int  # TODO: Replace with proper authentication dependency
):
    existing_comment = await blog_service.get_comment(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Authorization check
    if existing_comment.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this comment")
    
    return await blog_service.update_comment(comment_id, comment_data)

@router.delete("/comments/{comment_id}", response_model=dict, tags=["comments"])
async def delete_comment(
    comment_id: int,
    current_user_id: int  # TODO: Replace with proper authentication dependency
):
    existing_comment = await blog_service.get_comment(comment_id)
    if not existing_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    # Authorization check
    if existing_comment.author_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this comment")
    
    success = await blog_service.delete_comment(comment_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete comment")
    
    return {"detail": "Comment deleted successfully"}

@router.get("/posts/{post_id}/comments/", response_model=List[CommentResponse], tags=["comments"])
async def list_comments(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    return await blog_service.list_comments(post_id=post_id, skip=skip, limit=limit)

######## Likes Endpoints #########
@router.post("/likes/", response_model=dict, tags=["likes"])
async def like_post(
    post_id: int,
    current_user_id: int  # TODO: Replace with proper authentication dependency
):
    like_data = LikesBase(post_id=post_id, user_id=current_user_id)
    await blog_service.like_post(like_data)
    return {"detail": "Post liked successfully"}

@router.delete("/likes/", response_model=dict, tags=["likes"])
async def unlike_post(
    post_id: int,
    current_user_id: int  # TODO: Replace with proper authentication dependency
):
    success = await blog_service.unlike_post(post_id, current_user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Like not found")
    return {"detail": "Post unliked successfully"}

@router.get("/posts/{post_id}/likes/count", response_model=dict, tags=["likes"])
async def count_likes(post_id: int):
    count = await blog_service.count_likes(post_id)
    return {"post_id": post_id, "like_count": count}

@router.get("/posts/{post_id}/likes/check", response_model=dict, tags=["likes"])  
async def has_liked(
    post_id: int,
    current_user_id: int  # TODO: Replace with proper authentication dependency
):
    liked = await blog_service.has_liked(post_id, current_user_id)
    return {"post_id": post_id, "has_liked": liked}

@router.get("/posts/{post_id}/likes/", response_model=List[dict], tags=["likes"])
async def list_likes(
    post_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    likes = await blog_service.list_likes(post_id=post_id, skip=skip, limit=limit)
    return [{"user_id": like.user_id, "created_at": like.created_at} for like in likes]

# Note: Authentication TODOs
# The current_user_id parameters marked with TODO need to be replaced with proper
# authentication dependencies that extract the current user from JWT tokens or sessions.
# This clean architecture separates concerns:
# - Router: HTTP handling and validation
# - Service: Business logic and database operations  
# - Authentication: Should be handled via FastAPI dependencies