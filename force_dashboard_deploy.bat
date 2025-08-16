@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🚨 新しいダッシュボード版を強制デプロイ
echo ========================================

echo 1. 現在のindex.htmlを確認
dir index.html

echo 2. ダッシュボード版を生成
python generate_comprehensive_dashboard.py

echo 3. ダッシュボード版をindex.htmlに上書き
copy /Y dashboard.html index.html

echo 4. ファイルをステージング
git add index.html dashboard_data.json

echo 5. 強制コミット
git commit -m "force: Deploy new dashboard version [skip ci]

CRITICAL UPDATE:
- Replace old 8-item format with comprehensive dashboard
- 312 news items with full executive summary
- 271 X/Twitter posts with importance scoring
- Fixed external links (LLM Arena, AlphaXiv, Trend Words)
- Real-time Google Sheets integration

This is the complete dashboard format that should be live."

echo 6. 強制プッシュ
git push origin main --force

echo ✅ 強制デプロイ完了!
echo 🌐 サイト: https://awano27.github.io/daily-ai-news/
echo ⏰ 反映: 1-5分後
pause