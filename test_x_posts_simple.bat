@echo off
echo 🧪 Xポスト取得テスト
echo ===================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 環境変数設定...
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=25
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

echo 🔍 Xポストデバッグ実行...
python debug_x_posts_direct.py

echo 🚀 実際のビルドでXポスト確認...
python build_simple_ranking.py | findstr /C:"X投稿"

echo 📊 index.htmlでXポスト検索...
if exist index.html (
    findstr /C:"X (Twitter)" index.html
    if %errorlevel%==0 (
        echo ✅ Xポストが見つかりました
    ) else (
        echo ❌ Xポストが見つかりません
    )
) else (
    echo ❌ index.htmlが存在しません
)

pause