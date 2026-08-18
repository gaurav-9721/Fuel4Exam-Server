"""
Main FastAPI application entry point
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
import sys
import os

# Add app to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings
from app.db.session import init_db, Base, engine
from app.api.v1.api import api_router
from app.exceptions.exceptions import Fuel4ExamException
from app.utils.logging import setup_logging

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    description="Production-grade exam preparation backend API",
    version=settings.app_version,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)

# Setup CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


# Exception handlers
@app.exception_handler(Fuel4ExamException)
async def fuel4exam_exception_handler(request: Request, exc: Fuel4ExamException):
    """Handle custom Fuel4Exam exceptions"""
    logger.error(f"Fuel4Exam exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "detail": exc.message,
            "status_code": exc.status_code,
        },
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "InternalServerError",
            "detail": "An unexpected error occurred",
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
        },
    )


# Include routers
app.include_router(api_router)


# Health check endpoint
@app.get(
    "/health",
    status_code=status.HTTP_200_OK,
    tags=["Health"],
    summary="Health check endpoint"
)
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "service": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }


# Root endpoint
@app.get(
    "/",
    status_code=status.HTTP_200_OK,
    tags=["Root"],
    summary="API root endpoint"
)
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": f"Welcome to {settings.app_name} API",
        "version": settings.app_version,
        "docs": "/api/docs",
        "redoc": "/api/redoc",
    }


# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize database and run startup tasks"""
    try:
        logger.info(f"Starting {settings.app_name} v{settings.app_version}")
        logger.info(f"Environment: {settings.environment}")
        
        # Initialize database
        init_db()
        logger.info("Database initialized successfully")
        
        logger.info("Application started successfully")
    except Exception as e:
        logger.error(f"Startup error: {e}", exc_info=True)
        raise


# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run shutdown tasks"""
    logger.info(f"Shutting down {settings.app_name}")


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=settings.debug,
    )
