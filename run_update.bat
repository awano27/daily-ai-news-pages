@echo off
echo ===============================================
echo Enhanced AI News Update - 最新ニュース収集
echo ===============================================
echo.

echo 🔧 環境設定中...
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=48
set MAX_ITEMS_PER_CATEGORY=30
set X_POSTS_CSV="https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"

echo ✅ 環境設定完了
echo.

echo 🚀 Enhanced build.py実行中...
echo   - 過去48時間のニュース収集
echo   - カテゴリあたり最大30記事
echo   - Gemini URL Context統合
echo   - X投稿処理（重複排除・300字要約）
echo.

python build.py

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ ビルド成功！
    echo.
    
    echo 📝 HTMLファイル生成確認...
    if exist news_detail.html (
        echo ✅ news_detail.html 生成完了
        copy news_detail.html index.html
        echo ✅ index.html 更新完了
    ) else (
        echo ❌ news_detail.html が見つかりません
    )
    
    echo.
    echo 🔄 GitHubへのプッシュ準備...
    git add *.html style.css _cache/
    git commit -m "🤖 Enhanced AI News Update - %date% %time% [skip ci]"
    git push origin main
    
    echo.
    echo 🎉 更新完了！
    echo.
    echo 🌐 サイト確認:
    echo    https://awano27.github.io/daily-ai-news-pages/
    echo.
    echo ⏰ 反映時間: 約1-2分
    
) else (
    echo.
    echo ❌ ビルドエラーが発生しました
    echo エラーコード: %ERRORLEVEL%
)

pause