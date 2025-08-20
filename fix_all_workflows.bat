@echo off
echo 🔧 Fixing ALL GitHub Actions Workflow Errors
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📝 Adding all fixed workflow files...
git add .github/workflows/enhanced-daily-build.yml
git add .github/workflows/minimal-build.yml

echo.
echo 💾 Committing fixes...
git commit -m "fix: YAML syntax errors in GitHub Actions workflows - Remove multiline strings and fix heredoc issues"

echo.
echo 🚀 Pushing to GitHub...
git push origin main

echo.
echo ✅ All workflow fixes pushed!
echo.
echo 📋 Confirmation checklist:
echo [x] enhanced-daily-build.yml - Line 151 fixed (multiline commit message)
echo [x] minimal-build.yml - Line 33 fixed (heredoc variable expansion)
echo.
echo 🌐 Check status at:
echo - GitHub Actions: https://github.com/awano27/daily-ai-news-pages/actions
echo - Site: https://awano27.github.io/daily-ai-news-pages/
echo.
echo 🚀 To test manually:
echo 1. Go to Actions tab
echo 2. Select "Enhanced Daily AI News (Full Pipeline)"
echo 3. Click "Run workflow"
echo.
pause