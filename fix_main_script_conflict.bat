@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Fixing Git conflict for main script update...

echo Step 1: Fetch and pull remote changes
git fetch origin
git pull origin main --no-edit

echo Step 2: Re-apply the main script update
copy generate_fixed_dashboard.py generate_reference_format_dashboard.py

echo Step 3: Add and commit the updated main script
git add generate_reference_format_dashboard.py

git commit -m "fix: update main dashboard script with duplicate removal and proper SNS display

- Replace main script with fixed version containing duplicate removal
- Fix SNS section to show 5 featured posts and 5 tech discussions  
- Maintain 80 translation limit for Gemini API
- Ensure proper article deduplication by URL and title
- This will fix the duplicate article and empty SNS issues"

echo Step 4: Push to remote
git push origin main

echo.
echo Main script conflict resolved and pushed successfully!
echo Next GitHub Actions run will use the fixed version.
pause