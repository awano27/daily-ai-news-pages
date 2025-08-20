@echo off
chcp 65001 >nul
echo 🚀 Quick Fix Enhanced System Deployment
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📝 修正内容:
echo - ダッシュボード生成タイムアウト対策
echo - レポート生成スキップで高速化
echo - コアEnhanced機能にフォーカス
echo.

echo 🔄 修正をコミット...
git add .github/workflows/enhanced-daily-build.yml
git commit -m "fix: Optimize workflow timeout issues for faster deployment

- Skip comprehensive dashboard generation (was causing 5min timeout)
- Skip business report generation (speed optimization)  
- Focus on core Enhanced AI News functionality
- Reduce build time for reliable deployment"

echo.
echo 🚀 GitHubにプッシュ...
git push origin main

echo.
echo ✅ 修正完了!
echo.
echo 📋 次のステップ:
echo 1. GitHub Actions で Enhanced workflow を再実行
echo 2. タイムアウトなしで完了することを確認
echo 3. 新しいEnhanced AI News がデプロイされることを確認
echo.
echo 🎯 期待される結果:
echo - 高速ビルド完了 (5分以内)
echo - Enhanced X post processing 動作
echo - Gemini 強化機能 動作
echo - タイムアウトエラーなし
echo.
echo 🌐 確認URL:
echo - Actions: https://github.com/awano27/daily-ai-news/actions
echo - Site: https://awano27.github.io/daily-ai-news-pages/
echo.
pause