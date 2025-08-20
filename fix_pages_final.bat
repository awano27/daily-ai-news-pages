@echo off
echo 🔧 Final GitHub Pages Branch Fix
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📝 修正内容:
echo - deploy-to-public.yml: publish_branch を gh-pages に戻す
echo - これで GitHub Pages が正常に動作します
echo.

echo 🔄 修正をコミット...
git add .github/workflows/deploy-to-public.yml
git commit -m "fix: Revert to gh-pages branch for GitHub Pages deployment"

echo.
echo 🚀 GitHubにプッシュ...
git push origin main

echo.
echo ✅ 修正完了!
echo.
echo 📋 今すぐやること:
echo 1. GitHub Pages設定を開く
echo    https://github.com/awano27/daily-ai-news-pages/settings/pages
echo.
echo 2. Source設定:
echo    - Source: Deploy from a branch
echo    - Branch: gh-pages (これを選択)
echo    - Folder: / (root)
echo    - Save をクリック
echo.
echo 3. Enhanced ワークフローを手動実行
echo    https://github.com/awano27/daily-ai-news/actions
echo.
echo 🎯 これで完全に動作します!
pause