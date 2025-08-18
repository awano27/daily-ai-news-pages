@echo off
chcp 65001 > nul
echo 📊 元サイト完全準拠ダッシュボード生成・テスト
echo.
echo 🎯 要件:
echo    ✅ 元サイトと同じフォーマット
echo    ✅ 本日分の情報取得
echo    ✅ Xのソースリンク
echo    ✅ 日本語タイトル
echo.

echo 🧪 要件テスト実行中...
python test_exact_format.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 要件テスト合格！本格生成を開始...
    python generate_exact_format_dashboard.py
    
    if %ERRORLEVEL% == 0 (
        echo.
        echo 🎉 元サイト完全準拠ダッシュボード生成完了！
        echo.
        echo 📊 特徴:
        echo    🎨 元サイトデザイン: 完全準拠
        echo    📰 日本語記事: 全タイトル翻訳済み
        echo    🔗 Xソースリンク: 全投稿にリンク付き
        echo    💡 アクションアイテム: 実務的提案
        echo    ✨ AI選別タグ: 品質表示
        echo.
        echo 📂 生成されたHTMLファイルをブラウザで開いてご確認ください
        echo.
    )
) else (
    echo.
    echo ❌ 要件テスト失敗 - 修正が必要です
    echo.
)

pause