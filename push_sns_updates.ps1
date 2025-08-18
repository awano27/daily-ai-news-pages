# SNS強化ダッシュボードをGitHubにプッシュ
Set-Location "C:\Users\yoshitaka\daily-ai-news"

Write-Host "🚀 SNS強化ダッシュボードをGitHubにプッシュ中..." -ForegroundColor Cyan

# Git操作
Write-Host "`n📥 最新の変更を取得..." -ForegroundColor Yellow
git fetch origin

Write-Host "`n🔄 リモートの変更をマージ..." -ForegroundColor Yellow
git pull origin main --no-edit

Write-Host "`n📝 ファイルをステージング..." -ForegroundColor Yellow
git add generate_sns_enhanced_dashboard.py
git add run_sns_enhanced.bat
git add fetch_x_posts.py
git add push_sns_enhancements.py
git add commit_sns_enhanced.bat

Write-Host "`n💾 変更をコミット..." -ForegroundColor Yellow
$commitMessage = @"
feat: Add SNS enhanced dashboard with Google Sheets integration

- Add generate_sns_enhanced_dashboard.py for Google Sheets X/Twitter data fetching
- Direct CSV download from spreadsheet ID 1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg
- Display 5 featured posts and 5 tech discussions sections
- Automatic data cleaning and importance scoring
- Fallback data when Google Sheets is unavailable
- Responsive tabbed interface for different content categories
- Real-time engagement metrics display

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>
"@

git commit -m $commitMessage

Write-Host "`n📤 GitHubにプッシュ..." -ForegroundColor Yellow
git push origin main

Write-Host "`n✅ SNS強化ダッシュボードがGitHubにプッシュされました！" -ForegroundColor Green
Write-Host "📊 Google Sheets連携によるX投稿データ取得機能が追加されました" -ForegroundColor Green
Write-Host "🔗 https://awano27.github.io/daily-ai-news/" -ForegroundColor Cyan

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")