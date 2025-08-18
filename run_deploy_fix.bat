@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Running build.py duplicate removal fix deployment...
python deploy_build_fix.py
echo Deployment script completed.
pause