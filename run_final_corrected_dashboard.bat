@echo off
echo 🔧 実行中: 最終修正版ダッシュボード生成
echo 🎯 修正内容:
echo    - 個別記事URLの正確な抽出
echo    - ソースリンクが具体的な記事に移動
echo    - 48時間以内のX投稿フィルタリング
echo.

python generate_corrected_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 最終修正版ダッシュボード生成完了
    echo 🔗 ソースリンク修正: 個別記事URLを正確に抽出
    echo ⏰ X投稿フィルタ: 直近48時間データのみ表示
    echo 📊 デバッグ情報: URL抽出過程を詳細表示
) else (
    echo.
    echo ❌ エラーが発生しました。詳細をご確認ください。
)

pause