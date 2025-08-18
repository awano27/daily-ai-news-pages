@echo off
echo 🚀 コンパクト版フルダッシュボード生成
echo.
echo 🤖 特徴:
echo    ✅ Gemini-2.5-flashによるAI検証
echo    ✅ 既存分析データから情報豊富なコンテンツ抽出
echo    ✅ Google SheetsからX投稿データ取得
echo    ✅ AI自動ソース検証・投稿選別
echo    ✅ コンパクトで情報量豊富
echo.

python generate_compact_full_dashboard.py

if %ERRORLEVEL% == 0 (
    echo.
    echo ✅ コンパクト版フルダッシュボード生成完了！
    echo.
    echo 📊 結果:
    echo    🤖 Gemini-2.5-flash: ソース検証・投稿選別
    echo    📰 豊富な記事: 既存分析データ活用
    echo    📱 厳選投稿: Google Sheetsから自動選別
    echo    🔗 高品質: AI検証済みソースのみ
    echo    💎 コンパクト: 情報密度最適化
    echo.
    echo 📂 生成されたHTMLファイルをブラウザで開いてご確認ください
    echo.
) else (
    echo.
    echo ❌ エラーが発生しました
    echo 💡 確認事項:
    echo    - GEMINI_API_KEYが設定されているか
    echo    - google-generativeaiがインストールされているか
    echo    - comprehensive_analysis_20250818_101345.jsonが存在するか
    echo.
)

pause