"""
Logging Configuration
Centralized logging setup for the Islamic Telegram Bot
"""

import logging
import sys
from datetime import datetime
import os

def setup_logger(name="IslamicBot", level=logging.INFO):
    """Setup centralized logger with proper formatting"""
    
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid duplicate handlers
    if logger.handlers:
        return logger
    
    # Create formatters
    detailed_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    simple_formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(simple_formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional - only if LOG_FILE is set)
    log_file = os.getenv("LOG_FILE")
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(detailed_formatter)
            logger.addHandler(file_handler)
            logger.info(f"📝 Logging to file: {log_file}")
        except Exception as e:
            logger.warning(f"⚠️ Could not setup file logging: {e}")
    
    # Set third-party loggers to WARNING to reduce noise
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("telegram").setLevel(logging.WARNING)
    logging.getLogger("openai").setLevel(logging.WARNING)
    
    # Initial log message
    logger.info("🚀 Islamic Telegram Bot Logger initialized")
    
    return logger

def log_system_info():
    """Log system information for debugging"""
    logger = setup_logger()
    
    logger.info("📊 System Information:")
    logger.info(f"   Python Version: {sys.version}")
    logger.info(f"   Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info(f"   Working Directory: {os.getcwd()}")
    
    # Log environment variables (without sensitive data)
    env_vars = ["TELEGRAM_CHANNEL_ID", "MAX_CONTENT_LENGTH", "CONTENT_TEMPERATURE"]
    for var in env_vars:
        value = os.getenv(var, "Not Set")
        logger.info(f"   {var}: {value}")

if __name__ == "__main__":
    # Test the logger
    logger = setup_logger()
    log_system_info()
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
