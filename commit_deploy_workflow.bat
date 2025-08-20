@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo GitHub Pages分離デプロイワークフローを追加中...

git add .github/workflows/deploy-to-public.yml setup-public-repo.md

git commit -m "feat: Add workflow to deploy to public GitHub Pages repository

- Create deploy-to-public.yml workflow for automatic deployment
- Triggers on main branch HTML changes and successful builds
- Supports manual workflow dispatch
- Copies built files to separate public repository
- Maintains separation between private source and public site
- Includes setup documentation for configuration

This enables free GitHub Pages hosting while keeping source code private.

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"

echo プッシュ中...
git pull origin main --no-edit
git push origin main

echo.
echo ✅ デプロイワークフローがGitHubにプッシュされました！
echo.
echo 📝 次のステップ:
echo 1. GitHubでPersonal Access Tokenを作成
echo 2. daily-ai-newsリポジトリのSecretsにPERSONAL_TOKENを追加
echo 3. daily-ai-news-pagesという新しいPublicリポジトリを作成
echo 4. 詳細はsetup-public-repo.mdを参照
pause