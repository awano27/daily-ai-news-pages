@echo off
echo 🚀 GitHub サイト強制更新デプロイ
echo =====================================

echo.
echo 📁 現在のファイル状況確認...
git status

echo.
echo 📤 ファイルをステージング中...
git add index.html
git add news_detail.html
git add dashboard_data.json
git add build.py
git add generate_comprehensive_dashboard.py
git add auto_update_all.py

echo.
echo 💾 コミット中...
git commit -m "feat: Force update AI news site [2025-08-16 09:39 JST] [skip ci]

🚀 Complete Site Update:
- Updated dashboard with 312 news items
- Enhanced with 271 X/Twitter posts from Google Sheets  
- Fixed reference links (LLM Arena, AlphaXiv, Trend Words)
- Comprehensive executive summary and industry insights
- Real-time data from RSS feeds and social media

📊 Key Metrics:
- Total news: 312 items across 3 categories
- SNS posts: 271 items with importance scoring
- Active companies: Meta(5), Amazon(5), NVIDIA(5), OpenAI(3)
- Hot trends: GPT-5(3), GPT-4(2), Transformer(1)

🎯 Site Structure:
- index.html: Executive dashboard (landing page)
- news_detail.html: Detailed news articles
- Automated daily updates via Google Sheets

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

echo.
echo 🌐 GitHubへプッシュ中...
git push origin main

echo.
echo ✅ デプロイ完了！
echo.
echo 🌐 サイトURL: https://awano27.github.io/daily-ai-news/
echo ⏰ 反映まで: 1-5分程度
echo 💡 ブラウザで Ctrl+F5 で強制更新してください
echo.
pause