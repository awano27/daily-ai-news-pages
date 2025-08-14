@echo off
echo =======================================
echo Daily AI News - Deploy Script
echo =======================================

echo.
echo Step 1: Building index.html...
python run_build.py
if errorlevel 1 (
    echo ERROR: Build failed!
    pause
    exit /b 1
)

echo.
echo Step 2: Checking if index.html exists...
if not exist index.html (
    echo ERROR: index.html was not created!
    pause
    exit /b 1
)

echo.
echo Step 3: Adding files to Git...
git add index.html
git add _cache/translations.json 2>nul
git add build.py
git add CLAUDE.md

echo.
echo Step 4: Committing changes...
git commit -m "chore: Generate and deploy index.html"
if errorlevel 1 (
    echo No changes to commit or commit failed
)

echo.
echo Step 5: Pushing to GitHub...
git push
if errorlevel 1 (
    echo ERROR: Push failed!
    echo Please run 'git push' manually
    pause
    exit /b 1
)

echo.
echo =======================================
echo DEPLOYMENT SUCCESSFUL!
echo Your site will be live at:
echo https://awano27.github.io/daily-ai-news/
echo (May take a few minutes to update)
echo =======================================
pause