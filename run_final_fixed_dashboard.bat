@echo off
echo 🚀 最終修正版ダッシュボード生成を開始
echo.
echo 🎯 修正・改善内容:
echo    ✅ ソースリンクの正確性向上 - 改良されたURL抽出アルゴリズム
echo    ✅ Google Sheetsから直接X投稿データ取得
echo    ✅ AIによる有益な投稿10件の自動選別
echo    ✅ より詳細なデバッグ情報表示
echo.

python generate_final_fixed_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ 最終修正版ダッシュボード生成完了！
    echo.
    echo 📊 結果:
    echo    🔗 ソースリンク: 具体的な記事URLに正確にリンク
    echo    📱 X投稿: Google SheetsからAI選別済み有益投稿
    echo    🤖 AI機能: 有益性判定・スコアリング・自動選別
    echo    🌐 ブラウザで自動オープン
    echo.
) else (
    echo.
    echo ❌ エラーが発生しました。詳細をご確認ください。
    echo.
)

pause