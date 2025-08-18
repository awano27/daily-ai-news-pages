@echo off
cd /d "%~dp0"
echo 🔄 統合AIデイリーレポート生成中...
echo.
echo 📊 統合システム設定:
echo   - RSS フィード: 高信頼性ソース
echo   - SNS投稿: X(Twitter)データ統合
echo   - 対象期間: 過去48時間
echo   - スコア重み付け: 自動評価
echo   - Good News抽出: 上位情報特別表示
echo.
python generate_unified_daily_report.py
if %errorlevel% neq 0 (
    echo ❌ エラーが発生しました
    pause
    exit /b 1
)
echo ✅ 統合レポート生成完了！
echo.
echo 🌐 統合レポートを開きますか？ (Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    start unified_daily_report_latest.html
)
pause