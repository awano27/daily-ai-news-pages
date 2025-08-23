@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🔧 HTML構造修正とCSS生成機能を強制アップデート中...

echo 📝 ファイルを追加...
git add build_simple_ranking.py

echo 💾 コミット中...
git commit -m "fix: Tab functionality repair - JavaScript hidden class logic 2025-08-23

✅ Fix tab switching using hidden class instead of active class
✅ Update tab panel HTML generation (hidden vs active)
✅ Fix filterCards function to find visible panels correctly
✅ Enhanced card template with proper HTML structure
✅ CSS generation function confirmed present"

echo 📤 GitHubにプッシュ中...
git push origin main

echo ✅ HTML構造修正版がプッシュ完了！
echo 🔄 GitHub Actionsが自動で開始されます (~30秒後)
echo 🌐 サイト確認: https://awano27.github.io/daily-ai-news-pages/
echo ⏱️ 完了予定: 5-10分後
echo 📋 期待される修正:
echo   - タブ機能が正常に動作 (Business/Tools/Posts切り替え)
echo   - 正しいHTML構造 (enhanced-card template)
echo   - CSS スタイリング適用
echo   - 現在日付 (2025-08-23) 表示
echo   - 情報量維持 + ランキングシステム

pause