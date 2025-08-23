@echo off
echo 🚀 Final Deploy - Tab Functionality Fix
echo =====================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 Adding all changes...
git add .

echo 📤 Committing fix...
git commit -m "feat: Complete tab functionality fix with working article display"

echo 🌐 Pushing to main branch...
git push origin main

echo 🚀 Force pushing to gh-pages...
git push origin main:gh-pages --force

echo ✅ Deployment completed!
echo 🌐 Site will update at: https://awano27.github.io/daily-ai-news-pages/
echo 🕐 Allow 2-5 minutes for changes to appear

pause