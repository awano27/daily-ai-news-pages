@echo off
echo 🔧 実行中: 修正版ダッシュボード生成
echo.

python generate_corrected_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 修正版ダッシュボード生成完了
    echo 🔗 ソースリンク修正: フォールバックURL機能追加済み
    echo ⏰ X投稿フィルタ: 直近48時間データのみ表示設定済み
) else (
    echo.
    echo ❌ エラーが発生しました。詳細をご確認ください。
)

pause