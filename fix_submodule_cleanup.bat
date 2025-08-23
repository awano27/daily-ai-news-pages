@echo off
echo 🔧 GitHub Actions サブモジュール エラー修正
echo =======================================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 1. 現在のgit状態確認...
git status

echo 2. .gitmodulesファイル確認・削除...
if exist .gitmodules (
    echo .gitmodules found - removing...
    del .gitmodules
    echo ✅ .gitmodules removed
) else (
    echo No .gitmodules found
)

echo 3. サブモジュールをgitキャッシュから削除...
git rm --cached upstream_daily_ai_news 2>nul
git rm -r --cached upstream_daily_ai_news 2>nul

echo 4. upstream_daily_ai_newsディレクトリを強制削除...
if exist upstream_daily_ai_news (
    echo Removing upstream_daily_ai_news directory...
    rd /s /q upstream_daily_ai_news
    echo ✅ Directory removed
) else (
    echo Directory already removed
)

echo 5. gitインデックスをクリーンアップ...
git reset HEAD . 2>nul

echo 6. 現在のファイルを追加...
git add .

echo 7. サブモジュール修正をコミット...
git commit -m "fix: Remove problematic submodule upstream_daily_ai_news - resolves GitHub Actions error"

echo 8. 修正をGitHubにプッシュ...
git push origin main

echo 9. 最終確認...
git status

echo ✅ サブモジュール問題修正完了!
echo 🚀 GitHub Actions が正常に動作するはずです

pause