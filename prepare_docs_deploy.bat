@echo off
REM docs デプロイ補助バッチ
REM 1) 先にビルドを実行（例: python build_simple_ranking.py）
REM 2) このバッチを実行して docs を更新

setlocal

if not exist index.html (
  echo [ERROR] index.html が見つかりません。先にビルドを実行してください。
  exit /b 1
)
if not exist style.css (
  echo [ERROR] style.css が見つかりません。先にビルドを実行してください。
  exit /b 1
)

if not exist docs mkdir docs
copy /Y index.html docs\index.html >nul
copy /Y style.css docs\style.css >nul
type NUL > docs\.nojekyll

echo ✅ docs デプロイ準備が完了しました。
echo  - docs\index.html
echo  - docs\style.css
echo  - docs\.nojekyll
echo 次のステップ:
echo   1) 変更をコミット
echo   2) GitHub Pages のソースを main/docs に設定
echo   3) 数分後に https://awano27.github.io/daily-ai-news/ を確認

endlocal
exit /b 0

