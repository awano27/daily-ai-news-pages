#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Real Data UI Dashboard - 実データを使用した改善版ダッシュボード
"""
import os
import re
from datetime import datetime
from pathlib import Path

def extract_real_data_from_existing():
    """既存のindex.htmlから実際のデータを抽出"""
    
    index_path = Path("index.html")
    if not index_path.exists():
        print("❌ index.html が見つかりません")
        return None
    
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        # データ抽出
        data = {
            'total_news': 0,
            'active_companies': 0,
            'total_sources': 0,
            'sns_posts': 0,
            'summary_text': '',
            'business_news': [],
            'tech_news': [],
            'sns_news': [],
            'featured_posts': [],
            'tech_discussions': [],
            'trends': []
        }
        
        # KPIデータを抽出
        kpi_pattern = r'<div class="kpi-number">(\d+)</div>'
        kpi_matches = re.findall(kpi_pattern, content)
        if len(kpi_matches) >= 4:
            data['total_news'] = int(kpi_matches[0])
            data['active_companies'] = int(kpi_matches[1])
            data['total_sources'] = int(kpi_matches[2])
            data['sns_posts'] = int(kpi_matches[3])
        
        # サマリーテキストを抽出
        summary_pattern = r'<p>今日のAI業界: (\d+)件のニュース、(\d+)社が活動</p>'
        summary_match = re.search(summary_pattern, content)
        if summary_match:
            data['summary_text'] = f"今日のAI業界: {summary_match.group(1)}件のニュース、{summary_match.group(2)}社が活動"
        
        # ニュース記事を抽出（ビジネス・投資カテゴリ）
        business_pattern = r'<div class="topic-item">.*?<div class="topic-title">.*?<a href="([^"]+)"[^>]*>([^<]+)</a>.*?</div>.*?<div class="topic-meta">([^<]+).*?</div>.*?<div class="topic-summary">([^<]+)</div>.*?</div>'
        business_matches = re.findall(business_pattern, content, re.DOTALL)
        
        for match in business_matches[:6]:  # 最大6件
            link, title, meta, summary = match
            # メタ情報から情報源と時間を抽出
            meta_parts = meta.split(' • ')
            source = meta_parts[0].strip() if meta_parts else 'Unknown'
            time = meta_parts[1].strip() if len(meta_parts) > 1 else '00:00'
            
            data['business_news'].append({
                'title': title.strip(),
                'summary': summary.strip()[:200] + ('...' if len(summary.strip()) > 200 else ''),
                'link': link.strip(),
                'source': source,
                'time': time,
                'category': 'ビジネス'
            })
        
        # X/Twitter投稿を抽出
        sns_pattern = r'<div style="background: white; border-radius: 8px; padding: 12px; margin-bottom: 10px; border-left: 3px solid #667eea;">.*?<a href="([^"]+)"[^>]*>([^<]+)</a>.*?<div style="color: #4a5568[^>]*>([^<]+)</div>.*?<div style="color: #718096[^>]*>([^<]+)</div>'
        sns_matches = re.findall(sns_pattern, content, re.DOTALL)
        
        for match in sns_matches[:10]:  # 最大10件
            link, username, content_text, time_source = match
            
            data['featured_posts'].append({
                'username': username.strip(),
                'summary': content_text.strip(),
                'url': link.strip(),
                'time': time_source.split(' • ')[1].strip() if ' • ' in time_source else '00:00'
            })
        
        # トレンドキーワードを抽出
        trend_pattern = r'<span class="keyword">([^<(]+)\\s*\\((\\d+)\\)</span>'
        trend_matches = re.findall(trend_pattern, content)
        
        for match in trend_matches:
            keyword, count = match
            data['trends'].append({
                'keyword': keyword.strip(),
                'count': int(count),
                'hot': int(count) > 5
            })
        
        print(f"✅ 実データ抽出完了:")
        print(f"   - ニュース: {len(data['business_news'])}件")
        print(f"   - SNS投稿: {len(data['featured_posts'])}件") 
        print(f"   - トレンド: {len(data['trends'])}件")
        
        return data
        
    except Exception as e:
        print(f"❌ データ抽出エラー: {e}")
        return None

def generate_improved_dashboard_with_real_data():
    """実データを使用した改善版ダッシュボードを生成"""
    
    # 実データを抽出
    data = extract_real_data_from_existing()
    if not data:
        print("❌ 実データの抽出に失敗しました")
        return None
    
    # JST時刻
    jst = datetime.now()
    current_date = jst.strftime('%Y-%m-%d')
    current_time = jst.strftime('%H:%M')
    
    # HTMLテンプレート
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="AI業界の最新ニュース、トレンド、企業動向を毎日更新。{current_date}の重要な動向を一覧で確認">
    <meta name="theme-color" content="#3b82f6">
    <title>AI業界ダッシュボード | {current_date} | daily-ai-news</title>
    
    <style>
        /* Modern CSS Variables */
        :root {{
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --secondary: #10b981;
            --accent: #8b5cf6;
            --bg-main: #f8fafc;
            --bg-card: #ffffff;
            --bg-hover: #f1f5f9;
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --border: #e2e8f0;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 25px rgba(0,0,0,0.15);
            --radius: 12px;
            --radius-sm: 8px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-main: #0f172a;
                --bg-card: #1e293b;
                --bg-hover: #334155;
                --text-primary: #f1f5f9;
                --text-secondary: #cbd5e1;
                --text-muted: #94a3b8;
                --border: #475569;
            }}
        }}
        
        /* Reset and base styles */
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            scroll-behavior: smooth;
            -webkit-font-smoothing: antialiased;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans JP", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        /* Skip to content for accessibility */
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--primary);
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            z-index: 1000;
            border-radius: 0 0 8px 0;
        }}
        
        .skip-link:focus {{
            top: 0;
        }}
        
        /* Header with glassmorphism */
        .header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border);
            transition: var(--transition);
        }}
        
        @media (prefers-color-scheme: dark) {{
            .header {{
                background: rgba(15, 23, 42, 0.95);
            }}
        }}
        
        .header-content {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 1.25rem 2rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .header h1 {{
            font-size: clamp(1.5rem, 4vw, 2rem);
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary) 0%, var(--accent) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        .header-stats {{
            display: flex;
            gap: 2rem;
            font-size: 0.875rem;
            flex-wrap: wrap;
        }}
        
        .stat {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .stat-value {{
            font-weight: 700;
            color: var(--primary);
        }}
        
        /* Main container */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            background: var(--bg-main);
            border-radius: 20px 20px 0 0;
            margin-top: -10px;
            min-height: calc(100vh - 100px);
        }}
        
        /* Summary section with enhanced design */
        .summary {{
            background: var(--bg-card);
            border-radius: var(--radius);
            padding: 2.5rem;
            margin-bottom: 2.5rem;
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }}
        
        .summary::before {{
            content: '';
            position: absolute;
            top: -50%;
            right: -10%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
            opacity: 0.1;
            border-radius: 50%;
        }}
        
        .summary h2 {{
            font-size: 1.5rem;
            margin-bottom: 1rem;
            color: var(--text-primary);
            position: relative;
            z-index: 1;
        }}
        
        .summary p {{
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-bottom: 2rem;
            position: relative;
            z-index: 1;
        }}
        
        /* Enhanced KPI grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 1.5rem;
            position: relative;
            z-index: 1;
        }}
        
        .kpi {{
            background: var(--bg-hover);
            border-radius: var(--radius-sm);
            padding: 1.75rem 1.5rem;
            text-align: center;
            transition: var(--transition);
            cursor: pointer;
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
        }}
        
        .kpi::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            transform: scaleX(0);
            transition: transform 0.4s ease;
        }}
        
        .kpi:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary);
        }}
        
        .kpi:hover::before {{
            transform: scaleX(1);
        }}
        
        .kpi-number {{
            font-size: 2.5rem;
            font-weight: 800;
            color: var(--primary);
            margin-bottom: 0.5rem;
            line-height: 1;
        }}
        
        .kpi-label {{
            font-size: 0.9rem;
            color: var(--text-muted);
            font-weight: 500;
        }}
        
        /* Tab navigation with enhanced UX */
        .tabs {{
            display: flex;
            gap: 0.75rem;
            margin-bottom: 2.5rem;
            overflow-x: auto;
            padding: 0.5rem;
            scroll-snap-type: x mandatory;
        }}
        
        .tabs::-webkit-scrollbar {{
            height: 4px;
        }}
        
        .tabs::-webkit-scrollbar-track {{
            background: var(--bg-hover);
            border-radius: 2px;
        }}
        
        .tabs::-webkit-scrollbar-thumb {{
            background: var(--primary);
            border-radius: 2px;
        }}
        
        .tab {{
            flex-shrink: 0;
            padding: 1rem 2rem;
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: var(--radius);
            color: var(--text-secondary);
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            white-space: nowrap;
            scroll-snap-align: start;
            position: relative;
        }}
        
        .tab:hover {{
            background: var(--bg-hover);
            transform: translateY(-2px);
        }}
        
        .tab.active {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
            box-shadow: var(--shadow-sm);
        }}
        
        .tab-content {{
            display: none;
            animation: fadeInUp 0.4s ease;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        @keyframes fadeInUp {{
            from {{
                opacity: 0;
                transform: translateY(20px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* Enhanced news grid */
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 2rem;
            margin-bottom: 2rem;
        }}
        
        .news-card {{
            background: var(--bg-card);
            border-radius: var(--radius);
            padding: 2rem;
            box-shadow: var(--shadow-sm);
            transition: var(--transition);
            border-left: 5px solid var(--primary);
            position: relative;
            overflow: hidden;
        }}
        
        .news-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(135deg, transparent 0%, rgba(59, 130, 246, 0.03) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .news-card:hover {{
            transform: translateY(-6px);
            box-shadow: var(--shadow-lg);
        }}
        
        .news-card:hover::before {{
            opacity: 1;
        }}
        
        .news-category {{
            display: inline-block;
            padding: 0.4rem 1rem;
            background: var(--primary);
            color: white;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .news-title {{
            font-size: 1.25rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.75rem;
            line-height: 1.3;
            position: relative;
            z-index: 1;
        }}
        
        .news-title a {{
            color: inherit;
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .news-title a:hover {{
            color: var(--primary);
        }}
        
        .news-summary {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1.25rem;
            position: relative;
            z-index: 1;
        }}
        
        .news-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: var(--text-muted);
            position: relative;
            z-index: 1;
        }}
        
        .news-source {{
            font-weight: 600;
        }}
        
        /* SNS section */
        .sns-section {{
            background: var(--bg-card);
            border-radius: var(--radius);
            padding: 2.5rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-md);
        }}
        
        .sns-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}
        
        .sns-post {{
            background: var(--bg-hover);
            border-radius: var(--radius-sm);
            padding: 1.5rem;
            transition: var(--transition);
            border-left: 4px solid var(--secondary);
            position: relative;
        }}
        
        .sns-post:hover {{
            transform: translateY(-3px);
            box-shadow: var(--shadow-sm);
            border-left-color: var(--primary);
        }}
        
        .sns-username {{
            font-weight: 700;
            color: var(--primary);
            font-size: 0.95rem;
            margin-bottom: 0.75rem;
        }}
        
        .sns-username a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .sns-content {{
            color: var(--text-primary);
            font-size: 0.9rem;
            line-height: 1.5;
            margin-bottom: 1rem;
        }}
        
        .sns-time {{
            color: var(--text-muted);
            font-size: 0.8rem;
            font-weight: 500;
        }}
        
        /* Trends section */
        .trends-section {{
            background: var(--bg-card);
            border-radius: var(--radius);
            padding: 2.5rem;
            box-shadow: var(--shadow-md);
        }}
        
        .trend-keywords {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .keyword {{
            padding: 0.75rem 1.25rem;
            background: var(--primary);
            color: white;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: var(--transition);
            cursor: pointer;
        }}
        
        .keyword.hot {{
            background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%);
            animation: pulse 2s infinite;
        }}
        
        .keyword:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-sm);
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.8; }}
        }}
        
        /* Floating action button */
        .fab {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: var(--primary);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-lg);
            cursor: pointer;
            transition: var(--transition);
            z-index: 1000;
            font-size: 1.5rem;
            border: none;
        }}
        
        .fab:hover {{
            transform: scale(1.1);
            background: var(--primary-hover);
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .container {{
                padding: 1.5rem;
            }}
            
            .header-content {{
                padding: 1rem 1.5rem;
            }}
            
            .summary {{
                padding: 2rem;
            }}
            
            .kpi-grid {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .news-grid {{
                grid-template-columns: 1fr;
            }}
            
            .sns-grid {{
                grid-template-columns: 1fr;
            }}
            
            .tabs {{
                gap: 0.5rem;
            }}
            
            .tab {{
                padding: 0.75rem 1.5rem;
                font-size: 0.9rem;
            }}
            
            .header-stats {{
                display: none;
            }}
        }}
        
        @media (max-width: 480px) {{
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}
            
            .fab {{
                width: 50px;
                height: 50px;
                bottom: 1rem;
                right: 1rem;
            }}
        }}
        
        /* Focus styles for accessibility */
        button:focus, a:focus, .tab:focus {{
            outline: 3px solid var(--primary);
            outline-offset: 2px;
        }}
        
        /* Reduced motion */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        
        /* Print styles */
        @media print {{
            .header, .fab, .tabs {{
                display: none;
            }}
            
            .tab-content {{
                display: block !important;
            }}
            
            .container {{
                background: white;
                box-shadow: none;
            }}
        }}
    </style>
</head>
<body>
    <a href="#main-content" class="skip-link">メインコンテンツへスキップ</a>
    
    <header class="header" role="banner">
        <div class="header-content">
            <h1>🤖 AI業界ダッシュボード</h1>
            <div class="header-stats" aria-label="統計情報">
                <div class="stat">
                    <span>📅</span>
                    <span>{current_date}</span>
                </div>
                <div class="stat">
                    <span>🕐</span>
                    <span>{current_time} JST</span>
                </div>
                <div class="stat">
                    <span>📰</span>
                    <span class="stat-value">{data['total_news']}</span>件
                </div>
                <div class="stat">
                    <span>📊</span>
                    <span class="stat-value">{data['sns_posts']}</span>投稿
                </div>
            </div>
        </div>
    </header>
    
    <main id="main-content" class="container" role="main">
        <!-- サマリーセクション -->
        <section class="summary" aria-labelledby="summary-heading">
            <h2 id="summary-heading">📊 本日のサマリー</h2>
            <p>{data['summary_text'] or 'AI業界の最新動向を分析中...'}</p>
            
            <div class="kpi-grid" role="list">
                <div class="kpi" role="listitem" tabindex="0">
                    <div class="kpi-number">{data['total_news']}</div>
                    <div class="kpi-label">総ニュース数</div>
                </div>
                <div class="kpi" role="listitem" tabindex="0">
                    <div class="kpi-number">{data['active_companies']}</div>
                    <div class="kpi-label">活動企業数</div>
                </div>
                <div class="kpi" role="listitem" tabindex="0">
                    <div class="kpi-number">{data['total_sources']}</div>
                    <div class="kpi-label">情報ソース数</div>
                </div>
                <div class="kpi" role="listitem" tabindex="0">
                    <div class="kpi-number">{data['sns_posts']}</div>
                    <div class="kpi-label">SNS投稿数</div>
                </div>
            </div>
        </section>
        
        <!-- タブナビゲーション -->
        <nav class="tabs" role="tablist" aria-label="コンテンツカテゴリー">
            <button class="tab active" role="tab" aria-selected="true" data-tab="business">
                💼 ビジネス ({len(data['business_news'])}件)
            </button>
            <button class="tab" role="tab" aria-selected="false" data-tab="sns">
                🐦 SNS投稿 ({len(data['featured_posts'])}件)
            </button>
            <button class="tab" role="tab" aria-selected="false" data-tab="trends">
                📈 トレンド ({len(data['trends'])}件)
            </button>
        </nav>
        
        <!-- ビジネスニュース -->
        <div class="tab-content active" id="business" role="tabpanel">
            <div class="news-grid">'''
    
    # ビジネスニュースを追加
    for news in data['business_news']:
        html += f'''
                <article class="news-card">
                    <div class="news-category">{news['category']}</div>
                    <h3 class="news-title">
                        <a href="{news['link']}" target="_blank" rel="noopener noreferrer">
                            {news['title']}
                        </a>
                    </h3>
                    <p class="news-summary">{news['summary']}</p>
                    <div class="news-meta">
                        <span class="news-source">{news['source']}</span>
                        <span>{news['time']}</span>
                    </div>
                </article>'''
    
    # SNS投稿セクション
    html += '''
            </div>
        </div>
        
        <!-- SNS投稿 -->
        <div class="tab-content" id="sns" role="tabpanel">
            <div class="sns-section">
                <h3>📢 注目の投稿</h3>
                <div class="sns-grid">'''
    
    for post in data['featured_posts']:
        html += f'''
                    <article class="sns-post">
                        <div class="sns-username">
                            <a href="{post['url']}" target="_blank" rel="noopener noreferrer">
                                {post['username']}
                            </a>
                        </div>
                        <p class="sns-content">{post['summary']}</p>
                        <div class="sns-time">X/Twitter • {post['time']}</div>
                    </article>'''
    
    # トレンドセクション
    html += '''
                </div>
            </div>
        </div>
        
        <!-- トレンド -->
        <div class="tab-content" id="trends" role="tabpanel">
            <div class="trends-section">
                <h3>🔥 本日のトレンドキーワード</h3>
                <div class="trend-keywords">'''
    
    for trend in data['trends']:
        hot_class = ' hot' if trend['hot'] else ''
        html += f'<span class="keyword{hot_class}">{trend["keyword"]} ({trend["count"]})</span>'
    
    html += '''
                </div>
            </div>
        </div>
        
    </main>
    
    <!-- Floating Action Button -->
    <button class="fab" aria-label="トップへ戻る" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
        ↑
    </button>
    
    <script>
        // タブ切り替え機能
        document.querySelectorAll('.tab').forEach(tab => {{
            tab.addEventListener('click', () => {{
                const target = tab.dataset.tab;
                
                // アクティブなタブを更新
                document.querySelectorAll('.tab').forEach(t => {{
                    t.classList.remove('active');
                    t.setAttribute('aria-selected', 'false');
                }});
                tab.classList.add('active');
                tab.setAttribute('aria-selected', 'true');
                
                // コンテンツを切り替え
                document.querySelectorAll('.tab-content').forEach(content => {{
                    content.classList.remove('active');
                }});
                document.getElementById(target).classList.add('active');
            }});
        }});
        
        // インターセクションオブザーバーでスクロール時アニメーション
        if ('IntersectionObserver' in window) {{
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }}, {{
                threshold: 0.1
            }});
            
            document.querySelectorAll('.news-card, .sns-post, .kpi').forEach(el => {{
                el.style.opacity = '0';
                el.style.transform = 'translateY(30px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(el);
            }});
        }}
        
        // キーボードナビゲーション
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                document.activeElement.blur();
            }}
            
            // タブ切り替えのキーボードショートカット
            if (e.ctrlKey || e.metaKey) {{
                const tabs = document.querySelectorAll('.tab');
                const activeIndex = Array.from(tabs).findIndex(tab => tab.classList.contains('active'));
                
                if (e.key === 'ArrowRight' && activeIndex < tabs.length - 1) {{
                    e.preventDefault();
                    tabs[activeIndex + 1].click();
                }} else if (e.key === 'ArrowLeft' && activeIndex > 0) {{
                    e.preventDefault();
                    tabs[activeIndex - 1].click();
                }}
            }}
        }});
        
        // パフォーマンス監視
        if ('PerformanceObserver' in window) {{
            const observer = new PerformanceObserver((list) => {{
                const entries = list.getEntries();
                entries.forEach(entry => {{
                    if (entry.entryType === 'navigation') {{
                        console.log('Page load time:', entry.loadEventEnd - entry.loadEventStart, 'ms');
                    }}
                }});
            }});
            observer.observe({{entryTypes: ['navigation']}});
        }}
        
        // Service Worker for offline support (optional)
        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/sw.js').catch(() => {{}});
        }}
    </script>
</body>
</html>'''
    
    return html

if __name__ == "__main__":
    print("🎨 実データを使用した改善版ダッシュボード生成開始...")
    
    try:
        html = generate_improved_dashboard_with_real_data()
        
        if html:
            # ファイルに保存
            with open("index_improved_real.html", "w", encoding="utf-8") as f:
                f.write(html)
            
            print(f"✅ 実データ改善版ダッシュボード生成完了: index_improved_real.html")
            print(f"📊 ファイルサイズ: {len(html):,} characters")
            
            # 統計情報
            print(f"\n📈 データ統計:")
            print(f"   - HTMLサイズ: {len(html) // 1024}KB")
            print(f"   - CSSライン数: {html.count('{{')}")
            print(f"   - JSコード: {len(html.split('</script>')[0].split('<script>')[-1]) if '<script>' in html else 0} characters")
        else:
            print("❌ ダッシュボード生成に失敗しました")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()