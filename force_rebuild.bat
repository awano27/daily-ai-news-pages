@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo Force rebuild starting...

echo Committing all changes...
git add -A
git commit -m "FORCE REBUILD: Update dashboard with clean design and 403 fix - Triggers CI build"

echo Pushing to GitHub...
git push origin main

echo.
echo GitHub Actions will now build the site
echo Check progress at: https://github.com/awano27/daily-ai-news/actions
echo.
pause