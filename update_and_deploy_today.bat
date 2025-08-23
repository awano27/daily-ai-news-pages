@echo off
chcp 65001 >nul
echo 🔄 Daily AI News - 最新コンテンツ更新&デプロイ
echo ========================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📅 2025-08-23 の最新AIニュースを収集中...
echo.

REM 環境変数設定
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=25

echo 🔨 サイトビルド実行中...
python build_simple_ranking.py

if %ERRORLEVEL% neq 0 (
    echo ❌ ビルドに失敗しました
    pause
    exit /b 1
)

echo.
echo ✅ ビルド完了！
echo.

echo 📝 変更ファイルを追加...
git add index.html style.css

echo.
echo 💾 2025-08-23の最新コンテンツをコミット...
git commit -m "update: Latest AI news content for 2025-08-23

- Updated with latest AI news and developments
- Rebuilt with current RSS feeds and X posts
- Enhanced ranking system with engineer relevance scores
- Fixed CSS reference to style.css

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

if %ERRORLEVEL% neq 0 (
    echo ⚠️ コミットできませんでした（変更がない可能性があります）
)

echo.
echo 🚨 GitHub に強制プッシュ中...
git push --force origin main

if %ERRORLEVEL% neq 0 (
    echo ❌ プッシュに失敗しました
    pause
    exit /b 1
)

echo.
echo 🎉 最新コンテンツのデプロイ完了！
echo ========================================
echo 🌐 サイト: https://awano27.github.io/daily-ai-news-pages/
echo 📅 更新日: 2025-08-23
echo ⏱️ 反映まで: 2-5分
echo.
echo 📋 更新内容:
echo   - 今日の最新AIニュース
echo   - エンジニア関連度ランキング
echo   - Business/Tools/Posts カテゴリ
echo   - 正しいCSSスタイリング
echo   - タブ機能（完全動作）

pause