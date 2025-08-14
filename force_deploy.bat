@echo off
echo =========================================
echo Force Deploy to GitHub Pages
echo =========================================

echo.
echo Current Git status:
git status --short

echo.
echo Adding all files...
git add .
git add -f index.html
git add -f .nojekyll
git add -f style.css

echo.
echo Files to be committed:
git status --short

echo.
echo Committing changes...
git commit -m "fix: Force deploy index.html with complete content and .nojekyll for GitHub Pages"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo Checking remote repository...
echo index.html should now be available at:
echo https://github.com/awano27/daily-ai-news/blob/main/index.html

echo.
echo GitHub Pages URL:
echo https://awano27.github.io/daily-ai-news/
echo (May take 1-2 minutes to update)

echo.
echo =========================================
echo Deploy complete! 
echo If still 404, check GitHub Pages settings:
echo 1. Go to: https://github.com/awano27/daily-ai-news/settings/pages
echo 2. Source should be: Deploy from a branch
echo 3. Branch should be: main / (root)
echo =========================================

pause