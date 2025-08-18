#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
インテリジェンス・ダッシュボード生成器
包括的分析結果を美しいWebサイトに変換
"""

import json
import os
from datetime import datetime
from pathlib import Path

def generate_dashboard(analysis_file: str):
    """ダッシュボードHTML生成"""
    
    # 分析結果読み込み
    with open(analysis_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # サマリー情報取得
    summary_file = analysis_file.replace('comprehensive_analysis_', 'analysis_summary_')
    if os.path.exists(summary_file):
        with open(summary_file, 'r', encoding='utf-8') as f:
            summary = json.load(f)
    else:
        summary = {}
    
    # HTML生成
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Intelligence Dashboard | {datetime.now().strftime('%Y年%m月%d日')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        .header {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            padding: 30px;
            margin-bottom: 30px;
            text-align: center;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 3rem;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.9);
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            backdrop-filter: blur(5px);
        }}
        
        .stat-number {{
            font-size: 2.5rem;
            font-weight: bold;
            color: #667eea;
        }}
        
        .stat-label {{
            font-size: 1rem;
            color: #666;
            margin-top: 5px;
        }}
        
        .categories {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
        }}
        
        .category {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        
        .category-header {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            font-size: 1.5rem;
            font-weight: bold;
            text-align: center;
        }}
        
        .articles {{
            padding: 20px;
        }}
        
        .article {{
            border-bottom: 1px solid #eee;
            padding: 20px 0;
            transition: all 0.3s ease;
        }}
        
        .article:last-child {{
            border-bottom: none;
        }}
        
        .article:hover {{
            background: rgba(102, 126, 234, 0.05);
            border-radius: 10px;
            margin: 0 -10px;
            padding: 20px 10px;
        }}
        
        .article-title {{
            font-size: 1.3rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        
        .article-title a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .article-title a:hover {{
            color: #667eea;
        }}
        
        .article-summary {{
            color: #666;
            line-height: 1.6;
            margin-bottom: 15px;
        }}
        
        .article-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            font-size: 0.9rem;
            color: #888;
        }}
        
        .meta-item {{
            display: flex;
            align-items: center;
            gap: 5px;
        }}
        
        .ai-badge {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        
        .keywords {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 10px;
        }}
        
        .keyword {{
            background: rgba(102, 126, 234, 0.1);
            color: #667eea;
            padding: 4px 8px;
            border-radius: 15px;
            font-size: 0.8rem;
        }}
        
        .loading {{
            text-align: center;
            padding: 50px;
            color: #888;
        }}
        
        @media (max-width: 768px) {{
            .categories {{
                grid-template-columns: 1fr;
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
        }}
        
        .timestamp {{
            color: #888;
            font-size: 0.9rem;
            margin-top: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI Intelligence Dashboard</h1>
            <p>リアルタイム業界インテリジェンス・レポート</p>
            <div class="timestamp">
                生成日時: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}
            </div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{summary.get('total_successful', 0)}</div>
                <div class="stat-label">取得成功記事数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{summary.get('success_rate', '0%')}</div>
                <div class="stat-label">成功率</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(data)}</div>
                <div class="stat-label">カテゴリ数</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{sum(len(articles) for articles in data.values())}</div>
                <div class="stat-label">総分析記事数</div>
            </div>
        </div>
        
        <div class="categories">
"""
    
    # カテゴリ名日本語マッピング
    category_names = {
        'ai_breaking_news': '🔥 AI最新ニュース',
        'ai_research_labs': '🧪 AI研究ラボ',
        'business_startup': '💼 ビジネス・スタートアップ',
        'tech_innovation': '⚡ 技術革新',
        'policy_regulation': '📜 政策・規制',
        'academic_research': '🎓 学術研究'
    }
    
    # 各カテゴリの記事を生成
    for category, articles in data.items():
        if not articles:
            continue
            
        category_title = category_names.get(category, category)
        
        html += f"""
            <div class="category">
                <div class="category-header">
                    {category_title} ({len(articles)}件)
                </div>
                <div class="articles">
        """
        
        for article in articles:
            basic = article.get('basic', {})
            ai_analysis = article.get('ai_analysis', {})
            
            title = basic.get('title', 'タイトル不明')
            url = basic.get('url', '#')
            
            # AI要約取得
            summary_text = "要約情報なし"
            if 'summary' in ai_analysis and ai_analysis['summary'].get('success'):
                summary_data = ai_analysis['summary']
                if 'summary' in summary_data:
                    summary_text = summary_data['summary']
                elif 'raw_response' in summary_data:
                    summary_text = summary_data['raw_response'][:200] + "..."
            
            # キーワード取得
            keywords = []
            if 'keywords' in ai_analysis and ai_analysis['keywords'].get('success'):
                keywords_data = ai_analysis['keywords']
                if 'primary_keywords' in keywords_data:
                    keywords.extend(keywords_data['primary_keywords'][:5])
                elif 'raw_response' in keywords_data:
                    # 簡易キーワード抽出
                    keywords = ['AI', 'テクノロジー', 'イノベーション']
            
            # 統計情報
            content_stats = article.get('content_stats', {})
            char_count = content_stats.get('character_count', 0)
            link_count = content_stats.get('link_count', 0)
            
            html += f"""
                    <div class="article">
                        <div class="article-title">
                            <a href="{url}" target="_blank">{title}</a>
                        </div>
                        <div class="article-summary">
                            {summary_text}
                        </div>
                        <div class="article-meta">
                            <div class="meta-item">
                                📊 {char_count:,}文字
                            </div>
                            <div class="meta-item">
                                🔗 {link_count}リンク
                            </div>
                            <div class="ai-badge">AI分析済み</div>
                        </div>
            """
            
            if keywords:
                html += f"""
                        <div class="keywords">
                            {' '.join([f'<span class="keyword">{keyword}</span>' for keyword in keywords[:6]])}
                        </div>
                """
            
            html += """
                    </div>
            """
        
        html += """
                </div>
            </div>
        """
    
    html += """
        </div>
    </div>
    
    <script>
        // スムーススクロール
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                document.querySelector(this.getAttribute('href')).scrollIntoView({
                    behavior: 'smooth'
                });
            });
        });
        
        // 記事ホバー効果
        document.querySelectorAll('.article').forEach(article => {
            article.addEventListener('mouseenter', function() {
                this.style.transform = 'translateY(-2px)';
            });
            
            article.addEventListener('mouseleave', function() {
                this.style.transform = 'translateY(0)';
            });
        });
    </script>
</body>
</html>"""
    
    # HTMLファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"ai_intelligence_dashboard_{timestamp}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ ダッシュボード生成完了: {output_file}")
    return output_file

def main():
    """メイン実行"""
    # 最新の分析ファイルを検索
    analysis_files = list(Path('.').glob('comprehensive_analysis_*.json'))
    
    if not analysis_files:
        print("❌ 分析ファイルが見つかりません")
        print("先に python run_comprehensive_analysis.py を実行してください")
        return
    
    # 最新ファイルを使用
    latest_file = max(analysis_files, key=lambda f: f.stat().st_mtime)
    print(f"📊 使用ファイル: {latest_file}")
    
    # ダッシュボード生成
    output_file = generate_dashboard(str(latest_file))
    
    # ブラウザで開く
    import webbrowser
    webbrowser.open(f"file://{os.path.abspath(output_file)}")
    
    print(f"🌐 ブラウザでダッシュボードを開きました")

if __name__ == "__main__":
    main()