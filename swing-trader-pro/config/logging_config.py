
import os
import logging
from logging.handlers import RotatingFileHandler
from typing import Optional

DEFAULT_LOG_FILE = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "logs", "swing_trader_pro.log"
)


def configure_logging(
    log_file: Optional[str] = None,
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5,
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
) -> logging.Logger:
    """
    Configure logging for the trading system.

    Args:
        log_file (str): Path to the log file.
        level (int): Logging level (e.g., logging.INFO).
        max_bytes (int): Maximum size of a log file before rotation.
        backup_count (int): Number of backup log files to keep.
        log_format (str): Log message format.

    Returns:
        logging.Logger: The configured root logger.
    """
    if log_file is None:
        log_file = DEFAULT_LOG_FILE

    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    # Remove all handlers associated with the root logger (avoid duplicate logs)
    root_logger = logging.getLogger()
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    handlers = [
        RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        ),
        logging.StreamHandler()
    ]

    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=handlers
    )

    logger = logging.getLogger()
    logger.info("Logging configured. Log file: %s", log_file)
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Returns a logger with the given name.
    """
    return logging.getLogger(name)
