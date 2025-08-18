@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Google Sheets連携SNS強化ダッシュボードを生成中...
python generate_sns_enhanced_dashboard.py
echo 生成完了！ブラウザで確認してください。
pause