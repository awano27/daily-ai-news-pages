@echo off
echo 🎯 包括的AI Daily Intelligence Report Generator 実行中...
echo.

REM 環境変数設定
set HOURS_LOOKBACK=48
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

REM 実行ディレクトリに移動
cd /d "%~dp0"

echo 📊 包括的情報収集システム設定:
echo   - RSS フィード: 動作確認済み高信頼性ソース
echo   - X(Twitter)投稿: CSVデータソース統合
echo   - 対象期間: 過去%HOURS_LOOKBACK%時間
echo   - ドメイン制限: 許可サイトのみ
echo   - 重複除去: 高精度アルゴリズム
echo.

echo 🌐 統合情報ソース:
echo   RSS フィード:
echo   📰 Tier 1: TechCrunch, VentureBeat, The Verge, MIT Tech Review
echo   📰 Tier 2: AI News, Machine Learning Mastery, Analytics Vidhya
echo   📰 Tier 3: Hacker News, Reddit AI/ML
echo   📰 日本語: ASCII.jp, ITmedia, ZDNET Japan
echo.
echo   X(Twitter)投稿:
echo   📱 リアルタイム速報情報
echo   📱 スコア重み付け (0-10点)
echo   📱 Good News 自動判定
echo   📱 カテゴリ自動分類
echo.

echo 🎯 情報量増加の改善策:
echo   ✅ X投稿データによるリアルタイム情報追加
echo   ✅ RSS フィード拡張（追加英語ソース）
echo   ✅ 48時間データ収集期間
echo   ✅ 許可ドメイン制限で品質維持
echo   ✅ 重複除去で効率的情報整理
echo   ✅ Good News 特別セクション
echo.

REM Python実行
echo 🤖 包括的AIレポート生成開始...
python generate_comprehensive_news_report.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ エラーが発生しました。以下を確認してください:
    echo   1. インターネット接続が正常か
    echo   2. 必要なPythonライブラリがインストールされているか
    echo.
    echo 💡 必要ライブラリのインストール:
    echo pip install feedparser requests pandas pytz google-generativeai
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 包括的AIレポート生成完了！
echo.
echo 📁 生成されたファイル:
if exist comprehensive_ai_report_latest.html (
    echo   - comprehensive_ai_report_latest.html ^(最新版^)
)
for %%f in (comprehensive_ai_report_*.html) do (
    echo   - %%f
)

echo.
echo 🎯 情報量増加の成果:
echo   📈 情報源の多様化: RSS + X投稿の統合
echo   📈 リアルタイム性: X投稿による速報情報
echo   📈 収集期間拡張: 48時間データ対象
echo   📈 品質維持: スコア重み付けシステム
echo   📈 Good News抽出: 重要情報の特別表示
echo   📈 エグゼクティブ最適化: ビジネス価値重視
echo.

echo 🌐 包括的レポートを開きますか？ ^(Y/N^)
set /p choice=
if /i "%choice%"=="Y" (
    start comprehensive_ai_report_latest.html
)

echo.
echo 📊 期待される改善効果:
echo   - 情報量: 2-3倍増加 ^(RSS + X統合^)
echo   - 速報性: リアルタイム情報追加
echo   - 多様性: ソース種別の拡張
echo   - 品質: スコア重み付けで精度向上
echo   - 利便性: Good News特別セクション
echo.
pause