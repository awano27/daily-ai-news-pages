@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo Git status check...
git status

echo Adding files...
git add index.html
git add news_detail.html
git add dashboard_data.json
git add build.py
git add generate_comprehensive_dashboard.py

echo Committing changes...
git commit -m "Update AI news site with latest data [skip ci]"

echo Pushing to GitHub...
git push origin main

echo Deployment complete!
echo Site URL: https://awano27.github.io/daily-ai-news/
echo Wait 1-5 minutes for changes to appear
pause