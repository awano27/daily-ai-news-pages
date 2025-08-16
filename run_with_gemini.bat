@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🤖 Gemini API強化版ダッシュボード生成中...
echo.

REM 環境変数設定
set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=30
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set X_POSTS_CSV="https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"

echo 📊 ダッシュボード生成開始...
python generate_comprehensive_dashboard.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ ダッシュボード生成完了!
    echo.
    echo 🎉 Gemini AI機能:
    echo • ニュース重要度スコア (1-100)
    echo • 市場動向の洞察分析
    echo • エグゼクティブサマリー強化
    echo • 技術トレンドの予測
    echo.
    echo 📁 生成ファイル:
    echo • index.html - AIで強化されたダッシュボード
    echo • dashboard_data.json - 分析データ
    echo.
    echo 🌐 ブラウザで開く: index.html
) else (
    echo.
    echo ❌ エラーが発生しました
)

pause