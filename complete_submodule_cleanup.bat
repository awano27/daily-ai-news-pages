@echo off
echo 🔧 完全サブモジュール削除
echo ======================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 1. 現在のgit状態確認...
git status

echo 2. .gitmodulesファイル完全削除...
if exist .gitmodules (
    del .gitmodules
    echo ✅ .gitmodules削除完了
)

echo 3. 全てのサブモジュール参照削除...
git rm --cached upstream_daily_ai_news 2>nul
git rm --cached up2 2>nul
git rm -r --cached upstream_daily_ai_news 2>nul
git rm -r --cached up2 2>nul

echo 4. サブモジュールディレクトリ削除...
if exist upstream_daily_ai_news (
    rd /s /q upstream_daily_ai_news
    echo ✅ upstream_daily_ai_news削除完了
)
if exist up2 (
    rd /s /q up2
    echo ✅ up2削除完了
)

echo 5. .git/modulesディレクトリ削除...
if exist .git\modules (
    rd /s /q .git\modules
    echo ✅ .git/modules削除完了
)

echo 6. gitインデックスリセット...
git reset HEAD .

echo 7. .gitignoreにサブモジュール追加...
echo upstream_daily_ai_news/ >> .gitignore
echo up2/ >> .gitignore

echo 8. 全ての変更を追加...
git add .

echo 9. サブモジュール完全削除をコミット...
git commit -m "fix: Complete submodule cleanup - remove all submodule references (up2, upstream_daily_ai_news)"

echo 10. 強制プッシュでgh-pagesブランチを更新...
git push origin HEAD:gh-pages --force

echo 11. mainブランチにもプッシュ...
git push origin main

echo ✅ サブモジュール完全削除完了!
echo 🚀 GitHub Pages buildが正常に動作するはずです

pause