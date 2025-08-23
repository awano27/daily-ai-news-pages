@echo off
echo 🔄 Resolving conflicts and pushing clean HTML
echo ==========================================

echo 📥 Pulling remote changes...
git pull origin main --rebase

echo 🚀 Pushing final clean version...
git push origin main

echo ✅ Push complete!
echo 🌐 Site will update at: https://awano27.github.io/daily-ai-news/
echo ⏰ Expected update time: 2-3 minutes
echo 📋 Dashboard links should be permanently gone now!