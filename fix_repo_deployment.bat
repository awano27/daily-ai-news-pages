@echo off
echo 🔧 Fixing Repository Deployment Configuration
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📝 Key fixes applied:
echo - Deploy target: gh-pages → main branch
echo - Enhanced workflow integration
echo - news_detail.html → index.html mapping
echo.

echo 🔄 Adding fixed deployment workflow...
git add .github/workflows/deploy-to-public.yml

echo.
echo 💾 Committing deployment fixes...
git commit -m "fix: Repository deployment configuration - Deploy to main branch, integrate Enhanced workflow"

echo.
echo 🚀 Pushing to GitHub...
git push origin main

echo.
echo ✅ Deployment configuration fixed!
echo.
echo 📋 Configuration summary:
echo - Source repo: daily-ai-news (private)
echo - Target repo: daily-ai-news-pages (public)
echo - Deploy branch: main (was gh-pages)
echo - Main file: news_detail.html → index.html
echo.
echo 🎯 Required GitHub settings:
echo.
echo 📍 daily-ai-news (source) repository:
echo 1. Settings → Secrets → PERSONAL_TOKEN (for deployment)
echo 2. Settings → Secrets → GEMINI_API_KEY (for build)
echo.
echo 📍 daily-ai-news-pages (public) repository:
echo 1. Settings → Pages → Source: Deploy from branch
echo 2. Settings → Pages → Branch: main
echo 3. Settings → Pages → Folder: / (root)
echo.
echo 🚀 To test:
echo 1. Run Enhanced workflow in daily-ai-news
echo 2. Verify deployment to daily-ai-news-pages
echo 3. Check https://awano27.github.io/daily-ai-news-pages/
echo.
pause