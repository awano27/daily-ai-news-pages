@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo SNS強化ダッシュボードをコミット中...

git add generate_sns_enhanced_dashboard.py
git add run_sns_enhanced.bat
git add fetch_x_posts.py

git commit -m "feat: Add SNS enhanced dashboard with Google Sheets integration

- Add generate_sns_enhanced_dashboard.py for Google Sheets X/Twitter data fetching
- Direct CSV download from Google Sheets spreadsheet
- Display 5 featured posts and 5 tech discussions
- Automatic data cleaning and importance scoring
- Fallback data when Google Sheets is unavailable
- Responsive tabbed interface for different content categories

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

echo プッシュ中...
git pull origin main --no-edit
git push origin main

echo.
echo ✅ SNS強化ダッシュボードがGitHubにプッシュされました！
pause