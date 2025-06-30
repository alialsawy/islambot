#!/usr/bin/env python3
"""
Islamic Telegram Bot - Main Entry Point
Automated bot that generates and posts Islamic religious content throughout the day
"""

import os
import sys
import time
import signal
from datetime import datetime

from keep_alive import keep_alive
from logger_config import setup_logger
from bot_config import BotConfig
from scheduler import ContentScheduler
from telegram_bot import TelegramBot
from content_generator import IslamicContentGenerator
from azkar_counter import AzkarCounter
from bot_handler import CombinedBotHandler

# Setup logging
logger = setup_logger()

class IslamicTelegramBot:
    def __init__(self):
        """Initialize the Islamic Telegram Bot"""
        self.config = BotConfig()
        self.telegram_bot = TelegramBot(self.config.telegram_token, self.config.channel_id)
        self.content_generator = IslamicContentGenerator()
        self.scheduler = ContentScheduler(self.telegram_bot, self.content_generator)
        self.azkar_counter = AzkarCounter(self.config.telegram_token)
        self.bot_handler = CombinedBotHandler(
            self.config.telegram_token, 
            self.config.channel_id, 
            self.scheduler, 
            self.azkar_counter
        )
        self.running = False
        
    def start(self):
        """Start the bot with both scheduled content and interactive features - NEVER STOPS"""
        # Run forever - never give up, never shut down
        while True:
            try:
                logger.info("🤖 Starting Enhanced Islamic Telegram Bot...")
                
                # Validate configuration - retry if fails
                if not self.config.validate():
                    logger.error("❌ Configuration validation failed - retrying in 30 seconds...")
                    time.sleep(30)
                    continue
                
                # Test Telegram connection - retry if fails
                if not self.telegram_bot.test_connection():
                    logger.error("❌ Failed to connect to Telegram - retrying in 30 seconds...")
                    time.sleep(30)
                    continue
                
                # Test content generator - retry if fails
                if not self.content_generator.test_connection():
                    logger.error("❌ Failed to initialize content generator - retrying in 30 seconds...")
                    time.sleep(30)
                    continue
                
                # Setup signal handlers (but ignore shutdown signals)
                signal.signal(signal.SIGINT, self._signal_handler)
                signal.signal(signal.SIGTERM, self._signal_handler)
                
                logger.info("✅ Bot components initialized successfully!")
                logger.info("📅 Starting scheduled content posting...")
                logger.info("📿 Starting interactive azkar counter...")
                logger.info(f"📤 Channel: {self.config.channel_id}")
                
                # Send startup notification
                try:
                    startup_message = "سبحان الله"
                    self.telegram_bot.send_message(startup_message)
                except Exception as e:
                    logger.warning(f"⚠️ Could not send startup message: {e}")
                
                # Start interactive bot polling
                self.bot_handler.start_bot_polling()
                
                # Start scheduler (runs in main thread)
                self.bot_handler.start_scheduler()
                
                # If we reach here, something stopped the scheduler - restart
                logger.error("❌ Scheduler stopped unexpectedly - restarting in 10 seconds...")
                time.sleep(10)
                
            except Exception as e:
                logger.error(f"❌ Error in main bot loop: {e} - restarting in 30 seconds...")
                time.sleep(30)
                continue
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals - BUT NEVER ACTUALLY SHUTDOWN"""
        logger.info(f"📶 Received signal {signum} - IGNORING shutdown request! Bot will keep running...")
        # Completely ignore shutdown signals - bot must never stop!

def main():
    """Main entry point - NEVER STOPS"""
    # Start the keep alive server
    keep_alive()
    
    # Run forever - never exit under any circumstances
    while True:
        try:
            # Start the Islamic bot
            bot = IslamicTelegramBot()
            bot.start()  # This will also run forever
        except KeyboardInterrupt:
            logger.info("📶 Ignoring keyboard interrupt - Bot will continue running!")
            time.sleep(5)
            continue
        except Exception as e:
            logger.error(f"❌ Unexpected error: {e} - restarting in 30 seconds...")
            time.sleep(30)
            continue

if __name__ == "__main__":
    main()