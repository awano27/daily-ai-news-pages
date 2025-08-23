@echo off
echo 🔨 Building Daily AI News with today's content
echo ===============================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 Setting environment variables...
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=25

echo 🔨 Building site...
C:\Users\yoshitaka\AppData\Local\Programs\Python\Python311\python.exe build_simple_ranking.py

echo 📤 Deploying to GitHub Pages...
git add index.html style.css
git commit -m "feat: Update site with 2025-08-23 content"
git push origin main
git push origin gh-pages

echo ✅ Site updated successfully!
echo 🌐 Check: https://awano27.github.io/daily-ai-news-pages/

pause