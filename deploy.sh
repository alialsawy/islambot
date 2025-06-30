#!/bin/bash

# Islamic Telegram Bot - Render Deployment Script
echo "🚀 Preparing Islamic Telegram Bot for Render deployment..."

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing Git repository..."
    git init
fi

# Add all files
echo "📦 Adding all files to Git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "Islamic Telegram Bot ready for Render deployment"

echo "✅ Project is ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Push to GitHub: git remote add origin <your-repo-url> && git push -u origin main"
echo "2. Go to render.com and create a new Web Service"
echo "3. Connect your GitHub repository"
echo "4. Set environment variables:"
echo "   - TELEGRAM_BOT_TOKEN"
echo "   - TELEGRAM_CHANNEL_ID"
echo "5. Deploy!"
echo ""
echo "📖 Full instructions are in RENDER_DEPLOYMENT.md"