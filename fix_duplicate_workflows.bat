@echo off
chcp 65001 >nul
echo 🔧 Fix Duplicate Enhanced Workflows - Final Solution
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📝 問題:
echo - Enhanced Daily AI News (Full Pipeline)
echo - Enhanced Daily AI News Build (Gemini URL Context) 
echo 2つの類似ワークフローが存在して混乱
echo.

echo ✅ 修正内容:
echo - build.yml: 完全無効化 (全てのトリガー削除)
echo - enhanced-daily-build.yml: 唯一の有効なEnhancedワークフロー
echo.

echo 🔄 修正をコミット...
git add .github/workflows/build.yml
git commit -m "fix: Completely disable duplicate Enhanced workflow

- Remove all triggers from build.yml to prevent execution  
- Keep only enhanced-daily-build.yml as the single Enhanced workflow
- This eliminates confusion between similar workflow names"

echo.
echo 🚀 GitHubにプッシュ...
git push origin main

echo.
echo ✅ 修正完了!
echo.
echo 📋 これで残るのは1つだけ:
echo "Enhanced Daily AI News (Full Pipeline)" - enhanced-daily-build.yml
echo.
echo 🎯 次のステップ:
echo 1. GitHub Actions ページで確認
echo 2. "Enhanced Daily AI News (Full Pipeline)" のみ表示される
echo 3. このワークフローを手動実行
echo 4. 成功すれば Enhanced AI News System 完全稼働
echo.
echo 🌐 確認URL:
echo - Actions: https://github.com/awano27/daily-ai-news/actions
echo - Site: https://awano27.github.io/daily-ai-news-pages/
echo.
pause