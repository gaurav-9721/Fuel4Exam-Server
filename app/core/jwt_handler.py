"""
JWT token generation and validation
"""
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from typing import Optional, Dict, Any
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)


class TokenData:
    """Token payload data"""
    def __init__(self, sub: str, exp: datetime):
        self.sub = sub  # User ID or username
        self.exp = exp


def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create JWT access token
    
    Args:
        data: Payload data to encode in token
        expires_delta: Custom expiration time delta
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    return encoded_jwt


def create_refresh_token(data: Dict[str, Any]) -> str:
    """
    Create JWT refresh token with longer expiration
    
    Args:
        data: Payload data to encode in token
        
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(
        days=settings.refresh_token_expire_days
    )
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[Dict[str, Any]]:
    """
    Verify and decode JWT token
    
    Args:
        token: JWT token string to verify
        
    Returns:
        Token payload dictionary if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError as e:
        logger.warning(f"Invalid token: {e}")
        return None


def decode_token(token: str) -> Optional[str]:
    """
    Decode token and return the subject (usually user_id)
    
    Args:
        token: JWT token string
        
    Returns:
        Subject from token if valid, None otherwise
    """
    payload = verify_token(token)
    if payload is None:
        return None
    
    sub: str = payload.get("sub")
    if sub is None:
        return None
    
    return sub


def create_tokens(user_id: int) -> Dict[str, str]:
    """
    Create both access and refresh tokens for a user
    
    Args:
        user_id: User ID to encode in tokens
        
    Returns:
        Dictionary with access_token and refresh_token
    """
    access_token = create_access_token(data={"sub": str(user_id)})
    refresh_token = create_refresh_token(data={"sub": str(user_id)})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
