@echo off
echo Deploying X posts to GitHub...

git add .
git commit -m "Add real X posts from CSV data"
git push origin main

echo Done!
pause