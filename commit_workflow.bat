@echo off
echo 🚀 Committing GitHub Actions Workflow
echo ================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 Adding workflow files...
git add .github\workflows\deploy-pages.yml .nojekyll requirements.txt

echo 💾 Committing changes...
git commit -m "feat: Add GitHub Actions workflow for automatic Pages deployment"

echo 📤 Pushing to GitHub...
git push origin main

echo ✅ GitHub Actions workflow deployed!
echo 🌐 Workflow will now automatically build and deploy to GitHub Pages
echo 📊 Monitor at: https://github.com/awano27/daily-ai-news-pages/actions

pause