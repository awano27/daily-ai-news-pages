@echo off
echo 🎯 Enhanced AI Daily Business Report Generator (Fixed) 実行中...
echo.

REM 環境変数設定（修正版）
set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=30
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google

REM 実行ディレクトリに移動
cd /d "%~dp0"

echo 📊 修正版設定:
echo   - 過去%HOURS_LOOKBACK%時間のニュース収集（拡張）
echo   - SSL証明書エラー対応
echo   - ネットワーク接続エラー回避
echo   - 問題ソースの自動スキップ
echo   - フォールバックコンテンツ提供
echo.

echo 🛠️ エラー対応内容:
echo   ✅ SSL証明書検証の無効化
echo   ✅ 接続タイムアウトの短縮
echo   ✅ リトライ機能の強化
echo   ✅ 問題フィードの自動除外
echo   ✅ データ不足時のフォールバック
echo.

REM Python実行
echo 🤖 修正版日次ビジネスAIレポート生成開始...
python generate_enhanced_daily_report_fixed.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ エラーが発生しました。以下を確認してください:
    echo   1. GEMINI_API_KEYが設定されているか
    echo   2. インターネット接続が正常か
    echo   3. 必要なPythonライブラリがインストールされているか
    echo.
    echo 💡 必要ライブラリのインストール:
    echo pip install feedparser pyyaml google-generativeai deep-translator requests urllib3
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 修正版日次レポート生成完了！
echo.
echo 📁 生成されたファイル:
if exist enhanced_daily_report_fixed_latest.html (
    echo   - enhanced_daily_report_fixed_latest.html ^(最新修正版^)
)
for %%f in (enhanced_daily_report_fixed_*.html) do (
    echo   - %%f
)

echo.
echo 🔧 修正点サマリー:
echo   ✅ ネットワークエラー対応強化
echo   ✅ SSL証明書問題の回避
echo   ✅ 24時間→48時間フィルタに緩和
echo   ✅ 問題ソース自動スキップ機能
echo   ✅ データ不足時フォールバック
echo   ✅ エラー詳細ログ出力
echo.

echo 🌐 修正版レポートを開きますか？ ^(Y/N^)
set /p choice=
if /i "%choice%"=="Y" (
    start enhanced_daily_report_fixed_latest.html
)

echo.
echo 📋 トラブルシューティング:
echo   - ネットワーク接続: インターネット接続を確認
echo   - SSL エラー: 企業ファイアウォール設定確認
echo   - API エラー: GEMINI_API_KEY環境変数確認
echo   - データ不足: 48時間に拡張済み
echo.
pause