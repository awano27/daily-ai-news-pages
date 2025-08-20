@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo X投稿の重複除去と詳細要約修正を実行中...

git add build.py generate_comprehensive_dashboard.py test_x_data_debug.py

git commit -m "fix: Improve X post deduplication and content display

- Add URL and username-content based deduplication in build.py
- Enhanced text processing for more detailed X post summaries
- Improve fallback text generation with AI keywords detection
- Add company-specific contextual summaries (Google, OpenAI, Anthropic)
- Increase summary length limit from 200 to 300 characters
- Add debug logging for X post data processing
- Create detailed debug test script for CSV data analysis

This ensures unique posts and meaningful content instead of placeholders.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

echo プッシュ中...
git pull origin main --no-edit
git push origin main

echo.
echo ✅ X投稿重複除去・要約改善がGitHubにプッシュされました！
echo 📱 次回実行時に重複が削除され、詳細な要約が表示されます。
pause