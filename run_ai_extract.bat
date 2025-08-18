@echo off
cd /d "%~dp0"
echo 🤖 AI抽出スクレイピング実行
echo.
set /p url="スクレイピング対象URLを入力: "
echo.
echo 抽出タイプを選択:
echo 1. summary (要約)
echo 2. keywords (キーワード)
echo 3. structure (構造化)
echo 4. analysis (詳細分析)
echo.
set /p choice="選択 (1-4): "

if "%choice%"=="1" set extraction=summary
if "%choice%"=="2" set extraction=keywords
if "%choice%"=="3" set extraction=structure
if "%choice%"=="4" set extraction=analysis

python scripts/run_scraper.py %url% --method full --ai-extraction %extraction% --verbose
echo.
pause