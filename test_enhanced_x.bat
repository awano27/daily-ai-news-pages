@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 🚀 Enhanced X Processing Test
echo.

echo 🔧 環境確認...
python -c "import os; print('GEMINI_API_KEY:', 'SET' if os.getenv('GEMINI_API_KEY') else 'NOT SET')"

echo.
echo 🧪 Enhanced X Processor テスト実行...
python run_enhanced_x_test.py

echo.
echo 📊 テスト完了 - 結果を確認してください
pause