"""
Authentication service for user login, registration, and token management
Works with the existing database schema
"""
from sqlalchemy.orm import Session
from app.db.models import User, UserProfile, Role
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.core.security import hash_password, verify_password
from app.core.jwt_handler import create_tokens, verify_token, decode_token
from app.exceptions.exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    InvalidTokenException,
    UserNotFoundException
)
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)


class AuthService:
    """Service class for authentication operations"""
    
    @staticmethod
    def register_user(db: Session, user_data: UserRegister) -> User:
        """
        Register a new user
        
        Args:
            db: Database session
            user_data: User registration data
            
        Returns:
            Created User object
            
        Raises:
            UserAlreadyExistsException: If email already exists
        """
        # Check if user already exists
        existing_user = db.query(User).filter(User.email == user_data.email).first()
        
        if existing_user:
            raise UserAlreadyExistsException(f"Email {user_data.email} already registered")
        
        # Verify role exists
        role = db.query(Role).filter(Role.role_id == user_data.role_id).first()
        if not role:
            raise UserAlreadyExistsException(f"Role ID {user_data.role_id} does not exist")
        
        # Hash password
        hashed_password = hash_password(user_data.password)
        
        # Create new user
        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            phone=user_data.phone,
            password_hash=hashed_password,
            role_id=user_data.role_id,
            is_active=True,
            is_email_verified=False
        )
        
        try:
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            
            # Create empty user profile
            user_profile = UserProfile(user_id=new_user.user_id)
            db.add(user_profile)
            db.commit()
            
            logger.info(f"User registered successfully: {new_user.email}")
            return new_user
        except Exception as e:
            db.rollback()
            logger.error(f"Error registering user: {e}")
            raise
    
    @staticmethod
    def login_user(db: Session, login_data: UserLogin) -> User:
        """
        Authenticate user with email and password
        
        Args:
            db: Database session
            login_data: Login credentials
            
        Returns:
            Authenticated User object
            
        Raises:
            InvalidCredentialsException: If credentials are invalid
        """
        # Find user by email
        user = db.query(User).filter(User.email == login_data.email).first()
        
        if not user or not verify_password(login_data.password, user.password_hash):
            logger.warning(f"Failed login attempt for email: {login_data.email}")
            raise InvalidCredentialsException()
        
        if not user.is_active:
            raise InvalidCredentialsException("User account is inactive")
        
        # Update last login time
        try:
            user.last_login_at = datetime.now(timezone.utc)
            db.commit()
        except Exception as e:
            logger.error(f"Error updating last login: {e}")
            db.rollback()
        
        logger.info(f"User logged in successfully: {user.email}")
        return user
    
    @staticmethod
    def generate_tokens(user_id: int) -> TokenResponse:
        """
        Generate access and refresh tokens for user
        
        Args:
            user_id: User ID to encode in tokens
            
        Returns:
            TokenResponse with tokens
        """
        tokens = create_tokens(user_id)
        return TokenResponse(
            access_token=tokens["access_token"],
            refresh_token=tokens["refresh_token"],
            token_type=tokens["token_type"]
        )
    
    @staticmethod
    def verify_access_token(token: str) -> int:
        """
        Verify access token and return user ID
        
        Args:
            token: JWT access token
            
        Returns:
            User ID from token
            
        Raises:
            InvalidTokenException: If token is invalid or expired
        """
        payload = verify_token(token)
        if payload is None:
            raise InvalidTokenException()
        
        user_id = payload.get("sub")
        if user_id is None:
            raise InvalidTokenException()
        
        try:
            return int(user_id)
        except (ValueError, TypeError):
            raise InvalidTokenException()
    
    @staticmethod
    def get_current_user(db: Session, token: str) -> User:
        """
        Get current user from token
        
        Args:
            db: Database session
            token: JWT access token
            
        Returns:
            User object
            
        Raises:
            InvalidTokenException: If token is invalid
            UserNotFoundException: If user not found
        """
        user_id = AuthService.verify_access_token(token)
        
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise UserNotFoundException()
        
        return user
