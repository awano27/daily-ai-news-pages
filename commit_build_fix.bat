@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Committing build.py duplicate removal fix...

git add build.py

git commit -m "fix: add comprehensive duplicate removal to build.py

- Add global deduplication across all categories (Business, Tools, Posts)
- Remove duplicates by both URL and title before category processing
- Prevent same articles from appearing in multiple categories
- Maintain original X posts integration with duplicate checking
- This should finally resolve the duplicate article issue"

git push

echo.
echo Build.py duplicate removal fix committed and pushed!
echo Next GitHub Actions run should show no duplicate articles.
pause