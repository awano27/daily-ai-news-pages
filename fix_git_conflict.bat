@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Fixing Git conflict and pushing changes...

echo Step 1: Fetch remote changes
git fetch origin

echo Step 2: Pull with automatic merge
git pull origin main --no-edit

echo Step 3: Add our fixed dashboard files
git add generate_fixed_dashboard.py
git add run_fixed_dashboard.bat
git add commit_fixed_dashboard.bat
git add generate_reference_format_dashboard.py

echo Step 4: Commit our changes
git commit -m "feat: add fixed dashboard with duplicate removal and proper SNS display

- Add remove_duplicates() function to eliminate duplicate articles by URL and title
- Implement proper SNS section with 5 featured posts and 5 tech discussions
- Improve logging to show before/after duplicate removal counts
- Maintain Gemini translation with 80 translation limit
- Fix SNS post display format to match reference site structure"

echo Step 5: Push to remote
git push origin main

echo.
echo Git conflict resolved and changes pushed successfully!
pause