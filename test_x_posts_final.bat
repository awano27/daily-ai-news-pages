@echo off
echo 🔍 Xポスト最終デバッグテスト
echo ===========================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 環境変数設定...
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=25
set "X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"

echo 🔨 デバッグ版ビルド実行...
python build_simple_ranking.py > build_debug.log 2>&1

echo 📊 ビルドログ確認...
echo === DEBUG: X投稿関連ログ ===
findstr /C:"DEBUG" build_debug.log
findstr /C:"X投稿" build_debug.log
findstr /C:"📱" build_debug.log

echo.
echo === index.html の X投稿確認 ===
if exist index.html (
    findstr /C:"X (Twitter)" index.html && echo ✅ Xポスト発見! || echo ❌ Xポストなし
) else (
    echo ❌ index.html生成失敗
)

echo.
echo 📄 完全ビルドログ確認:
echo type build_debug.log

pause