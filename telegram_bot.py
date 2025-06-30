"""
Telegram Bot Handler
Manages communication with Telegram API
"""

import time
import telebot
from telebot.apihelper import ApiTelegramException
from logger_config import setup_logger

logger = setup_logger()

class TelegramBot:
    def __init__(self, token, channel_id):
        """Initialize Telegram bot with token and channel ID"""
        self.bot = telebot.TeleBot(token)
        self.channel_id = channel_id
        self.retry_attempts = 3
        self.retry_delay = 60
    
    def test_connection(self):
        """Test Telegram bot connection"""
        try:
            logger.info("🔍 Testing Telegram bot connection...")
            
            # Test bot connection
            bot_info = self.bot.get_me()
            logger.info(f"✅ Connected to Telegram bot: @{bot_info.username}")
            
            # Test channel access by getting chat info
            try:
                chat_info = self.bot.get_chat(self.channel_id)
                logger.info(f"✅ Channel access confirmed: {getattr(chat_info, 'title', self.channel_id)}")
                return True
            except ApiTelegramException as e:
                if "chat not found" in str(e).lower():
                    logger.error(f"❌ Channel {self.channel_id} not found")
                elif "bot was blocked" in str(e).lower():
                    logger.error(f"❌ Bot was blocked by the channel {self.channel_id}")
                else:
                    logger.error(f"❌ Cannot access channel {self.channel_id}: {e}")
                logger.error("💡 Make sure the bot is added as an administrator to the channel")
                return False
                
        except ApiTelegramException as e:
            logger.error(f"❌ Telegram bot connection failed: {e}")
            return False
        except Exception as e:
            logger.error(f"❌ Unexpected error testing connection: {e}")
            return False
    
    def send_message(self, message, retry_count=0):
        """Send message to the configured channel with retry logic"""
        try:
            logger.info(f"📤 Sending message to {self.channel_id}...")
            
            # Split long messages if needed
            if len(message) > 4096:
                message = message[:4090] + "..."
                logger.warning("⚠️ Message truncated to fit Telegram limit")
            
            self.bot.send_message(
                chat_id=self.channel_id,
                text=message,
                parse_mode='HTML',
                disable_web_page_preview=True
            )
            
            logger.info("✅ Message sent successfully")
            return True
            
        except ApiTelegramException as e:
            error_msg = str(e).lower()
            
            # Handle rate limiting
            if "too many requests" in error_msg:
                wait_time = 60  # Default wait time
                logger.warning(f"⏳ Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                
                if retry_count < self.retry_attempts:
                    return self.send_message(message, retry_count + 1)
                else:
                    logger.error("❌ Failed to send message after rate limit retries")
                    return False
            
            # Handle timeout
            elif "timeout" in error_msg:
                logger.warning(f"⏰ Request timed out: {e}")
                
                if retry_count < self.retry_attempts:
                    logger.info(f"🔄 Retrying... Attempt {retry_count + 1}/{self.retry_attempts}")
                    time.sleep(self.retry_delay)
                    return self.send_message(message, retry_count + 1)
                else:
                    logger.error("❌ Failed to send message after timeout retries")
                    return False
            
            # Handle critical errors
            elif "chat not found" in error_msg or "bot was blocked" in error_msg:
                logger.error("💀 Critical Telegram error - not retrying")
                return False
            
            # Handle other errors with retry
            else:
                logger.error(f"❌ Telegram error while sending message: {e}")
                
                if retry_count < self.retry_attempts:
                    logger.info(f"🔄 Retrying... Attempt {retry_count + 1}/{self.retry_attempts}")
                    time.sleep(self.retry_delay)
                    return self.send_message(message, retry_count + 1)
                else:
                    logger.error("❌ Failed to send message after all retries")
                    return False
                
        except Exception as e:
            logger.error(f"❌ Unexpected error while sending message: {e}")
            return False
    
    def send_formatted_content(self, content_type, content):
        """Send formatted content with appropriate emojis and formatting"""
        if not content:
            logger.error("❌ Cannot send empty content")
            return False
        
        # Add content type specific formatting
        emoji_map = {
            "morning_azkar": "🌅",
            "evening_azkar": "🌙",
            "quran_verse": "📖",
            "daily_hadith": "📚",
            "daily_dua": "🤲",
            "daily_reminder": "💭"
        }
        
        emoji = emoji_map.get(content_type, "🕌")
        
        # Format the message
        formatted_message = f"{emoji} <b>{self._get_content_title(content_type)}</b>\n\n{content}"
        
        return self.send_message(formatted_message)
    
    def _get_content_title(self, content_type):
        """Get Arabic title for content type"""
        titles = {
            "morning_azkar": "أذكار الصباح",
            "evening_azkar": "أذكار المساء",
            "quran_verse": "آية من القرآن الكريم",
            "daily_hadith": "حديث شريف",
            "daily_dua": "دعاء مستجاب",
            "daily_reminder": "تذكرة إيمانية"
        }
        return titles.get(content_type, "محتوى إسلامي")
    
    def get_bot_info(self):
        """Get bot information"""
        try:
            return self.bot.get_me()
        except ApiTelegramException as e:
            logger.error(f"❌ Error getting bot info: {e}")
            return None
