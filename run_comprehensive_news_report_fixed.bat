@echo off
echo 🎯 包括的AI Daily Intelligence Report Generator (修正版) 実行中...
echo.

REM 環境変数設定
set HOURS_LOOKBACK=48
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

REM 実行ディレクトリに移動
cd /d "%~dp0"

echo 📊 修正版：依存関係の簡素化
echo   ❌ pandas 依存を完全除去
echo   ✅ 標準ライブラリのみ使用
echo   ✅ CSV処理を軽量化
echo   ✅ エラーハンドリング強化
echo.

echo 🔧 修正内容:
echo   - pandas → 標準csv + io.StringIO
echo   - pytz → 標準datetime
echo   - 複数CSV カラム名対応
echo   - スコア計算アルゴリズム最適化
echo   - フォールバック機能追加
echo.

echo 📦 必要ライブラリ（最小限）:
echo   - feedparser (RSS解析)
echo   - requests (HTTP通信)
echo   - google-generativeai (Gemini分析・オプション)
echo.

echo 🎯 包括的情報収集システム:
echo   RSS フィード + X(Twitter)投稿の統合
echo   過去%HOURS_LOOKBACK%時間のデータ収集
echo   ビジネス価値重視のスコア算出
echo   Good News自動抽出
echo.

REM Python実行
echo 🤖 修正版包括的AIレポート生成開始...
python generate_comprehensive_news_report_fixed.py

if %errorlevel% neq 0 (
    echo.
    echo ❌ エラーが発生しました。以下を確認してください:
    echo   1. インターネット接続が正常か
    echo   2. 必要なPythonライブラリがインストールされているか
    echo.
    echo 💡 必要ライブラリのインストール（最小限）:
    echo pip install feedparser requests
    echo.
    echo 💡 Gemini分析を有効にする場合（オプション）:
    echo pip install google-generativeai
    echo set GEMINI_API_KEY=your_api_key_here
    echo.
    pause
    exit /b 1
)

echo.
echo ✅ 修正版包括的AIレポート生成完了！
echo.
echo 📁 生成されたファイル:
if exist comprehensive_ai_report_fixed_latest.html (
    echo   - comprehensive_ai_report_fixed_latest.html ^(最新修正版^)
)
for %%f in (comprehensive_ai_report_fixed_*.html) do (
    echo   - %%f
)

echo.
echo 🎯 修正版の改善点:
echo   📦 依存関係: 大幅削減 ^(pandas除去^)
echo   🚀 起動速度: 高速化
echo   🛠️ エラー処理: 強化
echo   📊 CSV処理: 軽量化
echo   💪 安定性: 向上
echo   🔄 フォールバック: 追加
echo.

echo 🌐 修正版レポートを開きますか？ ^(Y/N^)
set /p choice=
if /i "%choice%"=="Y" (
    start comprehensive_ai_report_fixed_latest.html
)

echo.
echo 📋 修正版の利点:
echo   - 軽量: 標準ライブラリ中心
echo   - 高速: 依存関係最小化
echo   - 安定: エラーハンドリング強化
echo   - 互換: 幅広い環境で動作
echo.
pause