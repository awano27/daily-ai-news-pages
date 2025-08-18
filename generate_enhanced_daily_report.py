#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企業向け改善版AIレポート生成システム
エグゼクティブ向けに最適化された日次AIインテリジェンス
"""

import os
import sys
import json
import yaml
import feedparser
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any, Tuple
import google.generativeai as genai
from deep_translator import GoogleTranslator
import re
from urllib.parse import urlparse

# Gemini API設定
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY and not os.getenv('DISABLE_GEMINI'):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

class NewsSourceClassifier:
    """ニュースソースの信頼性分類器"""
    
    # 信頼性レベル別の情報源定義
    TIER_1_SOURCES = {  # 最高信頼性：公式発表・主要メディア
        'Google AI Blog', 'Microsoft Research Blog', 'OpenAI Blog', 
        'Meta AI Blog', 'Anthropic Blog', 'DeepMind Blog', 'AWS AI Blog',
        'Harvard Business Review AI', 'MIT Technology Review AI', 'Reuters Tech',
        'Bloomberg Technology', 'VentureBeat AI', 'TechCrunch', 'Crunchbase AI News'
    }
    
    TIER_2_SOURCES = {  # 高信頼性：専門メディア・業界誌
        'AI Business News', 'MIT Sloan Management', 'Stanford Business AI',
        'CB Insights AI', 'The Batch by DeepLearning.AI', 'AI News Weekly',
        'McKinsey AI Insights', 'Nikkei AI News', 'ITmedia AI', 'ZDNET Japan AI'
    }
    
    TIER_3_SOURCES = {  # 中信頼性：技術コミュニティ・論文サイト
        'Hugging Face Blog', 'PyTorch Blog', 'TensorFlow Blog', 'Papers With Code',
        'Towards Data Science', 'Machine Learning Mastery', 'MarkTechPost',
        'AI Research', 'GitHub Trending', 'Weights & Biases Blog'
    }
    
    SNS_SOURCES = {  # SNS・コミュニティ：参考情報
        'Reddit AI', 'Reddit MachineLearning', 'Reddit DeepLearning', 
        'Reddit ArtificialIntelligence', 'Hacker News'
    }
    
    @classmethod
    def classify_source(cls, source_name: str) -> Tuple[str, int]:
        """ソースの信頼性レベルを分類 (レベル, 優先度)"""
        if source_name in cls.TIER_1_SOURCES:
            return ("公式・主要メディア", 1)
        elif source_name in cls.TIER_2_SOURCES:
            return ("専門メディア・業界誌", 2)
        elif source_name in cls.TIER_3_SOURCES:
            return ("技術コミュニティ", 3)
        elif source_name in cls.SNS_SOURCES:
            return ("SNS・コミュニティ", 4)
        else:
            return ("その他", 5)

class BusinessImpactAnalyzer:
    """ビジネスインパクト分析器"""
    
    @staticmethod
    def analyze_news_item(news_item: Dict, source_tier: int) -> Dict[str, Any]:
        """個別ニュース項目のビジネス価値を分析"""
        title = news_item.get('title', '').lower()
        summary = news_item.get('summary', '').lower()
        content = f"{title} {summary}"
        
        # 基本ビジネス価値スコア計算 (1-10)
        impact_score = 5  # デフォルト
        
        # 高インパクトキーワード (+3点)
        high_impact_keywords = [
            'funding', 'investment', 'ipo', 'acquisition', 'merger', 'billion', 'million',
            'breakthrough', 'launch', 'release', 'partnership', 'collaboration'
        ]
        
        # 中インパクトキーワード (+2点)
        medium_impact_keywords = [
            'startup', 'enterprise', 'revenue', 'growth', 'market', 'adoption',
            'efficiency', 'automation', 'productivity', 'cost'
        ]
        
        # 技術キーワード (+1点)
        tech_keywords = [
            'ai', 'artificial intelligence', 'machine learning', 'llm', 'gpt',
            'neural network', 'deep learning', 'generative', 'transformer'
        ]
        
        for keyword in high_impact_keywords:
            if keyword in content:
                impact_score += 3
                break
                
        for keyword in medium_impact_keywords:
            if keyword in content:
                impact_score += 2
                break
                
        for keyword in tech_keywords:
            if keyword in content:
                impact_score += 1
                break
        
        # ソース信頼性による重み付け
        source_multiplier = {1: 1.5, 2: 1.3, 3: 1.1, 4: 0.8, 5: 0.7}
        final_score = min(10, impact_score * source_multiplier.get(source_tier, 1.0))
        
        # 緊急度判定
        urgency_keywords = ['breaking', 'urgent', 'alert', 'immediate', 'critical', 'emergency']
        urgency = 'high' if any(keyword in content for keyword in urgency_keywords) else 'medium'
        
        # ROI推定
        roi_estimate = BusinessImpactAnalyzer._estimate_roi(content)
        
        # 投資規模推定
        investment_scale = BusinessImpactAnalyzer._extract_financial_info(content)
        
        return {
            'business_impact_score': round(final_score, 1),
            'urgency_level': urgency,
            'roi_estimate': roi_estimate,
            'investment_scale': investment_scale,
            'why_important': BusinessImpactAnalyzer._generate_importance_reason(title, summary),
            'business_implications': BusinessImpactAnalyzer._generate_business_implications(content),
            'source_tier': source_tier
        }
    
    @staticmethod
    def _estimate_roi(content: str) -> str:
        """ROI推定ロジック"""
        if any(keyword in content for keyword in ['billion', '10x', 'breakthrough']):
            return "高ROI期待 (50%+)"
        elif any(keyword in content for keyword in ['million', '5x', 'significant']):
            return "中ROI期待 (20-50%)"
        elif any(keyword in content for keyword in ['cost saving', 'efficiency', 'automation']):
            return "コスト削減効果 (10-30%)"
        else:
            return "要分析"
    
    @staticmethod
    def _extract_financial_info(content: str) -> str:
        """投資規模情報抽出"""
        # 数値パターンマッチング
        billion_pattern = r'(\d+(?:\.\d+)?)\s*billion'
        million_pattern = r'(\d+(?:\.\d+)?)\s*million'
        
        if re.search(billion_pattern, content):
            match = re.search(billion_pattern, content)
            return f"${match.group(1)}B規模"
        elif re.search(million_pattern, content):
            match = re.search(million_pattern, content)
            return f"${match.group(1)}M規模"
        else:
            return "金額未発表"
    
    @staticmethod
    def _generate_importance_reason(title: str, summary: str) -> str:
        """重要性の理由生成"""
        content = f"{title} {summary}".lower()
        
        if 'funding' in content or 'investment' in content:
            return "新たな資金調達により市場拡大が予想され、競合環境の変化を示唆"
        elif 'launch' in content or 'release' in content:
            return "新製品・サービスの市場投入により、業界標準や競争構造に影響"
        elif 'partnership' in content or 'collaboration' in content:
            return "戦略的提携により、新たなビジネス機会と市場アクセスが創出"
        elif 'acquisition' in content or 'merger' in content:
            return "業界再編により、市場シェアと技術優位性の再配分が発生"
        else:
            return "AI技術の進展により、ビジネス効率性と競争力向上の機会を提供"
    
    @staticmethod
    def _generate_business_implications(content: str) -> str:
        """ビジネス影響分析"""
        if 'enterprise' in content:
            return "企業向けソリューションとして導入検討価値あり"
        elif 'startup' in content:
            return "新興企業の動向として投資・提携機会を監視"
        elif 'regulation' in content or 'policy' in content:
            return "規制変化によるコンプライアンス対応が必要"
        else:
            return "技術トレンドとして継続監視が推奨"

def fetch_enhanced_ai_news(hours_back: int = 24) -> Dict[str, List[Dict]]:
    """信頼性重視の改善されたニュース収集"""
    print(f"📊 過去{hours_back}時間の企業向けAIニュースを収集中...")
    
    with open('feeds.yml', 'r', encoding='utf-8') as f:
        feeds_config = yaml.safe_load(f)
    
    cutoff_time = datetime.now() - timedelta(hours=hours_back)
    categorized_news = defaultdict(list)
    
    # ソース別処理優先度（Tier 1 > Tier 2 > Tier 3 > SNS）
    all_feeds = []
    for category in ['Business', 'Tools', 'Posts']:
        all_feeds.extend(feeds_config.get(category, []))
    
    # ソース信頼性でソート
    sorted_feeds = sorted(all_feeds, key=lambda x: NewsSourceClassifier.classify_source(x['name'])[1])
    
    for feed_config in sorted_feeds:
        name = feed_config['name']
        url = feed_config['url']
        source_tier_name, source_tier = NewsSourceClassifier.classify_source(name)
        
        print(f"🔍 {name} ({source_tier_name}) を処理中...")
        
        try:
            # HTTP Headers追加でアクセス改善
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            
            response = requests.get(url, headers=headers, timeout=10)
            feed = feedparser.parse(response.content)
            
            if not feed or not hasattr(feed, 'entries'):
                print(f"[WARN] {name}: フィード取得失敗")
                continue
            
            processed_count = 0
            for entry in feed.entries[:15]:  # 各ソース最大15件
                try:
                    # 時間フィルタリング
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        entry_time = datetime(*entry.published_parsed[:6])
                        if entry_time < cutoff_time:
                            continue
                    
                    # 重複チェック（タイトルベース）
                    title = entry.title.strip()
                    if any(title == existing['title'] for existing_news in categorized_news.values() 
                          for existing in existing_news):
                        continue
                    
                    # HTMLタグ除去とクリーンアップ
                    summary = getattr(entry, 'summary', '')
                    cleaned_summary = re.sub(r'<[^>]+>', '', summary)  # HTMLタグ除去
                    cleaned_summary = re.sub(r'\s+', ' ', cleaned_summary).strip()[:300]  # 改行・空白正規化
                    
                    news_item = {
                        'title': title,
                        'link': entry.link,
                        'summary': cleaned_summary,
                        'published': getattr(entry, 'published', ''),
                        'source': name,
                        'source_tier': source_tier,
                        'source_tier_name': source_tier_name,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # ビジネスインパクト分析
                    impact_analysis = BusinessImpactAnalyzer.analyze_news_item(news_item, source_tier)
                    news_item.update(impact_analysis)
                    
                    # カテゴリ分類（ビジネス価値重視）
                    category = categorize_enhanced_business_news(news_item, feed_config)
                    categorized_news[category].append(news_item)
                    
                    processed_count += 1
                    
                except Exception as e:
                    print(f"[ERROR] {name}のエントリ処理エラー: {e}")
                    continue
            
            print(f"✅ {name}: {processed_count}件処理完了")
            
        except Exception as e:
            print(f"[ERROR] {name}のフィード処理エラー: {e}")
            continue
    
    # ビジネス価値スコア順でソート
    for category in categorized_news:
        categorized_news[category].sort(key=lambda x: x.get('business_impact_score', 0), reverse=True)
    
    print(f"✅ 収集完了: {sum(len(items) for items in categorized_news.values())}件")
    return dict(categorized_news)

def categorize_enhanced_business_news(news_item: Dict, feed_config: Dict) -> str:
    """改善されたビジネスカテゴリ分類"""
    title = news_item.get('title', '').lower()
    summary = news_item.get('summary', '').lower()
    content = f"{title} {summary}"
    source_tier = news_item.get('source_tier', 5)
    
    # SNSソースは別カテゴリ
    if source_tier >= 4:
        return 'sns_community'
    
    # 高精度キーワードマッチング
    if any(keyword in content for keyword in [
        'funding', 'investment', 'ipo', 'venture capital', 'series a', 'series b', 
        'acquisition', 'merger', 'valuation', 'raise', 'round'
    ]):
        return 'investment'
    
    elif any(keyword in content for keyword in [
        'regulation', 'policy', 'governance', 'ethics', 'compliance', 'legal',
        'gdpr', 'ai act', 'safety', 'responsible ai'
    ]):
        return 'governance'
    
    elif any(keyword in content for keyword in [
        'tool', 'product launch', 'platform', 'api', 'saas', 'software',
        'app', 'application', 'service', 'solution'
    ]):
        return 'tools_immediate'
    
    elif any(keyword in content for keyword in [
        'strategy', 'management', 'executive', 'ceo', 'leadership', 
        'transformation', 'digital transformation', 'business model'
    ]):
        return 'strategy'
    
    elif any(keyword in content for keyword in [
        'implementation', 'case study', 'success story', 'roi', 'deployment',
        'adoption', 'best practice', 'enterprise'
    ]):
        return 'implementation'
    
    elif any(keyword in content for keyword in [
        'japan', 'japanese', '日本', 'tokyo', 'nikkei', 'sony', 'toyota',
        'softbank', 'rakuten', 'mitsubishi'
    ]):
        return 'japan_business'
    
    else:
        return 'general'

def generate_executive_summary_with_gemini(categorized_news: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """Geminiによる強化されたエグゼクティブサマリー生成"""
    if not GEMINI_API_KEY or os.getenv('DISABLE_GEMINI'):
        return {"error": "Gemini API無効化中"}
    
    print("🧠 Gemini Flash Thinkingでエグゼクティブサマリー生成中...")
    
    # Tier 1-2の信頼性高ニュースのみ分析対象
    high_value_news = []
    for category, news_list in categorized_news.items():
        if category != 'sns_community':  # SNSは除外
            for news in news_list[:3]:  # 各カテゴリトップ3
                if news.get('business_impact_score', 0) >= 6.0:  # 高スコアのみ
                    high_value_news.append({
                        'category': category,
                        'title': news['title'],
                        'summary': news['summary'][:150],
                        'source': news['source'],
                        'source_tier': news.get('source_tier_name', ''),
                        'business_impact_score': news.get('business_impact_score', 0),
                        'roi_estimate': news.get('roi_estimate', ''),
                        'investment_scale': news.get('investment_scale', '')
                    })
    
    if not high_value_news:
        return {"error": "高価値ニュースなし"}
    
    prompt = f"""あなたは企業経営層向けAI戦略コンサルタントです。
以下の本日の高価値AIニュース{len(high_value_news)}件を分析し、
エグゼクティブ向けの実用的なサマリーを作成してください。

=== 高価値AIニュース（ビジネスインパクト6.0+） ===
{json.dumps(high_value_news, ensure_ascii=False, indent=2)}

以下の形式でJSON出力してください：

{{
  "executive_summary": "本日の最重要トレンドを3行で要約",
  "key_insights": [
    "インサイト1：具体的なビジネス価値",
    "インサイト2：市場機会または脅威",
    "インサイト3：技術トレンドまたは投資機会"
  ],
  "top_3_priorities": [
    {{
      "priority": "最優先事項名",
      "urgency": "high/medium/low",
      "business_value": "具体的な価値提案",
      "estimated_roi": "ROI推定",
      "timeline": "実行タイムライン",
      "required_action": "推奨アクション"
    }}
  ],
  "market_outlook": {{
    "sentiment": "positive/neutral/negative",
    "key_drivers": ["市場牽引要因1", "要因2"],
    "risks": ["リスク要因1", "要因2"],
    "opportunities": ["機会1", "機会2"]
  }},
  "immediate_actions": {{
    "today": ["今日実行すべき具体的アクション"],
    "this_week": ["今週検討すべき戦略"],
    "this_quarter": ["今四半期計画すべき投資・取組み"]
  }},
  "financial_highlights": {{
    "major_funding": "主要資金調達情報",
    "market_size_impact": "市場規模への影響",
    "cost_efficiency": "コスト効率化機会"
  }},
  "competitive_intelligence": {{
    "new_entrants": "注目新規参入企業",
    "strategic_moves": "主要企業の戦略動向",
    "partnership_trends": "パートナーシップトレンド"
  }}
}}"""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # JSON抽出
        if '```json' in result_text:
            json_start = result_text.find('```json') + 7
            json_end = result_text.find('```', json_start)
            result_text = result_text[json_start:json_end]
        elif '{' in result_text:
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            result_text = result_text[json_start:json_end]
        
        analysis = json.loads(result_text)
        print("✅ エグゼクティブサマリー生成完了")
        return analysis
        
    except Exception as e:
        print(f"[ERROR] Gemini分析エラー: {e}")
        return {"error": f"分析失敗: {str(e)}"}

def generate_enhanced_html_report(categorized_news: Dict[str, List[Dict]], 
                                executive_analysis: Dict[str, Any]) -> str:
    """改善されたHTMLレポート生成"""
    
    today = datetime.now().strftime('%Y年%m月%d日')
    
    # カテゴリ名の日本語化（改善版）
    category_names = {
        'strategy': '📊 戦略・経営',
        'investment': '💰 投資・資金調達', 
        'tools_immediate': '🛠️ 新ツール・即戦力',
        'implementation': '🎯 実装・成功事例',
        'governance': '⚖️ 規制・ガバナンス',
        'japan_business': '🗾 日本市場',
        'general': '📈 一般ニュース',
        'sns_community': '💬 SNS・コミュニティ情報'
    }
    
    # 統一CSSスタイル（グラデーション削除、落ち着いた色調）
    css_styles = """
    <style>
        /* === 基本レイアウト === */
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, "Hiragino Kaku Gothic ProN", "Meiryo", sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8f9fb;
            color: #2d3748;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 8px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.08);
            overflow: hidden;
        }
        
        /* === ヘッダー === */
        .header {
            background: #1a365d;
            color: white;
            padding: 40px 30px;
            text-align: center;
        }
        
        .header h1 {
            margin: 0;
            font-size: 2.2em;
            font-weight: 600;
        }
        
        .subtitle {
            margin: 12px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
            font-weight: 300;
        }
        
        /* === コンテンツエリア === */
        .content {
            padding: 40px 30px;
        }
        
        /* === エグゼクティブサマリー === */
        .executive-summary {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            border-left: 4px solid #3182ce;
            padding: 30px;
            border-radius: 8px;
            margin-bottom: 40px;
        }
        
        .executive-summary h2 {
            margin: 0 0 16px 0;
            color: #1a365d;
            font-size: 1.4em;
            font-weight: 600;
        }
        
        .executive-summary .summary-text {
            font-size: 1.1em;
            line-height: 1.7;
            color: #2d3748;
            margin-bottom: 20px;
        }
        
        .key-insights {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 16px;
            margin-top: 20px;
        }
        
        .insight-card {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 16px;
            border-radius: 6px;
            font-size: 0.95em;
        }
        
        /* === 優先事項セクション === */
        .priorities-section {
            margin: 40px 0;
        }
        
        .priorities-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }
        
        .priority-card {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 24px;
            border-radius: 8px;
            border-left: 4px solid #38a169;
        }
        
        .priority-card.high { border-left-color: #e53e3e; }
        .priority-card.medium { border-left-color: #dd6b20; }
        .priority-card.low { border-left-color: #38a169; }
        
        .priority-title {
            font-weight: 600;
            font-size: 1.1em;
            color: #1a365d;
            margin-bottom: 12px;
        }
        
        .priority-details {
            font-size: 0.9em;
            color: #4a5568;
        }
        
        .priority-details strong {
            color: #2d3748;
        }
        
        /* === ニュースカテゴリ === */
        .news-category {
            margin-bottom: 40px;
        }
        
        .category-header {
            background: #2d3748;
            color: white;
            padding: 16px 24px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 1.1em;
            margin-bottom: 16px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .source-tier-badge {
            font-size: 0.8em;
            padding: 4px 8px;
            border-radius: 12px;
            background: rgba(255,255,255,0.2);
        }
        
        /* === ニュース項目 === */
        .news-item {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 20px;
            margin-bottom: 12px;
            border-radius: 6px;
            transition: box-shadow 0.2s ease;
        }
        
        .news-item:hover {
            box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        
        .news-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 12px;
        }
        
        .news-title {
            font-weight: 600;
            color: #1a365d;
            font-size: 1.05em;
            line-height: 1.4;
            flex: 1;
            margin-right: 16px;
        }
        
        .impact-score {
            background: #edf2f7;
            color: #2d3748;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.8em;
            font-weight: 600;
            white-space: nowrap;
        }
        
        .impact-score.high { background: #fed7d7; color: #c53030; }
        .impact-score.medium { background: #feebc8; color: #c05621; }
        .impact-score.low { background: #c6f6d5; color: #276749; }
        
        .news-summary {
            color: #4a5568;
            font-size: 0.9em;
            line-height: 1.5;
            margin-bottom: 16px;
        }
        
        .news-analysis {
            background: #f7fafc;
            border-radius: 4px;
            padding: 12px;
            margin: 12px 0;
        }
        
        .analysis-row {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 12px;
            font-size: 0.85em;
        }
        
        .analysis-item {
            color: #4a5568;
        }
        
        .analysis-item strong {
            color: #2d3748;
        }
        
        .news-meta {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8em;
            color: #718096;
            border-top: 1px solid #e2e8f0;
            padding-top: 12px;
        }
        
        /* === アクションセクション === */
        .actions-section {
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            padding: 30px;
            border-radius: 8px;
            margin: 40px 0;
        }
        
        .action-timeline {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 20px;
        }
        
        .action-card {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 20px;
            border-radius: 6px;
        }
        
        .action-card h3 {
            margin: 0 0 12px 0;
            color: #1a365d;
            font-size: 1em;
        }
        
        .action-card ul {
            margin: 0;
            padding-left: 20px;
        }
        
        .action-card li {
            margin-bottom: 8px;
            font-size: 0.9em;
            color: #4a5568;
        }
        
        /* === メトリクス === */
        .metrics-section {
            margin: 40px 0;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 16px;
        }
        
        .metric-card {
            background: white;
            border: 1px solid #e2e8f0;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
        }
        
        .metric-value {
            font-size: 1.8em;
            font-weight: 700;
            color: #1a365d;
            margin-bottom: 4px;
        }
        
        .metric-label {
            color: #718096;
            font-size: 0.9em;
        }
        
        /* === フッター === */
        .footer {
            background: #2d3748;
            color: white;
            padding: 24px;
            text-align: center;
            font-size: 0.9em;
        }
        
        /* === レスポンシブ === */
        @media (max-width: 768px) {
            .container { margin: 10px; }
            .content { padding: 20px; }
            .header { padding: 30px 20px; }
            .priorities-grid { grid-template-columns: 1fr; }
        }
    </style>
    """
    
    # HTMLコンテンツ生成開始
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>企業向けAI Daily Intelligence Report - {today}</title>
    {css_styles}
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 AI Daily Intelligence Report</h1>
            <div class="subtitle">{today} - エグゼクティブ向け戦略的AIインテリジェンス</div>
        </div>
        
        <div class="content">"""
    
    # エグゼクティブサマリー
    if 'executive_summary' in executive_analysis:
        html_content += f"""
            <div class="executive-summary">
                <h2>📋 エグゼクティブサマリー</h2>
                <div class="summary-text">{executive_analysis['executive_summary']}</div>"""
        
        if 'key_insights' in executive_analysis:
            html_content += """
                <div class="key-insights">"""
            for insight in executive_analysis['key_insights']:
                html_content += f"""
                    <div class="insight-card">💡 {insight}</div>"""
            html_content += "</div>"
        
        html_content += "</div>"
    
    # 最優先事項
    if 'top_3_priorities' in executive_analysis:
        html_content += """
            <div class="priorities-section">
                <h2>🎯 本日の最優先事項</h2>
                <div class="priorities-grid">"""
        
        for priority in executive_analysis['top_3_priorities']:
            urgency = priority.get('urgency', 'medium')
            urgency_icon = {'high': '🔥', 'medium': '⚡', 'low': '💡'}[urgency]
            
            html_content += f"""
                <div class="priority-card {urgency}">
                    <div class="priority-title">{urgency_icon} {priority.get('priority', '優先事項')}</div>
                    <div class="priority-details">
                        <strong>ビジネス価値:</strong> {priority.get('business_value', 'TBD')}<br>
                        <strong>ROI推定:</strong> {priority.get('estimated_roi', 'TBD')}<br>
                        <strong>実行期限:</strong> {priority.get('timeline', 'TBD')}<br>
                        <strong>推奨アクション:</strong> {priority.get('required_action', 'TBD')}
                    </div>
                </div>"""
        
        html_content += "</div></div>"
    
    # ニュースカテゴリ別表示（信頼性順）
    category_order = ['investment', 'strategy', 'tools_immediate', 'implementation', 
                     'governance', 'japan_business', 'general', 'sns_community']
    
    for category in category_order:
        news_list = categorized_news.get(category, [])
        if not news_list:
            continue
        
        category_display = category_names.get(category, category)
        
        # カテゴリの信頼性情報
        tier_info = ""
        if category == 'sns_community':
            tier_info = '<span class="source-tier-badge">SNS・コミュニティ</span>'
        else:
            high_tier_count = sum(1 for news in news_list if news.get('source_tier', 5) <= 2)
            if high_tier_count > 0:
                tier_info = f'<span class="source-tier-badge">信頼性高: {high_tier_count}件</span>'
        
        html_content += f"""
            <div class="news-category">
                <div class="category-header">
                    {category_display} ({len(news_list)}件)
                    {tier_info}
                </div>"""
        
        # 表示件数制限（SNSは少なめ）
        display_limit = 3 if category == 'sns_community' else 5
        
        for news in news_list[:display_limit]:
            title = news.get('title', '無題')
            summary = news.get('summary', '')[:250] + ('...' if len(news.get('summary', '')) > 250 else '')
            source = news.get('source', '不明')
            source_tier_name = news.get('source_tier_name', '')
            
            # インパクトスコア表示
            impact_score = news.get('business_impact_score', 0)
            score_class = 'high' if impact_score >= 8 else 'medium' if impact_score >= 6 else 'low'
            
            html_content += f"""
                <div class="news-item">
                    <div class="news-header">
                        <div class="news-title">{title}</div>
                        <div class="impact-score {score_class}">スコア: {impact_score}</div>
                    </div>
                    <div class="news-summary">{summary}</div>"""
            
            # ビジネス分析情報
            if news.get('why_important') or news.get('roi_estimate'):
                html_content += """
                    <div class="news-analysis">
                        <div class="analysis-row">"""
                
                if news.get('why_important'):
                    html_content += f"""
                        <div class="analysis-item">
                            <strong>重要性:</strong> {news['why_important']}
                        </div>"""
                
                if news.get('roi_estimate'):
                    html_content += f"""
                        <div class="analysis-item">
                            <strong>ROI推定:</strong> {news['roi_estimate']}
                        </div>"""
                
                if news.get('investment_scale'):
                    html_content += f"""
                        <div class="analysis-item">
                            <strong>投資規模:</strong> {news['investment_scale']}
                        </div>"""
                
                if news.get('business_implications'):
                    html_content += f"""
                        <div class="analysis-item">
                            <strong>ビジネス影響:</strong> {news['business_implications']}
                        </div>"""
                
                html_content += "</div></div>"
            
            html_content += f"""
                    <div class="news-meta">
                        <span>📰 {source} ({source_tier_name})</span>
                        <span>緊急度: {news.get('urgency_level', 'medium').upper()}</span>
                    </div>
                </div>"""
        
        html_content += "</div>"
    
    # アクションプラン
    if 'immediate_actions' in executive_analysis:
        html_content += """
            <div class="actions-section">
                <h2>⚡ 推奨アクションプラン</h2>
                <div class="action-timeline">"""
        
        actions = executive_analysis['immediate_actions']
        timelines = [
            ('today', '今日実行', '🔥', actions.get('today', [])),
            ('this_week', '今週検討', '📅', actions.get('this_week', [])),
            ('this_quarter', '今四半期計画', '📊', actions.get('this_quarter', []))
        ]
        
        for timeline_key, timeline_name, icon, timeline_actions in timelines:
            html_content += f"""
                <div class="action-card">
                    <h3>{icon} {timeline_name}</h3>
                    <ul>"""
            
            for action in timeline_actions:
                html_content += f"<li>{action}</li>"
            
            html_content += "</ul></div>"
        
        html_content += "</div></div>"
    
    # 重要指標
    if 'market_outlook' in executive_analysis:
        market_data = executive_analysis['market_outlook']
        sentiment = market_data.get('sentiment', 'neutral')
        sentiment_icon = {'positive': '📈', 'neutral': '📊', 'negative': '📉'}[sentiment]
        
        # 統計計算
        total_news = sum(len(items) for items in categorized_news.values())
        high_impact_news = sum(1 for items in categorized_news.values() for item in items 
                              if item.get('business_impact_score', 0) >= 7)
        tier1_news = sum(1 for items in categorized_news.values() for item in items 
                        if item.get('source_tier', 5) <= 2)
        
        html_content += f"""
            <div class="metrics-section">
                <h2>📊 本日の重要指標</h2>
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-value">{total_news}</div>
                        <div class="metric-label">総ニュース数</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{high_impact_news}</div>
                        <div class="metric-label">高インパクト情報</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{tier1_news}</div>
                        <div class="metric-label">信頼性高情報</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-value">{sentiment_icon}</div>
                        <div class="metric-label">市場センチメント</div>
                    </div>
                </div>
            </div>"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>🎯 Generated by Enhanced AI Daily Intelligence System</p>
            <p>データソース: 信頼性重視50+ 情報源 | Gemini 2.0 Flash Thinking分析 | エグゼクティブ最適化</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    """メイン実行関数"""
    print("🎯 Enhanced AI Daily Business Report Generator 開始")
    
    # 環境変数設定
    hours_back = int(os.getenv('HOURS_LOOKBACK', 24))
    
    try:
        # 1. 改善されたニュース収集（信頼性重視）
        categorized_news = fetch_enhanced_ai_news(hours_back)
        
        if not any(categorized_news.values()):
            print("❌ 分析対象のニュースが見つかりませんでした")
            return
        
        # 2. Gemini強化分析
        executive_analysis = generate_executive_summary_with_gemini(categorized_news)
        
        # 3. 改善HTML生成
        html_report = generate_enhanced_html_report(categorized_news, executive_analysis)
        
        # 4. ファイル保存
        today_str = datetime.now().strftime('%Y%m%d')
        report_filename = f'enhanced_daily_report_{today_str}.html'
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        # 5. 最新レポートコピー
        with open('enhanced_daily_report_latest.html', 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"✅ 改善版日次レポート生成完了: {report_filename}")
        
        # 統計サマリー表示
        print(f"📊 改善効果サマリー:")
        total_news = sum(len(items) for items in categorized_news.values())
        high_tier_news = sum(1 for items in categorized_news.values() for item in items 
                           if item.get('source_tier', 5) <= 2)
        high_impact_news = sum(1 for items in categorized_news.values() for item in items 
                             if item.get('business_impact_score', 0) >= 7)
        
        print(f"   総ニュース数: {total_news}件")
        print(f"   高信頼性情報: {high_tier_news}件 ({high_tier_news/total_news*100:.1f}%)")
        print(f"   高インパクト情報: {high_impact_news}件 ({high_impact_news/total_news*100:.1f}%)")
        
        for category, news_list in categorized_news.items():
            if news_list:
                avg_score = sum(item.get('business_impact_score', 0) for item in news_list) / len(news_list)
                print(f"   {category}: {len(news_list)}件 (平均スコア: {avg_score:.1f})")
        
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()