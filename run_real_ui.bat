@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 実データを使用した改善UI生成中...

python generate_real_data_ui.py

if exist "index_improved_real.html" (
    echo.
    echo ✅ 実データ改善版ダッシュボード生成完了！
    echo 📄 ファイル: index_improved_real.html
    echo.
    echo 🚀 ブラウザで開きますか？
    pause
    start index_improved_real.html
) else (
    echo.
    echo ❌ ファイル生成に失敗しました
    echo デバッグ情報を確認してください
)
pause