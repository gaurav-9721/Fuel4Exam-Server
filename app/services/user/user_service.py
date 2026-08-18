"""
User profile service for profile updates and retrieval
Works with the existing database schema (User and UserProfile tables)
"""
from sqlalchemy.orm import Session
from app.db.models import User, UserProfile
from app.schemas.user import UserProfileUpdate, UserDetailResponse
from app.exceptions.exceptions import UserNotFoundException, DatabaseException
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


class UserService:
    """Service class for user profile operations"""
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """
        Get user by ID
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User object
            
        Raises:
            UserNotFoundException: If user not found
        """
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise UserNotFoundException(f"User with ID {user_id} not found")
        return user
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """
        Get user by email
        
        Args:
            db: Database session
            email: User email
            
        Returns:
            User object
            
        Raises:
            UserNotFoundException: If user not found
        """
        user = db.query(User).filter(User.email == email).first()
        if not user:
            raise UserNotFoundException(f"User with email {email} not found")
        return user
    
    @staticmethod
    def get_user_profile(db: Session, user_id: int) -> dict:
        """
        Get user profile with details
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            User profile dictionary
        """
        user = UserService.get_user_by_id(db, user_id)
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        
        return {
            "user_id": user.user_id,
            "public_id": str(user.public_id),
            "full_name": user.full_name,
            "email": user.email,
            "phone": user.phone,
            "role_id": user.role_id,
            "is_email_verified": user.is_email_verified,
            "is_active": user.is_active,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "last_login_at": user.last_login_at,
            # Profile details
            "city": profile.city if profile else None,
            "date_of_birth": profile.date_of_birth if profile else None,
            "avatar_url": profile.avatar_url if profile else None,
            "bio": profile.bio if profile else None,
            "profile_updated_at": profile.updated_at if profile else None,
        }
    
    @staticmethod
    def update_user_profile(
        db: Session,
        user_id: int,
        profile_data: UserProfileUpdate
    ) -> User:
        """
        Update user profile
        
        Args:
            db: Database session
            user_id: User ID to update
            profile_data: Updated profile data
            
        Returns:
            Updated User object
            
        Raises:
            UserNotFoundException: If user not found
            DatabaseException: If update fails
        """
        user = UserService.get_user_by_id(db, user_id)
        
        # Get or create user profile
        profile = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
        if not profile:
            profile = UserProfile(user_id=user_id)
            db.add(profile)
        
        try:
            # Update profile fields
            update_data = profile_data.model_dump(exclude_unset=True)
            for key, value in update_data.items():
                if value is not None:
                    setattr(profile, key, value)
            
            profile.updated_at = datetime.now(timezone.utc)
            user.updated_at = datetime.now(timezone.utc)
            
            db.commit()
            db.refresh(user)
            logger.info(f"User profile updated: {user.email}")
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating user profile: {e}")
            raise DatabaseException(f"Failed to update profile: {str(e)}")
    
    @staticmethod
    def deactivate_user(db: Session, user_id: int) -> User:
        """
        Deactivate user account
        
        Args:
            db: Database session
            user_id: User ID to deactivate
            
        Returns:
            Updated User object
            
        Raises:
            UserNotFoundException: If user not found
            DatabaseException: If update fails
        """
        user = UserService.get_user_by_id(db, user_id)
        
        try:
            user.is_active = False
            user.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user)
            logger.info(f"User deactivated: {user.email}")
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Error deactivating user: {e}")
            raise DatabaseException(f"Failed to deactivate user: {str(e)}")
    
    @staticmethod
    def activate_user(db: Session, user_id: int) -> User:
        """
        Activate user account
        
        Args:
            db: Database session
            user_id: User ID to activate
            
        Returns:
            Updated User object
            
        Raises:
            UserNotFoundException: If user not found
            DatabaseException: If update fails
        """
        user = UserService.get_user_by_id(db, user_id)
        
        try:
            user.is_active = True
            user.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user)
            logger.info(f"User activated: {user.email}")
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Error activating user: {e}")
            raise DatabaseException(f"Failed to activate user: {str(e)}")
    
    @staticmethod
    def verify_email(db: Session, user_id: int) -> User:
        """
        Mark email as verified
        
        Args:
            db: Database session
            user_id: User ID
            
        Returns:
            Updated User object
        """
        user = UserService.get_user_by_id(db, user_id)
        
        try:
            user.is_email_verified = True
            user.updated_at = datetime.now(timezone.utc)
            db.commit()
            db.refresh(user)
            logger.info(f"Email verified for user: {user.email}")
            return user
        except Exception as e:
            db.rollback()
            logger.error(f"Error verifying email: {e}")
            raise DatabaseException(f"Failed to verify email: {str(e)}")
