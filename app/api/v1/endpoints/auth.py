"""
Authentication endpoints - Login, Register, Refresh Token
Works with the existing database schema
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import (
    UserRegister,
    UserLogin,
    AuthResponse,
    UserResponse,
    TokenResponse,
    RefreshTokenRequest,
    MessageResponse
)
from app.services.auth.auth_service import AuthService
from app.services.user.user_service import UserService
from app.exceptions.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    InvalidTokenException,
    UserNotFoundException,
    Fuel4ExamException
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    responses={
        201: {"description": "User registered successfully"},
        409: {"description": "User already exists"},
        422: {"description": "Validation error"},
    }
)
def register(
    user_data: UserRegister,
    db: Session = Depends(get_db)
):
    """
    Register a new user account
    
    - **full_name**: User's full name
    - **email**: User email address (must be unique)
    - **password**: User password (minimum 8 characters)
    - **phone**: User phone number (optional)
    - New accounts are assigned the candidate role automatically
    """
    try:
        # Register user
        user = AuthService.register_user(db, user_data)
        
        # Tokens are issued only after an explicit login.
        return UserResponse.model_validate(user)
    except UserAlreadyExistsException as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message
        )
    except Exception as e:
        logger.error(f"Registration error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Registration failed"
        )


@router.post(
    "/login",
    response_model=AuthResponse,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    responses={
        200: {"description": "Login successful"},
        401: {"description": "Invalid credentials"},
    }
)
def login(
    login_data: UserLogin,
    db: Session = Depends(get_db)
):
    """
    Login with email and password
    
    - **email**: User email address
    - **password**: User password
    """
    try:
        # Authenticate user
        user = AuthService.login_user(db, login_data)
        
        # Generate tokens
        tokens = AuthService.generate_tokens(user.user_id)
        
        # Build response
        return AuthResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type,
            user=UserResponse.model_validate(user)
        )
    except InvalidCredentialsException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Login failed"
        )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Refresh access token",
    responses={
        200: {"description": "Token refreshed successfully"},
        401: {"description": "Invalid refresh token"},
    }
)
def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    
    - **refresh_token**: Valid refresh token
    """
    try:
        # Verify refresh token
        payload = AuthService.verify_access_token(request.refresh_token)
        
        # Generate new tokens
        tokens = AuthService.generate_tokens(payload)
        
        return TokenResponse(
            access_token=tokens.access_token,
            refresh_token=tokens.refresh_token,
            token_type=tokens.token_type
        )
    except InvalidTokenException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Token refresh error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )
