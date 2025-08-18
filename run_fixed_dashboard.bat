@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Testing fixed dashboard with duplicate removal and 5 SNS posts...
python generate_fixed_dashboard.py
echo.
echo Fixed dashboard generation completed!
pause