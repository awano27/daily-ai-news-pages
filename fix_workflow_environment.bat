@echo off
echo 🔧 GitHub Actions 環境保護ルール修正
echo =================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 修正内容:
echo - environment: github-pages を削除
echo - X_POSTS_CSV 環境変数を追加
echo - python-dateutil 依存関係を追加
echo - HOURS_LOOKBACK を 48 に変更

echo 📤 修正をGitHubにプッシュ...
git add .github/workflows/deploy-pages.yml
git commit -m "fix: Remove environment protection rules and add X posts configuration"
git push origin main

echo ✅ ワークフロー修正完了!
echo 🚀 新しいGitHub Actionが自動実行されます
echo 🕐 数分後にサイトが更新されるはずです

pause