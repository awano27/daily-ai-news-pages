@echo off
chcp 65001 > nul
echo 📊 最終改良版AI業界定点観測ダッシュボード
echo.
echo 🎯 完全修正内容:
echo    ✅ X投稿にソースリンク追加
echo    ✅ 要約を分かりやすい日本語に改善
echo    ✅ 元サイトと同じフォーマットに準拠
echo    ✅ "AI業界定点観測（毎日更新）"タイトル復活
echo    ✅ ビジネス実務者向けの実践的要約
echo.

python generate_improved_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 最終改良版ダッシュボード生成完了！
    echo.
    echo 📊 改善点まとめ:
    echo    🔗 X投稿: ソースリンクボタン付き
    echo    📝 要約: "〜すべき"など実践的表現
    echo    🎨 デザイン: 元サイト完全準拠
    echo    📰 タイトル: AI業界定点観測（毎日更新）
    echo    💼 内容: ビジネス判断に役立つ情報
    echo.
    echo 📂 生成されたHTMLファイルをブラウザで開いてご確認ください
    echo.
) else (
    echo.
    echo ❌ エラーが発生しました
    echo.
)

pause