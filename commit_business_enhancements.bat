@echo off
echo 🚀 ビジネスマン向けAIニュースダッシュボード改善をGitHubにアップロード中...

git add .
git commit -m "feat: Enhanced AI news dashboard with business-focused improvements

🎯 Major Business Enhancements:
- Added 15+ business-practical information sources
- Enhanced Gemini Flash Thinking analysis for business impact
- Implemented 5-criteria practicality scoring system
- Added executive briefing auto-generation
- Improved error handling for RSS feed stability

🔥 New Information Sources:
- Product Hunt AI (immediate tools)
- AI News Weekly (practical insights)
- Crunchbase AI News (funding/M&A data)
- McKinsey AI Insights (strategic analysis)
- Zapier AI Automation (workflow tools)
- Microsoft/Salesforce AI Updates (enterprise solutions)

🧠 Gemini Flash Thinking Features:
- Business impact analysis with 5-stage reasoning
- Practicality-focused article selection (25/50+ score threshold)
- Executive briefing with actionable insights
- ROI and implementation feasibility evaluation

🛠️ Technical Improvements:
- Enhanced error handling for RSS parsing failures
- Disabled problematic feeds (403 errors)
- Improved stability for continuous operation
- Better fallback mechanisms for feed failures

🎯 Business Value:
- Focus on immediately usable AI tools and services
- Concrete ROI examples and implementation costs
- Competitor strategy and market intelligence
- Regulatory updates with compliance impact
- Japanese enterprise AI success cases

🤖 Generated with Claude Code (https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git push origin main

echo ✅ GitHubアップロード完了！
pause