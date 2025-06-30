"""
Azkar Counter Bot
Interactive Telegram bot with counting buttons for Islamic remembrances
"""

import telebot
from telebot import types
import json
import os
import time
from logger_config import setup_logger

logger = setup_logger()

class AzkarCounter:
    def __init__(self, bot_token):
        """Initialize the azkar counter bot"""
        self.bot = telebot.TeleBot(bot_token)
        self.user_counts = {}  # Store user counting data
        
        # Azkar types with their Arabic names and recommended counts
        self.azkar_types = {
            'subhan_allah': {
                'arabic': 'سبحان الله',
                'transliteration': 'Subhan Allah',
                'meaning': 'Glory be to Allah',
                'recommended': 33
            },
            'alhamdulillah': {
                'arabic': 'الحمد لله',
                'transliteration': 'Alhamdulillah',
                'meaning': 'All praise be to Allah',
                'recommended': 33
            },
            'allahu_akbar': {
                'arabic': 'الله أكبر',
                'transliteration': 'Allahu Akbar',
                'meaning': 'Allah is Greatest',
                'recommended': 34
            },
            'la_ilaha_illa_allah': {
                'arabic': 'لا إله إلا الله',
                'transliteration': 'La ilaha illa Allah',
                'meaning': 'There is no god but Allah',
                'recommended': 100
            },
            'astaghfirullah': {
                'arabic': 'أستغفر الله',
                'transliteration': 'Astaghfirullah',
                'meaning': 'I seek forgiveness from Allah',
                'recommended': 100
            },
            'salawat': {
                'arabic': 'اللهم صل وسلم على نبينا محمد',
                'transliteration': 'Allahumma salli wa sallim ala nabiyyina Muhammad',
                'meaning': 'O Allah, send prayers and peace upon our Prophet Muhammad',
                'recommended': 10
            }
        }
        
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup message and callback handlers"""
        
        @self.bot.message_handler(commands=['start'])
        def start_message(message):
            self.send_welcome(message)
        
        @self.bot.message_handler(commands=['azkar', 'اذكار'])
        def azkar_menu(message):
            self.send_azkar_menu(message)
        
        @self.bot.message_handler(commands=['count', 'عد'])
        def show_counts(message):
            self.show_user_counts(message)
        
        @self.bot.message_handler(commands=['reset', 'مسح'])
        def reset_counts(message):
            self.reset_user_counts(message)
        
        @self.bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call):
            self.handle_callback(call)
    
    def send_welcome(self, message):
        """Send welcome message with instructions"""
        welcome_text = """
🕌 مرحباً بك في حاسبة الأذكار الإسلامية

📿 هذا البوت يساعدك على عد الأذكار والتسبيحات بسهولة

🔹 /azkar أو /اذكار - قائمة الأذكار
🔹 /count أو /عد - عرض العدد الحالي
🔹 /reset أو /مسح - مسح العداد

✨ ابدأ بالضغط على /azkar لاختيار الذكر
        """
        self.bot.send_message(message.chat.id, welcome_text)
    
    def send_azkar_menu(self, message):
        """Send azkar selection menu"""
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        for key, azkar in self.azkar_types.items():
            button_text = f"📿 {azkar['arabic']} ({azkar['recommended']})"
            callback_data = f"select_{key}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        text = "🔹 اختر الذكر الذي تريد عده:\n\n"
        text += "الأرقام بين القوسين تشير للعدد المستحب"
        
        self.bot.send_message(message.chat.id, text, reply_markup=markup)
    
    def show_user_counts(self, message):
        """Show current user counts"""
        user_id = str(message.from_user.id)
        
        if user_id not in self.user_counts or not self.user_counts[user_id]:
            self.bot.send_message(message.chat.id, "📊 لم تبدأ العد بعد\n\nاستخدم /azkar لبدء العد")
            return
        
        text = "📊 عدادك الحالي:\n\n"
        
        for azkar_key, count in self.user_counts[user_id].items():
            if count > 0:
                azkar_info = self.azkar_types[azkar_key]
                progress = f"({count}/{azkar_info['recommended']})"
                text += f"📿 {azkar_info['arabic']}: {count} {progress}\n"
        
        self.bot.send_message(message.chat.id, text)
    
    def reset_user_counts(self, message):
        """Reset user counts"""
        user_id = str(message.from_user.id)
        self.user_counts[user_id] = {}
        
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔄 ابدأ العد مرة أخرى", callback_data="menu"))
        
        self.bot.send_message(
            message.chat.id, 
            "✅ تم مسح العداد بنجاح\n\n🔄 يمكنك البدء من جديد", 
            reply_markup=markup
        )
    
    def handle_callback(self, call):
        """Handle inline keyboard callbacks"""
        user_id = str(call.from_user.id)
        
        # Initialize user data if doesn't exist
        if user_id not in self.user_counts:
            self.user_counts[user_id] = {}
        
        if call.data == "menu":
            # Go back to azkar menu
            self.edit_to_azkar_menu(call)
        
        elif call.data.startswith("select_"):
            # Select azkar type
            azkar_key = call.data.replace("select_", "")
            self.start_counting(call, azkar_key)
        
        elif call.data.startswith("count_"):
            # Count button pressed
            azkar_key = call.data.replace("count_", "")
            self.increment_count(call, azkar_key)
        
        elif call.data.startswith("reset_"):
            # Reset specific azkar
            azkar_key = call.data.replace("reset_", "")
            self.reset_specific_azkar(call, azkar_key)
        
        # Answer callback to remove loading
        self.bot.answer_callback_query(call.id)
    
    def edit_to_azkar_menu(self, call):
        """Edit message to show azkar menu"""
        markup = types.InlineKeyboardMarkup(row_width=1)
        
        for key, azkar in self.azkar_types.items():
            button_text = f"📿 {azkar['arabic']} ({azkar['recommended']})"
            callback_data = f"select_{key}"
            markup.add(types.InlineKeyboardButton(button_text, callback_data=callback_data))
        
        text = "🔹 اختر الذكر الذي تريد عده:\n\n"
        text += "الأرقام بين القوسين تشير للعدد المستحب"
        
        self.bot.edit_message_text(
            text, 
            call.message.chat.id, 
            call.message.message_id, 
            reply_markup=markup
        )
    
    def start_counting(self, call, azkar_key):
        """Start counting for specific azkar"""
        user_id = str(call.from_user.id)
        azkar_info = self.azkar_types[azkar_key]
        
        # Initialize count if doesn't exist
        if azkar_key not in self.user_counts[user_id]:
            self.user_counts[user_id][azkar_key] = 0
        
        current_count = self.user_counts[user_id][azkar_key]
        recommended = azkar_info['recommended']
        
        # Create counting interface
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # Count button (large)
        count_btn = types.InlineKeyboardButton(
            f"👆 اضغط للعد ({current_count})", 
            callback_data=f"count_{azkar_key}"
        )
        markup.add(count_btn)
        
        # Reset and Menu buttons
        reset_btn = types.InlineKeyboardButton("🔄 مسح", callback_data=f"reset_{azkar_key}")
        menu_btn = types.InlineKeyboardButton("📋 القائمة", callback_data="menu")
        markup.add(reset_btn, menu_btn)
        
        # Progress indicator
        progress = f"{current_count}/{recommended}"
        if current_count >= recommended:
            progress += " ✅"
        
        text = f"📿 {azkar_info['arabic']}\n\n"
        text += f"🔤 {azkar_info['transliteration']}\n"
        text += f"💡 {azkar_info['meaning']}\n\n"
        text += f"📊 التقدم: {progress}\n\n"
        text += "👆 اضغط على الزر أدناه لبدء العد"
        
        self.bot.edit_message_text(
            text, 
            call.message.chat.id, 
            call.message.message_id, 
            reply_markup=markup
        )
    
    def increment_count(self, call, azkar_key):
        """Increment count for specific azkar"""
        user_id = str(call.from_user.id)
        azkar_info = self.azkar_types[azkar_key]
        
        # Increment count
        self.user_counts[user_id][azkar_key] += 1
        current_count = self.user_counts[user_id][azkar_key]
        recommended = azkar_info['recommended']
        
        # Update interface
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # Count button with updated count
        count_btn = types.InlineKeyboardButton(
            f"👆 اضغط للعد ({current_count})", 
            callback_data=f"count_{azkar_key}"
        )
        markup.add(count_btn)
        
        # Reset and Menu buttons
        reset_btn = types.InlineKeyboardButton("🔄 مسح", callback_data=f"reset_{azkar_key}")
        menu_btn = types.InlineKeyboardButton("📋 القائمة", callback_data="menu")
        markup.add(reset_btn, menu_btn)
        
        # Progress indicator
        progress = f"{current_count}/{recommended}"
        completion_msg = ""
        
        if current_count >= recommended:
            progress += " ✅"
            completion_msg = "\n\n🎉 مبروك! أكملت العدد المستحب"
        
        text = f"📿 {azkar_info['arabic']}\n\n"
        text += f"🔤 {azkar_info['transliteration']}\n"
        text += f"💡 {azkar_info['meaning']}\n\n"
        text += f"📊 التقدم: {progress}{completion_msg}\n\n"
        text += "👆 استمر في الضغط للعد"
        
        try:
            self.bot.edit_message_text(
                text, 
                call.message.chat.id, 
                call.message.message_id, 
                reply_markup=markup
            )
        except Exception as e:
            # If edit fails (same content), just log
            logger.debug(f"Edit message failed: {e}")
    
    def reset_specific_azkar(self, call, azkar_key):
        """Reset count for specific azkar"""
        user_id = str(call.from_user.id)
        self.user_counts[user_id][azkar_key] = 0
        
        # Restart counting interface
        self.start_counting(call, azkar_key)
    
    def start_polling(self):
        """Start the bot polling - NEVER STOPS"""
        logger.info("🔢 Starting Azkar Counter Bot...")
        while True:
            try:
                self.bot.polling(none_stop=True, interval=0, timeout=20)
            except Exception as e:
                logger.error(f"❌ Azkar Counter Bot error: {e} - restarting in 30 seconds...")
                time.sleep(30)
                continue

def main():
    """Main entry point for azkar counter"""
    from bot_config import BotConfig
    
    config = BotConfig()
    if not config.telegram_token:
        logger.error("❌ TELEGRAM_BOT_TOKEN not found")
        return
    
    counter = AzkarCounter(config.telegram_token)
    counter.start_polling()

if __name__ == "__main__":
    main()