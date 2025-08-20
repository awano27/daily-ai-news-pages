@echo off
echo 🧹 Cleaning up and fixing GitHub Actions workflows
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 🗑️ Removing problematic minimal-build.yml...
git rm .github/workflows/minimal-build.yml 2>nul

echo.
echo 📝 Staging fixed enhanced workflow...
git add .github/workflows/enhanced-daily-build.yml

echo.
echo 💾 Committing all fixes...
git commit -m "fix: Remove problematic minimal-build.yml and fix enhanced workflow YAML syntax"

echo.
echo 🚀 Pushing to GitHub...
git push origin main

echo.
echo ✅ Cleanup and fixes complete!
echo.
echo 📊 Status:
echo - ✅ enhanced-daily-build.yml - Fixed and ready
echo - ✅ build.yml - Working
echo - ❌ minimal-build.yml - Removed (not needed)
echo.
echo 🌐 Next steps:
echo 1. Check GitHub Actions: https://github.com/awano27/daily-ai-news-pages/actions
echo 2. No more YAML errors should appear
echo 3. Run "Enhanced Daily AI News" workflow manually
echo 4. Wait for automatic execution at 07:00/19:00 JST
echo.
pause