@echo off
chcp 65001 >nul
git add build.py
git commit -m "fix: HTML template and character encoding fixes for SNS posts"
git push origin main
echo Template and encoding fixes pushed successfully
pause