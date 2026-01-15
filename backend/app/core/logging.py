"""
Logging configuration using Loguru.
"""

import sys
from pathlib import Path
from loguru import logger

from app.core.config import settings


def setup_logging():
    """Configure application logging."""
    
    # Remove default handler
    logger.remove()
    
    # Console logging
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level=settings.LOG_LEVEL,
        colorize=True,
    )
    
    # File logging
    log_path = Path(settings.LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        settings.LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=settings.LOG_LEVEL,
        rotation="1 day",  # Rotate daily
        retention="1 month",  # Keep logs for 1 month
        compression="zip",  # Compress rotated logs
        enqueue=True,  # Async logging
    )
    
    # Error logging to separate file
    error_log_path = log_path.parent / "error.log"
    logger.add(
        str(error_log_path),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="1 week",
        retention="1 month",
        compression="zip",
        enqueue=True,
    )
    
    logger.info(f"Logging configured - Level: {settings.LOG_LEVEL}")
    logger.info(f"Log file: {settings.LOG_FILE}")