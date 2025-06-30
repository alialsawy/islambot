# Islamic Telegram Bot

## Overview

This is an automated Islamic Telegram bot that generates and posts authentic Islamic religious content throughout the day. The bot uses OpenAI's GPT-4o model to create content in Arabic, including morning/evening azkar, Quranic verses, hadiths, daily reminders, and duas. It's designed to provide spiritual content at scheduled times to help Muslims maintain their daily Islamic practices.

## System Architecture

The application follows a modular architecture with clear separation of concerns:

- **Configuration Management**: Environment-based configuration with validation
- **Content Generation**: AI-powered Islamic content creation using OpenAI API
- **Telegram Integration**: Bot communication with Telegram channels
- **Scheduling System**: Time-based content posting automation
- **Logging System**: Centralized logging for monitoring and debugging

The system is designed as a long-running service that operates autonomously once configured.

## Key Components

### 1. Bot Configuration (`bot_config.py`)
- **Purpose**: Manages environment variables and validates required configuration
- **Key Features**: 
  - Environment variable loading with defaults
  - Configuration validation for required API keys
  - Customizable schedule times for different content types
  - Content generation parameters (temperature, max length, retry settings)

### 2. Content Generator (`content_generator.py`)
- **Purpose**: Generates authentic Islamic content using OpenAI's GPT-4o model
- **Content Types**:
  - Morning and evening azkar (Islamic remembrances)
  - Quranic verses with simple explanations
  - Authentic hadiths with sources and practical lessons
  - Daily reminders and duas
- **Language**: All content generated in Arabic (Fusha)
- **Validation**: Ensures content authenticity and appropriateness for Islamic channels

### 3. Telegram Bot Handler (`telegram_bot.py`)
- **Purpose**: Manages communication with Telegram API
- **Features**:
  - Connection testing and validation
  - Message sending with retry logic
  - Error handling for rate limiting and network issues
  - Channel access verification

### 4. Content Scheduler (`scheduler.py`)
- **Purpose**: Handles timing and automation of content posts
- **Schedule**: 8 different content types posted throughout the day
- **Default Times**:
  - Morning Azkar: 06:00 (Complete authentic azkar sequences)
  - Quran Verse: 08:00
  - Daily Hadith: 12:00 (30+ rotating authentic hadiths)
  - Religious Post: 14:00 (AI-generated style content without API)
  - Daily Reminder: 17:00
  - Companion Story: 19:00 (Inspiring stories about Sahaba)
  - Daily Dua: 20:00
  - Evening Azkar: 21:00 (Complete authentic azkar sequences)

### 5. Logging System (`logger_config.py`)
- **Purpose**: Centralized logging configuration
- **Features**: Console and optional file logging with proper formatting

### 6. Main Application (`main.py`)
- **Purpose**: Entry point that orchestrates all components
- **Features**: Signal handling, startup validation, continuous operation

## Data Flow

1. **Initialization**: Bot loads configuration and validates API connections
2. **Scheduling**: Content scheduler sets up daily posting times
3. **Content Generation**: At scheduled times, OpenAI API generates Islamic content
4. **Content Delivery**: Generated content is sent to configured Telegram channel
5. **Error Handling**: Failed operations are retried with exponential backoff
6. **Logging**: All operations are logged for monitoring and debugging

## External Dependencies

### Required APIs
- **OpenAI API**: For AI-powered content generation using GPT-4o model
- **Telegram Bot API**: For sending messages to Telegram channels

### Required Environment Variables
- `OPENAI_API_KEY`: OpenAI API authentication key
- `TELEGRAM_BOT_TOKEN`: Telegram bot authentication token
- `TELEGRAM_CHANNEL_ID`: Target channel ID for posting content

### Optional Configuration
- `MAX_CONTENT_LENGTH`: Maximum character limit for generated content (default: 500)
- `CONTENT_TEMPERATURE`: AI creativity parameter (default: 0.8)
- `RETRY_ATTEMPTS`: Number of retry attempts for failed operations (default: 3)
- `RETRY_DELAY`: Delay between retry attempts in seconds (default: 60)
- Custom schedule times for each content type

### Python Dependencies
- `openai`: Official OpenAI API client
- `python-telegram-bot`: Telegram Bot API wrapper
- `schedule`: Job scheduling library

## Deployment Strategy

The application is designed to run as a long-running service:

1. **Environment Setup**: Configure required environment variables
2. **Service Deployment**: Run as a background service or daemon
3. **Process Management**: Handles graceful shutdown with signal handling
4. **Error Recovery**: Automatic retry logic for temporary failures
5. **Monitoring**: Comprehensive logging for operational visibility

The bot requires continuous operation to maintain the daily posting schedule.

## Changelog

- June 29, 2025: Initial setup with OpenAI-powered content generation
- June 29, 2025: Updated to use pre-defined authentic Islamic content instead of OpenAI API
- June 29, 2025: Replaced python-telegram-bot with pyTelegramBotAPI for better compatibility
- June 29, 2025: Bot successfully connects to Telegram (@Qurraan_Post_bot) - awaiting channel administrator access
- June 29, 2025: Fixed Flask dependency and main.py structure - Bot now fully operational with scheduled content posting
- June 29, 2025: Enhanced bot with 30 rotating daily hadiths, complete azkar sequences, and interactive azkar counter with counting buttons
- June 29, 2025: Removed watermarks from all content and updated startup/shutdown messages to Islamic phrases (سبحان الله/الحمد لله)
- June 29, 2025: Made bot completely bulletproof - will NEVER shut down under any circumstances, handles all errors gracefully with automatic retries
- June 29, 2025: Prepared project for Render hosting deployment with complete configuration files and documentation
- June 29, 2025: Enhanced bot with comprehensive content - Complete authentic azkar (6 groups each for morning/evening), AI-generated religious posts (without API), and inspiring companion stories (10 Sahaba stories)

## User Preferences

Preferred communication style: Simple, everyday language.