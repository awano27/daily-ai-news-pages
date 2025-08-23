@echo off
echo 🔨 Xポスト修正後の再ビルド
echo =============================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 環境変数設定中...
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=25
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

echo 🔍 現在のindex.htmlをバックアップ...
if exist index.html (
    copy index.html index_before_x_fix.html
    echo ✅ バックアップ完了: index_before_x_fix.html
)

echo 🚀 サイト再ビルド中...
python build_simple_ranking.py

echo 📊 結果確認...
if exist index.html (
    echo ✅ index.html が生成されました
    
    findstr /C:"X (Twitter)" index.html >nul
    if %errorlevel%==0 (
        echo ✅ Xポストが含まれています
    ) else (
        echo ⚠️ Xポストが見つかりません
    )
    
    findstr /C:"twitter.com" index.html >nul
    if %errorlevel%==0 (
        echo ✅ Twitterリンクが含まれています
    ) else (
        echo ⚠️ Twitterリンクが見つかりません  
    )
) else (
    echo ❌ index.html の生成に失敗しました
)

echo 🌐 ローカルファイルを確認:
echo file:///C:/Users/yoshitaka/daily-ai-news/index.html

pause