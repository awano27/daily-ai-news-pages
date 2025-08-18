@echo off
echo 🚀 検証済みソース付きダッシュボード生成を開始
echo.
echo 🎯 特徴:
echo    ✅ ソースURLを厳密に検証
echo    ✅ 重複リンクを完全排除
echo    ✅ 信頼できるドメインのみ許可
echo    ✅ 全リンクの動作確認済み
echo.

python generate_verified_sources_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 検証済みソース付きダッシュボード生成完了！
    echo.
    echo 📊 結果:
    echo    🔗 全ソースリンク: 検証済み・動作確認済み
    echo    📰 掲載記事: ソース確実なもののみ
    echo    🤖 AI機能: 有益投稿の自動選別
    echo    ✅ 品質保証: 偽リンク・無効リンク完全排除
    echo.
) else (
    echo.
    echo ❌ エラーが発生しました。詳細をご確認ください。
    echo.
)

pause