@echo off
chcp 65001 >nul
echo 🚀 Fix Deploy Now - 即座にデプロイ問題を解決
echo ======================================================
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo.
echo 📋 現在の状況:
echo - リモートに新しい変更があるためプッシュが拒否されています
echo - ローカルとリモートを同期してからプッシュが必要です
echo.

echo 🔄 Step 1: リモートの最新情報を取得...
git fetch origin

echo.
echo 🔄 Step 2: ローカルの変更を一時保存...
git stash push -m "accessibility-improvements-backup"

echo.
echo 🔄 Step 3: リモートの変更を取得...
git pull origin main

echo.
echo 🔄 Step 4: 保存した変更を復元...
git stash pop

echo.
echo 🔄 Step 5: 変更を再度コミット...
git add style.css
git commit -m "enhance: Improve accessibility and visual hierarchy

• WCAG AA compliant color contrast (4.5:1+)
• Enhanced visual hierarchy with proper spacing  
• Improved KPI area prominence and layout
• Accessible tab navigation with focus indicators
• Better chip design with visual indicators
• Mobile-first responsive improvements
• Enhanced touch targets and hover states

🎯 Fixed deployment sync issues"

echo.
echo 🚀 Step 6: GitHubにプッシュ...
git push origin main

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ デプロイ成功!
    echo.
    echo 🌐 確認URL:
    echo - GitHub Actions: https://github.com/awano27/daily-ai-news/actions
    echo - 改善サイト: https://awano27.github.io/daily-ai-news/
    echo.
    echo ⏱️ サイト反映まで2-3分お待ちください
) else (
    echo ❌ デプロイに失敗しました
    echo 💡 smart_deploy.py を実行してください
    echo python smart_deploy.py
)

echo.
pause