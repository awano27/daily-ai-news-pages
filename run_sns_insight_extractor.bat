@echo off
echo 📱 SNSインサイト抽出エージェント実行中...
echo.

REM 実行ディレクトリに移動
cd /d "%~dp0"

echo 🔍 SNSインサイト抽出エージェント設定:
echo   - X(Twitter)投稿データ解析
echo   - 48時間フィルタリング
echo   - 有益度スコア計算 (0-10)
echo   - Japanese タイトル生成
echo   - カテゴリ自動分類
echo   - Good News抽出
echo.

echo 📊 処理フロー:
echo   1. CSVデータ取得（Google Spreadsheet）
echo   2. 投稿データ正規化
echo   3. 48時間フィルタリング（strict/lenient対応）
echo   4. 有益度スコア計算
echo   5. HTMLレポート生成
echo.

echo 🎯 特徴:
echo   ✅ スコア重み付けシステム（テーマ・具体性・信頼性・鮮度）
echo   ✅ 日本語タイトル自動生成（14字前後）
echo   ✅ カテゴリ分類（6種類）
echo   ✅ Good News特別抽出
echo   ✅ 検証データ付き
echo.

REM Python実行
echo 🤖 SNSインサイト抽出開始...
python sns_insight_extractor.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ エラーが発生しました。以下を確認してください:
    echo   1. インターネット接続が正常か
    echo   2. 必要なPythonライブラリがインストールされているか
    echo.
    echo 💡 必要ライブラリのインストール:
    echo pip install requests
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ SNSインサイト抽出完了！
echo.

echo 📁 生成されたファイル:
if exist sns_insight_report_latest.html (
    echo   - sns_insight_report_latest.html (最新版)
)
for %%f in (sns_insight_report_*.html) do (
    echo   - %%f
)

echo.
echo 🎯 SNSインサイトの特徴:
echo   📱 リアルタイム: X投稿による速報情報
echo   🎯 有益度評価: 0-10点スコアリング
echo   🇯🇵 日本語対応: タイトル自動生成
echo   📊 分類整理: 6カテゴリ自動分類
echo   👍 Good News: 高スコア情報特別表示
echo   🔍 検証可能: データ検証情報付き
echo.

echo 🌐 SNSインサイトレポートを開きますか？ (Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    start sns_insight_report_latest.html
)

echo.
echo 📋 SNSインサイト抽出の利点:
echo   - 速報性: リアルタイム情報キャッチ
echo   - 精度: スコア重み付けで品質保証
echo   - 効率: 日本語要約で理解しやすさ
echo   - 分類: カテゴリ別整理で検索しやすさ
echo   - 検証: 透明性のあるデータ処理
echo.
pause