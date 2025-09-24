# BlogPost schema for full post. icluding author name and email
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum
from src.modules.blog.enums import PostStatus, CommentApprovalStatus

######### BlogPost Schema #########
class BlogPostBase(BaseModel):
    title: str = Field(..., max_length=255)
    content: str
    excerpt: Optional[str] = Field(None, max_length=200)
    tags: Optional[List[str]] = Field(default_factory=list)
    status: PostStatus = PostStatus.DRAFT
    category: Optional[str] = Field(None, max_length=255)
    author_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    
    model_config = {
        "use_enum_values": True,
        "from_attributes": True,  # Replaces orm_mode=True
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }

class BlogPostCreate(BlogPostBase):
    pass

class BlogPostUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    excerpt: Optional[str] = Field(None, max_length=200)
    tags: Optional[List[str]] = None
    status: Optional[PostStatus] = None
    category: Optional[str] = Field(None, max_length=255)
    published_at: Optional[datetime] = None
    
    model_config = {
        "use_enum_values": True,
        "from_attributes": True,  # Replaces orm_mode=True
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }

class BlogPostResponse(BaseModel):
    """Response schema for BlogPost with ID"""
    id: int
    title: str
    content: str
    excerpt: Optional[str] = None
    tags: Optional[List[str]] = Field(default_factory=list)
    status: PostStatus
    category: Optional[str] = None
    author_id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    published_at: Optional[datetime] = None
    
    model_config = {
        "use_enum_values": True,
        "from_attributes": True,  # This allows conversion from SQLAlchemy models
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    } 

######### Comment Schema #########
class CommentBase(BaseModel):
    post_id: int
    author_id: int
    content: str
    created_at: Optional[datetime] = None
    approved: CommentApprovalStatus = CommentApprovalStatus.PENDING

    model_config = {
        "use_enum_values": True,
        "from_attributes": True,  # Replaces orm_mode=True
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }
class CommentCreate(CommentBase):
    pass
class CommentUpdate(BaseModel):
    content: Optional[str] = None
    approved: Optional[CommentApprovalStatus] = None

    model_config = {
        "use_enum_values": True,
        "from_attributes": True,  # Replaces orm_mode=True
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }

class CommentResponse(BaseModel):
    """Response schema for Comment with ID"""
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: Optional[datetime] = None
    approved: CommentApprovalStatus = CommentApprovalStatus.PENDING

    model_config = {
        "use_enum_values": True,
        "from_attributes": True,  # Replaces orm_mode=True
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }

######### Likes Schema #########
class LikesBase(BaseModel):
    post_id: int
    user_id: int
    created_at: Optional[datetime] = None

    model_config = {
        "use_enum_values": True,
        "from_attributes": True,  # Replaces orm_mode=True
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }
class LikesCreate(LikesBase):
    pass
class LikesUpdate(BaseModel):
    pass
    model_config = {
        "use_enum_values": True,
        "from_attributes": True,  # Replaces orm_mode=True
        "json_encoders": {
            datetime: lambda v: v.isoformat() if v else None
        }
    }
