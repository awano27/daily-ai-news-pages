@echo off
echo 🎨 元サイトスタイル準拠ダッシュボード生成
echo.
echo 🎯 特徴:
echo    ✅ 元サイト(awano27.github.io)のデザイン準拠
echo    ✅ KPIグリッド・カテゴリカード構造復活
echo    ✅ 情報収集元を大幅拡張
echo    ✅ エグゼクティブサマリー表示
echo    ✅ SNS投稿セクション追加
echo.

python generate_original_style_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 元サイトスタイルダッシュボード生成完了！
    echo.
    echo 📊 元サイトの特徴を再現:
    echo    🎨 オリジナルデザイン: 青基調のモダンUI
    echo    📊 KPIダッシュボード: 統計情報表示
    echo    📂 カテゴリー分け: Business/Tools/Posts
    echo    📈 グリッドレイアウト: レスポンシブ対応
    echo    📱 SNS統合: X投稿表示
    echo.
    echo 📂 生成されたHTMLファイルをブラウザで開いてご確認ください
    echo.
) else (
    echo.
    echo ❌ エラーが発生しました
    echo.
)

pause