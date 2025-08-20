@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"
echo 🧪 Summary Length Fix Test
echo 要約を300文字以内に制限する修正のテスト
echo.

echo 🔧 修正内容:
echo - Gemini強化要約: 200文字以内で生成
echo - 全要約: 最終チェックで300文字制限
echo - フォールバック処理: 300文字制限適用
echo.

echo 📡 テスト実行中...
python test_summary_length.py

echo.
echo 📊 テスト完了
echo 次のステップ: python build.py で実際のサイト生成
pause