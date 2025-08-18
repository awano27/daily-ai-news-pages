#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日次ビジネスAIレポート生成システム
毎日の重要なAI情報をビジネスマン向けに要約・分析
"""

import os
import sys
import json
import yaml
import feedparser
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any
import google.generativeai as genai
from deep_translator import GoogleTranslator

# Gemini API設定
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY and not os.getenv('DISABLE_GEMINI'):
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-2.0-flash-thinking-exp')

def categorize_business_news(news_item: Dict, feed_config: Dict) -> str:
    """ビジネスカテゴリを自動分類"""
    business_category = feed_config.get('business_category', 'general')
    
    title = news_item.get('title', '').lower()
    summary = news_item.get('summary', '').lower()
    content = f"{title} {summary}"
    
    # キーワードによる自動分類
    if any(keyword in content for keyword in ['funding', 'investment', 'ipo', 'venture', 'startup', 'raise', 'valuation']):
        return 'investment'
    elif any(keyword in content for keyword in ['regulation', 'policy', 'governance', 'ethics', 'compliance', 'legal']):
        return 'governance'
    elif any(keyword in content for keyword in ['tool', 'product', 'launch', 'release', 'app', 'platform', 'saas']):
        return 'tools_immediate'
    elif any(keyword in content for keyword in ['strategy', 'management', 'executive', 'ceo', 'leadership', 'transformation']):
        return 'strategy'
    elif any(keyword in content for keyword in ['implementation', 'case study', 'success', 'roi', 'deployment', 'adoption']):
        return 'implementation'
    elif any(keyword in content for keyword in ['japan', 'japanese', '日本', 'tokyo', 'nikkei']):
        return 'japan_business'
    
    return business_category

def fetch_ai_news_for_report(hours_back: int = 24) -> Dict[str, List[Dict]]:
    """日次レポート用のAIニュース収集"""
    print(f"📈 過去{hours_back}時間のビジネスAIニュースを収集中...")
    
    # feeds.ymlから設定読み込み
    with open('feeds.yml', 'r', encoding='utf-8') as f:
        feeds_config = yaml.safe_load(f)
    
    cutoff_time = datetime.now() - timedelta(hours=hours_back)
    categorized_news = defaultdict(list)
    
    # ビジネス関連フィードを優先処理
    business_feeds = feeds_config.get('Business', [])
    
    for feed_config in business_feeds:
        name = feed_config['name']
        url = feed_config['url']
        
        print(f"🔍 {name} を処理中...")
        
        try:
            feed = feedparser.parse(url)
            if not feed or not hasattr(feed, 'entries'):
                print(f"[WARN] {name}: フィード取得失敗")
                continue
                
            for entry in feed.entries[:10]:  # 最新10件に限定
                try:
                    # 時間フィルタリング
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        entry_time = datetime(*entry.published_parsed[:6])
                        if entry_time < cutoff_time:
                            continue
                    
                    news_item = {
                        'title': entry.title,
                        'link': entry.link,
                        'summary': getattr(entry, 'summary', ''),
                        'published': getattr(entry, 'published', ''),
                        'source': name,
                        'timestamp': datetime.now().isoformat()
                    }
                    
                    # ビジネスカテゴリ分類
                    category = categorize_business_news(news_item, feed_config)
                    categorized_news[category].append(news_item)
                    
                except Exception as e:
                    print(f"[ERROR] {name}のエントリ処理エラー: {e}")
                    continue
                    
        except Exception as e:
            print(f"[ERROR] {name}のフィード処理エラー: {e}")
            continue
    
    print(f"✅ 収集完了: {sum(len(items) for items in categorized_news.values())}件")
    return dict(categorized_news)

def analyze_daily_trends_with_gemini(categorized_news: Dict[str, List[Dict]]) -> Dict[str, Any]:
    """Geminiによる日次トレンド分析"""
    if not GEMINI_API_KEY or os.getenv('DISABLE_GEMINI'):
        return {"error": "Gemini API無効化中"}
    
    print("🧠 Gemini Flash Thinkingで日次トレンド分析中...")
    
    # 全ニュースを分析用に整理
    all_news = []
    for category, news_list in categorized_news.items():
        for news in news_list:
            all_news.append({
                'category': category,
                'title': news['title'],
                'summary': news['summary'][:200],  # 要約を制限
                'source': news['source']
            })
    
    if not all_news:
        return {"error": "分析対象ニュースなし"}
    
    prompt = f"""あなたは経営層向けAI情報分析の専門家です。
以下の本日のAIニュース{len(all_news)}件を分析し、ビジネス戦略に重要な日次インサイトを提供してください。

=== 本日のAIニュース ===
{json.dumps(all_news, ensure_ascii=False, indent=2)}

以下の形式でJSON出力してください：

{{
  "daily_summary": "本日のAI業界全体の動向を2-3文で要約",
  "top_3_trends": [
    {{
      "trend_name": "トレンド名",
      "business_impact": "ビジネスインパクト説明",
      "action_items": ["具体的アクション1", "具体的アクション2"],
      "urgency_level": "high/medium/low"
    }}
  ],
  "investment_highlights": {{
    "funding_news": "資金調達・投資関連の重要情報",
    "market_opportunities": "新たな市場機会",
    "competitive_threats": "競合脅威の分析"
  }},
  "immediate_actions": {{
    "today": ["今日すぐ実行すべきアクション"],
    "this_week": ["今週実行すべきアクション"],
    "this_month": ["今月検討すべきアクション"]
  }},
  "japanese_market_focus": "日本市場特有の重要情報・影響分析",
  "overall_sentiment": "positive/neutral/negative",
  "key_metrics": {{
    "new_tools_count": "新ツール・プロダクト数",
    "funding_amount": "発表された資金調達総額（推定）",
    "major_partnerships": "主要パートナーシップ数"
  }}
}}"""
    
    try:
        response = model.generate_content(prompt)
        result_text = response.text.strip()
        
        # JSON部分を抽出
        if '```json' in result_text:
            json_start = result_text.find('```json') + 7
            json_end = result_text.find('```', json_start)
            result_text = result_text[json_start:json_end]
        elif '{' in result_text:
            json_start = result_text.find('{')
            json_end = result_text.rfind('}') + 1
            result_text = result_text[json_start:json_end]
        
        analysis = json.loads(result_text)
        print("✅ Gemini分析完了")
        return analysis
        
    except Exception as e:
        print(f"[ERROR] Gemini分析エラー: {e}")
        return {"error": f"分析失敗: {str(e)}"}

def translate_to_japanese(text: str) -> str:
    """日本語翻訳（必要に応じて）"""
    try:
        translator = GoogleTranslator(source='en', target='ja')
        return translator.translate(text)
    except:
        return text

def generate_daily_html_report(categorized_news: Dict[str, List[Dict]], 
                             gemini_analysis: Dict[str, Any]) -> str:
    """日次レポートHTML生成"""
    
    today = datetime.now().strftime('%Y年%m月%d日')
    
    # カテゴリ名の日本語化
    category_names = {
        'strategy': '📊 戦略・経営',
        'investment': '💰 投資・資金調達',
        'tools_immediate': '🛠️ 新ツール・即戦力',
        'implementation': '🎯 実装・成功事例',
        'governance': '⚖️ 規制・ガバナンス',
        'japan_business': '🗾 日本市場',
        'general': '📈 一般ニュース'
    }
    
    html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Daily Business Report - {today}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 700;
        }}
        .subtitle {{
            margin: 10px 0 0 0;
            opacity: 0.9;
            font-size: 1.2em;
        }}
        .content {{
            padding: 30px;
        }}
        .executive-summary {{
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 25px;
            border-radius: 10px;
            margin-bottom: 30px;
            border-left: 5px solid #ff6b6b;
        }}
        .trends-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .trend-card {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            border-left: 4px solid #4ecdc4;
        }}
        .urgency-high {{ border-left-color: #ff6b6b; }}
        .urgency-medium {{ border-left-color: #feca57; }}
        .urgency-low {{ border-left-color: #48dbfb; }}
        .news-category {{
            margin-bottom: 30px;
        }}
        .category-header {{
            background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1.2em;
            margin-bottom: 15px;
        }}
        .news-item {{
            background: white;
            padding: 15px;
            margin-bottom: 10px;
            border-radius: 8px;
            border-left: 3px solid #74b9ff;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .news-title {{
            font-weight: 600;
            color: #2d3436;
            margin-bottom: 8px;
        }}
        .news-summary {{
            color: #636e72;
            font-size: 0.9em;
            line-height: 1.5;
        }}
        .news-meta {{
            font-size: 0.8em;
            color: #74b9ff;
            margin-top: 8px;
        }}
        .actions-section {{
            background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
            padding: 25px;
            border-radius: 10px;
            margin-top: 30px;
        }}
        .action-timeline {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
        }}
        .action-card {{
            background: white;
            padding: 15px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .metrics-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .metric-card {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .metric-value {{
            font-size: 2em;
            font-weight: 700;
            color: #2d3436;
        }}
        .metric-label {{
            color: #636e72;
            font-size: 0.9em;
        }}
        .sentiment-positive {{ color: #00b894; }}
        .sentiment-neutral {{ color: #fdcb6e; }}
        .sentiment-negative {{ color: #e17055; }}
        .footer {{
            background: #2d3436;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 AI Daily Business Report</h1>
            <div class="subtitle">{today} - エグゼクティブ向け日次AIインテリジェンス</div>
        </div>
        
        <div class="content">"""
    
    # エグゼクティブサマリー
    if 'daily_summary' in gemini_analysis:
        html_content += f"""
            <div class="executive-summary">
                <h2>📋 エグゼクティブサマリー</h2>
                <p style="font-size: 1.1em; font-weight: 500;">{gemini_analysis['daily_summary']}</p>
            </div>"""
    
    # 重要トレンド
    if 'top_3_trends' in gemini_analysis:
        html_content += """
            <h2>🚀 本日の重要トレンド</h2>
            <div class="trends-section">"""
        
        for i, trend in enumerate(gemini_analysis['top_3_trends'][:3]):
            urgency_class = f"urgency-{trend.get('urgency_level', 'medium')}"
            urgency_icon = {'high': '🔥', 'medium': '⚡', 'low': '💡'}.get(trend.get('urgency_level', 'medium'), '⚡')
            
            html_content += f"""
                <div class="trend-card {urgency_class}">
                    <h3>{urgency_icon} {trend.get('trend_name', f'トレンド{i+1}')}</h3>
                    <p><strong>ビジネスインパクト:</strong> {trend.get('business_impact', '分析中')}</p>
                    <div><strong>推奨アクション:</strong>
                        <ul>"""
            
            for action in trend.get('action_items', []):
                html_content += f"<li>{action}</li>"
            
            html_content += """</ul></div>
                </div>"""
        
        html_content += "</div>"
    
    # ニュースカテゴリ別表示
    for category, news_list in categorized_news.items():
        if not news_list:
            continue
            
        category_display = category_names.get(category, category)
        html_content += f"""
            <div class="news-category">
                <div class="category-header">{category_display} ({len(news_list)}件)</div>"""
        
        for news in news_list[:5]:  # 最新5件まで表示
            title = news.get('title', '無題')
            summary = news.get('summary', '')[:200] + ('...' if len(news.get('summary', '')) > 200 else '')
            source = news.get('source', '不明')
            
            html_content += f"""
                <div class="news-item">
                    <div class="news-title">{title}</div>
                    <div class="news-summary">{summary}</div>
                    <div class="news-meta">📰 {source}</div>
                </div>"""
        
        html_content += "</div>"
    
    # アクションプラン
    if 'immediate_actions' in gemini_analysis:
        html_content += """
            <div class="actions-section">
                <h2>⚡ アクションプラン</h2>
                <div class="action-timeline">"""
        
        actions = gemini_analysis['immediate_actions']
        timelines = [
            ('today', '今日', '🔥', actions.get('today', [])),
            ('this_week', '今週', '📅', actions.get('this_week', [])),
            ('this_month', '今月', '📊', actions.get('this_month', []))
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
    if 'key_metrics' in gemini_analysis:
        metrics = gemini_analysis['key_metrics']
        sentiment = gemini_analysis.get('overall_sentiment', 'neutral')
        sentiment_class = f"sentiment-{sentiment}"
        sentiment_icon = {'positive': '📈', 'neutral': '📊', 'negative': '📉'}.get(sentiment, '📊')
        
        html_content += f"""
            <h2>📊 本日の重要指標</h2>
            <div class="metrics-grid">
                <div class="metric-card">
                    <div class="metric-value">{metrics.get('new_tools_count', '集計中')}</div>
                    <div class="metric-label">新ツール・プロダクト</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{metrics.get('funding_amount', '集計中')}</div>
                    <div class="metric-label">資金調達総額</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value">{metrics.get('major_partnerships', '集計中')}</div>
                    <div class="metric-label">主要パートナーシップ</div>
                </div>
                <div class="metric-card">
                    <div class="metric-value {sentiment_class}">{sentiment_icon}</div>
                    <div class="metric-label">市場センチメント</div>
                </div>
            </div>"""
    
    # 日本市場特化情報
    if 'japanese_market_focus' in gemini_analysis:
        html_content += f"""
            <div class="executive-summary" style="background: linear-gradient(135deg, #ffeaa7 0%, #fab1a0 100%);">
                <h2>🗾 日本市場特化インサイト</h2>
                <p style="font-size: 1.1em;">{gemini_analysis['japanese_market_focus']}</p>
            </div>"""
    
    html_content += """
        </div>
        
        <div class="footer">
            <p>🤖 Generated by AI Daily Business Intelligence System</p>
            <p>データソース: 50+ AI業界RSS、Gemini 2.0 Flash Thinking分析</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_content

def main():
    """メイン実行関数"""
    print("🚀 AI Daily Business Report Generator 開始")
    
    # 環境変数設定
    hours_back = int(os.getenv('HOURS_LOOKBACK', 24))
    
    try:
        # 1. ニュース収集
        categorized_news = fetch_ai_news_for_report(hours_back)
        
        if not any(categorized_news.values()):
            print("❌ 分析対象のニュースが見つかりませんでした")
            return
        
        # 2. Gemini分析
        gemini_analysis = analyze_daily_trends_with_gemini(categorized_news)
        
        # 3. HTMLレポート生成
        html_report = generate_daily_html_report(categorized_news, gemini_analysis)
        
        # 4. ファイル保存
        today_str = datetime.now().strftime('%Y%m%d')
        report_filename = f'daily_report_{today_str}.html'
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        # 5. 最新レポートとしてもコピー
        with open('daily_report_latest.html', 'w', encoding='utf-8') as f:
            f.write(html_report)
        
        print(f"✅ 日次レポート生成完了: {report_filename}")
        print(f"📊 収集ニュース数: {sum(len(items) for items in categorized_news.values())}件")
        print(f"🔗 レポートURL: file://{os.path.abspath(report_filename)}")
        
        # 簡易統計表示
        for category, news_list in categorized_news.items():
            if news_list:
                print(f"   {category}: {len(news_list)}件")
        
    except Exception as e:
        print(f"❌ エラー発生: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()