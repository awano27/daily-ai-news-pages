@echo off
echo 🎯 FINAL COMMIT: Clean HTML without dashboard links
echo ==============================================

echo 📝 Adding clean files...
git add index.html
git add news_detail.html
git add build.py

echo ✅ Final commit...
git commit -m "fix: Complete removal of dashboard links and clean HTML structure

🎯 FINAL HTML CLEANUP:
✅ Removed all dashboard navigation references
✅ Fixed broken HTML structure in index.html
✅ Clean header without dashboard links
✅ Proper HTML formatting and structure

🧹 Result: Permanent clean navigation
📋 No more dashboard confusion for users
🌐 Ready for deployment

[skip ci]"

echo 🚀 Final push...
git push origin main

echo ✅ COMPLETE! Dashboard links permanently removed!
echo 🌐 Site: https://awano27.github.io/daily-ai-news/
echo ⏰ Update time: 2-3 minutes