@echo off
chcp 65001 >nul
echo 🚀 GitHub Actions 手動トリガー & ワークフロー修正
echo ===============================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🔧 ワークフロー修正をコミット...
git add .github\workflows\deploy-pages.yml

git commit -m "fix: Correct GitHub Pages URL in workflow

- Fixed deploy-pages.yml to show correct site URL
- Changed from daily-ai-news to daily-ai-news-pages
- This ensures workflow displays proper deployment URL

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

echo 📤 修正をプッシュ...
git push --force origin main

echo.
echo 🔄 GitHub Actions ワークフローを手動トリガー中...

REM GitHub CLI でワークフローをトリガー
gh workflow run deploy-pages.yml

if %ERRORLEVEL% neq 0 (
    echo ⚠️ GitHub CLI でのトリガーに失敗しました
    echo 🔄 ダミーコミットでトリガーします...
    
    REM ダミーファイルを作成してコミット
    echo Manual workflow trigger at %date% %time% > trigger_%date:~0,4%%date:~5,2%%date:~8,2%_%time:~0,2%%time:~3,2%.txt
    
    git add trigger_*.txt
    git commit -m "trigger: Force GitHub Actions workflow execution"
    git push --force origin main
    
    echo ✅ ダミーコミットでワークフローをトリガーしました
) else (
    echo ✅ GitHub CLI でワークフローをトリガーしました
)

echo.
echo 🎯 GitHub Actions 確認:
echo   https://github.com/awano27/daily-ai-news-pages/actions
echo.
echo ⏳ 5-10分後に以下のサイトを確認:
echo   https://awano27.github.io/daily-ai-news-pages/
echo.
echo 📅 期待される内容:
echo   - 最終更新: 2025-08-23 (今日の日付)
echo   - 最新AIニュース 75件
echo   - 正常なCSSスタイリング
echo   - タブ機能の動作

pause