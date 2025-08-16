#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Comprehensive AI News Dashboard - 1日のAI全体像が分かるダッシュボード
"""
import os
import sys
import json
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict
from pathlib import Path

def analyze_ai_landscape():
    """今日のAI業界全体を分析してダッシュボードデータを生成"""
    
    # 環境設定
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    
    # ビルドシステムから最新データを取得
    import build
    
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    print("🌏 AI業界全体像ダッシュボード生成")
    print("=" * 60)
    print(f"📅 日付: {now.strftime('%Y年%m月%d日 (%A)')}")
    print(f"⏰ 生成時刻: {now.strftime('%H:%M JST')}")
    print("=" * 60)
    
    # データ収集
    feeds_conf = build.parse_feeds()
    
    dashboard_data = {
        'timestamp': now.isoformat(),
        'date': now.strftime('%Y-%m-%d'),
        'jst_time': now.strftime('%H:%M JST'),
        'categories': {},
        'market_insights': {},
        'tech_developments': {},
        'industry_moves': {},
        'global_trends': {},
        'highlights': [],
        'stats': {}
    }
    
    total_items = 0
    
    # カテゴリ別データ分析
    category_mapping = {
        'Business': {'name': 'ビジネス・投資', 'icon': '💼', 'focus': 'market'},
        'Tools': {'name': 'テクノロジー・ツール', 'icon': '⚡', 'focus': 'tech'}, 
        'Posts': {'name': 'SNS・論文', 'icon': '🧪', 'focus': 'research'}
    }
    
    for category_name in ['Business', 'Tools', 'Posts']:
        feeds = build.get_category(feeds_conf, category_name)
        items = build.gather_items(feeds, category_name)
        
        category_key = category_name.lower()
        cat_info = category_mapping[category_name]
        
        # 詳細分析
        sources = Counter()
        companies = Counter()
        topics = []
        keywords = defaultdict(int)
        
        # 重要度による企業・技術分析
        important_companies = {
            'openai': 'OpenAI', 'anthropic': 'Anthropic', 'google': 'Google',
            'meta': 'Meta', 'microsoft': 'Microsoft', 'nvidia': 'NVIDIA',
            'apple': 'Apple', 'amazon': 'Amazon', 'tesla': 'Tesla',
            'deepmind': 'DeepMind', 'huggingface': 'Hugging Face'
        }
        
        tech_keywords = {
            'gpt-5': 'GPT-5', 'gpt-4': 'GPT-4', 'claude': 'Claude', 'gemini': 'Gemini',
            'llm': '大規模言語モデル', 'transformer': 'Transformer', 'neural network': 'ニューラルネット',
            'computer vision': 'コンピュータビジョン', 'reinforcement learning': '強化学習',
            'autonomous': '自動運転', 'robotics': 'ロボティクス', 'quantum': '量子コンピューティング',
            'edge ai': 'エッジAI', 'generative ai': '生成AI', 'multimodal': 'マルチモーダル'
        }
        
        business_keywords = {
            'funding': '資金調達', 'valuation': '企業価値', 'ipo': 'IPO', 'acquisition': '買収',
            'partnership': 'パートナーシップ', 'investment': '投資', 'revenue': '収益',
            'regulation': '規制', 'policy': '政策', 'ethics': 'AI倫理'
        }
        
        for item in items:
            sources[item['_source']] += 1
            
            # テキスト分析
            text = f"{item['title']} {item['_summary']}".lower()
            
            # 企業検出
            for company_key, company_name in important_companies.items():
                if company_key in text:
                    companies[company_name] += 1
            
            # キーワード分析
            all_keywords = {**tech_keywords, **business_keywords}
            for keyword, display_name in all_keywords.items():
                if keyword in text:
                    keywords[display_name] += 1
            
            # 重要度スコア計算
            importance = 0
            if any(comp in text for comp in important_companies.keys()):
                importance += 10
            if any(tech in text for tech in ['breakthrough', 'release', 'launch']):
                importance += 5
            
            topics.append({
                'title': item['title'],
                'source': item['_source'],
                'time': item['_dt'].strftime('%H:%M'),
                'summary': item['_summary'][:120] + '...' if len(item['_summary']) > 120 else item['_summary'],
                'importance': importance,
                'url': item.get('url', '#')
            })
        
        # 重要度でソート
        topics.sort(key=lambda x: x['importance'], reverse=True)
        
        dashboard_data['categories'][category_key] = {
            'name': cat_info['name'],
            'icon': cat_info['icon'],
            'count': len(items),
            'top_sources': dict(sources.most_common(3)),
            'top_companies': dict(companies.most_common(5)),
            'top_keywords': dict(Counter(keywords).most_common(8)),
            'featured_topics': topics[:6],
            'focus_area': cat_info['focus']
        }
        
        total_items += len(items)
    
    # X投稿分析
    try:
        x_posts = build.gather_x_posts(build.X_POSTS_CSV)
        
        # X投稿の詳細分析
        influencer_posts = []
        tech_discussions = []
        
        for post in x_posts[:10]:
            username = ""
            if "xポスト" in post['title']:
                username = post['title'].replace("xポスト", "").strip()
            
            post_data = {
                'username': username,
                'summary': post['_summary'][:100] + '...',
                'time': post['_dt'].strftime('%H:%M')
            }
            
            # インフルエンサー判定
            if any(user in username.lower() for user in ['@openai', '@anthropic', '@sama', '@ylecun']):
                influencer_posts.append(post_data)
            else:
                tech_discussions.append(post_data)
        
        dashboard_data['x_posts'] = {
            'total_count': len(x_posts),
            'influencer_posts': influencer_posts[:3],
            'tech_discussions': tech_discussions[:5]
        }
        total_items += len(x_posts)
    except Exception as e:
        print(f"⚠️ X投稿の分析でエラー: {e}")
        dashboard_data['x_posts'] = {'total_count': 0, 'influencer_posts': [], 'tech_discussions': []}
    
    # 市場洞察分析
    market_insights = analyze_market_trends(dashboard_data)
    dashboard_data['market_insights'] = market_insights
    
    # 技術動向分析
    tech_trends = analyze_tech_developments(dashboard_data)
    dashboard_data['tech_developments'] = tech_trends
    
    # 業界動向分析
    industry_analysis = analyze_industry_moves(dashboard_data)
    dashboard_data['industry_moves'] = industry_analysis
    
    # グローバルトレンド
    global_trends = analyze_global_trends(dashboard_data)
    dashboard_data['global_trends'] = global_trends
    
    # 統計情報
    all_companies = Counter()
    for cat in dashboard_data['categories'].values():
        for company, count in cat['top_companies'].items():
            all_companies[company] += count
    
    dashboard_data['stats'] = {
        'total_items': total_items,
        'total_sources': len(set(
            source for cat in dashboard_data['categories'].values() 
            for source in cat['top_sources'].keys()
        )),
        'active_companies': len(all_companies),
        'top_company': max(all_companies.items(), key=lambda x: x[1]) if all_companies else ('AI企業', 0),
        'last_updated': now.strftime('%Y-%m-%d %H:%M JST')
    }
    
    # エグゼクティブサマリー生成
    executive_summary = generate_executive_summary(dashboard_data)
    dashboard_data['executive_summary'] = executive_summary
    
    return dashboard_data

def analyze_market_trends(data):
    """市場トレンド分析"""
    business_data = data['categories'].get('business', {})
    
    return {
        'funding_activities': extract_funding_news(business_data),
        'valuation_changes': extract_valuation_news(business_data),
        'market_sentiment': analyze_sentiment(business_data),
        'key_developments': business_data.get('featured_topics', [])[:3]
    }

def analyze_tech_developments(data):
    """技術開発動向分析"""
    tools_data = data['categories'].get('tools', {})
    
    return {
        'new_releases': extract_product_releases(tools_data),
        'breakthrough_tech': extract_breakthroughs(tools_data),
        'developer_tools': extract_dev_tools(tools_data),
        'research_highlights': tools_data.get('featured_topics', [])[:3]
    }

def analyze_industry_moves(data):
    """業界動向分析"""
    all_companies = Counter()
    for cat in data['categories'].values():
        for company, count in cat.get('top_companies', {}).items():
            all_companies[company] += count
    
    return {
        'most_active_companies': dict(all_companies.most_common(5)),
        'partnerships': extract_partnerships(data),
        'regulatory_updates': extract_regulation_news(data),
        'talent_moves': extract_talent_news(data)
    }

def analyze_global_trends(data):
    """グローバルトレンド分析"""
    all_keywords = Counter()
    for cat in data['categories'].values():
        for keyword, count in cat.get('top_keywords', {}).items():
            all_keywords[keyword] += count
    
    return {
        'hot_technologies': dict(all_keywords.most_common(6)),
        'emerging_themes': identify_emerging_themes(data),
        'geographic_focus': analyze_geographic_trends(data),
        'future_outlook': generate_outlook(data)
    }

def extract_funding_news(business_data):
    """資金調達ニュース抽出"""
    topics = business_data.get('featured_topics', [])
    funding_topics = []
    
    for topic in topics:
        text = topic['title'].lower()
        if any(keyword in text for keyword in ['funding', 'valuation', 'investment', 'raise']):
            funding_topics.append(topic)
    
    return funding_topics[:2]

def extract_valuation_news(business_data):
    """企業価値ニュース抽出"""
    topics = business_data.get('featured_topics', [])
    valuation_topics = []
    
    for topic in topics:
        text = topic['title'].lower()
        if any(keyword in text for keyword in ['valuation', 'billion', 'worth', 'value']):
            valuation_topics.append(topic)
    
    return valuation_topics[:2]

def analyze_sentiment(business_data):
    """市場センチメント分析"""
    topics = business_data.get('featured_topics', [])
    positive_keywords = ['breakthrough', 'success', 'growth', 'launch', 'advance']
    negative_keywords = ['challenge', 'concern', 'delay', 'issue', 'problem']
    
    positive_count = 0
    negative_count = 0
    
    for topic in topics:
        text = topic['title'].lower()
        if any(keyword in text for keyword in positive_keywords):
            positive_count += 1
        if any(keyword in text for keyword in negative_keywords):
            negative_count += 1
    
    if positive_count > negative_count:
        return "楽観的"
    elif negative_count > positive_count:
        return "慎重"
    else:
        return "中立"

def extract_product_releases(tools_data):
    """製品リリース抽出"""
    topics = tools_data.get('featured_topics', [])
    release_topics = []
    
    for topic in topics:
        text = topic['title'].lower()
        if any(keyword in text for keyword in ['release', 'launch', 'unveil', 'announce']):
            release_topics.append(topic)
    
    return release_topics[:3]

def extract_breakthroughs(tools_data):
    """技術ブレークスルー抽出"""
    topics = tools_data.get('featured_topics', [])
    breakthrough_topics = []
    
    for topic in topics:
        text = topic['title'].lower()
        if any(keyword in text for keyword in ['breakthrough', 'revolutionary', 'first', 'new']):
            breakthrough_topics.append(topic)
    
    return breakthrough_topics[:2]

def extract_dev_tools(tools_data):
    """開発者ツール抽出"""
    topics = tools_data.get('featured_topics', [])
    dev_topics = []
    
    for topic in topics:
        text = topic['title'].lower()
        if any(keyword in text for keyword in ['api', 'framework', 'library', 'tool', 'sdk']):
            dev_topics.append(topic)
    
    return dev_topics[:2]

def extract_partnerships(data):
    """パートナーシップ抽出"""
    partnerships = []
    for cat in data['categories'].values():
        for topic in cat.get('featured_topics', []):
            text = topic['title'].lower()
            if any(keyword in text for keyword in ['partnership', 'collaboration', 'team', 'join']):
                partnerships.append(topic)
    
    return partnerships[:2]

def extract_regulation_news(data):
    """規制ニュース抽出"""
    regulation_news = []
    for cat in data['categories'].values():
        for topic in cat.get('featured_topics', []):
            text = topic['title'].lower()
            if any(keyword in text for keyword in ['regulation', 'policy', 'law', 'government']):
                regulation_news.append(topic)
    
    return regulation_news[:2]

def extract_talent_news(data):
    """人事ニュース抽出"""
    talent_news = []
    for cat in data['categories'].values():
        for topic in cat.get('featured_topics', []):
            text = topic['title'].lower()
            if any(keyword in text for keyword in ['hire', 'ceo', 'cto', 'join', 'appoint']):
                talent_news.append(topic)
    
    return talent_news[:2]

def identify_emerging_themes(data):
    """新興テーマ特定"""
    themes = []
    all_keywords = Counter()
    
    for cat in data['categories'].values():
        for keyword, count in cat.get('top_keywords', {}).items():
            all_keywords[keyword] += count
    
    # 上位テーマを抽出
    for keyword, count in all_keywords.most_common(3):
        themes.append({'theme': keyword, 'mentions': count})
    
    return themes

def analyze_geographic_trends(data):
    """地理的トレンド分析"""
    geographic_mentions = Counter()
    
    regions = {
        'japan': '日本', 'china': '中国', 'usa': 'アメリカ', 'europe': 'ヨーロッパ',
        'silicon valley': 'シリコンバレー', 'tokyo': '東京', 'beijing': '北京'
    }
    
    for cat in data['categories'].values():
        for topic in cat.get('featured_topics', []):
            text = topic['title'].lower()
            for region_key, region_name in regions.items():
                if region_key in text:
                    geographic_mentions[region_name] += 1
    
    return dict(geographic_mentions.most_common(3))

def generate_outlook(data):
    """今後の見通し生成"""
    total_items = data.get('stats', {}).get('total_items', 0)
    
    if total_items > 20:
        return "活発な動きが続く"
    elif total_items > 10:
        return "安定した成長期"
    else:
        return "注意深い観察期"

def generate_executive_summary(data):
    """エグゼクティブサマリー生成"""
    stats = data.get('stats', {})
    market = data.get('market_insights', {})
    tech = data.get('tech_developments', {})
    
    summary = {
        'headline': f"今日のAI業界: {stats.get('total_items', 0)}件のニュース、{stats.get('active_companies', 0)}社が活動",
        'key_points': [
            f"📈 市場動向: {market.get('market_sentiment', '中立')}なセンチメント",
            f"🚀 技術開発: {len(tech.get('new_releases', []))}件の新製品リリース",
            f"🏢 企業動向: {stats.get('top_company', ['', 0])[0]}が最も活発",
            f"💬 SNS: {data.get('x_posts', {}).get('total_count', 0)}件の関連投稿"
        ],
        'outlook': data.get('global_trends', {}).get('future_outlook', '安定した成長期')
    }
    
    return summary

def generate_comprehensive_dashboard_html(data):
    """包括的ダッシュボードHTML生成"""
    
    exec_summary = data.get('executive_summary', {})
    
    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI業界全体像ダッシュボード - {data['date']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 15px;
            color: #1a202c;
        }}
        .dashboard {{ 
            max-width: 1400px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 20px; 
            overflow: hidden;
            box-shadow: 0 25px 50px rgba(0,0,0,0.15);
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 25px 30px; 
            text-align: center; 
        }}
        .header h1 {{ font-size: 2.2rem; margin-bottom: 8px; font-weight: 700; }}
        .header .subtitle {{ font-size: 1rem; opacity: 0.9; margin-bottom: 15px; }}
        .header .update-time {{ font-size: 0.9rem; opacity: 0.8; }}
        
        .content {{ padding: 25px; }}
        
        /* エグゼクティブサマリー */
        .exec-summary {{ 
            background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            padding: 25px; 
            border-radius: 15px; 
            margin-bottom: 25px;
            border-left: 5px solid #667eea;
        }}
        .exec-summary h2 {{ color: #2d3748; margin-bottom: 15px; font-size: 1.3rem; }}
        .exec-summary .headline {{ font-size: 1.1rem; font-weight: 600; margin-bottom: 15px; color: #1a202c; }}
        .key-points {{ list-style: none; }}
        .key-points li {{ padding: 8px 0; font-size: 0.95rem; color: #4a5568; }}
        
        /* KPI グリッド */
        .kpi-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
            gap: 15px; 
            margin-bottom: 25px; 
        }}
        .kpi-card {{ 
            background: white; 
            padding: 20px; 
            border-radius: 12px; 
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
            text-align: center;
        }}
        .kpi-number {{ font-size: 2rem; font-weight: bold; color: #667eea; margin-bottom: 5px; }}
        .kpi-label {{ color: #64748b; font-size: 0.9rem; font-weight: 500; }}
        
        /* セクショングリッド */
        .sections-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(450px, 1fr)); 
            gap: 20px; 
            margin-bottom: 25px; 
        }}
        .section-card {{ 
            background: white; 
            border: 1px solid #e2e8f0; 
            border-radius: 12px; 
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .section-header {{ 
            background: #f8fafc; 
            padding: 15px 20px; 
            border-bottom: 1px solid #e2e8f0; 
        }}
        .section-title {{ font-size: 1.1rem; font-weight: 600; color: #2d3748; }}
        .section-content {{ padding: 20px; }}
        
        /* カテゴリカード */
        .categories-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr)); 
            gap: 20px; 
            margin-bottom: 25px; 
        }}
        .category-card {{ 
            background: white; 
            border: 1px solid #e2e8f0; 
            border-radius: 12px; 
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .category-header {{ 
            background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
            padding: 18px 20px; 
            border-bottom: 1px solid #e2e8f0; 
        }}
        .category-title {{ font-size: 1.2rem; font-weight: 600; color: #2d3748; }}
        .category-count {{ color: #667eea; font-size: 1rem; margin-top: 3px; }}
        
        /* アイテムリスト */
        .topic-item {{ 
            padding: 12px 0; 
            border-bottom: 1px solid #f1f5f9; 
        }}
        .topic-item:last-child {{ border-bottom: none; }}
        .topic-title {{ font-weight: 600; color: #2d3748; margin-bottom: 5px; font-size: 0.9rem; line-height: 1.4; }}
        .topic-meta {{ color: #64748b; font-size: 0.8rem; }}
        .topic-summary {{ color: #4a5568; font-size: 0.8rem; margin-top: 5px; line-height: 1.3; }}
        
        /* キーワードタグ */
        .keywords {{ 
            display: flex; 
            flex-wrap: wrap; 
            gap: 6px; 
            margin-top: 12px; 
        }}
        .keyword {{ 
            background: #667eea; 
            color: white; 
            padding: 4px 10px; 
            border-radius: 15px; 
            font-size: 0.75rem; 
            font-weight: 500;
        }}
        
        /* トレンドセクション */
        .trends-section {{ 
            background: #fef7e0; 
            border: 1px solid #f6d55c; 
            border-radius: 12px; 
            padding: 20px; 
            margin-bottom: 25px; 
        }}
        .trends-section h3 {{ color: #92400e; margin-bottom: 15px; }}
        
        /* インサイトセクション */
        .insights-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
            gap: 15px; 
            margin-bottom: 25px; 
        }}
        .insight-card {{ 
            background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
            border: 1px solid #93c5fd; 
            border-radius: 10px; 
            padding: 18px; 
        }}
        .insight-title {{ color: #1e40af; font-weight: 600; margin-bottom: 10px; font-size: 0.95rem; }}
        .insight-content {{ color: #1e3a8a; font-size: 0.85rem; line-height: 1.4; }}
        
        .footer {{ 
            text-align: center; 
            padding: 20px; 
            color: #64748b; 
            border-top: 1px solid #e2e8f0; 
            font-size: 0.9rem;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .content {{ padding: 15px; }}
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .sections-grid {{ grid-template-columns: 1fr; }}
            .categories-grid {{ grid-template-columns: 1fr; }}
            .insights-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🌏 AI業界全体像ダッシュボード</h1>
            <div class="subtitle">{exec_summary.get('headline', 'AIニュース総合分析')}</div>
            <div class="update-time">{data['date']} | 最終更新: {data['jst_time']}</div>
        </div>
        
        <div class="content">
            <!-- エグゼクティブサマリー -->
            <div class="exec-summary">
                <h2>📋 エグゼクティブサマリー</h2>
                <div class="headline">{exec_summary.get('headline', '')}</div>
                <ul class="key-points">
                    {''.join(f'<li>{point}</li>' for point in exec_summary.get('key_points', []))}
                    <li>🔮 見通し: {exec_summary.get('outlook', '安定した成長期')}</li>
                </ul>
            </div>
            
            <!-- KPI統計 -->
            <div class="kpi-grid">
                <div class="kpi-card">
                    <div class="kpi-number">{data['stats']['total_items']}</div>
                    <div class="kpi-label">総ニュース数</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-number">{data['stats']['active_companies']}</div>
                    <div class="kpi-label">活動企業数</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-number">{data['stats']['total_sources']}</div>
                    <div class="kpi-label">情報ソース数</div>
                </div>
                <div class="kpi-card">
                    <div class="kpi-number">{data['x_posts']['total_count']}</div>
                    <div class="kpi-label">SNS投稿数</div>
                </div>
            </div>
            
            <!-- 主要インサイト -->
            <div class="insights-grid">
                <div class="insight-card">
                    <div class="insight-title">💼 市場動向</div>
                    <div class="insight-content">
                        センチメント: {data['market_insights']['market_sentiment']}<br>
                        資金調達: {len(data['market_insights']['funding_activities'])}件<br>
                        企業価値変動: {len(data['market_insights']['valuation_changes'])}件
                    </div>
                </div>
                <div class="insight-card">
                    <div class="insight-title">⚡ 技術開発</div>
                    <div class="insight-content">
                        新製品リリース: {len(data['tech_developments']['new_releases'])}件<br>
                        技術ブレークスルー: {len(data['tech_developments']['breakthrough_tech'])}件<br>
                        開発者ツール: {len(data['tech_developments']['developer_tools'])}件
                    </div>
                </div>
                <div class="insight-card">
                    <div class="insight-title">🏢 業界動向</div>
                    <div class="insight-content">
                        最活発企業: {data['stats']['top_company'][0]}<br>
                        パートナーシップ: {len(data['industry_moves']['partnerships'])}件<br>
                        人事異動: {len(data['industry_moves']['talent_moves'])}件
                    </div>
                </div>
            </div>
            
            <!-- グローバルトレンド -->
            <div class="trends-section">
                <h3>🔥 グローバルトレンド</h3>
                <div class="keywords">
                    {''.join(f'<span class="keyword">{tech} ({mentions})</span>' 
                            for tech, mentions in data['global_trends']['hot_technologies'].items())}
                </div>
            </div>
            
            <!-- カテゴリ別詳細 -->
            <div class="categories-grid">"""
    
    # カテゴリカード生成
    for cat_key, cat_data in data['categories'].items():
        html_template += f"""
                <div class="category-card">
                    <div class="category-header">
                        <div class="category-title">{cat_data['icon']} {cat_data['name']}</div>
                        <div class="category-count">{cat_data['count']}件のニュース</div>
                    </div>
                    <div class="section-content">
                        <h4 style="margin-bottom: 12px; color: #2d3748; font-size: 0.9rem;">📈 注目トピック</h4>
                        {''.join(f'''
                        <div class="topic-item">
                            <div class="topic-title">{topic['title'][:65]}{'...' if len(topic['title']) > 65 else ''}</div>
                            <div class="topic-meta">{topic['source']} • {topic['time']}</div>
                            <div class="topic-summary">{topic['summary'][:80]}{'...' if len(topic['summary']) > 80 else ''}</div>
                        </div>
                        ''' for topic in cat_data['featured_topics'][:4])}
                        
                        <h4 style="margin: 15px 0 10px 0; color: #2d3748; font-size: 0.9rem;">🏢 活発企業</h4>
                        <div class="keywords">
                            {''.join(f'<span class="keyword">{company} ({count})</span>' 
                                    for company, count in list(cat_data['top_companies'].items())[:4])}
                        </div>
                        
                        <h4 style="margin: 15px 0 10px 0; color: #2d3748; font-size: 0.9rem;">🔑 キーワード</h4>
                        <div class="keywords">
                            {''.join(f'<span class="keyword">{keyword} ({count})</span>' 
                                    for keyword, count in list(cat_data['top_keywords'].items())[:5])}
                        </div>
                    </div>
                </div>"""
    
    html_template += f"""
            </div>
            
            <!-- 固定リンクセクション（毎日変わらず表示） -->
            <div style="background: #f0f9ff; border-radius: 15px; padding: 25px; margin-bottom: 25px; border: 1px solid #0ea5e9;">
                <h2 style="color: #0c4a6e; margin-bottom: 20px; font-size: 1.3rem;">📌 AI業界定点観測（毎日更新）</h2>
                
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
                    <!-- LLMリーダーボード -->
                    <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 1.5rem; margin-right: 10px;">🏆</span>
                            <h3 style="color: #1e293b; font-size: 1.1rem; margin: 0;">LLMアリーナ リーダーボード</h3>
                        </div>
                        <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px; line-height: 1.4;">
                            世界中のLLMモデルの性能を人間の評価でランキング。ChatGPT、Claude、Gemini等の最新順位を確認
                        </p>
                        <a href="https://lmarena.ai/leaderboard" target="_blank" rel="noopener" style="
                            display: inline-block;
                            padding: 8px 16px;
                            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                            color: white;
                            text-decoration: none;
                            border-radius: 6px;
                            font-size: 0.9rem;
                            font-weight: 500;
                            transition: transform 0.2s;
                        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            リーダーボードを見る →
                        </a>
                    </div>
                    
                    <!-- AlphaXiv論文 -->
                    <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 1.5rem; margin-right: 10px;">📚</span>
                            <h3 style="color: #1e293b; font-size: 1.1rem; margin: 0;">AlphaXiv - AI論文ランキング</h3>
                        </div>
                        <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px; line-height: 1.4;">
                            arXivの最新AI論文を影響度・引用数でランキング。今日の重要論文、トレンド研究分野を把握
                        </p>
                        <a href="https://www.alphaxiv.org/" target="_blank" rel="noopener" style="
                            display: inline-block;
                            padding: 8px 16px;
                            background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                            color: white;
                            text-decoration: none;
                            border-radius: 6px;
                            font-size: 0.9rem;
                            font-weight: 500;
                            transition: transform 0.2s;
                        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            論文ランキングを見る →
                        </a>
                    </div>
                    
                    <!-- トレンドワード -->
                    <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                        <div style="display: flex; align-items: center; margin-bottom: 12px;">
                            <span style="font-size: 1.5rem; margin-right: 10px;">📈</span>
                            <h3 style="color: #1e293b; font-size: 1.1rem; margin: 0;">AIトレンドワード（日次）</h3>
                        </div>
                        <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px; line-height: 1.4;">
                            AI業界で今日最も話題になっているキーワードをリアルタイム解析。急上昇ワードで業界動向を把握
                        </p>
                        <a href="https://tech-word-spikes.vercel.app/trend-word/AI?period=daily" target="_blank" rel="noopener" style="
                            display: inline-block;
                            padding: 8px 16px;
                            background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                            color: white;
                            text-decoration: none;
                            border-radius: 6px;
                            font-size: 0.9rem;
                            font-weight: 500;
                            transition: transform 0.2s;
                        " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                            トレンドワードを見る →
                        </a>
                    </div>
                </div>
                
                <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #cbd5e1;">
                    <p style="color: #64748b; font-size: 0.8rem; text-align: center;">
                        💡 これらの外部サービスは毎日自動更新され、AI業界の最新動向を多角的に把握できます
                    </p>
                </div>
            </div>
            
            <!-- SNS動向セクション -->
            <div class="section-card">
                <div class="section-header">
                    <div class="section-title">💬 SNS・コミュニティ動向</div>
                </div>
                <div class="section-content">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <div>
                            <h4 style="margin-bottom: 10px; color: #2d3748; font-size: 0.9rem;">👑 インフルエンサー投稿</h4>
                            {''.join(f'''
                            <div class="topic-item">
                                <div class="topic-title">{post['username']}</div>
                                <div class="topic-summary">{post['summary']}</div>
                                <div class="topic-meta">{post['time']}</div>
                            </div>
                            ''' for post in data['x_posts']['influencer_posts'])}
                        </div>
                        <div>
                            <h4 style="margin-bottom: 10px; color: #2d3748; font-size: 0.9rem;">🗨️ 技術ディスカッション</h4>
                            {''.join(f'''
                            <div class="topic-item">
                                <div class="topic-title">{post['username']}</div>
                                <div class="topic-summary">{post['summary']}</div>
                                <div class="topic-meta">{post['time']}</div>
                            </div>
                            ''' for post in data['x_posts']['tech_discussions'][:3])}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>🤖 AI業界全体像ダッシュボード | {data['stats']['total_sources']}の情報源から生成 | 
            Claude Code により作成</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_template

def main():
    """メイン実行関数"""
    try:
        print("🔄 AI業界データを包括分析中...")
        dashboard_data = analyze_ai_landscape()
        
        print("📊 包括的ダッシュボードを生成中...")
        html_content = generate_comprehensive_dashboard_html(dashboard_data)
        
        # HTMLファイルとして保存
        dashboard_path = Path("index.html")
        dashboard_path.write_text(html_content, encoding='utf-8')
        
        # JSON形式でも保存
        json_path = Path("dashboard_data.json")
        json_path.write_text(json.dumps(dashboard_data, ensure_ascii=False, indent=2), encoding='utf-8')
        
        print("✅ AI業界全体像ダッシュボード生成完了!")
        print(f"📁 ファイル: {dashboard_path.absolute()}")
        print(f"📄 データ: {json_path.absolute()}")
        print("\n🌐 ブラウザで index.html を開いてダッシュボードを確認してください!")
        print("\n📋 主要ハイライト:")
        
        exec_summary = dashboard_data.get('executive_summary', {})
        print(f"   {exec_summary.get('headline', '')}")
        for point in exec_summary.get('key_points', [])[:3]:
            print(f"   • {point}")
        
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()