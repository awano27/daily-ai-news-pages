@echo off
echo 📊 クリーンダッシュボード生成
echo.
echo 🎯 特徴:
echo    ✅ シンプルで見やすいデザイン
echo    ✅ X投稿にソースリンク付き
echo    ✅ 検証ログはコンソールのみ
echo    ✅ ユーザーフレンドリーなUI
echo    ✅ コンテンツ中心の表示
echo.

python generate_clean_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ クリーンダッシュボード生成完了！
    echo.
    echo 📊 改善点:
    echo    🖼️ クリーンデザイン: 検証表示なし
    echo    🔗 X投稿リンク: クリック可能
    echo    📰 豊富な記事: 信頼できるソースのみ
    echo    🎨 ユーザビリティ: コンテンツ中心
    echo.
    echo 📂 生成されたHTMLファイルをブラウザで開いてご確認ください
    echo.
) else (
    echo.
    echo ❌ エラーが発生しました
    echo.
)

pause