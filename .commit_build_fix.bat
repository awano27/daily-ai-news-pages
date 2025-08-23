@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🔧 Committing build script with correct CSS/JS references...

echo 📝 Adding build_simple_ranking.py...
git add build_simple_ranking.py

echo 💾 Committing changes...
git commit -m "fix: Ensure build_simple_ranking.py has correct CSS and inline JS references

✅ CSS reference: style.css (not style_enhanced_ranking.css)
✅ JavaScript: Inline for tab functionality
✅ Ready for GitHub Pages deployment

[skip ci]"

echo 📤 Pushing to GitHub...
git push origin main

echo ✅ Build script updated and pushed to GitHub!
echo 🔗 GitHub Actions will rebuild the site automatically
echo ⏳ Check https://awano27.github.io/daily-ai-news-pages/ in a few minutes

pause