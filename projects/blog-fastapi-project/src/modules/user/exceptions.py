# User module related Custom Exceptions and Error Messages
from fastapi import HTTPException as HttpException

class UserException(HttpException):
    def __init__(self, status_code: int, detail: str = "An error occurred"):
        self.status_code = status_code
        self.detail = detail
        super().__init__(status_code=self.status_code, detail=self.detail)

    # Error Messages
    USER_NOT_FOUND = "User not found"
    USER_ALREADY_EXISTS = "User already exists"
    INVALID_USER_DATA = "Invalid user data provided"
    USER_CREATION_FAILED = "Failed to create user"
    USER_UPDATE_FAILED = "Failed to update user"
    USER_DELETION_FAILED = "Failed to delete user"  
    USER_SERVICE_ERROR = "User service error"
    