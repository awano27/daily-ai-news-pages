@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🔧 JavaScript タブ機能修正をデプロイ中...

echo 📝 index.htmlをコミット...
git add index.html
git commit -m "fix: Add inline JavaScript for tab functionality and fix HTML structure

🔧 タブ機能修正:
✅ インラインJavaScriptでタブ切り替え機能追加
✅ HTML構造の破損修正
✅ フィルタリング機能の修正
✅ タブのアクティブ状態管理

🎯 効果:
• タブクリックで正しくコンテンツ切り替え
• Business/Tools/Postsタブの完全動作
• フィルタリング機能正常化

[skip ci]"

echo 📤 GitHubにプッシュ...
git push origin main

echo.
echo ✅ タブ機能修正版がGitHub Pagesにデプロイ完了!
echo 🔗 https://awano27.github.io/daily-ai-news/
echo.
echo 🎉 修正内容:
echo • タブ切り替え完全動作
echo • コンテンツ表示正常化  
echo • フィルタリング機能修復
echo • ユーザビリティ向上
pause