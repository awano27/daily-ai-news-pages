@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Updating main script with fixed version...

rem Backup current script
copy generate_reference_format_dashboard.py generate_reference_format_dashboard_backup.py

rem Replace with fixed version
copy generate_fixed_dashboard.py generate_reference_format_dashboard.py

echo Script updated successfully!
echo.
echo Now committing and pushing the updated main script...

git add generate_reference_format_dashboard.py
git commit -m "fix: update main dashboard script with duplicate removal and proper SNS display

- Replace main script with fixed version containing duplicate removal
- Fix SNS section to show 5 featured posts and 5 tech discussions  
- Maintain 80 translation limit for Gemini API
- Ensure proper article deduplication by URL and title"

git push

echo.
echo Main script updated and pushed successfully!
pause