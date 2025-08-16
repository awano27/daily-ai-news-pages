@echo off
cd /d "C:\Users\yoshitaka\daily-ai-news"

echo 🚀 Gemini API強化版をGitHub Pagesにデプロイ中...

echo 📊 Git状態確認...
git status --porcelain

echo 📝 新ファイルをステージング...
git add gemini_analyzer.py test_gemini.py .env.example deploy_gemini_enhanced.py deploy_gemini_enhanced.bat

echo 💾 変更をコミット...
git commit -m "feat: Gemini API integration for enhanced AI news analysis

🤖 Added comprehensive Gemini API integration:
• GeminiAnalyzer class for AI-powered news analysis  
• Automatic news importance scoring (1-100)
• Market insights generation
• Enhanced executive summaries
• Technology trend prediction
• Intelligent content ranking

📁 New files:
• gemini_analyzer.py - Core Gemini API client
• test_gemini.py - Functionality testing script
• .env.example - Environment configuration template

🔧 Enhanced generate_comprehensive_dashboard.py:
• Integrated Gemini analyzer at multiple points
• AI-powered news importance evaluation
• Market sentiment analysis
• Enhanced executive summaries

💡 Features:
• Fallback system when API unavailable
• Rate limiting and error handling
• Structured response parsing
• Automatic content prioritization

🚀 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

echo 📤 GitHub Pagesにプッシュ...
git push origin main

echo.
echo 🎉 Gemini API強化版がGitHub Pagesにデプロイされました!
echo 🔗 URL: https://awano27.github.io/daily-ai-news/
echo ⏰ 変更は1-5分で反映されます
echo.
echo 🤖 新しいGemini API機能:
echo ✅ AIによるニュース重要度評価 (1-100スコア)
echo ✅ 市場動向の洞察分析
echo ✅ エグゼクティブサマリーの強化
echo ✅ 技術トレンドの予測
echo ✅ 重要度に基づく自動ソート
echo ✅ フォールバック機能（API無効時）
echo.
echo 📋 Gemini API設定方法:
echo 1. Google AI StudioでAPIキーを取得:
echo    https://makersuite.google.com/app/apikey
echo 2. 環境変数を設定:
echo    set GEMINI_API_KEY=your_actual_api_key
echo 3. または.envファイルを作成:
echo    GEMINI_API_KEY=your_actual_api_key
echo.
echo 🧪 テスト方法:
echo python test_gemini.py

pause