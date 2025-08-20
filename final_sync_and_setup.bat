@echo off
chcp 65001 >nul
echo 🔄 Final Sync and GitHub Pages Setup
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📥 Pulling remote changes...
git pull origin main

echo.
echo 🚀 Pushing local changes...
git push origin main

echo.
echo ✅ Git sync completed!
echo.
echo 📋 GitHub Pages Settings Required:
echo.
echo 1. Open: https://github.com/awano27/daily-ai-news-pages/settings/pages
echo 2. Source: Deploy from a branch
echo 3. Branch: gh-pages
echo 4. Folder: / (root)
echo 5. Click Save
echo.
echo 🎯 After Pages setup:
echo - Run Enhanced workflow manually
echo - Check site: https://awano27.github.io/daily-ai-news-pages/
echo.
pause