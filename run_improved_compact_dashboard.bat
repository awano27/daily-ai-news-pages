@echo off
echo 🚀 改良版コンパクトフルダッシュボード生成
echo.
echo 🎯 改善点:
echo    ✅ 記事数大幅増加（信頼ドメイン拡張）
echo    ✅ X投稿データ取得改善（フォールバック付き）
echo    ✅ AI検証プロセスの可視化
echo    ✅ ユーザーフレンドリーな説明追加
echo    ✅ 検証統計レポート表示
echo.

python generate_compact_full_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 改良版コンパクトダッシュボード生成完了！
    echo.
    echo 📊 期待される改善:
    echo    🤖 Gemini-2.5-flash: 高精度AI検証
    echo    📰 豊富な記事: 拡張ドメインリスト対応
    echo    📱 確実な投稿: フォールバック機能付き
    echo    🔍 透明性: 検証プロセス可視化
    echo    📈 詳細統計: AI検証レポート表示
    echo.
    echo 📂 生成されたHTMLファイルをブラウザで開いてご確認ください
    echo.
) else (
    echo.
    echo ❌ エラーが発生しました
    echo 💡 確認事項:
    echo    - comprehensive_analysis_20250818_101345.jsonが存在するか
    echo    - ネットワーク接続が正常か
    echo    - Python依存関係がインストールされているか
    echo.
)

pause