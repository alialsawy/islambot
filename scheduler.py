"""
Content Scheduler
Handles timing and scheduling of content posts
"""

import schedule
import time
from datetime import datetime
from logger_config import setup_logger

logger = setup_logger()

class ContentScheduler:
    def __init__(self, telegram_bot, content_generator):
        """Initialize scheduler with bot and content generator"""
        self.telegram_bot = telegram_bot
        self.content_generator = content_generator
        self.scheduled_jobs = []
        
        # Default schedule times (can be overridden by config)
        self.default_schedule = {
            "morning_azkar": "06:00",
            "quran_verse": "08:00", 
            "daily_hadith": "12:00",
            "religious_post": "14:00",
            "daily_reminder": "17:00",
            "companion_story": "19:00",
            "daily_dua": "20:00",
            "evening_azkar": "21:00"
        }
    
    def setup_schedule(self, custom_times=None):
        """Setup the daily content schedule"""
        schedule_times = custom_times or self.default_schedule
        
        logger.info("📅 Setting up content schedule...")
        
        # Clear existing jobs
        schedule.clear()
        
        # Schedule each content type
        for content_type, time_str in schedule_times.items():
            try:
                job = schedule.every().day.at(time_str).do(
                    self._generate_and_send_content, content_type
                )
                self.scheduled_jobs.append((content_type, time_str, job))
                logger.info(f"   📍 {content_type} scheduled at {time_str}")
            except Exception as e:
                logger.error(f"❌ Failed to schedule {content_type} at {time_str}: {e}")
        
        logger.info(f"✅ Successfully scheduled {len(self.scheduled_jobs)} content types")
        self._log_next_runs()
    
    def run_pending_tasks(self):
        """Run any pending scheduled tasks"""
        try:
            schedule.run_pending()
        except Exception as e:
            logger.error(f"❌ Error running scheduled tasks: {e}")
    
    def _generate_and_send_content(self, content_type):
        """Generate and send content for the specified type"""
        try:
            current_time = datetime.now().strftime("%H:%M")
            logger.info(f"⏰ {current_time} - Executing scheduled task: {content_type}")
            
            # Generate content
            content = self.content_generator.generate_content(content_type)
            
            if content:
                # Send to Telegram
                success = self.telegram_bot.send_formatted_content(content_type, content)
                
                if success:
                    logger.info(f"✅ Successfully posted {content_type}")
                else:
                    logger.error(f"❌ Failed to post {content_type}")
            else:
                logger.error(f"❌ No content generated for {content_type}")
                
        except Exception as e:
            logger.error(f"❌ Error in scheduled task {content_type}: {e}")
    
    def _log_next_runs(self):
        """Log the next scheduled runs"""
        logger.info("🔜 Next scheduled posts:")
        
        # Get all jobs sorted by next run time
        jobs_info = []
        for job in schedule.jobs:
            next_run = job.next_run
            if next_run:
                # Find the content type for this job
                content_type = "unknown"
                for ct, time_str, scheduled_job in self.scheduled_jobs:
                    if scheduled_job == job:
                        content_type = ct
                        break
                
                jobs_info.append((next_run, content_type))
        
        jobs_info.sort(key=lambda x: x[0])
        
        for next_run, content_type in jobs_info[:3]:  # Show next 3 runs
            formatted_time = next_run.strftime("%Y-%m-%d %H:%M")
            logger.info(f"   📍 {content_type}: {formatted_time}")
    
    def get_schedule_status(self):
        """Get current schedule status"""
        status = {
            "total_jobs": len(schedule.jobs),
            "scheduled_content_types": len(self.scheduled_jobs),
            "next_run": None
        }
        
        if schedule.jobs:
            next_job = min(schedule.jobs, key=lambda x: x.next_run)
            status["next_run"] = next_job.next_run.strftime("%Y-%m-%d %H:%M:%S")
        
        return status
    
    def run_content_now(self, content_type):
        """Manually trigger content generation and posting"""
        if content_type not in self.default_schedule:
            logger.error(f"❌ Unknown content type: {content_type}")
            return False
        
        logger.info(f"🚀 Manually triggering {content_type}")
        self._generate_and_send_content(content_type)
        return True
    
    def test_all_content_types(self):
        """Test generation of all content types (for debugging)"""
        logger.info("🧪 Testing all content types...")
        
        for content_type in self.default_schedule.keys():
            logger.info(f"Testing {content_type}...")
            content = self.content_generator.generate_content(content_type)
            
            if content:
                logger.info(f"✅ {content_type}: Generated successfully")
                logger.debug(f"Preview: {content[:100]}...")
            else:
                logger.error(f"❌ {content_type}: Generation failed")
        
        logger.info("🧪 Content type testing complete")
