@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo X投稿の実際のテキスト表示修正をコミット中...

git add build.py generate_comprehensive_dashboard.py

git commit -m "fix: Display actual X/Twitter post text instead of placeholder

- Store full text in build.py with _full_text field
- Increase preview length from 50 to 150 characters
- Use full text in comprehensive dashboard fallback analysis
- Remove placeholder text like '手動でいいねしたポストから自動抽出'
- This ensures actual tweet content is displayed

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

echo プッシュ中...
git pull origin main --no-edit
git push origin main

echo.
echo ✅ X投稿テキスト表示修正がGitHubにプッシュされました！
echo 📱 次回実行時に実際の投稿内容が表示されます。
pause