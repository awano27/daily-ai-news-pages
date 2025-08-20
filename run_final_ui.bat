@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 🎨 最終版UI/UXダッシュボード生成中...

python generate_final_ui_dashboard.py

if exist "index_final.html" (
    echo.
    echo ✅ 最終版ダッシュボード生成完了！
    echo 📄 ファイル: index_final.html
    echo.
    echo 🚀 主な機能:
    echo    - タブ切り替え機能（完全動作）
    echo    - 実データ使用
    echo    - レスポンシブデザイン
    echo    - アクセシビリティ対応
    echo    - キーボードショートカット対応
    echo.
    echo 📱 ブラウザで開いて確認しますか？
    pause
    start index_final.html
) else (
    echo.
    echo ❌ ファイル生成に失敗しました
    echo python generate_final_ui_dashboard.py を直接実行して確認してください
    pause
)