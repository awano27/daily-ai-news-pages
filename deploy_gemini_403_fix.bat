@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo Deploying Gemini 403 error fix to GitHub...
echo.

echo Adding new files...
git add gemini_web_fetcher.py test_gemini_fetcher.bat .env

echo Committing changes...
git commit -m "feat: Add Gemini Web Fetcher to fix 403 errors

- Created gemini_web_fetcher.py to handle 403 error sources
- Use Gemini API to fetch news from problematic sources
- Automatic fallback for Google News and other blocked feeds
- Trend analysis and supplemental data generation
- Complete solution for persistent 403 errors

[skip ci]"

echo Pushing to GitHub...
git push origin main

echo.
echo Complete! Gemini 403 fix deployed to GitHub.
echo URL: https://awano27.github.io/daily-ai-news/
pause