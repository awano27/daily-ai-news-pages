@echo off
chcp 65001 >nul
echo Syncing with remote repository...
git pull origin main

echo Adding template fixes...
git add build.py

echo Committing template and encoding fixes...
git commit -m "fix: HTML template and character encoding fixes for SNS posts"

echo Pushing to remote...
git push origin main

if %errorlevel% equ 0 (
    echo ✅ Template fixes successfully pushed!
) else (
    echo ❌ Failed to push template fixes
)
pause