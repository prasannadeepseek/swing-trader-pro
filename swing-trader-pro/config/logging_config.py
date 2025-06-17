from typing import Optional
import os
import logging
from logging.handlers import RotatingFileHandler


def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            RotatingFileHandler(
                'logs/trading_system.log',
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5
            ),
            logging.StreamHandler()
        ]
    )

# method 3 final version


def configure_logging(
    log_file: str = 'logs/trading_system.log',
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,
    backup_count: int = 5
) -> logging.Logger:
    """
    Configure logging for the trading system.

    Args:
        log_file (str): Path to the log file.
        level (int): Logging level (e.g., logging.INFO).
        max_bytes (int): Maximum size of a log file before rotation.
        backup_count (int): Number of backup log files to keep.

    Returns:
        logging.Logger: The configured root logger.
    """
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

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
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=handlers
    )

    logger = logging.getLogger()
    logger.info("Logging configured. Log file: %s", log_file)
    return logger
