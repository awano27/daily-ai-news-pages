@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 🧪 Gemini API動作テスト

python quick_test_gemini.py

echo.
echo 📋 テスト結果に基づく次のステップ:
echo ✅ 成功した場合: python test_integration_fixed.py を実行
echo ❌ 失敗した場合: API keyの設定を確認

pause