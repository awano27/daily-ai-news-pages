@echo off
echo 🔧 Final Dashboard Link Removal
echo ===============================

echo 📝 Copying clean news_detail.html to index.html...
copy news_detail.html index.html

echo 📝 Adding files to git...
git add build.py
git add index.html
git add news_detail.html

echo ✅ Creating final commit...
git commit -m "fix: Final removal of dashboard link from all files

🔧 FINAL DASHBOARD CLEANUP:
✅ Removed dashboard nav from news_detail.html
✅ Copied clean file to index.html
✅ Ensures consistent clean navigation across all files
✅ No more dashboard links anywhere in the codebase

🎯 Result: Permanently clean navigation
🧹 Final fix for user-reported dashboard confusion

[skip ci]"

echo 🚀 Pushing final fix...
git push origin main

echo ✅ Final dashboard cleanup complete!
echo 🌐 Site will update at: https://awano27.github.io/daily-ai-news/
echo ⏰ Expected update time: 2-3 minutes
echo 📋 Dashboard link should be completely gone now