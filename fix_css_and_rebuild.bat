@echo off
echo CSS崩れ修正＆再ビルド
echo ========================

REM 環境変数設定
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=25
set X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0

echo 強化版を再生成中...
python build_simple_ranking.py

if %ERRORLEVEL% NEQ 0 (
    echo ❌ ビルドに失敗しました
    pause
    exit /b %ERRORLEVEL%
)

echo ✅ ビルド完了！

echo GitHubにプッシュ中...
git add index.html style_enhanced_ranking.css
git commit -m "fix: CSS reference and rebuild enhanced version

✅ Fixed CSS link to style_enhanced_ranking.css  
✅ Rebuilt with proper SNS/arXiv integration
✅ 24+ articles with engineer ranking system

🧪 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin main

echo ✅ デプロイ完了！
echo 🌐 数分後にhttps://awano27.github.io/daily-ai-news/で確認できます

pause