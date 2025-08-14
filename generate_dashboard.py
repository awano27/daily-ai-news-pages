#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate AI News Dashboard for today
"""
import os
import sys
import json
from datetime import datetime, timezone, timedelta
from collections import Counter, defaultdict
from pathlib import Path

def analyze_ai_news():
    """今日のAIニュースを分析してダッシュボードデータを生成"""
    
    # 環境設定
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '20'  # 分析用に多めに取得
    
    # ビルドシステムから最新データを取得
    import build
    
    print("🤖 AI News Dashboard Generator")
    print("=" * 60)
    print(f"📅 日付: {datetime.now().strftime('%Y年%m月%d日 (%A)')}")
    print(f"⏰ 生成時刻: {datetime.now().strftime('%H:%M JST')}")
    print("=" * 60)
    
    # データ収集
    feeds_conf = build.parse_feeds()
    
    dashboard_data = {
        'timestamp': datetime.now().isoformat(),
        'date': datetime.now().strftime('%Y-%m-%d'),
        'categories': {},
        'trends': {},
        'highlights': [],
        'stats': {}
    }
    
    total_items = 0
    filtered_items = 0
    
    # 各カテゴリのデータを分析
    for category_name in ['Business', 'Tools', 'Posts']:
        category_key = category_name.lower()
        feeds = build.get_category(feeds_conf, category_name)
        items = build.gather_items(feeds, category_name)
        
        # カテゴリ分析
        sources = Counter()
        topics = []
        keywords = defaultdict(int)
        
        for item in items:
            sources[item['_source']] += 1
            
            # キーワード抽出（簡易版）
            text = f"{item['title']} {item['_summary']}".lower()
            ai_keywords = [
                'gpt', 'llm', 'ai', 'machine learning', 'deep learning',
                'neural network', 'transformer', 'chatgpt', 'anthropic',
                'openai', 'meta', 'google', 'microsoft', 'nvidia',
                'computer vision', 'nlp', 'reinforcement learning'
            ]
            
            for keyword in ai_keywords:
                if keyword in text:
                    keywords[keyword] += 1
            
            topics.append({
                'title': item['title'],
                'source': item['_source'],
                'time': item['_dt'].strftime('%H:%M'),
                'summary': item['_summary'][:100] + '...' if len(item['_summary']) > 100 else item['_summary']
            })
        
        dashboard_data['categories'][category_key] = {
            'count': len(items),
            'top_sources': dict(sources.most_common(5)),
            'top_keywords': dict(Counter(keywords).most_common(10)),
            'recent_topics': topics[:10]
        }
        
        total_items += len(items)
    
    # X投稿データも分析
    try:
        x_posts = build.gather_x_posts(build.X_POSTS_CSV)
        dashboard_data['x_posts'] = {
            'count': len(x_posts),
            'recent': [{
                'title': post['title'],
                'summary': post['_summary'][:80] + '...',
                'time': post['_dt'].strftime('%H:%M')
            } for post in x_posts[:5]]
        }
        total_items += len(x_posts)
    except Exception as e:
        print(f"⚠️ X投稿の分析でエラー: {e}")
        dashboard_data['x_posts'] = {'count': 0, 'recent': []}
    
    # 統計情報
    dashboard_data['stats'] = {
        'total_items': total_items,
        'total_sources': len(set(item['source'] for cat in dashboard_data['categories'].values() 
                                for item in cat['recent_topics'])),
        'update_frequency': '24時間',
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M JST')
    }
    
    # 主要トレンド分析
    all_keywords = defaultdict(int)
    for cat in dashboard_data['categories'].values():
        for keyword, count in cat['top_keywords'].items():
            all_keywords[keyword] += count
    
    dashboard_data['trends'] = {
        'hot_keywords': dict(Counter(all_keywords).most_common(8)),
        'category_distribution': {
            cat: data['count'] for cat, data in dashboard_data['categories'].items()
        }
    }
    
    # ハイライト生成
    highlights = []
    
    # 最もアクティブなソース
    all_sources = defaultdict(int)
    for cat in dashboard_data['categories'].values():
        for source, count in cat['top_sources'].items():
            all_sources[source] += count
    
    top_source = max(all_sources.items(), key=lambda x: x[1])
    highlights.append(f"📈 最もアクティブなソース: {top_source[0]} ({top_source[1]}件)")
    
    # 人気キーワード
    top_keyword = max(all_keywords.items(), key=lambda x: x[1]) if all_keywords else ('AI', 0)
    highlights.append(f"🔥 トレンドキーワード: {top_keyword[0]} ({top_keyword[1]}回言及)")
    
    # カテゴリ分布
    max_category = max(dashboard_data['trends']['category_distribution'].items(), key=lambda x: x[1])
    highlights.append(f"📊 最多カテゴリ: {max_category[0].title()} ({max_category[1]}件)")
    
    # X投稿統計
    if dashboard_data['x_posts']['count'] > 0:
        highlights.append(f"💬 SNS投稿: {dashboard_data['x_posts']['count']}件の最新投稿")
    
    dashboard_data['highlights'] = highlights
    
    return dashboard_data

def generate_dashboard_html(data):
    """ダッシュボードHTMLを生成"""
    
    html_template = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI News Dashboard - {data['date']}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        .dashboard {{ 
            max-width: 1200px; 
            margin: 0 auto; 
            background: white; 
            border-radius: 20px; 
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        .header {{ 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            padding: 30px; 
            text-align: center; 
        }}
        .header h1 {{ font-size: 2.5rem; margin-bottom: 10px; }}
        .header p {{ font-size: 1.2rem; opacity: 0.9; }}
        .content {{ padding: 30px; }}
        .stats-grid {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); 
            gap: 20px; 
            margin-bottom: 30px; 
        }}
        .stat-card {{ 
            background: #f8fafc; 
            padding: 25px; 
            border-radius: 15px; 
            border-left: 5px solid #667eea; 
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .stat-number {{ font-size: 2.5rem; font-weight: bold; color: #667eea; }}
        .stat-label {{ color: #64748b; margin-top: 5px; }}
        .highlights {{ 
            background: #eff6ff; 
            padding: 25px; 
            border-radius: 15px; 
            margin-bottom: 30px; 
            border: 1px solid #dbeafe;
        }}
        .highlights h3 {{ color: #1e40af; margin-bottom: 15px; }}
        .highlight-item {{ 
            padding: 10px 0; 
            border-bottom: 1px solid #dbeafe; 
            font-size: 1.1rem;
        }}
        .highlight-item:last-child {{ border-bottom: none; }}
        .categories {{ 
            display: grid; 
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
            gap: 25px; 
        }}
        .category-card {{ 
            background: white; 
            border: 1px solid #e2e8f0; 
            border-radius: 15px; 
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }}
        .category-header {{ 
            background: #f1f5f9; 
            padding: 20px; 
            border-bottom: 1px solid #e2e8f0; 
        }}
        .category-title {{ font-size: 1.3rem; font-weight: bold; color: #334155; }}
        .category-count {{ color: #667eea; font-size: 1.1rem; }}
        .category-content {{ padding: 20px; }}
        .topic-item {{ 
            padding: 12px 0; 
            border-bottom: 1px solid #f1f5f9; 
        }}
        .topic-item:last-child {{ border-bottom: none; }}
        .topic-title {{ font-weight: 600; color: #1e293b; margin-bottom: 5px; }}
        .topic-meta {{ color: #64748b; font-size: 0.9rem; }}
        .keywords {{ 
            display: flex; 
            flex-wrap: wrap; 
            gap: 8px; 
            margin-top: 15px; 
        }}
        .keyword {{ 
            background: #667eea; 
            color: white; 
            padding: 5px 12px; 
            border-radius: 20px; 
            font-size: 0.85rem; 
        }}
        .footer {{ 
            text-align: center; 
            padding: 20px; 
            color: #64748b; 
            border-top: 1px solid #e2e8f0; 
        }}
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 2rem; }}
            .content {{ padding: 20px; }}
            .stats-grid {{ grid-template-columns: 1fr; }}
            .categories {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>🤖 AI News Dashboard</h1>
            <p>{data['date']} | 最終更新: {data['stats']['last_updated']}</p>
        </div>
        
        <div class="content">
            <!-- 統計サマリー -->
            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-number">{data['stats']['total_items']}</div>
                    <div class="stat-label">総記事数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{data['stats']['total_sources']}</div>
                    <div class="stat-label">ニュースソース数</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{data['categories']['business']['count']}</div>
                    <div class="stat-label">ビジネスニュース</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">{data['x_posts']['count']}</div>
                    <div class="stat-label">SNS投稿</div>
                </div>
            </div>
            
            <!-- ハイライト -->
            <div class="highlights">
                <h3>📊 今日のハイライト</h3>
                {''.join(f'<div class="highlight-item">{highlight}</div>' for highlight in data['highlights'])}
            </div>
            
            <!-- トレンドキーワード -->
            <div class="highlights">
                <h3>🔥 トレンドキーワード</h3>
                <div class="keywords">
                    {''.join(f'<span class="keyword">{keyword} ({count})</span>' for keyword, count in data['trends']['hot_keywords'].items())}
                </div>
            </div>
            
            <!-- カテゴリ別詳細 -->
            <div class="categories">
"""
    
    # カテゴリカード生成
    category_names = {'business': 'ビジネスニュース', 'tools': 'ツール・技術', 'posts': '研究・論文'}
    
    for cat_key, cat_data in data['categories'].items():
        cat_name = category_names.get(cat_key, cat_key.title())
        
        html_template += f"""
                <div class="category-card">
                    <div class="category-header">
                        <div class="category-title">{cat_name}</div>
                        <div class="category-count">{cat_data['count']}件</div>
                    </div>
                    <div class="category-content">
                        <h4>主要トピック</h4>
                        {''.join(f'''
                        <div class="topic-item">
                            <div class="topic-title">{topic['title'][:60]}{'...' if len(topic['title']) > 60 else ''}</div>
                            <div class="topic-meta">{topic['source']} • {topic['time']}</div>
                        </div>
                        ''' for topic in cat_data['recent_topics'][:5])}
                        
                        <h4 style="margin-top: 20px;">人気キーワード</h4>
                        <div class="keywords">
                            {''.join(f'<span class="keyword">{keyword} ({count})</span>' for keyword, count in list(cat_data['top_keywords'].items())[:5])}
                        </div>
                    </div>
                </div>
"""
    
    html_template += f"""
            </div>
        </div>
        
        <div class="footer">
            <p>Generated by Daily AI News System | Data from {data['stats']['total_sources']} sources</p>
        </div>
    </div>
</body>
</html>"""
    
    return html_template

def main():
    """メイン実行関数"""
    try:
        print("🔄 AIニュースデータを収集中...")
        dashboard_data = analyze_ai_news()
        
        print("📊 ダッシュボードを生成中...")
        html_content = generate_dashboard_html(dashboard_data)
        
        # HTMLファイルとして保存
        dashboard_path = Path("ai_news_dashboard.html")
        dashboard_path.write_text(html_content, encoding='utf-8')
        
        # JSON形式でも保存
        json_path = Path("dashboard_data.json")
        json_path.write_text(json.dumps(dashboard_data, ensure_ascii=False, indent=2), encoding='utf-8')
        
        print("✅ ダッシュボード生成完了!")
        print(f"📁 ファイル: {dashboard_path.absolute()}")
        print(f"📄 データ: {json_path.absolute()}")
        print("\n🌐 ブラウザで ai_news_dashboard.html を開いてダッシュボードを確認してください!")
        
        return True
        
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()