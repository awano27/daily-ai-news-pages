@echo off
echo 🚀 Simple Deploy to GitHub Pages
echo ===============================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 Setting environment variables...
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBOOK=24
set MAX_ITEMS_PER_CATEGORY=25

echo 🔨 Building site...
python build_simple_ranking.py

echo 📋 Checking build output...
if exist index.html (
    echo ✅ index.html generated successfully
) else (
    echo ❌ Build failed - index.html not found
    pause
    exit /b 1
)

echo 📤 Adding and committing changes...
git add index.html style.css
git commit -m "feat: Update site content %date% %time%"

echo 🌐 Deploying to gh-pages branch...
git push origin main:gh-pages --force

echo ✅ Deployment completed!
echo 🌐 Site should update at: https://awano27.github.io/daily-ai-news-pages/
echo 🕐 Allow 2-5 minutes for changes to appear

pause