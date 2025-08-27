@echo off
echo 🚀 即座にX投稿修正版をデプロイ開始
echo =======================================

set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=8
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

echo ✓ 環境変数設定完了

echo 🔧 サイト再構築中...
python build.py
if %errorlevel% neq 0 (
    echo ❌ build.py実行失敗
    exit /b 1
)

echo ✅ サイト構築完了

echo 📤 GitHubにプッシュ中...
git add .
git commit -m "fix: Force X posts display with score 10.0 and enhanced debug logging"
git push origin main

if %errorlevel% neq 0 (
    echo ❌ Gitプッシュ失敗
    exit /b 1
)

echo 🎉 即座修正完了！数分でサイトに反映されます
pause