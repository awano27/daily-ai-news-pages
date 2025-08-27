@echo off
echo 🚨 Xポスト優先統合修正版デプロイ
echo ===============================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 修正内容:
echo - Xポストのスコアを10.0に強制設定（最優先表示）
echo - X_POSTS_CSV環境変数の値をログ出力
echo - HOURS_LOOKBACKの値をログ出力
echo - 取得したXポストの詳細情報をログ出力
echo - Xポスト統合の全過程をデバッグ出力

echo 📤 GitHubにデプロイ...
git add build_simple_ranking.py
git commit -m "fix: Force X posts display with score 10.0 and enhanced debug logging"
git push origin main

echo ✅ デバッグ強化版デプロイ完了!
echo 🔍 GitHub Actionsログで以下を確認:
echo    - "🔍 DEBUG: X_POSTS_CSV環境変数"
echo    - "🔍 DEBUG: X投稿取得完了"
echo    - "🔍 DEBUG: Xポスト[N] - タイトル"
echo    - "✅ Found X X posts in generated HTML"

pause