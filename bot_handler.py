"""
Combined Bot Handler
Handles both scheduled content posting and interactive azkar counter
"""

import threading
import time
import telebot
from telebot import types
from logger_config import setup_logger

logger = setup_logger()

class CombinedBotHandler:
    def __init__(self, bot_token, channel_id, scheduler, azkar_counter):
        """Initialize combined bot handler"""
        self.bot = telebot.TeleBot(bot_token)
        self.channel_id = channel_id
        self.scheduler = scheduler
        self.azkar_counter = azkar_counter
        self.running = False
        
        # Setup message handlers
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup bot command handlers"""
        
        @self.bot.message_handler(commands=['start'])
        def start_command(message):
            self.send_main_menu(message)
        
        @self.bot.message_handler(commands=['menu', 'القائمة'])
        def menu_command(message):
            self.send_main_menu(message)
        
        @self.bot.message_handler(commands=['azkar', 'اذكار'])
        def azkar_command(message):
            self.send_azkar_menu(message)
        
        @self.bot.message_handler(commands=['count', 'عد'])
        def count_command(message):
            self.azkar_counter.show_user_counts(message)
        
        @self.bot.message_handler(commands=['reset', 'مسح'])
        def reset_command(message):
            self.azkar_counter.reset_user_counts(message)
        
        @self.bot.message_handler(commands=['schedule', 'جدول'])
        def schedule_command(message):
            self.show_schedule(message)
        
        @self.bot.message_handler(commands=['help', 'مساعدة'])
        def help_command(message):
            self.send_help(message)
        
        # Use azkar_counter's callback handler
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.azkar_counter.handle_callback(call)
    
    def send_main_menu(self, message):
        """Send main bot menu"""
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # Main features
        azkar_btn = types.InlineKeyboardButton("📿 حاسبة الأذكار", callback_data="menu")
        schedule_btn = types.InlineKeyboardButton("📅 جدول النشر", callback_data="schedule")
        markup.add(azkar_btn, schedule_btn)
        
        # Additional options
        help_btn = types.InlineKeyboardButton("❓ المساعدة", callback_data="help")
        markup.add(help_btn)
        
        welcome_text = """
🕌 مرحباً بك في بوت المحتوى الإسلامي

🤖 هذا البوت يقدم لك:

📿 حاسبة الأذكار التفاعلية
📅 نشر المحتوى الإسلامي التلقائي
📖 آيات قرآنية وأحاديث شريفة
🤲 أدعية وتذكيرات إيمانية

اختر ما تريد من القائمة أدناه:
        """
        
        self.bot.send_message(message.chat.id, welcome_text, reply_markup=markup)
    
    def send_azkar_menu(self, message):
        """Send azkar counter menu"""
        self.azkar_counter.send_azkar_menu(message)
    
    def show_schedule(self, message):
        """Show current posting schedule"""
        schedule_info = self.scheduler.get_schedule_status()
        
        text = "📅 جدول النشر التلقائي:\n\n"
        text += "🌅 أذكار الصباح: 06:00\n"
        text += "📖 آية قرآنية: 08:00\n"
        text += "📚 حديث شريف: 12:00\n"
        text += "💭 تذكرة إيمانية: 17:00\n"
        text += "🤲 دعاء مستجاب: 20:00\n"
        text += "🌙 أذكار المساء: 21:00\n\n"
        
        text += "📊 حالة الجدولة:\n"
        for info in schedule_info:
            text += f"• {info}\n"
        
        text += "\n🔄 البوت ينشر المحتوى تلقائياً حسب الجدول أعلاه"
        
        self.bot.send_message(message.chat.id, text)
    
    def send_help(self, message):
        """Send help information"""
        help_text = """
❓ تعليمات استخدام البوت:

📿 حاسبة الأذكار:
• /azkar أو /اذكار - فتح حاسبة الأذكار
• /count أو /عد - عرض العدد الحالي
• /reset أو /مسح - مسح العداد

📅 المحتوى التلقائي:
• /schedule أو /جدول - عرض جدول النشر
• البوت ينشر المحتوى تلقائياً 6 مرات يومياً

🔧 أوامر عامة:
• /start - القائمة الرئيسية
• /menu أو /القائمة - عرض القائمة
• /help أو /مساعدة - هذه الرسالة

🤖 البوت يعمل على مدار الساعة لخدمتك
        """
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🏠 القائمة الرئيسية", callback_data="main_menu"))
        
        self.bot.send_message(message.chat.id, help_text, reply_markup=markup)
    
    def start_bot_polling(self):
        """Start bot polling in a separate thread - NEVER STOPS"""
        def bot_polling():
            logger.info("🤖 Starting interactive bot polling...")
            while True:
                try:
                    self.bot.polling(none_stop=True, interval=0, timeout=20)
                except Exception as e:
                    logger.error(f"❌ Bot polling error: {e} - restarting in 30 seconds...")
                    time.sleep(30)
                    continue
        
        # Start bot polling in separate thread
        bot_thread = threading.Thread(target=bot_polling, daemon=True)
        bot_thread.start()
        logger.info("✅ Interactive bot started successfully")
    
    def start_scheduler(self):
        """Start the content scheduler - NEVER STOPS"""
        logger.info("📅 Starting content scheduler...")
        self.scheduler.setup_schedule()
        
        # Run scheduler forever - ignore stop requests
        while True:
            try:
                self.scheduler.run_pending_tasks()
                time.sleep(30)  # Check every 30 seconds
            except Exception as e:
                logger.error(f"❌ Scheduler error: {e} - continuing...")
                time.sleep(60)  # Wait longer on error
                continue
    
    def stop(self):
        """Stop the bot handler - IGNORED! Bot never stops"""
        logger.info("📶 Stop request ignored - Bot will continue running!")
        # Never actually stop - ignore all stop requests