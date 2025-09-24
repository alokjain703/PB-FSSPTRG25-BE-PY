# Define enums
from enum import Enum

class PostStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    PENDING_REVIEW = "pending_review"

class CommentApprovalStatus(int, Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2