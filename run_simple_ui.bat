@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 軽量版改善UIダッシュボード生成中...

python generate_simple_improved_ui.py

if exist "index_improved.html" (
    echo ✅ 生成完了: index_improved.html
    echo 📂 ファイルを開きますか？ 
    pause
    start index_improved.html
) else (
    echo ❌ ファイル生成に失敗しました
    pause
)