@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🤖 Gemini AI強化版ダッシュボード生成中...
echo.

REM 環境変数設定
set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=30
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

echo 📊 AIによる分析開始...
python generate_comprehensive_dashboard.py

echo.
echo ✅ 生成完了！
echo.
start index.html
pause