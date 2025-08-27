@echo off
echo 🔍 Xポストデバッグ版デプロイ
echo ===========================

cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 📝 デバッグ版の修正内容:
echo - postsカテゴリでのX投稿処理にデバッグ出力追加
echo - fetch_x_posts関数に詳細ログ追加
echo - HTTP応答とデータ内容の詳細表示

echo 📤 GitHubにデバッグ版をデプロイ...
git add build_simple_ranking.py
git commit -m "debug: Add detailed logging for X posts processing in Posts category"
git push origin main

echo ✅ デバッグ版デプロイ完了!
echo 🔍 GitHub ActionsログでX投稿の取得状況が確認できます
echo 📊 ワークフローログで以下を確認:
echo    - "📱 X投稿取得中"
echo    - "🔍 DEBUG: postsカテゴリでX投稿取得開始"
echo    - "📄 受信データサイズ"
echo    - "✅ Found X X posts in generated HTML"

pause