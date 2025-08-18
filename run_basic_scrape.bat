@echo off
cd /d "%~dp0"
echo 🔍 基本スクレイピング実行
echo.
set /p url="スクレイピング対象URLを入力: "
python scripts/run_scraper.py %url% --method basic --verbose
echo.
pause