@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo マージコンフリクトを解決中...

echo 1. 新しいダッシュボード版を優先して保持
git checkout --ours index.html

echo 2. ファイルをステージングに追加
git add index.html

echo 3. マージを完了
git commit --no-edit

echo 4. 最終的にプッシュ
git push origin main

echo 解決完了!
echo サイトURL: https://awano27.github.io/daily-ai-news/
pause