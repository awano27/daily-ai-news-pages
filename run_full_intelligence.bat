@echo off
cd /d "%~dp0"
echo 🚀 全情報取得モード
echo.
echo 実行オプション:
echo   1. フル分析    - 全カテゴリ5件ずつ、全AI分析タイプ (推奨)
echo   2. 大容量分析  - 全カテゴリ10件ずつ、全AI分析タイプ  
echo   3. 超大容量    - 全カテゴリ15件ずつ、全AI分析タイプ
echo   4. クイック    - 全カテゴリ2件ずつ、要約のみ (テスト用)
echo.
set /p choice="選択 (1-4): "

if "%choice%"=="1" (
    echo 🎯 フル分析を実行中...
    python run_comprehensive_analysis.py --max-per-category 5
) else if "%choice%"=="2" (
    echo 🎯 大容量分析を実行中...
    python run_comprehensive_analysis.py --max-per-category 10
) else if "%choice%"=="3" (
    echo 🎯 超大容量分析を実行中...
    python run_comprehensive_analysis.py --max-per-category 15
) else if "%choice%"=="4" (
    echo ⚡ クイック分析を実行中...
    python run_comprehensive_analysis.py --quick
) else (
    echo ❌ 無効な選択です
    goto :end
)

echo.
echo ✅ 実行完了！生成されたJSONファイルを確認してください。
:end
pause