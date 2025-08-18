@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Committing workflow fix to use fixed dashboard script...

git add .github/workflows/build.yml
git add generate_fixed_dashboard.py

git commit -m "fix: update GitHub Actions to use fixed dashboard script

- Change workflow to execute generate_fixed_dashboard.py instead
- Copy generated file to index.html for proper deployment
- This ensures duplicate removal and proper SNS display work in production
- Should resolve the remaining duplicate article and empty SNS issues"

git push

echo.
echo Workflow updated to use fixed dashboard script!
echo Next GitHub Actions run will use the corrected version.
pause