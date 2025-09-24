
class AuthException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

    # Error Messages
    INVALID_CREDENTIALS = "Invalid username or password"
    USER_NOT_ACTIVE = "User account is disabled"
    TOKEN_EXPIRED = "Token has expired"
    TOKEN_INVALID = "Invalid token"
    UNAUTHORIZED_ACCESS = "Unauthorized access"
    FORBIDDEN_ACCESS = "Forbidden access"
    AUTHENTICATION_FAILED = "Authentication failed"
    AUTHORIZATION_FAILED = "Authorization failed"
    ROLE_ASSIGNMENT_FAILED = "Failed to assign role to user"
    ROLE_REMOVAL_FAILED = "Failed to remove role from user"
    PERMISSION_CHECK_FAILED = "Failed to check user permissions"
    