@echo off
echo 🎯 Enhanced AI Daily Business Report Generator 実行中...
echo.

REM 環境変数設定
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=30
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google

REM 実行ディレクトリに移動
cd /d "%~dp0"

echo 📊 改善版設定:
echo   - 信頼性重視のニュース収集
echo   - ビジネスインパクト分析強化
echo   - エグゼクティブ向けUI最適化
echo   - SNS情報の適切な分類
echo   - ROI・投資規模の自動推定
echo.

REM Python実行
echo 🤖 改善版日次ビジネスAIレポート生成開始...
python generate_enhanced_daily_report.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ エラーが発生しました。以下を確認してください:
    echo   1. GEMINI_API_KEYが設定されているか
    echo   2. インターネット接続が正常か
    echo   3. 必要なPythonライブラリがインストールされているか
    echo.
    echo 💡 必要ライブラリのインストール:
    echo pip install feedparser pyyaml google-generativeai deep-translator requests
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 改善版日次レポート生成完了！
echo.
echo 📁 生成されたファイル:
if exist enhanced_daily_report_latest.html (
    echo   - enhanced_daily_report_latest.html ^(最新改善版^)
)
for %%f in (enhanced_daily_report_*.html) do (
    echo   - %%f
)

echo.
echo 🎯 改善点サマリー:
echo   ✅ グラデーション削除・統一カラーパレット採用
echo   ✅ 信頼性重視の情報源分類 (Tier 1-4)
echo   ✅ ビジネスインパクトスコア自動計算
echo   ✅ ROI推定・投資規模の自動抽出
echo   ✅ エグゼクティブサマリー＋アクション提示
echo   ✅ SNS情報の適切な分離・分類
echo   ✅ レスポンシブ対応・視認性向上
echo.

echo 🌐 改善版レポートを開きますか？ ^(Y/N^)
set /p choice=
if /i "%choice%"=="Y" (
    start enhanced_daily_report_latest.html
)

echo.
pause