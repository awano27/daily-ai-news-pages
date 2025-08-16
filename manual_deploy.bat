@echo off
echo Deploying enhanced SNS functionality...

echo.
echo Checking git status...
git status

echo.
echo Adding build.py...
git add build.py

echo.
echo Adding index.html...
git add index.html

echo.
echo Committing changes...
git commit -m "feat: Enhanced SNS posts from 8/14+ with importance scoring (30 items) [2025-08-15 JST]" -m "" -m "📱 Improvements:" -m "- Focus on 8/14+ recent posts only" -m "- Increased to 30 SNS posts max" -m "- Importance-based ranking" -m "- Enterprise accounts prioritized" -m "- No old news, fresh content only"

echo.
echo Pushing to GitHub...
git push origin main

echo.
echo Deployment complete!
pause