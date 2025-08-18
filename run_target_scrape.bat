@echo off
cd /d "%~dp0"
echo 🎯 対象URL別スクレイピング
echo.
echo 利用可能カテゴリ:
echo   1. ai_news      - AI関連ニュース
echo   2. ai_research  - AI研究・企業ブログ  
echo   3. tech_news    - テクノロジーニュース
echo   4. business     - ビジネス・スタートアップ
echo.
set /p category="カテゴリを入力 (ai_news/ai_research/tech_news/business): "
set /p max_urls="最大URL数 (デフォルト: 3): "

if "%max_urls%"=="" set max_urls=3

python target_urls.py %category% %max_urls%
echo.
pause