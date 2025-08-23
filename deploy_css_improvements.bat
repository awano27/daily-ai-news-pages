@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🎨 CSS改善をGitHubにデプロイ中...

echo 📝 CSS変更をコミット...
git add style_enhanced_ranking.css
git commit -m "feat: Enhanced CSS design improvements

🎨 Visual enhancements:
✅ Gradient backgrounds and animations
✅ Improved shadows and depth
✅ Card hover scale effects
✅ Priority indicators with emoji animations

🖱️ Interaction improvements:
✅ Button hover effects with shimmer
✅ Search box with magnifying glass icon
✅ Tab underline animations
✅ Card left border hover effect

📐 Layout enhancements:
✅ KPI cards with gradient top line
✅ Filter controls with labels
✅ Sticky header with backdrop blur
✅ Custom scrollbar styling

🎯 Color and contrast:
✅ Priority-based gradient backgrounds
✅ Score badges with star icons
✅ Enhanced tech tag hover effects
✅ Improved action button depth

🧪 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
[skip ci]"

echo 📤 GitHubにプッシュ...
git push origin main

echo.
echo ✅ CSS改善版がGitHub Pagesにデプロイ完了!
echo 🔗 https://awano27.github.io/daily-ai-news-pages/
echo.
echo 🎉 改善効果:
echo • 視覚的な洗練度向上
echo • インタラクションの強化
echo • レイアウトの最適化
echo • ユーザー体験の向上
pause