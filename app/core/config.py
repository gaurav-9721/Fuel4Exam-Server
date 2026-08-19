"""
Configuration management for Fuel4Exam application
Uses Pydantic settings for type-safe configuration
"""
from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application
    app_name: str = "Fuel4Exam"
    app_version: str = "1.0.0"
    debug: bool = False
    environment: str = "production"
    
    # Database
    database_url: str
    
    # JWT Configuration
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # CORS
    allowed_origins: str = "http://localhost:3000,http://localhost:8000"
    
    # Email
    mail_from: str = "noreply@fuel4exam.com"
    mail_server: str = ""
    mail_port: int = 587
    mail_username: str = ""
    mail_password: str = ""

    # Logging
    log_level: str = "INFO"

    # Seed credentials are supplied only through the local environment.
    seed_candidate_password: str = ""
    
    class Config:
        env_file = ".env"
        case_sensitive = False
    
    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert comma-separated origins to list"""
        return [origin.strip() for origin in self.allowed_origins.split(",")]


settings = Settings()  # type: ignore
