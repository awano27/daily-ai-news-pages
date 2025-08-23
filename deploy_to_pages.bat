@echo off
chcp 65001 >nul
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🚀 最新のHTMLとCSS改善をGitHub Pagesにデプロイ中...

echo.
echo 📋 Git状態を確認中...
git status --short

echo.
echo 📁 変更ファイルを追加中...
git add index.html
git add style_enhanced_ranking.css

echo.
echo 💾 変更をコミット中...
git commit -m "feat: Deploy updated content with enhanced CSS design

🆕 コンテンツ更新:
✅ 最新のindex.html (24記事, 2025-08-22 23:43 JST)
✅ 優先度ベースのランキングシステム
✅ エンジニア関連度スコアでソート

🎨 CSS デザイン改善:
✅ モダンなグラデーション背景とアニメーション
✅ カードホバー効果の強化
✅ 優先度インジケーターにアニメーション
✅ スティッキーヘッダーとブラーエフェクト
✅ カスタムスクロールバー
✅ レスポンシブデザイン最適化

🔧 技術的改善:
✅ 検索機能と虫眼鏡アイコン
✅ タブナビゲーションアニメーション
✅ ブックマーク機能
✅ モバイル対応レイアウト

🧪 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>
[skip ci]"

echo.
echo 🌐 GitHub Pagesにプッシュ中...
git push origin main

echo.
echo ===============================================
echo ✅ GitHub Pagesへのデプロイ完了！
echo 🔗 https://awano27.github.io/daily-ai-news-pages/
echo ⏳ 変更が反映されるまで数分かかる場合があります
echo ===============================================
echo.
echo 🎉 デプロイ内容:
echo • ✅ 最新コンテンツ (24記事)
echo • ✅ 強化されたCSS デザイン
echo • ✅ 優先度ベースランキング
echo • ✅ モダンなアニメーション効果
echo • ✅ レスポンシブデザイン
echo • ✅ 改善されたUX/UI
echo.
pause