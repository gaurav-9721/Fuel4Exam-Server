"""
Logging configuration
"""
import logging
import logging.config
from app.core.config import settings

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
        "detailed": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "detailed": {
            "formatter": "detailed",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "logs/fuel4exam.log",
            "maxBytes": 10485760,  # 10MB
            "backupCount": 5,
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO" if not settings.debug else "DEBUG",
        },
        "app": {
            "handlers": ["default", "detailed"],
            "level": "DEBUG" if settings.debug else "INFO",
            "propagate": False,
        },
    },
}


def setup_logging():
    """Configure logging"""
    logging.config.dictConfig(LOGGING_CONFIG)
    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured for {settings.environment} environment")
