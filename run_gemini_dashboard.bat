@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo Gemini AI Dashboard Generation...
echo.

set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=30
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

echo Starting AI analysis...
python generate_comprehensive_dashboard.py

echo.
echo Complete!
echo Opening index.html...
start index.html
pause