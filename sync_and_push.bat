@echo off
echo 🔄 Syncing with remote and pushing changes
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📥 Pulling latest changes from remote...
git pull origin main

echo.
echo 🔍 Checking status after pull...
git status

echo.
echo 🚀 Pushing local changes...
git push origin main

echo.
echo ✅ Sync and push completed!
echo.
echo 📋 Next steps:
echo 1. Verify deployment workflow is updated
echo 2. Check GitHub settings for both repos
echo 3. Run manual workflow test
echo.
pause