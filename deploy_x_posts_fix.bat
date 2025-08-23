@echo off
echo 🔧 Xポスト修正版デプロイ
echo ========================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 環境変数設定...
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=25
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

echo 🔨 修正版でサイト再ビルド...
python build_simple_ranking.py

echo 📊 index.htmlでXポスト確認...
if exist index.html (
    findstr /C:"X (Twitter)" index.html >nul
    if %errorlevel%==0 (
        echo ✅ Xポストが含まれています!
        findstr /C:"X (Twitter)" index.html | find /C "X (Twitter)"
    ) else (
        echo ❌ まだXポストが含まれていません
    )
    
    findstr /C:"@" index.html >nul
    if %errorlevel%==0 (
        echo ✅ ユーザー名（@）が含まれています
    ) else (
        echo ⚠️ ユーザー名（@）が見つかりません
    )
) else (
    echo ❌ index.html生成失敗
    pause
    exit /b 1
)

echo 📤 GitHubにデプロイ...
git add .
git commit -m "fix: Enhanced X posts processing to handle both CSV and text formats from Google Sheets"
git push origin main

echo ✅ デプロイ完了!
echo 🌐 サイト更新確認: https://awano27.github.io/daily-ai-news-pages/
echo 🕐 数分後にXポストが表示されるはずです

pause