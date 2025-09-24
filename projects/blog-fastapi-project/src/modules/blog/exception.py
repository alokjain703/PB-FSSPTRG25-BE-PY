class BlogException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    # Error Messages
    BLOG_NOT_FOUND = "Blog not found"
    BLOG_CREATION_FAILED = "Failed to create blog"
    BLOG_UPDATE_FAILED = "Failed to update blog"
    BLOG_DELETION_FAILED = "Failed to delete blog"
    INVALID_BLOG_DATA = "Invalid blog data provided"
    COMMENT_NOT_FOUND = "Comment not found"
    COMMENT_CREATION_FAILED = "Failed to create comment"
    COMMENT_UPDATE_FAILED = "Failed to update comment"
    COMMENT_DELETION_FAILED = "Failed to delete comment"
    INVALID_COMMENT_DATA = "Invalid comment data provided"
    UNAUTHORIZED_ACTION = "You are not authorized to perform this action"
    LIKE_ALREADY_EXISTS = "You have already liked this post"
    LIKE_CREATION_FAILED = "Failed to like the post"
    LIKE_DELETION_FAILED = "Failed to unlike the post"
    INVALID_LIKE_DATA = "Invalid like data provided"
    