"""
Custom exceptions for Fuel4Exam application
"""


class Fuel4ExamException(Exception):
    """Base exception for all Fuel4Exam exceptions"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationException(Fuel4ExamException):
    """Raised when authentication fails"""
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, status_code=401)


class AuthorizationException(Fuel4ExamException):
    """Raised when user lacks required permissions"""
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, status_code=403)


class UserNotFoundException(Fuel4ExamException):
    """Raised when user is not found"""
    def __init__(self, message: str = "User not found"):
        super().__init__(message, status_code=404)


class UserAlreadyExistsException(Fuel4ExamException):
    """Raised when trying to create user that already exists"""
    def __init__(self, message: str = "User already exists"):
        super().__init__(message, status_code=409)


class InvalidCredentialsException(Fuel4ExamException):
    """Raised when invalid credentials are provided"""
    def __init__(self, message: str = "Invalid email or password"):
        super().__init__(message, status_code=401)


class InvalidTokenException(Fuel4ExamException):
    """Raised when token is invalid or expired"""
    def __init__(self, message: str = "Invalid or expired token"):
        super().__init__(message, status_code=401)


class ValidationException(Fuel4ExamException):
    """Raised when validation fails"""
    def __init__(self, message: str = "Validation error"):
        super().__init__(message, status_code=422)


class DatabaseException(Fuel4ExamException):
    """Raised when database operation fails"""
    def __init__(self, message: str = "Database error"):
        super().__init__(message, status_code=500)
