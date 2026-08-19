"""
User profile endpoints - Get, Update, Deactivate
Works with the existing database schema
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.user import (
    UserResponse,
    UserProfileUpdate,
    MessageResponse
)
from app.services.auth.auth_service import AuthService
from app.services.user.user_service import UserService
from app.exceptions.exceptions import (
    UserNotFoundException,
    InvalidTokenException,
    DatabaseException
)
from typing import Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["User Profile"])
security = HTTPBearer(auto_error=False)


def get_current_user_from_header(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Dependency to extract and validate user from Authorization header
    """
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authorization header",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        user = AuthService.get_current_user(db, credentials.credentials)
        return user
    except InvalidTokenException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )


@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Get current user profile",
    responses={
        200: {"description": "User profile retrieved successfully"},
        401: {"description": "Unauthorized"},
    }
)
def get_my_profile(
    current_user = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user's profile with all details
    
    Requires valid access token in Authorization header: `Bearer <token>`
    """
    try:
        profile = UserService.get_user_profile(db, current_user.user_id)
        return profile
    except UserNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    except Exception as e:
        logger.error(f"Get profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve profile"
        )


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Get user profile by ID",
    responses={
        200: {"description": "User profile retrieved successfully"},
        404: {"description": "User not found"},
    }
)
def get_user_profile(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Get user profile by user ID (public endpoint)
    
    - **user_id**: User ID to retrieve
    """
    try:
        profile = UserService.get_user_profile(db, user_id)
        return profile
    except UserNotFoundException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except Exception as e:
        logger.error(f"Get user profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )


@router.put(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Update current user profile",
    responses={
        200: {"description": "Profile updated successfully"},
        401: {"description": "Unauthorized"},
    }
)
def update_my_profile(
    profile_data: UserProfileUpdate,
    current_user = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """
    Update current authenticated user's profile
    
    Requires valid access token in Authorization header
    
    - **city**: City name (optional)
    - **date_of_birth**: Date of birth (optional)
    - **avatar_url**: Avatar picture URL (optional)
    - **bio**: User bio (optional)
    """
    try:
        updated_user = UserService.update_user_profile(
            db,
            current_user.user_id,
            profile_data
        )
        profile = UserService.get_user_profile(db, updated_user.user_id)
        return profile
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
    except Exception as e:
        logger.error(f"Update profile error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update profile"
        )


@router.post(
    "/me/deactivate",
    response_model=MessageResponse,
    status_code=status.HTTP_200_OK,
    summary="Deactivate current user account",
    responses={
        200: {"description": "Account deactivated successfully"},
        401: {"description": "Unauthorized"},
    }
)
def deactivate_account(
    current_user = Depends(get_current_user_from_header),
    db: Session = Depends(get_db)
):
    """
    Deactivate current user's account
    
    Requires valid access token in Authorization header
    """
    try:
        UserService.deactivate_user(db, current_user.user_id)
        return MessageResponse(
            message="Account deactivated successfully",
            success=True
        )
    except DatabaseException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e.message
        )
    except Exception as e:
        logger.error(f"Deactivate account error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to deactivate account"
        )
