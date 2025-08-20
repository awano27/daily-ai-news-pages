@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 🚀 Enhanced AI News System - Gemini URL Context使用

echo.
echo 🔧 環境確認中...
python -c "import os; print('GEMINI_API_KEY:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"

echo.
echo 📡 強化版ニュース収集システム実行中...
python enhanced_build.py

echo.
echo 📊 実行結果確認:
if exist "_cache\enhanced_news_*.json" (
    echo ✅ 強化版データファイル生成完了
    dir "_cache\enhanced_news_*.json" /b
) else (
    echo ⚠️ 強化版データファイルが見つかりません
)

if exist "index.html" (
    echo ✅ ダッシュボードHTMLファイル存在確認
) else (
    echo ⚠️ index.htmlが見つかりません
)

echo.
echo 🎯 次回実行時のポイント:
echo - Gemini API keyが有効であること
echo - インターネット接続が安定していること  
echo - feeds.ymlファイルが存在すること

pause