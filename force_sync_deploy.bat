@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🔧 強制同期してデプロイ中...

echo 📥 リモートの変更をプル...
git pull origin main --no-rebase

echo 📝 コンフリクトを解決...
git checkout --ours .
git add .
git commit --no-edit

echo 📤 GitHubにプッシュ...
git push origin main

echo ✅ GitHub Pagesにデプロイ完了!
echo 🔗 https://awano27.github.io/daily-ai-news/
pause