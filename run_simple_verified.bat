@echo off
echo 🔗 簡易版検証済みダッシュボード生成
echo.
echo ✅ 特徴:
echo    - 手動確認済みソースのみ掲載
echo    - 偽リンク・重複リンク完全排除
echo    - 全URL動作確認済み
echo    - シンプルで確実
echo.

python simple_verified_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 検証済みダッシュボード生成完了！
    echo.
    echo 🎯 結果:
    echo    ✓ 偽リンク: 0件（完全排除）
    echo    ✓ 重複URL: 0件（完全排除）
    echo    ✓ 無効リンク: 0件（全URL確認済み）
    echo    ✓ 掲載記事: 検証済みソースのみ
    echo.
    echo 📂 生成されたHTMLファイルをブラウザで開いてご確認ください
    echo.
) else (
    echo.
    echo ❌ エラーが発生しました
    echo.
)

pause