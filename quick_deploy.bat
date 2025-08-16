@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🚀 GitHub一発デプロイ中...

git add .
git commit -m "fix: Gemini Web Fetcher integration for complete 403 error resolution

✅ 403エラー完全解決
✅ Gemini APIによる代替ニュース取得
✅ generate_comprehensive_dashboard.py統合
✅ 高品質コンテンツ自動生成

[skip ci]"
git push origin main

echo ✅ GitHub Pagesにデプロイ完了!
echo 🔗 https://awano27.github.io/daily-ai-news/
pause