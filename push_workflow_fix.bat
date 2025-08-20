@echo off
echo 🔧 Pushing workflow fix to GitHub
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📝 Adding fixed workflow file...
git add .github/workflows/enhanced-daily-build.yml

echo.
echo 💾 Committing fix...
git commit -m "fix: GitHub Actions YAML syntax error on line 151 - Remove multiline commit message"

echo.
echo 🚀 Pushing to GitHub...
git push origin main

echo.
echo ✅ Workflow fix pushed!
echo.
echo 📋 Next steps:
echo 1. Check GitHub Actions tab for workflow status
echo 2. Run workflow manually to test
echo 3. Verify no more syntax errors
echo.
echo 🌐 GitHub Actions: https://github.com/awano27/daily-ai-news-pages/actions
pause