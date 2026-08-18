"""
API v1 router - Aggregates all v1 endpoints
"""
from fastapi import APIRouter
from app.api.v1.endpoints import auth, users

# Create API v1 router
api_router = APIRouter(prefix="/api/v1")

# Include endpoint routers
api_router.include_router(auth.router)
api_router.include_router(users.router)

__all__ = ["api_router"]
