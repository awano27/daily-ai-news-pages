@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Committing translation quota increase...
git add generate_reference_format_dashboard.py
git commit -m "fix: increase Gemini translation quota from 30 to 80 to ensure more articles are translated to Japanese"
git push
echo.
echo Translation quota fix committed and pushed successfully!
pause