@echo off
echo 🔍 Xポスト詳細デバッグ
echo ===================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 環境変数設定...
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=25
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

echo 🔨 サイトをローカルビルド（Xポストデバッグ有効）...
python build_simple_ranking.py

echo 📊 index.htmlでXポスト検索...
if exist index.html (
    echo.
    echo === X (Twitter) 検索結果 ===
    findstr /C:"X (Twitter)" index.html
    echo.
    echo === @ 記号検索結果 ===
    findstr /C:"@" index.html | head -5
    echo.
    echo === twitter.com URL検索結果 ===
    findstr /C:"twitter.com" index.html | head -3
    echo.
    echo === x.com URL検索結果 ===
    findstr /C:"x.com" index.html | head -3
    echo.
    
    findstr /C:"X (Twitter)" index.html >nul
    if %errorlevel%==0 (
        for /f %%i in ('findstr /C:"X (Twitter)" index.html ^| find /C "X (Twitter)"') do echo ✅ Xポスト数: %%i件
    ) else (
        echo ❌ Xポストが見つかりません
        echo.
        echo === postsセクションの内容確認 ===
        findstr /C:"posts" index.html | head -3
    )
) else (
    echo ❌ index.htmlが生成されませんでした
)

echo.
echo 🌐 ローカルファイル確認:
echo file:///C:/Users/yoshitaka/daily-ai-news/index.html

pause