#!/usr/bin/env python3
"""
Quick test script to check bot connection
"""

import os
from telegram_bot import TelegramBot
from logger_config import setup_logger

logger = setup_logger()

def test_bot_connection():
    """Test bot connection and send a simple test message"""
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    channel_id = os.getenv("TELEGRAM_CHANNEL_ID")
    
    if not token or not channel_id:
        logger.error("Missing credentials")
        return False
    
    bot = TelegramBot(token, channel_id)
    
    # Test connection
    if bot.test_connection():
        logger.info("Bot connection successful!")
        
        # Send a test message
        test_message = "🤖 السلام عليكم! بوت المحتوى الإسلامي جاهز للعمل\n\n✅ تم تشغيل البوت بنجاح"
        if bot.send_message(test_message):
            logger.info("Test message sent successfully!")
            return True
        else:
            logger.error("Failed to send test message")
            return False
    else:
        logger.error("Bot connection failed")
        return False

if __name__ == "__main__":
    test_bot_connection()