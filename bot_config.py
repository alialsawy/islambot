"""
Bot Configuration
Handles environment variables and configuration validation
"""

import os
from logger_config import setup_logger

logger = setup_logger()

class BotConfig:
    def __init__(self):
        """Initialize configuration from environment variables"""
        # Only Telegram credentials needed - no OpenAI API key required
        self.telegram_token = os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.channel_id = os.getenv("TELEGRAM_CHANNEL_ID", "")
        
        # Optional configurations with defaults
        self.max_content_length = int(os.getenv("MAX_CONTENT_LENGTH", "500"))
        self.content_temperature = float(os.getenv("CONTENT_TEMPERATURE", "0.8"))
        self.retry_attempts = int(os.getenv("RETRY_ATTEMPTS", "3"))
        self.retry_delay = int(os.getenv("RETRY_DELAY", "60"))
        
        # Schedule configuration (24-hour format)
        self.schedule_config = {
            "morning_azkar": os.getenv("MORNING_AZKAR_TIME", "06:00"),
            "quran_verse": os.getenv("QURAN_VERSE_TIME", "08:00"),
            "daily_hadith": os.getenv("DAILY_HADITH_TIME", "12:00"),
            "religious_post": os.getenv("RELIGIOUS_POST_TIME", "14:00"),
            "daily_reminder": os.getenv("DAILY_REMINDER_TIME", "17:00"),
            "companion_story": os.getenv("COMPANION_STORY_TIME", "19:00"),
            "daily_dua": os.getenv("DAILY_DUA_TIME", "20:00"),
            "evening_azkar": os.getenv("EVENING_AZKAR_TIME", "21:00")
        }
    
    def validate(self):
        """Validate required configuration"""
        required_vars = [
            ("TELEGRAM_BOT_TOKEN", self.telegram_token),
            ("TELEGRAM_CHANNEL_ID", self.channel_id)
        ]
        
        missing_vars = []
        for var_name, var_value in required_vars:
            if not var_value.strip():
                missing_vars.append(var_name)
        
        if missing_vars:
            logger.error(f"❌ Missing required environment variables: {', '.join(missing_vars)}")
            logger.error("📝 Please set the following environment variables:")
            for var in missing_vars:
                logger.error(f"   export {var}='your_value_here'")
            return False
        
        # Validate channel ID format
        if not (self.channel_id.startswith('@') or self.channel_id.startswith('-')):
            logger.error("❌ TELEGRAM_CHANNEL_ID must start with '@' (for public channels) or '-' (for private channels)")
            return False
        
        logger.info("✅ Configuration validation successful")
        return True
    
    def get_schedule_times(self):
        """Get the schedule configuration"""
        return self.schedule_config
    
    def log_config(self):
        """Log current configuration (without sensitive data)"""
        logger.info("📋 Current Configuration:")
        logger.info(f"   Channel ID: {self.channel_id}")
        logger.info(f"   Max Content Length: {self.max_content_length}")
        logger.info(f"   Content Temperature: {self.content_temperature}")
        logger.info(f"   Retry Attempts: {self.retry_attempts}")
        logger.info(f"   Schedule Times: {self.schedule_config}")
