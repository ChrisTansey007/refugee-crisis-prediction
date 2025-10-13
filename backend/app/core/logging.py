import logging
import sys
from pythonjsonlogger import jsonlogger
from app.core.config import settings

def setup_logging():
    """Configure JSON logging for the application."""
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    # Create logger
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Remove existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    # JSON formatter
    formatter = jsonlogger.JsonFormatter(
        "%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optionally add file handler later if needed
    # file_handler = logging.FileHandler("app.log")
    # file_handler.setFormatter(formatter)
    # logger.addHandler(file_handler)
