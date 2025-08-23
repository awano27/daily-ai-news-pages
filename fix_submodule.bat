@echo off
echo 🔧 Fixing submodule reference issues
echo ===============================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 Removing submodule references...
if exist .gitmodules del .gitmodules
if exist .serena-src rmdir /s /q .serena-src

echo 🧹 Clearing git cache...
git rm --cached .serena-src 2>nul
git rm --cached .gitmodules 2>nul

echo 📝 Adding all changes...
git add .

echo 💾 Committing fix...
git commit -m "fix: Remove .serena-src submodule references completely"

echo 📤 Pushing to main...
git push origin main

echo 📤 Pushing to gh-pages...
git push origin gh-pages

echo ✅ Submodule issue fixed!
echo 🌐 GitHub Pages should now deploy successfully

pause