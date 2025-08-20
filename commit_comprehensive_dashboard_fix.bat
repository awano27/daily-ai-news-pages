@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 総合ダッシュボードのX投稿表示修正をコミット中...

git add generate_comprehensive_dashboard.py

git commit -m "fix: Resolve 'featured posts not found' issue in comprehensive dashboard

- Add fallback processing when Gemini API analysis fails
- Ensure X posts are always processed even on API errors
- Lower quality threshold from 6 to 4 for featured posts selection
- Move tech discussions to featured posts when insufficient
- This resolves the '注目の投稿が見つかりませんでした' message
- Guarantees at least some posts will appear in featured section

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

echo プッシュ中...
git pull origin main --no-edit
git push origin main

echo.
echo ✅ 総合ダッシュボード修正がGitHubにプッシュされました！
echo 📱 次回実行時に「注目の投稿」が表示されるはずです。
pause