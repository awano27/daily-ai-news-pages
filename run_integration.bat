@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 🔧 Gemini URL Context統合作業開始...

python integrate_enhanced_system.py

echo.
echo 📋 次のステップ:
echo 1. pip install -r requirements.txt
echo 2. .envファイルにGEMINI_API_KEYを設定
echo 3. python test_integration.py でテスト
echo 4. python enhanced_build.py で強化版実行

pause