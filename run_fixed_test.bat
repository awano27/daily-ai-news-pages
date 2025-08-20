@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 🔧 Fixed X Processing Test
echo CSV列名修正版のテスト実行
echo.

echo 修正内容:
echo - CSV列名を "Tweet Text" に変更
echo - CSV列名を "Tweet URL" に変更  
echo - 詳細なデバッグログを追加
echo - 要約を300文字以内に制限
echo.

echo 📡 テスト実行中...
python test_fixed_x_processing.py

pause