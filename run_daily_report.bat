@echo off
echo 🚀 AI Daily Business Report Generator 実行中...
echo.

REM 環境変数設定
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=30
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google

REM 実行ディレクトリに移動
cd /d "%~dp0"

echo 📊 設定:
echo   - 過去%HOURS_LOOKBACK%時間のニュースを分析
echo   - カテゴリ別最大%MAX_ITEMS_PER_CATEGORY%件
echo   - Gemini AI分析: 有効
echo.

REM Python実行
echo 🤖 日次ビジネスAIレポート生成開始...
python generate_daily_business_report.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ エラーが発生しました。以下を確認してください:
    echo   1. GEMINI_API_KEYが設定されているか
    echo   2. インターネット接続が正常か
    echo   3. 必要なPythonライブラリがインストールされているか
    echo.
    echo 💡 必要ライブラリのインストール:
    echo pip install feedparser pyyaml google-generativeai deep-translator
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 日次レポート生成完了！
echo.
echo 📁 生成されたファイル:
if exist daily_report_latest.html (
    echo   - daily_report_latest.html ^(最新レポート^)
)
for %%f in (daily_report_*.html) do (
    echo   - %%f
)

echo.
echo 🌐 レポートを開きますか？ ^(Y/N^)
set /p choice=
if /i "%choice%"=="Y" (
    start daily_report_latest.html
)

echo.
echo 🎯 今後の自動実行設定:
echo   - タスクスケジューラで毎朝7:00に実行可能
echo   - GitHub Actionsで自動デプロイも設定可能
echo.
pause