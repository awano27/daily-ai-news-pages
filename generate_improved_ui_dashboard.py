#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate Improved UI/UX Dashboard - モバイル対応・アクセシビリティ改善版
"""
import os
import sys
import json
from datetime import datetime
from pathlib import Path

# 既存のモジュールをインポート
sys.path.insert(0, str(Path(__file__).parent))

def get_mock_dashboard_data():
    """デモ用のモックデータを生成"""
    return {
        'total_news': 18,
        'active_companies': 6,
        'total_sources': 9,
        'sns_posts': 217,
        'summary_text': 'AI業界は引き続き活発で、NVIDIAの新技術発表、Perplexity AIの大型買収提案、DeepMindの地球観測AI研究などが注目されています。X/Twitterでは技術者による活発な議論が継続中です。',
        'business_news': [
            {
                'title': '最新のNvidiaゲームAIおよびニューラルレンダリングテクノロジーの発表',
                'summary': 'Gamescom 2025でNVIDIAがRTXニューラルレンダリングとACE生成AI技術の最新アップデートを発表。ゲーム体験の向上を目指す。',
                'link': 'https://developer.nvidia.com/blog/announcing-the-latest-nvidia-gaming-ai-and-neural-rendering-technologies/',
                'source': 'NVIDIA Developer Blog',
                'time': '19:30',
                'category': 'ビジネス'
            },
            {
                'title': 'Perplexity AIの345億ドルのChrome入札は戦略的マスターストロークか',
                'summary': 'AI検索エンジンPerplexityがGoogle ChromeブラウザーへBidを提出。業界に大きな波紋を呼んでいる。',
                'link': 'https://www.artificialintelligence-news.com/news/perplexity-ai-chrome-bid-analysis/',
                'source': 'AI News',
                'time': '14:49',
                'category': 'ビジネス'
            }
        ],
        'tech_news': [
            {
                'title': 'AlphaEarth Foundations：地球観測データのための普遍的な埋め込み',
                'summary': 'DeepMindが数十億の多様な地球観測データで訓練された新しいAIモデルAlphaEarth Foundations(AEF)をリリース。',
                'link': 'https://www.reddit.com/r/deeplearning/comments/1mtg7mz/alphaearth_foundations_a_universal_embedding_for/',
                'source': 'Reddit DeepLearning',
                'time': '08:25',
                'category': 'テクノロジー'
            },
            {
                'title': 'モデルコンテキストプロトコルMCPは、AIインフラストラクチャの欠落標準ですか？',
                'summary': '大規模言語モデルの爆発的成長により、AIインフラストラクチャーの標準化ニーズが高まっている。',
                'link': 'https://www.marktechpost.com/2025/08/17/is-model-context-protocol-mcp-the-missing-standard-in-ai-infrastructure/',
                'source': 'MarkTechPost',
                'time': '06:57',
                'category': 'テクノロジー'
            }
        ],
        'featured_posts': [
            {
                'username': '@Majin_AppSheet',
                'summary': 'Google AppSheetを使ったAIアプリケーション開発の新しいアプローチについて詳しく解説。ノーコード環境でのAI統合の可能性を探る。',
                'url': 'https://x.com/Majin_AppSheet/status/1956930830326284344',
                'time': '06:27'
            },
            {
                'username': '@alfredplpl',
                'summary': '最新の機械学習モデルのパフォーマンス比較と実装時の注意点について。実際のプロジェクトでの経験を基にした貴重なインサイトを共有。',
                'url': 'https://x.com/alfredplpl/status/1957065303650640337',
                'time': '08:15'
            }
        ],
        'tech_discussions': [
            {
                'username': '@maru56',
                'summary': 'Transformerアーキテクチャの最新改良について技術的議論。計算効率の向上と精度のトレードオフについて深掘り。',
                'url': 'https://x.com/maru56/status/1956882934910374149',
                'time': '03:45'
            },
            {
                'username': '@__syumai',
                'summary': 'Go言語でのAIモデル推論最適化テクニック。メモリ使用量とレイテンシの改善方法について具体的なコード例付きで解説。',
                'url': 'https://x.com/__syumai/status/1957030353685668348',
                'time': '07:22'
            }
        ],
        'trends': [
            {'keyword': '大規模言語モデル', 'count': 12, 'hot': True},
            {'keyword': '生成AI', 'count': 8, 'hot': True},
            {'keyword': 'NVIDIA', 'count': 6, 'hot': False},
            {'keyword': 'Transformer', 'count': 5, 'hot': False},
            {'keyword': 'DeepMind', 'count': 4, 'hot': False}
        ]
    }

def generate_improved_dashboard():
    """改善されたUI/UXでダッシュボードを生成"""
    
    # まずはモックデータを使用（実際のデータ取得は後で統合）
    try:
        # 実データの取得を試行
        from generate_comprehensive_dashboard import analyze_ai_landscape
        dashboard_data = analyze_ai_landscape()
        
        # データが空の場合はモックデータを使用
        if not dashboard_data or dashboard_data.get('total_news', 0) == 0:
            print("⚠️ 実データが空のため、デモ用モックデータを使用します")
            dashboard_data = get_mock_dashboard_data()
        else:
            print("✅ 実データを取得しました")
            
    except Exception as e:
        print(f"⚠️ 実データ取得に失敗: {e}")
        print("デモ用モックデータを使用します")
        dashboard_data = get_mock_dashboard_data()
    
    # JST時刻
    jst = datetime.now()
    current_date = jst.strftime('%Y-%m-%d')
    current_time = jst.strftime('%H:%M')
    
    # HTMLテンプレート
    html_template = '''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="AI業界の最新ニュース、トレンド、企業動向を毎日更新。{current_date}の重要な動向を一覧で確認">
    <meta name="theme-color" content="#3b82f6">
    <title>AI業界ダッシュボード | {current_date} | daily-ai-news</title>
    
    <!-- Preload critical fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    
    <style>
        /* CSS Variables for easy theming */
        :root {{
            --primary-color: #3b82f6;
            --primary-hover: #2563eb;
            --secondary-color: #10b981;
            --accent-color: #8b5cf6;
            --danger-color: #ef4444;
            --bg-primary: #ffffff;
            --bg-secondary: #f8fafc;
            --bg-tertiary: #f1f5f9;
            --text-primary: #1e293b;
            --text-secondary: #475569;
            --text-tertiary: #64748b;
            --border-color: #e2e8f0;
            --shadow-sm: 0 1px 3px rgba(0,0,0,0.12);
            --shadow-md: 0 4px 6px rgba(0,0,0,0.1);
            --shadow-lg: 0 10px 15px rgba(0,0,0,0.1);
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            --max-width: 1400px;
        }}
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-primary: #0f172a;
                --bg-secondary: #1e293b;
                --bg-tertiary: #334155;
                --text-primary: #f1f5f9;
                --text-secondary: #cbd5e1;
                --text-tertiary: #94a3b8;
                --border-color: #475569;
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
            -moz-osx-font-smoothing: grayscale;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Noto Sans JP", Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-attachment: fixed;
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
        }}
        
        /* Skip to content link for accessibility */
        .skip-link {{
            position: absolute;
            top: -40px;
            left: 0;
            background: var(--primary-color);
            color: white;
            padding: 8px 16px;
            text-decoration: none;
            z-index: 100;
            border-radius: 0 0 var(--radius-sm) 0;
        }}
        
        .skip-link:focus {{
            top: 0;
        }}
        
        /* Sticky header with blur effect */
        .header {{
            position: sticky;
            top: 0;
            z-index: 50;
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid var(--border-color);
            transition: var(--transition);
        }}
        
        @media (prefers-color-scheme: dark) {{
            .header {{
                background: rgba(15, 23, 42, 0.95);
            }}
        }}
        
        .header-content {{
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 1rem 1.5rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 1rem;
        }}
        
        .header h1 {{
            font-size: clamp(1.25rem, 3vw, 1.75rem);
            font-weight: 700;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--accent-color) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        
        /* Quick stats bar */
        .quick-stats {{
            display: flex;
            gap: 1.5rem;
            flex-wrap: wrap;
            font-size: 0.875rem;
        }}
        
        .stat-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .stat-value {{
            font-weight: 600;
            color: var(--primary-color);
        }}
        
        /* Main container */
        .container {{
            max-width: var(--max-width);
            margin: 0 auto;
            padding: 1.5rem;
            background: var(--bg-secondary);
            min-height: calc(100vh - 80px);
        }}
        
        /* Loading skeleton animation */
        @keyframes skeleton {{
            0%% {{ background-position: -200% 0; }}
            100%% {{ background-position: 200% 0; }}
        }}
        
        .skeleton {{
            background: linear-gradient(90deg, 
                var(--bg-tertiary) 25%, 
                var(--bg-secondary) 50%, 
                var(--bg-tertiary) 75%);
            background-size: 200% 100%;
            animation: skeleton 1.5s ease-in-out infinite;
            border-radius: var(--radius-sm);
        }}
        
        /* Summary section with glass morphism */
        .summary-section {{
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }}
        
        .summary-section::before {{
            content: '';
            position: absolute;
            top: 0;
            right: 0;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, var(--primary-color) 0%, transparent 70%);
            opacity: 0.1;
            transform: translate(50%, -50%);
        }}
        
        /* KPI Grid with hover effects */
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .kpi-card {{
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            text-align: center;
            transition: var(--transition);
            cursor: pointer;
            border: 2px solid transparent;
            position: relative;
            overflow: hidden;
        }}
        
        .kpi-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .kpi-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
            border-color: var(--primary-color);
        }}
        
        .kpi-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .kpi-number {{
            font-size: 2rem;
            font-weight: 700;
            color: var(--primary-color);
            line-height: 1;
            margin-bottom: 0.5rem;
        }}
        
        .kpi-label {{
            font-size: 0.875rem;
            color: var(--text-secondary);
        }}
        
        /* Tab navigation */
        .tab-nav {{
            display: flex;
            gap: 0.5rem;
            margin-bottom: 2rem;
            overflow-x: auto;
            padding-bottom: 0.5rem;
            scroll-snap-type: x mandatory;
        }}
        
        .tab-nav::-webkit-scrollbar {{
            height: 4px;
        }}
        
        .tab-nav::-webkit-scrollbar-track {{
            background: var(--bg-tertiary);
            border-radius: 2px;
        }}
        
        .tab-nav::-webkit-scrollbar-thumb {{
            background: var(--primary-color);
            border-radius: 2px;
        }}
        
        .tab-button {{
            flex-shrink: 0;
            padding: 0.75rem 1.5rem;
            background: var(--bg-primary);
            border: 2px solid var(--border-color);
            border-radius: var(--radius-md);
            color: var(--text-secondary);
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition);
            scroll-snap-align: start;
            white-space: nowrap;
        }}
        
        .tab-button:hover {{
            background: var(--bg-tertiary);
        }}
        
        .tab-button.active {{
            background: var(--primary-color);
            color: white;
            border-color: var(--primary-color);
        }}
        
        .tab-content {{
            display: none;
            animation: fadeIn 0.3s ease;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        /* News cards with better hierarchy */
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 1.5rem;
            margin-bottom: 2rem;
        }}
        
        .news-card {{
            background: var(--bg-primary);
            border-radius: var(--radius-md);
            padding: 1.5rem;
            box-shadow: var(--shadow-sm);
            transition: var(--transition);
            position: relative;
            border-left: 4px solid var(--primary-color);
        }}
        
        .news-card:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        
        .news-category {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            background: var(--primary-color);
            color: white;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            margin-bottom: 0.75rem;
        }}
        
        .news-title {{
            font-size: 1.125rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
            line-height: 1.4;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .news-title a {{
            color: inherit;
            text-decoration: none;
            transition: color 0.2s;
        }}
        
        .news-title a:hover {{
            color: var(--primary-color);
        }}
        
        .news-summary {{
            color: var(--text-secondary);
            font-size: 0.875rem;
            line-height: 1.5;
            margin-bottom: 1rem;
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}
        
        .news-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.75rem;
            color: var(--text-tertiary);
        }}
        
        /* SNS posts section */
        .sns-section {{
            background: var(--bg-primary);
            border-radius: var(--radius-lg);
            padding: 2rem;
            margin-bottom: 2rem;
            box-shadow: var(--shadow-md);
        }}
        
        .sns-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }}
        
        .sns-post {{
            background: var(--bg-secondary);
            border-radius: var(--radius-md);
            padding: 1.25rem;
            transition: var(--transition);
            border: 1px solid var(--border-color);
        }}
        
        .sns-post:hover {{
            border-color: var(--primary-color);
            transform: scale(1.02);
        }}
        
        .sns-username {{
            font-weight: 600;
            color: var(--primary-color);
            font-size: 0.875rem;
            margin-bottom: 0.5rem;
        }}
        
        .sns-content {{
            color: var(--text-primary);
            font-size: 0.875rem;
            line-height: 1.5;
            margin-bottom: 0.75rem;
        }}
        
        .sns-time {{
            color: var(--text-tertiary);
            font-size: 0.75rem;
        }}
        
        /* Floating action button for mobile */
        .fab {{
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            width: 56px;
            height: 56px;
            border-radius: 50%;
            background: var(--primary-color);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            box-shadow: var(--shadow-lg);
            cursor: pointer;
            transition: var(--transition);
            z-index: 40;
        }}
        
        .fab:hover {{
            transform: scale(1.1);
            background: var(--primary-hover);
        }}
        
        /* Responsive breakpoints */
        @media (max-width: 768px) {{
            .container {{
                padding: 1rem;
            }}
            
            .summary-section {{
                padding: 1.5rem;
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
            
            .tab-nav {{
                gap: 0.25rem;
            }}
            
            .tab-button {{
                padding: 0.5rem 1rem;
                font-size: 0.875rem;
            }}
        }}
        
        @media (max-width: 480px) {{
            .quick-stats {{
                display: none;
            }}
            
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* Print styles */
        @media print {{
            .header, .fab, .tab-nav {{
                display: none;
            }}
            
            .tab-content {{
                display: block !important;
            }}
            
            .news-card {{
                break-inside: avoid;
            }}
        }}
        
        /* Focus styles for accessibility */
        a:focus, button:focus, .tab-button:focus {{
            outline: 3px solid var(--primary-color);
            outline-offset: 2px;
        }}
        
        /* Reduced motion for accessibility */
        @media (prefers-reduced-motion: reduce) {{
            * {{
                animation-duration: 0.01ms !important;
                animation-iteration-count: 1 !important;
                transition-duration: 0.01ms !important;
            }}
        }}
    </style>
</head>
<body>
    <a href="#main-content" class="skip-link">メインコンテンツへスキップ</a>
    
    <header class="header" role="banner">
        <div class="header-content">
            <h1>🤖 AI業界ダッシュボード</h1>
            <div class="quick-stats" aria-label="統計情報">
                <div class="stat-item">
                    <span>📅</span>
                    <span>{current_date}</span>
                </div>
                <div class="stat-item">
                    <span>🕐</span>
                    <span>{current_time} JST</span>
                </div>
                <div class="stat-item">
                    <span>📰</span>
                    <span class="stat-value">{total_news}</span>件
                </div>
            </div>
        </div>
    </header>
    
    <main id="main-content" class="container" role="main">
        <!-- エグゼクティブサマリー -->
        <section class="summary-section" aria-labelledby="summary-heading">
            <h2 id="summary-heading">📊 本日のサマリー</h2>
            <p>{summary_text}</p>
            
            <div class="kpi-grid" role="list">
                <div class="kpi-card" role="listitem" tabindex="0">
                    <div class="kpi-number">{total_news}</div>
                    <div class="kpi-label">総ニュース数</div>
                </div>
                <div class="kpi-card" role="listitem" tabindex="0">
                    <div class="kpi-number">{active_companies}</div>
                    <div class="kpi-label">活動企業数</div>
                </div>
                <div class="kpi-card" role="listitem" tabindex="0">
                    <div class="kpi-number">{total_sources}</div>
                    <div class="kpi-label">情報ソース数</div>
                </div>
                <div class="kpi-card" role="listitem" tabindex="0">
                    <div class="kpi-number">{sns_posts}</div>
                    <div class="kpi-label">SNS投稿数</div>
                </div>
            </div>
        </section>
        
        <!-- タブナビゲーション -->
        <nav class="tab-nav" role="tablist" aria-label="コンテンツカテゴリー">
            <button class="tab-button active" role="tab" aria-selected="true" aria-controls="tab-business" data-tab="business">
                💼 ビジネス
            </button>
            <button class="tab-button" role="tab" aria-selected="false" aria-controls="tab-tech" data-tab="tech">
                ⚡ テクノロジー
            </button>
            <button class="tab-button" role="tab" aria-selected="false" aria-controls="tab-sns" data-tab="sns">
                🐦 SNS投稿
            </button>
            <button class="tab-button" role="tab" aria-selected="false" aria-controls="tab-trends" data-tab="trends">
                📈 トレンド
            </button>
        </nav>
        
        <!-- タブコンテンツ -->
        <div class="tab-content active" id="tab-business" role="tabpanel" aria-labelledby="business-tab">
            <div class="news-grid">
                {business_content}
            </div>
        </div>
        
        <div class="tab-content" id="tab-tech" role="tabpanel" aria-labelledby="tech-tab">
            <div class="news-grid">
                {tech_content}
            </div>
        </div>
        
        <div class="tab-content" id="tab-sns" role="tabpanel" aria-labelledby="sns-tab">
            <div class="sns-section">
                <h3>📢 注目の投稿</h3>
                <div class="sns-grid">
                    {featured_sns}
                </div>
                
                <h3 style="margin-top: 2rem;">💬 技術ディスカッション</h3>
                <div class="sns-grid">
                    {tech_sns}
                </div>
            </div>
        </div>
        
        <div class="tab-content" id="tab-trends" role="tabpanel" aria-labelledby="trends-tab">
            <div class="summary-section">
                <h3>🔥 本日のトレンドキーワード</h3>
                <div style="display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 1rem;">
                    {trend_keywords}
                </div>
            </div>
        </div>
    </main>
    
    <!-- Floating Action Button -->
    <button class="fab" aria-label="トップへ戻る" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})">
        ↑
    </button>
    
    <script>
        // Tab navigation
        document.querySelectorAll('.tab-button').forEach(button => {{
            button.addEventListener('click', () => {{
                const tabName = button.dataset.tab;
                
                // Update buttons
                document.querySelectorAll('.tab-button').forEach(btn => {{
                    btn.classList.remove('active');
                    btn.setAttribute('aria-selected', 'false');
                }});
                button.classList.add('active');
                button.setAttribute('aria-selected', 'true');
                
                // Update content
                document.querySelectorAll('.tab-content').forEach(content => {{
                    content.classList.remove('active');
                }});
                document.getElementById(`tab-${{tabName}}`).classList.add('active');
            }});
        }});
        
        // Progressive enhancement: Add loading states
        if ('IntersectionObserver' in window) {{
            const observer = new IntersectionObserver((entries) => {{
                entries.forEach(entry => {{
                    if (entry.isIntersecting) {{
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }}
                }});
            }});
            
            document.querySelectorAll('.news-card, .sns-post').forEach(el => {{
                el.style.opacity = '0';
                el.style.transform = 'translateY(20px)';
                el.style.transition = 'opacity 0.5s, transform 0.5s';
                observer.observe(el);
            }});
        }}
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'Escape') {{
                document.activeElement.blur();
            }}
        }});
        
        // Service Worker for offline support (optional)
        if ('serviceWorker' in navigator) {{
            navigator.serviceWorker.register('/sw.js').catch(() => {{}});
        }}
    </script>
</body>
</html>'''
    
    # プレースホルダーに実際のデータを挿入
    html = html_template.format(
        current_date=current_date,
        current_time=current_time,
        total_news=dashboard_data.get('total_news', 0),
        active_companies=dashboard_data.get('active_companies', 0),
        total_sources=dashboard_data.get('total_sources', 0),
        sns_posts=dashboard_data.get('sns_posts', 0),
        summary_text=dashboard_data.get('summary_text', 'AI業界の最新動向を分析中...'),
        business_content=generate_news_cards(dashboard_data.get('business_news', [])),
        tech_content=generate_news_cards(dashboard_data.get('tech_news', [])),
        featured_sns=generate_sns_posts(dashboard_data.get('featured_posts', [])),
        tech_sns=generate_sns_posts(dashboard_data.get('tech_discussions', [])),
        trend_keywords=generate_trend_keywords(dashboard_data.get('trends', []))
    )
    
    return html

def generate_news_cards(news_items):
    """ニュースカードのHTMLを生成"""
    if not news_items:
        return '<p style="text-align: center; color: var(--text-tertiary);">ニュースがありません</p>'
    
    cards = []
    for item in news_items[:8]:  # 最大8件
        card = f'''
        <article class="news-card">
            <div class="news-category">{item.get('category', 'AI')}</div>
            <h3 class="news-title">
                <a href="{item.get('link', '#')}" target="_blank" rel="noopener noreferrer">
                    {item.get('title', 'タイトルなし')}
                </a>
            </h3>
            <p class="news-summary">{item.get('summary', '')[:150]}...</p>
            <div class="news-meta">
                <span>{item.get('source', 'Unknown')}</span>
                <span>{item.get('time', '')}</span>
            </div>
        </article>'''
        cards.append(card)
    
    return '\n'.join(cards)

def generate_sns_posts(posts):
    """SNS投稿のHTMLを生成"""
    if not posts:
        return '<p style="text-align: center; color: var(--text-tertiary);">投稿がありません</p>'
    
    cards = []
    for post in posts[:5]:  # 最大5件
        card = f'''
        <article class="sns-post">
            <div class="sns-username">
                <a href="{post.get('url', '#')}" target="_blank" rel="noopener noreferrer">
                    {post.get('username', '@anonymous')}
                </a>
            </div>
            <p class="sns-content">{post.get('summary', '')[:200]}...</p>
            <div class="sns-time">{post.get('time', '')}</div>
        </article>'''
        cards.append(card)
    
    return '\n'.join(cards)

def generate_trend_keywords(trends):
    """トレンドキーワードのHTMLを生成"""
    if not trends:
        return '<span style="color: var(--text-tertiary);">トレンドデータなし</span>'
    
    keywords = []
    for trend in trends[:10]:  # 最大10個
        style = f'background: var(--{"primary" if trend.get("hot") else "secondary"}-color);'
        keyword = f'<span style="padding: 0.5rem 1rem; {style} color: white; border-radius: 9999px; font-size: 0.875rem;">{trend.get("keyword", "")} ({trend.get("count", 0)})</span>'
        keywords.append(keyword)
    
    return '\n'.join(keywords)

if __name__ == "__main__":
    print("🎨 改善版ダッシュボード生成開始...")
    
    try:
        html = generate_improved_dashboard()
        
        # ファイルに保存
        output_path = Path("index_improved.html")
        output_path.write_text(html, encoding='utf-8')
        
        print(f"✅ 改善版ダッシュボード生成完了: {output_path}")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()