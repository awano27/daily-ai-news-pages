@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🔄 ダッシュボードを生成中（クリック可能なSNS投稿付き）
python generate_comprehensive_dashboard.py

echo 📄 dashboard.html を index.html にコピー
copy /Y dashboard.html index.html

echo ✅ 完了！index.htmlを確認してください
pause