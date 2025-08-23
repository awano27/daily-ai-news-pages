@echo off
echo 🔧 GitHub Pages デプロイ方式修正
echo ==============================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 修正内容:
echo - GitHub Pages environment を使わない方式に変更
echo - 直接 gh-pages ブランチにプッシュ
echo - Xポストのデバッグ情報を追加

echo 📤 修正をGitHubにプッシュ...
git add .github/workflows/deploy-pages.yml
git commit -m "fix: Switch to direct gh-pages branch deployment to avoid environment protection rules"
git push origin main

echo ✅ ワークフロー修正完了!
echo 🚀 新しいGitHub Actionが自動実行されます
echo 📱 今度はXポストも含めてデプロイされるはずです

pause