@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo X投稿の実際のテキスト表示を修正中...

git add build.py generate_comprehensive_dashboard.py

git commit -m "fix: Fix X post text display issue - critical indentation bug

- Fix indentation bug in build.py _extract_x_data_from_csv function
- Posts were only being added when date parsing failed
- Add debug logging to track actual text content
- Improve text validation and fallback logic
- X posts should now display actual tweet content

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

echo プッシュ中...
git pull origin main --no-edit
git push origin main

echo.
echo ✅ X投稿テキスト表示修正がGitHubにプッシュされました！
echo 📱 次回実行時に実際の投稿内容が表示されます。
pause