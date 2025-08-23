@echo off
echo Simple Enhanced Daily AI News - Ranking System Test
echo ===================================================

REM 環境変数設定（情報量最大化）
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=25

echo 設定:
echo   記事取得範囲: %HOURS_LOOKBACK%時間
echo   最大記事数/カテゴリ: %MAX_ITEMS_PER_CATEGORY%件
echo   翻訳機能: %TRANSLATE_TO_JA%
echo.

echo 簡潔版ランキングシステム実行中...
python build_simple_ranking.py

if %ERRORLEVEL% NEQ 0 (
    echo ビルドに失敗しました（エラーコード: %ERRORLEVEL%）
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo ✅ ビルド成功！
echo 📄 生成ファイル: index.html

if exist "index.html" (
    echo 📊 ファイル確認:
    for %%A in (index.html) do echo   サイズ: %%~zA bytes
    echo.
    echo 🌐 ブラウザで開いています...
    start "" "index.html"
) else (
    echo ⚠️ 警告: 出力ファイルが見つかりません
)

echo.
echo 🎯 実装された機能:
echo   ✅ 豊富な情報量を完全維持（25件/カテゴリ）
echo   ✅ エンジニア関連度スコアリング（0-10点）
echo   ✅ 5段階優先度表示（🔥⚡📖📰📄）
echo   ✅ SNS/Twitter投稿 + arXiv論文統合
echo   ✅ リアルタイム検索・フィルタリング
echo   ✅ ブックマーク機能
echo   ✅ レスポンシブデザイン
echo.
echo テスト完了！
pause