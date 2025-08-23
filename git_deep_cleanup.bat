@echo off
echo 🔧 Git深層クリーンアップ
echo ========================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 1. Git設定からサブモジュール削除...
git config --remove-section submodule.upstream_daily_ai_news 2>nul
git config --remove-section submodule.up2 2>nul

echo 2. .git/configファイルのサブモジュール設定確認...
if exist .git\config (
    echo .git/config content:
    type .git\config | findstr /C:"submodule" || echo "No submodule entries found"
)

echo 3. インデックスの状態確認...
git ls-files --stage | findstr /C:"upstream_daily_ai_news"
git ls-files --stage | findstr /C:"up2"

echo 4. サブモジュール関連ディレクトリ削除...
if exist .git\modules\upstream_daily_ai_news (
    rd /s /q .git\modules\upstream_daily_ai_news
    echo ✅ .git/modules/upstream_daily_ai_news削除
)
if exist .git\modules\up2 (
    rd /s /q .git\modules\up2
    echo ✅ .git/modules/up2削除
)

echo 5. .gitmodulesファイル再確認...
if exist .gitmodules (
    echo "⚠️ .gitmodulesファイルが存在します:"
    type .gitmodules
    del .gitmodules
) else (
    echo "✅ .gitmodulesファイルなし"
)

echo 6. Git状態最終確認...
git status

echo 7. 必要に応じてクリーンアップコミット...
git add . 2>nul
git commit -m "fix: Deep cleanup of submodule references and git configuration" 2>nul || echo "No changes to commit"

echo 8. リモートプッシュ...
git push origin main
git push origin HEAD:gh-pages --force

echo ✅ Git深層クリーンアップ完了!

pause