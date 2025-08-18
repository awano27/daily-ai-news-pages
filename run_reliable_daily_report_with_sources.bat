@echo off
echo 🎯 Reliable AI Daily Business Report Generator (ソース情報強化版) 実行中...
echo.

REM 環境変数設定
set HOURS_LOOKBACK=72
set MAX_ITEMS_PER_CATEGORY=30

REM 実行ディレクトリに移動
cd /d "%~dp0"

echo 📊 ソース情報強化版設定:
echo   - 動作確認済みフィードのみ使用
echo   - 詳細ソース情報の表示強化
echo   - 元記事へのリンク付与
echo   - 情報源別統計表示
echo   - 信頼性レベル表示
echo.

echo ✅ ソース情報の強化内容:
echo   🔗 元記事リンク: すべてのニュースに元記事URLを表示
echo   📊 ソース統計: 情報源別の記事数を集計表示
echo   🏷️ 信頼性バッジ: Tier 1-3の信頼性レベルを色分け表示
echo   📰 公開日時: 記事の公開日時を表示
echo   🎯 緊急度: 各記事の緊急度レベルを表示
echo.

echo 🥇 使用フィード（動作確認済み）:
echo   Tier 1 主要メディア:
echo   - TechCrunch, VentureBeat AI, The Verge
echo   - MIT Technology Review, Ars Technica
echo.
echo   Tier 2 専門メディア:
echo   - AI News, Machine Learning Mastery
echo   - Analytics Vidhya, Towards AI
echo.
echo   Tier 3 コミュニティ:
echo   - Hacker News, Reddit AI/ML
echo.
echo   日本語ソース:
echo   - ASCII.jp, ITmedia AI, ZDNET Japan
echo.

REM Python実行
echo 🤖 ソース情報強化版AIレポート生成開始...
python generate_reliable_daily_report_with_sources.py

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
echo ✅ ソース情報強化版レポート生成完了！
echo.
echo 📁 生成されたファイル:
if exist reliable_daily_report_with_sources_latest.html (
    echo   - reliable_daily_report_with_sources_latest.html ^(最新版^)
)
for %%f in (reliable_daily_report_with_sources_*.html) do (
    echo   - %%f
)

echo.
echo 🎯 ソース情報強化の特徴:
echo   ✅ 各ニュースに元記事へのクリック可能リンク
echo   ✅ 情報源名と信頼性レベルの明確表示
echo   ✅ 公開日時と緊急度の表示
echo   ✅ 情報源別統計の可視化
echo   ✅ 信頼性レベル別の色分けバッジ
echo   ✅ エグゼクティブ向け最適化デザイン
echo.

echo 🌐 ソース情報強化版レポートを開きますか？ ^(Y/N^)
set /p choice=
if /i "%choice%"=="Y" (
    start reliable_daily_report_with_sources_latest.html
)

echo.
echo 📋 ソース情報の価値:
echo   - 情報の信頼性検証: 元記事で詳細確認可能
echo   - 追加情報取得: 関連記事への展開読み
echo   - 情報源の多様性: バランスの取れた情報収集
echo   - 透明性の確保: 情報の出処を明確化
echo.
pause