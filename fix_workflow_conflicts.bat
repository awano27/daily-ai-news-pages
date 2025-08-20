@echo off
chcp 65001 >nul
echo 🔧 Fix GitHub Actions Workflow Conflicts
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📝 修正内容:
echo - enhanced-daily-build.yml に同時実行制限追加
echo - deploy-to-public.yml のワークフロー名修正と同時実行制限追加
echo - これでキャンセルエラーが解決されます
echo.

echo 🔄 修正をコミット...
git add .github/workflows/enhanced-daily-build.yml
git add .github/workflows/deploy-to-public.yml
git commit -m "fix: Add concurrency controls to prevent workflow conflicts

- Add concurrency group to enhanced-daily-build.yml
- Update workflow_run reference in deploy-to-public.yml  
- Prevent simultaneous execution conflicts"

echo.
echo 🚀 GitHubにプッシュ...
git push origin main

echo.
echo ✅ 修正完了!
echo.
echo 📋 次のステップ:
echo 1. GitHub Actions でワークフローが正常実行されることを確認
echo 2. キャンセルエラーが解消されることを確認
echo 3. サイトが正常にデプロイされることを確認
echo.
echo 🌐 確認URL:
echo - Actions: https://github.com/awano27/daily-ai-news/actions
echo - Site: https://awano27.github.io/daily-ai-news-pages/
echo.
pause