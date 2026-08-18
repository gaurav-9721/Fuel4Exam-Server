"""
SQLAlchemy ORM Models for Fuel4Exam
Matches the existing database schema
"""
from app.db.session import Base
from sqlalchemy import Column, Integer, String, SmallInteger, BigInteger, DateTime, Boolean, Text, Date, UUID, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from uuid import uuid4


class Role(Base):
    """Role model - defines user roles in the system"""
    __tablename__ = "roles"
    
    role_id = Column(SmallInteger, primary_key=True, index=True)
    role_code = Column(String(50), unique=True, nullable=False, index=True)
    description = Column(String(255), nullable=True)
    
    # Relationships
    users = relationship("User", back_populates="role_obj")
    
    def __repr__(self):
        return f"<Role(role_id={self.role_id}, role_code={self.role_code})>"


class User(Base):
    """User model for authentication and system access"""
    __tablename__ = "users"
    
    user_id = Column(BigInteger, primary_key=True, index=True)
    public_id = Column(UUID(as_uuid=True), unique=True, nullable=False, default=uuid4, index=True)
    role_id = Column(SmallInteger, ForeignKey("roles.role_id"), nullable=False)
    
    full_name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone = Column(String(20), nullable=True)
    password_hash = Column(String(255), nullable=False)
    
    # Account status
    is_email_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    last_login_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    role_obj = relationship("Role", back_populates="users")
    profile = relationship("UserProfile", uselist=False, back_populates="user", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<User(user_id={self.user_id}, email={self.email}, full_name={self.full_name})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "user_id": self.user_id,
            "public_id": str(self.public_id),
            "full_name": self.full_name,
            "email": self.email,
            "phone": self.phone,
            "role_id": self.role_id,
            "is_email_verified": self.is_email_verified,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "last_login_at": self.last_login_at,
        }


class UserProfile(Base):
    """User profile model - extended profile information"""
    __tablename__ = "user_profiles"
    
    user_id = Column(BigInteger, ForeignKey("users.user_id"), primary_key=True)
    
    # Profile information
    city = Column(String(100), nullable=True)
    date_of_birth = Column(Date, nullable=True)
    avatar_url = Column(Text, nullable=True)
    bio = Column(Text, nullable=True)
    
    # Timestamps
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    # Relationships
    user = relationship("User", back_populates="profile")
    
    def __repr__(self):
        return f"<UserProfile(user_id={self.user_id}, city={self.city})>"
    
    def to_dict(self):
        """Convert model to dictionary"""
        return {
            "user_id": self.user_id,
            "city": self.city,
            "date_of_birth": self.date_of_birth,
            "avatar_url": self.avatar_url,
            "bio": self.bio,
            "updated_at": self.updated_at,
        }
