@echo off
echo プッシュ処理を開始します...
echo =============================

echo リモートの変更を取得中...
git pull origin main --rebase

echo 修正をプッシュ中...
git push origin main

echo 完了！
echo サイト: https://awano27.github.io/daily-ai-news/
echo 更新反映まで: 2-3分