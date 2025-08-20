#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final UI Dashboard - タブ機能完全版
"""
import os
import re
from datetime import datetime
from pathlib import Path

def extract_comprehensive_data():
    """既存HTMLから包括的なデータを抽出"""
    
    index_path = Path("index.html")
    if not index_path.exists():
        print("❌ index.html が見つかりません")
        return create_fallback_data()
    
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        print("📊 実データを抽出中...")
        
        # 基本データ構造
        data = {
            'total_news': 0,
            'active_companies': 0, 
            'total_sources': 0,
            'sns_posts': 0,
            'summary_text': '',
            'business_news': [],
            'tech_news': [],
            'research_news': [],
            'featured_posts': [],
            'tech_discussions': [],
            'trends': []
        }
        
        # KPI数値の抽出
        kpi_numbers = re.findall(r'<div class="kpi-number">(\d+)</div>', content)
        if len(kpi_numbers) >= 4:
            data['total_news'] = int(kpi_numbers[0])
            data['active_companies'] = int(kpi_numbers[1]) 
            data['total_sources'] = int(kpi_numbers[2])
            data['sns_posts'] = int(kpi_numbers[3])
        
        # サマリーテキスト
        summary_match = re.search(r'<p>([^<]+)</p>', content)
        if summary_match:
            data['summary_text'] = summary_match.group(1)
        
        # ビジネス・投資ニュース（💼 セクション）
        business_section = re.search(r'💼 ビジネス・投資.*?<div class="section-content">(.*?)</div>\s*</div>\s*<div class="category-card">', content, re.DOTALL)
        if business_section:
            business_content = business_section.group(1)
            topic_items = re.findall(r'<div class="topic-item">.*?<a href="([^"]+)"[^>]*>([^<]+)</a>.*?<div class="topic-meta">([^<]+).*?</div>.*?<div class="topic-summary">([^<]+)</div>', business_content, re.DOTALL)
            
            for link, title, meta, summary in topic_items[:8]:
                source_time = meta.split(' • ')
                source = source_time[0].strip() if source_time else 'Unknown'
                time_str = source_time[1].strip() if len(source_time) > 1 else '00:00'
                
                data['business_news'].append({
                    'title': title.strip(),
                    'summary': summary.strip()[:300],
                    'link': link.strip(),
                    'source': source,
                    'time': time_str
                })
        
        # テクノロジー・ツールニュース（⚡ セクション）
        tech_section = re.search(r'⚡ テクノロジー・ツール.*?<div class="section-content">(.*?)</div>\s*</div>\s*<div class="category-card">', content, re.DOTALL)
        if tech_section:
            tech_content = tech_section.group(1)
            topic_items = re.findall(r'<div class="topic-item">.*?<a href="([^"]+)"[^>]*>([^<]+)</a>.*?<div class="topic-meta">([^<]+).*?</div>.*?<div class="topic-summary">([^<]+)</div>', tech_content, re.DOTALL)
            
            for link, title, meta, summary in topic_items[:8]:
                source_time = meta.split(' • ')
                source = source_time[0].strip() if source_time else 'Unknown'
                time_str = source_time[1].strip() if len(source_time) > 1 else '00:00'
                
                data['tech_news'].append({
                    'title': title.strip(),
                    'summary': summary.strip()[:300],
                    'link': link.strip(),
                    'source': source,
                    'time': time_str
                })
        
        # 研究・論文ニュース（🧪 セクション）
        research_section = re.search(r'🧪 SNS・論文.*?<div class="section-content">(.*?)</div>\s*</div>', content, re.DOTALL)
        if research_section:
            research_content = research_section.group(1)
            topic_items = re.findall(r'<div class="topic-item">.*?<a href="([^"]+)"[^>]*>([^<]+)</a>.*?<div class="topic-meta">([^<]+).*?</div>.*?<div class="topic-summary">([^<]+)</div>', research_content, re.DOTALL)
            
            for link, title, meta, summary in topic_items[:8]:
                source_time = meta.split(' • ')
                source = source_time[0].strip() if source_time else 'Unknown'
                time_str = source_time[1].strip() if len(source_time) > 1 else '00:00'
                
                data['research_news'].append({
                    'title': title.strip(),
                    'summary': summary.strip()[:300],
                    'link': link.strip(),
                    'source': source,
                    'time': time_str
                })
        
        # 注目の投稿（SNSセクション）
        featured_section = re.search(r'📢 注目の投稿（最大5件表示）(.*?)💬 技術ディスカッション', content, re.DOTALL)
        if featured_section:
            featured_content = featured_section.group(1)
            sns_posts = re.findall(r'<a href="([^"]+)"[^>]*>\s*(@[^<]+)\s*</a>.*?<div[^>]*>([^<]+)</div>.*?<div[^>]*>([^<]+)</div>', featured_content, re.DOTALL)
            
            for url, username, summary, time_info in sns_posts:
                time_str = time_info.split(' • ')[1] if ' • ' in time_info else '00:00'
                data['featured_posts'].append({
                    'username': username.strip(),
                    'summary': summary.strip(),
                    'url': url.strip(),
                    'time': time_str.strip()
                })
        
        # 技術ディスカッション
        tech_discussion_section = re.search(r'💬 技術ディスカッション（最大5件表示）(.*?)</div>\s*</div>\s*</div>', content, re.DOTALL)
        if tech_discussion_section:
            tech_content = tech_discussion_section.group(1)
            tech_posts = re.findall(r'<a href="([^"]+)"[^>]*>\s*(@[^<]+)\s*</a>.*?<div[^>]*>([^<]+)</div>.*?<div[^>]*>([^<]+)</div>', tech_content, re.DOTALL)
            
            for url, username, summary, time_info in tech_posts:
                time_str = time_info.split(' • ')[1] if ' • ' in time_info else '00:00'
                data['tech_discussions'].append({
                    'username': username.strip(),
                    'summary': summary.strip(),
                    'url': url.strip(),
                    'time': time_str.strip()
                })
        
        # トレンドキーワード
        trend_matches = re.findall(r'<span class="keyword">([^<(]+)\s*\((\d+)\)</span>', content)
        for keyword, count in trend_matches:
            data['trends'].append({
                'keyword': keyword.strip(),
                'count': int(count),
                'hot': int(count) > 5
            })
        
        print(f"✅ データ抽出完了:")
        print(f"   - ビジネスニュース: {len(data['business_news'])}件")
        print(f"   - テクノロジーニュース: {len(data['tech_news'])}件") 
        print(f"   - 研究・論文: {len(data['research_news'])}件")
        print(f"   - 注目の投稿: {len(data['featured_posts'])}件")
        print(f"   - 技術ディスカッション: {len(data['tech_discussions'])}件")
        print(f"   - トレンドキーワード: {len(data['trends'])}件")
        
        return data
        
    except Exception as e:
        print(f"❌ データ抽出エラー: {e}")
        return create_fallback_data()

def create_fallback_data():
    """フォールバックデータを作成"""
    return {
        'total_news': 18,
        'active_companies': 6,
        'total_sources': 9,
        'sns_posts': 217,
        'summary_text': '今日のAI業界: 18件のニュース、6社が活動',
        'business_news': [
            {
                'title': 'データ読み込み中...',
                'summary': '実際のデータを読み込んでいます。しばらくお待ちください。',
                'link': '#',
                'source': 'System',
                'time': '00:00'
            }
        ],
        'tech_news': [],
        'research_news': [],
        'featured_posts': [],
        'tech_discussions': [],
        'trends': []
    }

def generate_final_dashboard():
    """完全版ダッシュボード生成"""
    
    # 実データを取得
    data = extract_comprehensive_data()
    
    # 現在時刻
    jst = datetime.now()
    current_date = jst.strftime('%Y-%m-%d')
    current_time = jst.strftime('%H:%M')
    
    html = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="AI業界の最新ニュース、トレンド、企業動向を毎日更新。{current_date}の重要な動向を一覧で確認">
    <meta name="theme-color" content="#3b82f6">
    <title>AI業界ダッシュボード | {current_date}</title>
    
    <style>
        :root {{
            --primary: #3b82f6;
            --primary-hover: #2563eb;
            --secondary: #10b981;
            --accent: #8b5cf6;
            --success: #22c55e;
            --warning: #f59e0b;
            --error: #ef4444;
            
            --bg-main: #f8fafc;
            --bg-card: #ffffff;
            --bg-hover: #f1f5f9;
            --bg-active: #e2e8f0;
            
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --text-muted: #64748b;
            --text-light: #94a3b8;
            
            --border-light: #f1f5f9;
            --border-main: #e2e8f0;
            --border-dark: #cbd5e1;
            
            --shadow-sm: 0 1px 2px rgba(0,0,0,0.05);
            --shadow: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
            --shadow-xl: 0 20px 25px rgba(0,0,0,0.15);
            
            --radius: 12px;
            --radius-sm: 8px;
            --radius-lg: 16px;
            
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            --transition-fast: all 0.15s ease;
        }}
        
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-main: #0f172a;
                --bg-card: #1e293b;
                --bg-hover: #334155;
                --bg-active: #475569;
                
                --text-primary: #f1f5f9;
                --text-secondary: #cbd5e1;
                --text-muted: #94a3b8;
                --text-light: #64748b;
                
                --border-light: #334155;
                --border-main: #475569;
                --border-dark: #64748b;
            }}
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        html {{
            scroll-behavior: smooth;
            font-size: 16px;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans JP", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        /* Skip Link for Accessibility */
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--primary);
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            z-index: 1000;
            border-radius: 0 0 var(--radius-sm) 0;
            transition: var(--transition-fast);
        }}
        
        .skip-link:focus {{
            top: 0;
        }}
        
        /* Header */
        .header {{
            position: sticky;
            top: 0;
            z-index: 100;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(20px);
            border-bottom: 1px solid var(--border-main);
            transition: var(--transition);
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
            font-weight: 800;
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
            font-weight: 500;
        }}
        
        .stat-value {{
            font-weight: 700;
            color: var(--primary);
        }}
        
        /* Main Container */
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 2rem;
            background: var(--bg-main);
            border-radius: var(--radius-lg) var(--radius-lg) 0 0;
            margin-top: -10px;
            min-height: calc(100vh - 100px);
        }}
        
        /* Summary Section */
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
            opacity: 0.08;
            border-radius: 50%;
        }}
        
        .summary h2 {{
            font-size: 1.75rem;
            font-weight: 700;
            margin-bottom: 1rem;
            color: var(--text-primary);
            position: relative;
            z-index: 1;
        }}
        
        .summary p {{
            color: var(--text-secondary);
            font-size: 1.125rem;
            margin-bottom: 2rem;
            position: relative;
            z-index: 1;
            line-height: 1.7;
        }}
        
        /* KPI Grid */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 1.5rem;
            position: relative;
            z-index: 1;
        }}
        
        .kpi {{
            background: var(--bg-hover);
            border-radius: var(--radius);
            padding: 2rem 1.5rem;
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
            transform: translateY(-6px);
            box-shadow: var(--shadow-lg);
            border-color: var(--primary);
        }}
        
        .kpi:hover::before {{
            transform: scaleX(1);
        }}
        
        .kpi:focus {{
            outline: 3px solid var(--primary);
            outline-offset: 2px;
        }}
        
        .kpi-number {{
            font-size: 3rem;
            font-weight: 800;
            color: var(--primary);
            margin-bottom: 0.5rem;
            line-height: 1;
        }}
        
        .kpi-label {{
            font-size: 1rem;
            color: var(--text-muted);
            font-weight: 600;
        }}
        
        /* Tab Navigation */
        .tabs {{
            display: flex;
            gap: 1rem;
            margin-bottom: 2.5rem;
            overflow-x: auto;
            padding: 0.5rem;
            scroll-snap-type: x mandatory;
            -webkit-overflow-scrolling: touch;
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
            border: 2px solid var(--border-main);
            border-radius: var(--radius);
            color: var(--text-secondary);
            font-weight: 600;
            font-size: 0.95rem;
            cursor: pointer;
            transition: var(--transition);
            white-space: nowrap;
            scroll-snap-align: start;
            position: relative;
            user-select: none;
        }}
        
        .tab:hover {{
            background: var(--bg-hover);
            transform: translateY(-2px);
            box-shadow: var(--shadow);
        }}
        
        .tab.active {{
            background: var(--primary);
            color: white;
            border-color: var(--primary);
            box-shadow: var(--shadow);
        }}
        
        .tab:focus {{
            outline: 3px solid var(--primary);
            outline-offset: 2px;
        }}
        
        /* Tab Content */
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
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        /* News Grid */
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(380px, 1fr));
            gap: 2rem;
        }}
        
        .news-card {{
            background: var(--bg-card);
            border-radius: var(--radius);
            padding: 2rem;
            box-shadow: var(--shadow);
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
            background: linear-gradient(135deg, transparent 0%, rgba(59, 130, 246, 0.02) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
        }}
        
        .news-card:hover {{
            transform: translateY(-8px);
            box-shadow: var(--shadow-xl);
        }}
        
        .news-card:hover::before {{
            opacity: 1;
        }}
        
        .news-category {{
            display: inline-block;
            padding: 0.5rem 1rem;
            background: var(--primary);
            color: white;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 700;
            margin-bottom: 1.25rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        
        .news-title {{
            font-size: 1.375rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1rem;
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
        
        .news-title a:focus {{
            outline: 2px solid var(--primary);
            outline-offset: 2px;
        }}
        
        .news-summary {{
            color: var(--text-secondary);
            font-size: 1rem;
            line-height: 1.7;
            margin-bottom: 1.5rem;
            position: relative;
            z-index: 1;
        }}
        
        .news-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.875rem;
            color: var(--text-muted);
            position: relative;
            z-index: 1;
        }}
        
        .news-source {{
            font-weight: 600;
            color: var(--text-secondary);
        }}
        
        /* SNS Section */
        .sns-section {{
            margin-bottom: 3rem;
        }}
        
        .sns-section h3 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1.5rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--border-main);
        }}
        
        .sns-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 1.5rem;
        }}
        
        .sns-post {{
            background: var(--bg-card);
            border-radius: var(--radius);
            padding: 1.75rem;
            box-shadow: var(--shadow);
            transition: var(--transition);
            border-left: 4px solid var(--secondary);
            position: relative;
        }}
        
        .sns-post:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
            border-left-color: var(--primary);
        }}
        
        .sns-username {{
            font-weight: 700;
            color: var(--primary);
            font-size: 1rem;
            margin-bottom: 1rem;
        }}
        
        .sns-username a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .sns-username a:hover {{
            text-decoration: underline;
        }}
        
        .sns-username a:focus {{
            outline: 2px solid var(--primary);
            outline-offset: 2px;
        }}
        
        .sns-content {{
            color: var(--text-primary);
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 1rem;
        }}
        
        .sns-time {{
            color: var(--text-muted);
            font-size: 0.875rem;
            font-weight: 500;
        }}
        
        /* Trends Section */
        .trends-section {{
            background: var(--bg-card);
            border-radius: var(--radius);
            padding: 2.5rem;
            box-shadow: var(--shadow);
        }}
        
        .trends-section h3 {{
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 1.5rem;
        }}
        
        .trend-keywords {{
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .keyword {{
            padding: 0.875rem 1.5rem;
            background: var(--primary);
            color: white;
            border-radius: 30px;
            font-size: 0.9rem;
            font-weight: 600;
            transition: var(--transition);
            cursor: pointer;
            user-select: none;
        }}
        
        .keyword.hot {{
            background: linear-gradient(135deg, var(--accent) 0%, var(--primary) 100%);
            animation: pulse 2s infinite;
            position: relative;
        }}
        
        .keyword.hot::before {{
            content: '🔥';
            margin-right: 0.5rem;
        }}
        
        .keyword:hover {{
            transform: translateY(-3px);
            box-shadow: var(--shadow);
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.85; }}
        }}
        
        /* Empty State */
        .empty-state {{
            text-align: center;
            padding: 3rem;
            color: var(--text-muted);
        }}
        
        .empty-state .emoji {{
            font-size: 3rem;
            margin-bottom: 1rem;
        }}
        
        /* Floating Action Button */
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
        
        .fab:focus {{
            outline: 3px solid var(--primary);
            outline-offset: 3px;
        }}
        
        /* Responsive Design */
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
                padding: 0.25rem;
            }}
            
            .tab {{
                padding: 0.875rem 1.25rem;
                font-size: 0.875rem;
            }}
            
            .header-stats {{
                display: none;
            }}
            
            .kpi-number {{
                font-size: 2.5rem;
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
            
            .news-card, .sns-post {{
                padding: 1.5rem;
            }}
        }}
        
        /* High Contrast Mode */
        @media (prefers-contrast: high) {{
            :root {{
                --border-main: #000000;
                --text-primary: #000000;
            }}
        }}
        
        /* Reduced Motion */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
        
        /* Print Styles */
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
                max-width: none;
            }}
            
            .news-card, .sns-post {{
                break-inside: avoid;
                box-shadow: none;
                border: 1px solid #ccc;
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
        <!-- Summary Section -->
        <section class="summary" aria-labelledby="summary-heading">
            <h2 id="summary-heading">📊 本日のサマリー</h2>
            <p>{data['summary_text']}</p>
            
            <div class="kpi-grid" role="list">
                <div class="kpi" role="listitem" tabindex="0" aria-label="総ニュース数 {data['total_news']}件">
                    <div class="kpi-number">{data['total_news']}</div>
                    <div class="kpi-label">総ニュース数</div>
                </div>
                <div class="kpi" role="listitem" tabindex="0" aria-label="活動企業数 {data['active_companies']}社">
                    <div class="kpi-number">{data['active_companies']}</div>
                    <div class="kpi-label">活動企業数</div>
                </div>
                <div class="kpi" role="listitem" tabindex="0" aria-label="情報ソース数 {data['total_sources']}個">
                    <div class="kpi-number">{data['total_sources']}</div>
                    <div class="kpi-label">情報ソース数</div>
                </div>
                <div class="kpi" role="listitem" tabindex="0" aria-label="SNS投稿数 {data['sns_posts']}件">
                    <div class="kpi-number">{data['sns_posts']}</div>
                    <div class="kpi-label">SNS投稿数</div>
                </div>
            </div>
        </section>
        
        <!-- Tab Navigation -->
        <nav class="tabs" role="tablist" aria-label="コンテンツカテゴリー">
            <button 
                class="tab active" 
                role="tab" 
                aria-selected="true" 
                aria-controls="business" 
                id="tab-business"
                data-target="business"
            >
                💼 ビジネス ({len(data['business_news'])}件)
            </button>
            <button 
                class="tab" 
                role="tab" 
                aria-selected="false" 
                aria-controls="technology" 
                id="tab-technology"
                data-target="technology"
            >
                ⚡ テクノロジー ({len(data['tech_news'])}件)
            </button>
            <button 
                class="tab" 
                role="tab" 
                aria-selected="false" 
                aria-controls="research" 
                id="tab-research"
                data-target="research"
            >
                🧪 研究・論文 ({len(data['research_news'])}件)
            </button>
            <button 
                class="tab" 
                role="tab" 
                aria-selected="false" 
                aria-controls="sns" 
                id="tab-sns"
                data-target="sns"
            >
                🐦 SNS投稿 ({len(data['featured_posts']) + len(data['tech_discussions'])}件)
            </button>
            <button 
                class="tab" 
                role="tab" 
                aria-selected="false" 
                aria-controls="trends" 
                id="tab-trends"
                data-target="trends"
            >
                📈 トレンド ({len(data['trends'])}件)
            </button>
        </nav>
        
        <!-- Business News -->
        <div class="tab-content active" id="business" role="tabpanel" aria-labelledby="tab-business">
            {generate_news_grid(data['business_news'], 'ビジネス')}
        </div>
        
        <!-- Technology News -->
        <div class="tab-content" id="technology" role="tabpanel" aria-labelledby="tab-technology">
            {generate_news_grid(data['tech_news'], 'テクノロジー')}
        </div>
        
        <!-- Research News -->
        <div class="tab-content" id="research" role="tabpanel" aria-labelledby="tab-research">
            {generate_news_grid(data['research_news'], '研究・論文')}
        </div>
        
        <!-- SNS Posts -->
        <div class="tab-content" id="sns" role="tabpanel" aria-labelledby="tab-sns">
            <div class="sns-section">
                <h3>📢 注目の投稿</h3>
                {generate_sns_grid(data['featured_posts'])}
            </div>
            
            <div class="sns-section">
                <h3>💬 技術ディスカッション</h3>
                {generate_sns_grid(data['tech_discussions'])}
            </div>
        </div>
        
        <!-- Trends -->
        <div class="tab-content" id="trends" role="tabpanel" aria-labelledby="tab-trends">
            <div class="trends-section">
                <h3>🔥 本日のトレンドキーワード</h3>
                {generate_trends_section(data['trends'])}
            </div>
        </div>
        
    </main>
    
    <!-- Floating Action Button -->
    <button 
        class="fab" 
        aria-label="トップへ戻る" 
        onclick="scrollToTop()"
        onkeydown="handleFabKeydown(event)"
    >
        ↑
    </button>
    
    <script>
        // Tab functionality with proper event handling
        class TabController {{
            constructor() {{
                this.tabs = document.querySelectorAll('.tab');
                this.contents = document.querySelectorAll('.tab-content');
                this.init();
            }}
            
            init() {{
                // Add click event listeners to all tabs
                this.tabs.forEach(tab => {{
                    tab.addEventListener('click', (e) => this.switchTab(e));
                    tab.addEventListener('keydown', (e) => this.handleTabKeydown(e));
                }});
                
                // Set initial state
                this.updateActiveTab('business');
            }}
            
            switchTab(event) {{
                const target = event.target.dataset.target;
                if (target) {{
                    this.updateActiveTab(target);
                }}
            }}
            
            updateActiveTab(targetId) {{
                // Update tab states
                this.tabs.forEach(tab => {{
                    const isActive = tab.dataset.target === targetId;
                    tab.classList.toggle('active', isActive);
                    tab.setAttribute('aria-selected', isActive);
                }});
                
                // Update content states
                this.contents.forEach(content => {{
                    const isActive = content.id === targetId;
                    content.classList.toggle('active', isActive);
                }});
                
                // Announce change to screen readers
                const activeTab = document.querySelector(`[data-target="${{targetId}}"]`);
                if (activeTab) {{
                    activeTab.focus();
                }}
                
                console.log(`Switched to tab: ${{targetId}}`);
            }}
            
            handleTabKeydown(event) {{
                const tabs = Array.from(this.tabs);
                const currentIndex = tabs.indexOf(event.target);
                
                switch (event.key) {{
                    case 'ArrowLeft':
                        event.preventDefault();
                        const prevIndex = currentIndex > 0 ? currentIndex - 1 : tabs.length - 1;
                        tabs[prevIndex].click();
                        break;
                        
                    case 'ArrowRight':
                        event.preventDefault();
                        const nextIndex = currentIndex < tabs.length - 1 ? currentIndex + 1 : 0;
                        tabs[nextIndex].click();
                        break;
                        
                    case 'Home':
                        event.preventDefault();
                        tabs[0].click();
                        break;
                        
                    case 'End':
                        event.preventDefault();
                        tabs[tabs.length - 1].click();
                        break;
                }}
            }}
        }}
        
        // Initialize tab controller
        let tabController;
        document.addEventListener('DOMContentLoaded', () => {{
            tabController = new TabController();
        }});
        
        // Scroll to top function
        function scrollToTop() {{
            window.scrollTo({{
                top: 0,
                behavior: 'smooth'
            }});
        }}
        
        // FAB keyboard handling
        function handleFabKeydown(event) {{
            if (event.key === 'Enter' || event.key === ' ') {{
                event.preventDefault();
                scrollToTop();
            }}
        }}
        
        // Intersection Observer for scroll animations
        if ('IntersectionObserver' in window) {{
            const observerOptions = {{
                threshold: 0.1,
                rootMargin: '0px 0px -50px 0px'
            }};
            
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }}, observerOptions);
            
            // Observe elements for animation
            document.querySelectorAll('.news-card, .sns-post, .kpi').forEach(el => {{
                el.style.opacity = '0';
                el.style.transform = 'translateY(30px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(el);
            }});
        }}
        
        // Global keyboard shortcuts
        document.addEventListener('keydown', (event) => {{
            // Escape to close focus
            if (event.key === 'Escape') {{
                document.activeElement.blur();
            }}
            
            // Ctrl/Cmd + number keys for tab switching
            if ((event.ctrlKey || event.metaKey) && event.key >= '1' && event.key <= '5') {{
                event.preventDefault();
                const tabIndex = parseInt(event.key) - 1;
                const tabs = document.querySelectorAll('.tab');
                if (tabs[tabIndex]) {{
                    tabs[tabIndex].click();
                }}
            }}
        }});
        
        // Performance monitoring
        if ('PerformanceObserver' in window) {{
            try {{
                const observer = new PerformanceObserver((list) => {{
                    const entries = list.getEntries();
                    entries.forEach(entry => {{
                        if (entry.entryType === 'navigation') {{
                            console.log('Page load performance:', {{
                                'DOM Content Loaded': entry.domContentLoadedEventEnd - entry.domContentLoadedEventStart,
                                'Load Event': entry.loadEventEnd - entry.loadEventStart,
                                'Total Load Time': entry.loadEventEnd - entry.fetchStart
                            }});
                        }}
                    }});
                }});
                observer.observe({{entryTypes: ['navigation']}});
            }} catch (e) {{
                console.log('Performance monitoring not available');
            }}
        }}
        
        // Service Worker registration (optional)
        if ('serviceWorker' in navigator) {{
            window.addEventListener('load', () => {{
                navigator.serviceWorker.register('/sw.js')
                    .then(() => console.log('SW registered'))
                    .catch(() => console.log('SW registration failed'));
            }});
        }}
        
        console.log('🤖 AI Dashboard initialized successfully');
    </script>
</body>
</html>'''
    
    return html

def generate_news_grid(news_items, category):
    """ニュースグリッドを生成"""
    if not news_items:
        return '''
        <div class="empty-state">
            <div class="emoji">📰</div>
            <p>現在このカテゴリにはニュースがありません</p>
        </div>'''
    
    grid_html = '<div class="news-grid">'
    
    for item in news_items:
        grid_html += f'''
        <article class="news-card">
            <div class="news-category">{category}</div>
            <h3 class="news-title">
                <a href="{item['link']}" target="_blank" rel="noopener noreferrer">
                    {item['title']}
                </a>
            </h3>
            <p class="news-summary">{item['summary']}</p>
            <div class="news-meta">
                <span class="news-source">{item['source']}</span>
                <span>{item['time']}</span>
            </div>
        </article>'''
    
    grid_html += '</div>'
    return grid_html

def generate_sns_grid(posts):
    """SNSグリッドを生成"""
    if not posts:
        return '''
        <div class="empty-state">
            <div class="emoji">🐦</div>
            <p>現在投稿がありません</p>
        </div>'''
    
    grid_html = '<div class="sns-grid">'
    
    for post in posts:
        grid_html += f'''
        <article class="sns-post">
            <div class="sns-username">
                <a href="{post['url']}" target="_blank" rel="noopener noreferrer">
                    {post['username']}
                </a>
            </div>
            <p class="sns-content">{post['summary']}</p>
            <div class="sns-time">X/Twitter • {post['time']}</div>
        </article>'''
    
    grid_html += '</div>'
    return grid_html

def generate_trends_section(trends):
    """トレンドセクションを生成"""
    if not trends:
        return '''
        <div class="empty-state">
            <div class="emoji">📈</div>
            <p>現在トレンドデータがありません</p>
        </div>'''
    
    keywords_html = '<div class="trend-keywords">'
    
    for trend in trends:
        hot_class = ' hot' if trend['hot'] else ''
        keywords_html += f'''
        <span class="keyword{hot_class}" tabindex="0">
            {trend['keyword']} ({trend['count']})
        </span>'''
    
    keywords_html += '</div>'
    return keywords_html

if __name__ == "__main__":
    print("🎨 最終版UI/UXダッシュボード生成開始...")
    
    try:
        html = generate_final_dashboard()
        
        # ファイル保存
        output_file = "index_final.html"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        
        print(f"✅ 最終版ダッシュボード生成完了!")
        print(f"📄 ファイル: {output_file}")
        print(f"📊 ファイルサイズ: {len(html) // 1024}KB")
        print(f"🎯 機能: タブ切り替え、レスポンシブ、アクセシビリティ対応")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()