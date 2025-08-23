@echo off
echo 🔄 Resolving Git conflicts and pushing template fix
echo ================================================

echo 📥 Pulling remote changes...
git pull origin main --rebase

echo 🚀 Pushing template fix...
git push origin main

echo ✅ Template fix pushed successfully!
echo 🌐 Site will update at: https://awano27.github.io/daily-ai-news/
echo ⏰ Expected update time: 2-3 minutes
echo 📋 Dashboard link should be permanently removed