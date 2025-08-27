@echo off
echo 🚀 実際のXポストをデプロイ中...
echo ==============================

echo ✓ 実際のXポストデータをHTMLに反映済み

echo 📤 GitHubにコミット中...
git add index.html
git commit -m "feat: Replace dummy X posts with real CSV data from users"
git push origin main

echo 🎉 実際のXポストのデプロイ完了！
echo 数分でサイトに反映されます
echo.
echo 含まれるXポスト:
echo - @oikon48: Anthropic Computer Use API
echo - @godofprompt: Chain-of-Verification手法
echo - @suh_sunaneko: Hugging Face Transformers
echo - @newsfromgoogle: Google Sparse Expert Models
echo - @pop_ikeda: MLOpsパイプライン事例
echo.
pause