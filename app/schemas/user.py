"""
Pydantic schemas for request/response validation
Matches the existing database schema
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime, date
from uuid import UUID


# ==================== Role Schemas ====================

class RoleResponse(BaseModel):
    """Schema for role response"""
    role_id: int
    role_code: str
    description: Optional[str]
    
    class Config:
        from_attributes = True


# ==================== User Schemas ====================

class UserRegister(BaseModel):
    """Schema for user registration"""
    full_name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=72)
    phone: Optional[str] = Field(None, max_length=20)
    
    @field_validator('full_name')
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Full name cannot be empty')
        return v


class UserLogin(BaseModel):
    """Schema for user login"""
    email: EmailStr
    password: str = Field(..., min_length=1)


class PasswordReset(BaseModel):
    """Schema for password reset"""
    current_password: str = Field(..., min_length=1)
    new_password: str = Field(..., min_length=8)
    confirm_password: str = Field(..., min_length=8)


# ==================== Token Schemas ====================

class TokenResponse(BaseModel):
    """Schema for token response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 30  # minutes


class RefreshTokenRequest(BaseModel):
    """Schema for token refresh request"""
    refresh_token: str


# ==================== User Profile Schemas ====================

class UserProfileUpdate(BaseModel):
    """Schema for user profile update"""
    city: Optional[str] = Field(None, max_length=100)
    date_of_birth: Optional[date] = None
    avatar_url: Optional[str] = None
    bio: Optional[str] = Field(None, max_length=1000)


class UserProfileResponse(BaseModel):
    """Schema for user profile response"""
    user_id: int
    city: Optional[str]
    date_of_birth: Optional[date]
    avatar_url: Optional[str]
    bio: Optional[str]
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== User Response Schemas ====================

class UserResponse(BaseModel):
    """Schema for user response (without sensitive data)"""
    user_id: int
    public_id: UUID
    full_name: str
    email: str
    phone: Optional[str]
    role_id: int
    is_email_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


class UserDetailResponse(BaseModel):
    """Schema for detailed user response with profile"""
    user_id: int
    public_id: UUID
    full_name: str
    email: str
    phone: Optional[str]
    role_id: int
    is_email_verified: bool
    is_active: bool
    is_email_verified: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    
    # Profile information
    city: Optional[str]
    date_of_birth: Optional[date]
    avatar_url: Optional[str]
    bio: Optional[str]
    profile_updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class UserFullProfile(BaseModel):
    """Schema for complete user profile"""
    user_id: int
    public_id: UUID
    full_name: str
    email: str
    phone: Optional[str]
    role_id: int
    is_email_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime
    last_login_at: Optional[datetime]
    
    # Profile details
    profile: Optional[UserProfileResponse] = None
    
    class Config:
        from_attributes = True


# ==================== Authentication Response ====================

class AuthResponse(BaseModel):
    """Schema for authentication response"""
    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse


class MessageResponse(BaseModel):
    """Schema for simple message response"""
    message: str
    success: bool = True


class ErrorResponse(BaseModel):
    """Schema for error response"""
    error: str
    detail: Optional[str] = None
    status_code: int
