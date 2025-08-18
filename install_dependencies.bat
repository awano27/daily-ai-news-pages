@echo off
echo Installing required dependencies...
echo.

echo Installing python-dotenv...
pip install python-dotenv

echo Installing google-generativeai...
pip install google-generativeai

echo Installing other dependencies...
pip install feedparser pyyaml requests

echo.
echo Installation completed!
echo You can now run: run_gemini_dashboard.bat
pause