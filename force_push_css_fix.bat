@echo off
chcp 65001 >nul
echo 🚨 CSS修正 - 強制プッシュ実行
echo ================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📊 現在の状況確認...
git status

echo.
echo 📝 修正されたファイルを追加...
git add index.html style.css

echo.
echo 💾 CSS修正をコミット...
git commit -m "fix: Force update CSS reference to style.css

- Corrected href from style_enhanced_ranking.css to style.css
- This fixes broken styling on GitHub Pages
- Force push to ensure immediate deployment

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

echo.
echo 🚨 GitHub に強制プッシュ中...
git push --force-with-lease origin main

echo.
echo ✅ 強制プッシュ完了！
echo 🔄 GitHub Actions 自動開始予定
echo 🌐 サイト: https://awano27.github.io/daily-ai-news-pages/
echo ⏱️ CSS修正反映まで: 2-5分
echo.
echo 📋 期待される結果:
echo   - サイトのスタイリングが完全復旧
echo   - 色、レイアウト、デザインが正常表示
echo   - タブ機能も継続して動作

pause