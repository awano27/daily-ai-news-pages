@echo off
echo 🔧 HTML構造修正をコミット・プッシュ中...
echo.

git add html_fix_trigger_20250823.md
if %ERRORLEVEL% EQU 0 (
    echo ✅ トリガーファイルをステージング
) else (
    echo ❌ ステージングに失敗
    exit /b 1
)

git commit -m "fix: HTML構造修正を強制実行 - enhanced card template確認済み"
if %ERRORLEVEL% EQU 0 (
    echo ✅ コミット完了
) else (
    echo ❌ コミットに失敗 - 変更がない可能性があります
)

git push origin main
if %ERRORLEVEL% EQU 0 (
    echo ✅ GitHubにプッシュ完了
    echo 🚀 GitHub Actions が自動的にトリガーされます
    echo 🌐 5-10分後に https://awano27.github.io/daily-ai-news-pages/ を確認
) else (
    echo ❌ プッシュに失敗
    exit /b 1
)

echo.
echo 🎉 HTML構造修正プロセス完了！
pause