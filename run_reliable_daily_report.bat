@echo off
echo 🎯 Reliable AI Daily Business Report Generator 実行中...
echo.

REM 環境変数設定
set HOURS_LOOKBACK=72
set MAX_ITEMS_PER_CATEGORY=30

REM 実行ディレクトリに移動
cd /d "%~dp0"

echo 📊 信頼性重視設定:
echo   - 動作確認済みフィードのみ使用
echo   - 404/403エラーフィード完全除外
echo   - 過去%HOURS_LOOKBACK%時間のニュース収集
echo   - 高品質フォールバックコンテンツ提供
echo.

echo ✅ 使用する信頼性フィード:
echo   🥇 Tier 1 (主要メディア):
echo      - TechCrunch, VentureBeat AI, The Verge
echo      - MIT Technology Review, Ars Technica
echo   🥈 Tier 2 (専門メディア):
echo      - AI News, Machine Learning Mastery
echo      - Analytics Vidhya, Towards AI
echo   🥉 Tier 3 (コミュニティ):
echo      - Hacker News, Reddit AI/ML
echo   🇯🇵 日本語ソース:
echo      - ASCII.jp, ITmedia AI, ZDNET Japan
echo.

REM Python実行
echo 🤖 信頼性重視日次AIレポート生成開始...
python generate_reliable_daily_report.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ エラーが発生しました。以下を確認してください:
    echo   1. インターネット接続が正常か
    echo   2. 必要なPythonライブラリがインストールされているか
    echo.
    echo 💡 必要ライブラリのインストール:
    echo pip install feedparser requests google-generativeai
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 信頼性重視レポート生成完了！
echo.
echo 📁 生成されたファイル:
if exist reliable_daily_report_latest.html (
    echo   - reliable_daily_report_latest.html ^(最新版^)
)
for %%f in (reliable_daily_report_*.html) do (
    echo   - %%f
)

echo.
echo 🎯 信頼性重視アプローチの利点:
echo   ✅ 404/403エラー完全回避
echo   ✅ 動作確認済みフィードのみ使用
echo   ✅ 高品質情報源による信頼性向上
echo   ✅ ビジネス価値重視の分析・分類
echo   ✅ エグゼクティブ向け最適化デザイン
echo   ✅ 安定したデータ収集・レポート生成
echo.

echo 🌐 信頼性重視レポートを開きますか？ ^(Y/N^)
set /p choice=
if /i "%choice%"=="Y" (
    start reliable_daily_report_latest.html
)

echo.
echo 📋 成果:
echo   - エラー率: 大幅削減 ^(動作確認済みソースのみ^)
echo   - 信頼性: 向上 ^(主要メディア中心^)
echo   - 品質: 向上 ^(ビジネス価値重視フィルタ^)
echo   - 安定性: 向上 ^(フォールバック機能付き^)
echo.
pause