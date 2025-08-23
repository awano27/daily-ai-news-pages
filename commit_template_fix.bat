@echo off
echo 🔧 Commit Build Template Fix
echo ============================

echo 📝 Adding files to git...
git add build.py
git add index.html
git add news_detail.html

echo ✅ Creating commit...
git commit -m "fix: Remove dashboard link from build.py template permanently

🔧 BUILD TEMPLATE FIX:
✅ Removed dashboard navigation from HTML template in build.py
✅ Prevents regeneration of unused dashboard links
✅ Ensures clean navigation on every future rebuild
✅ Updated both index.html and news_detail.html

🎯 Result: No more dashboard links in future builds
🧹 Permanent fix for navigation cleanup
📋 Addresses user feedback about confusing dashboard button

[skip ci]"

echo 🚀 Pushing to GitHub...
git push origin main

echo ✅ Template fix complete!
echo 🌐 Site will update at: https://awano27.github.io/daily-ai-news/
echo ⏰ Expected update time: 2-3 minutes