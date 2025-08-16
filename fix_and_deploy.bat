@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo Step 1: Fetch latest remote changes...
git fetch origin main

echo Step 2: Add important files...
git add index.html
git add news_detail.html  
git add dashboard_data.json
git add build.py
git add generate_comprehensive_dashboard.py
git add auto_update_all.py

echo Step 3: Commit local changes...
git commit -m "Update AI news site with latest dashboard data [skip ci]"

echo Step 4: Pull and merge remote changes...
git pull origin main --no-edit

echo Step 5: Push merged changes...
git push origin main

echo Deployment complete!
echo Site URL: https://awano27.github.io/daily-ai-news/
pause