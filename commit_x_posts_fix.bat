@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo X/Twitter投稿表示修正をコミット中...

git add build.py

git commit -m "fix: Improve X/Twitter posts display in build.py

- Extend time filter from 48 hours to 7 days for more posts
- Add fallback to current time when date parsing fails
- Support more date formats (ISO, Japanese, MM/DD/YYYY)
- Skip header row in CSV processing  
- Process posts with valid text even without URL
- Generate dummy URL when missing
- This should resolve the issue where X posts were not appearing

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

echo プッシュ中...
git pull origin main --no-edit
git push origin main

echo.
echo ✅ X投稿表示修正がGitHubにプッシュされました！
echo 📱 次のGitHub Actions実行でX投稿が表示されるはずです。
pause