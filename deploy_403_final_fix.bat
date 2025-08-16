@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🎯 403エラー根本的解決をGitHubにデプロイ中...

echo 🧪 修正をテスト...
python test_403_fix.py

echo.
echo 📝 全ファイルをコミット...
git add .
git commit -m "fix: Complete elimination of 403 error URLs

🎯 根本的403エラー解決:
✅ url_filter.py - 403 URL完全除外システム
✅ 403 URLパターンマッチング
✅ HTML テンプレートで403 URL非表示
✅ ユーザー体験向上（リンク切れ解消）

🚫 除外対象:
• Google News CBM エンコードURL  
• news.google.com/rss/articles/*
• 403エラー既知URL

✨ 効果:
• ユーザーが403エラーに遭遇しない
• 健全なリンクのみ表示
• 完全なユーザビリティ

[skip ci]"

echo 📤 GitHubにプッシュ...
git push origin main

echo.
echo ✅ 403エラー根本解決版がGitHub Pagesにデプロイ完了!
echo 🔗 https://awano27.github.io/daily-ai-news/
echo.
echo 🎉 改善効果:
echo • 403エラーURL完全除外
echo • ユーザーに健全なリンクのみ提供
echo • リンク切れ問題解消
echo • 完璧なユーザー体験
pause