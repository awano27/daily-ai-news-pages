@echo off
chcp 65001 >nul
echo 🔧 Fix Workflow Conflicts - Final Solution
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📝 修正内容:
echo - auto_update.yml: 無効化 (古いシステム)
echo - build.yml: 無効化 (古いシステム)  
echo - minimal-build.yml: 無効化 (テスト用)
echo - enhanced-daily-build.yml: 有効 (Enhanced System)
echo - deploy-to-public.yml: 有効 (デプロイメント)
echo.
echo ✅ これで Enhanced AI News System のみが動作します
echo.

echo 🔄 修正をコミット...
git add .github/workflows/auto_update.yml
git add .github/workflows/build.yml
git add .github/workflows/minimal-build.yml
git commit -m "fix: Disable conflicting old workflows to fix deployment

- Disable auto_update.yml (old system)
- Disable build.yml (legacy build)  
- Disable minimal-build.yml (test workflow)
- Keep only enhanced-daily-build.yml (Enhanced System)
- This fixes the old dashboard deployment issue"

echo.
echo 🚀 GitHubにプッシュ...
git push origin main

echo.
echo ✅ 修正完了!
echo.
echo 📋 次のステップ:
echo 1. GitHub Secrets確認: GEMINI_API_KEY 設定済みかチェック
echo 2. Enhanced workflow手動実行してテスト
echo 3. 新しいEnhanced AIニュースサイトがデプロイされることを確認
echo.
echo 🌐 確認URL:
echo - Secrets: https://github.com/awano27/daily-ai-news/settings/secrets/actions
echo - Actions: https://github.com/awano27/daily-ai-news/actions  
echo - Site: https://awano27.github.io/daily-ai-news-pages/
echo.
echo 🎯 Enhanced workflow実行方法:
echo 1. GitHub Actions ページを開く
echo 2. "Enhanced Daily AI News (Full Pipeline)" を選択
echo 3. "Run workflow" をクリック
echo 4. "main" ブランチを選択して実行
echo.
pause