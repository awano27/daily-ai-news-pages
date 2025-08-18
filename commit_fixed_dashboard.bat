@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Committing fixed dashboard script...

git add generate_fixed_dashboard.py
git add run_fixed_dashboard.bat

git commit -m "feat: add fixed dashboard with duplicate removal and proper SNS display

- Add remove_duplicates() function to eliminate duplicate articles by URL and title
- Implement proper SNS section with 5 featured posts and 5 tech discussions
- Improve logging to show before/after duplicate removal counts
- Maintain Gemini translation with 80 translation limit
- Fix SNS post display format to match reference site structure"

git push

echo.
echo Fixed dashboard script committed and pushed successfully!
pause