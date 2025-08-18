@echo off
chcp 65001 > nul
echo 📊 参考サイト完全準拠ダッシュボード生成
echo.
echo 🎯 要件:
echo    ✅ https://awano27.github.io/daily-ai-news/ と同じフォーマット
echo    ✅ Google SheetsからX投稿データ取得
echo    ✅ カテゴリ別内容: ビジネス・開発ツール・研究論文
echo    ✅ フッターにLLMアリーナ・AlphaXiv・AIトレンドワードリンク
echo    ✅ ニッチで有益なX投稿を48時間以内から選別
echo    ✅ 全タイトルを日本語に翻訳
echo.

echo 🧪 要件テスト実行中...
python test_reference_format.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 要件テスト合格！本格生成を開始...
    python generate_reference_format_dashboard.py
    
    if %ERRORLEVEL% == 0 (
        echo.
        echo 🎉 参考サイト完全準拠ダッシュボード生成完了！
        echo.
        echo 📊 特徴:
        echo    🎨 デザイン: 参考サイト完全準拠
        echo    📰 記事: カテゴリ別に整理（ビジネス・ツール・研究）
        echo    🔗 X投稿: Google Sheetsから有益な投稿を選別
        echo    💡 インサイト: 各記事にビジネス向けアクションアイテム
        echo    🔗 フッター: LLMアリーナ・AlphaXiv・AIトレンドワード
        echo    ✨ 品質: AI選別タグ付き
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