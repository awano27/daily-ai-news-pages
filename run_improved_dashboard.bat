@echo off
chcp 65001 > nul
echo 📊 改良版AI業界ダッシュボード生成
echo.
echo 🎯 改善内容:
echo    ✅ feeds.ymlから全RSSフィード取得
echo    ✅ 48時間分のデータ取得に拡張
echo    ✅ UTF-8エンコーディング対応
echo    ✅ X投稿の文字化け修正
echo    ✅ フォールバックデータ実装
echo.

python generate_improved_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 改良版ダッシュボード生成完了！
    echo.
    echo 📊 期待される改善:
    echo    📰 豊富な記事数: feeds.yml全ソース活用
    echo    🎨 元サイトデザイン: 青基調のモダンUI
    echo    📱 正常なX投稿: 文字化け解消
    echo    📂 カテゴリー分け: Business/Tools/Posts
    echo    📈 KPI表示: 統計ダッシュボード
    echo.
    echo 📂 生成されたHTMLファイルをブラウザで開いてご確認ください
    echo.
) else (
    echo.
    echo ❌ エラーが発生しました
    echo 確認事項:
    echo    - feeds.ymlが存在するか
    echo    - Pythonパッケージがインストール済みか
    echo    - ネットワーク接続が正常か
    echo.
)

pause