@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo Installing deep-translator...
pip install deep-translator==1.11.4
echo Running dashboard generation...
python generate_comprehensive_dashboard.py
pause