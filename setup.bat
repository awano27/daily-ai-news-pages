@echo off
echo ???????...
pip install -r requirements.txt
python -m playwright install chromium
if not exist outputs mkdir outputs
if not exist redis-data mkdir redis-data
echo ??
pause
