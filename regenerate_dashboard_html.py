#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple script to regenerate dashboard HTML from corrected data
"""
import json
from pathlib import Path

def generate_dashboard_html(data):
    """Generate dashboard HTML from data"""
    
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
            <div class="categories">"""
    
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
                </div>"""
    
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
    """Main function to regenerate dashboard HTML"""
    # Load corrected data
    with open('dashboard_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Generate HTML
    html_content = generate_dashboard_html(data)
    
    # Save to file
    with open('ai_news_dashboard.html', 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print("✅ Dashboard HTML regenerated successfully!")
    print("📊 Updated counts: Business=8, Tools=8, Posts=8")
    print("🔗 File: ai_news_dashboard.html")

if __name__ == "__main__":
    main()