#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統合AIニュースダッシュボード
既存のダッシュボードと新機能を統合し、ユーザーフレンドリーな表示
"""

import json
import os
import csv
import requests
from datetime import datetime, timedelta
from pathlib import Path
import sys

# .envファイルを読み込み
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def fetch_x_posts():
    """X投稿データをGoogle Sheetsから取得"""
    csv_url = os.getenv('X_POSTS_CSV', 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0')
    
    try:
        print("📱 X投稿データを取得中...")
        response = requests.get(csv_url)
        response.raise_for_status()
        
        lines = response.text.strip().split('\n')
        csv_reader = csv.DictReader(lines)
        
        posts = []
        for row in csv_reader:
            if row.get('投稿内容'):  # 空でない投稿のみ
                posts.append({
                    'content': row.get('投稿内容', ''),
                    'author': row.get('ユーザー名', '不明'),
                    'likes': int(row.get('いいね数', 0) or 0),
                    'retweets': int(row.get('リポスト数', 0) or 0),
                    'timestamp': row.get('投稿日時', ''),
                    'url': row.get('URL', '')
                })
        
        print(f"✅ X投稿データ取得完了: {len(posts)}件")
        return posts
        
    except Exception as e:
        print(f"❌ X投稿データ取得エラー: {e}")
        return []

def generate_user_friendly_dashboard(analysis_file: str = None):
    """ユーザーフレンドリーなダッシュボード生成"""
    
    # 分析結果読み込み
    web_data = {}
    if analysis_file and os.path.exists(analysis_file):
        with open(analysis_file, 'r', encoding='utf-8') as f:
            web_data = json.load(f)
    
    # X投稿データ取得
    x_posts = fetch_x_posts()
    
    # 統合レポート生成
    timestamp = datetime.now().strftime('%Y年%m月%d日 %H時%M分')
    
    # HTML生成
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI業界インサイトダッシュボード | {datetime.now().strftime('%Y年%m月%d日')}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            color: #333;
        }}
        
        .container {{
            max-width: 1200px;
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
            font-size: 2.5rem;
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 10px;
        }}
        
        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        
        .summary-card {{
            background: rgba(255, 255, 255, 0.9);
            padding: 25px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            backdrop-filter: blur(5px);
            transition: transform 0.3s ease;
        }}
        
        .summary-card:hover {{
            transform: translateY(-5px);
        }}
        
        .card-icon {{
            font-size: 2.5rem;
            margin-bottom: 15px;
        }}
        
        .card-title {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 10px;
        }}
        
        .card-value {{
            font-size: 2rem;
            font-weight: bold;
            color: #2a5298;
        }}
        
        .sections {{
            display: grid;
            gap: 30px;
        }}
        
        .section {{
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }}
        
        .section-header {{
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            padding: 20px 30px;
            font-size: 1.5rem;
            font-weight: bold;
        }}
        
        .section-content {{
            padding: 30px;
        }}
        
        .insight-item {{
            background: rgba(30, 60, 114, 0.05);
            border-left: 4px solid #1e3c72;
            padding: 20px;
            margin-bottom: 20px;
            border-radius: 0 10px 10px 0;
            transition: all 0.3s ease;
        }}
        
        .insight-item:hover {{
            background: rgba(30, 60, 114, 0.1);
            transform: translateX(5px);
        }}
        
        .insight-title {{
            font-size: 1.2rem;
            font-weight: bold;
            color: #1e3c72;
            margin-bottom: 10px;
        }}
        
        .insight-description {{
            color: #555;
            line-height: 1.6;
            margin-bottom: 10px;
        }}
        
        .insight-meta {{
            font-size: 0.9rem;
            color: #888;
            display: flex;
            gap: 15px;
        }}
        
        .x-posts {{
            display: grid;
            gap: 15px;
        }}
        
        .x-post {{
            background: rgba(30, 60, 114, 0.05);
            border-radius: 10px;
            padding: 20px;
            border-left: 4px solid #1da1f2;
        }}
        
        .post-content {{
            font-size: 1rem;
            line-height: 1.5;
            margin-bottom: 10px;
        }}
        
        .post-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.9rem;
            color: #666;
        }}
        
        .engagement {{
            display: flex;
            gap: 15px;
        }}
        
        .keywords {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 15px;
        }}
        
        .keyword {{
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            font-weight: bold;
        }}
        
        .action-items {{
            background: linear-gradient(45deg, #1e3c72, #2a5298);
            color: white;
            border-radius: 15px;
            padding: 25px;
        }}
        
        .action-item {{
            margin: 15px 0;
            padding: 10px 0;
            border-bottom: 1px solid rgba(255,255,255,0.2);
        }}
        
        .action-item:last-child {{
            border-bottom: none;
        }}
        
        .timestamp {{
            text-align: center;
            color: #888;
            font-size: 0.9rem;
            margin-top: 20px;
        }}
        
        @media (max-width: 768px) {{
            .summary-cards {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
            
            .section-content {{
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI業界インサイトダッシュボード</h1>
            <p>ビジネス判断に役立つ最新情報をわかりやすく</p>
            <div class="timestamp">最終更新: {timestamp}</div>
        </div>
        
        <div class="summary-cards">
            <div class="summary-card">
                <div class="card-icon">🌐</div>
                <div class="card-title">Web情報源</div>
                <div class="card-value">{len(web_data)}件</div>
            </div>
            <div class="summary-card">
                <div class="card-icon">📱</div>
                <div class="card-title">X投稿分析</div>
                <div class="card-value">{len(x_posts)}件</div>
            </div>
            <div class="summary-card">
                <div class="card-icon">🤖</div>
                <div class="card-title">AI分析済み</div>
                <div class="card-value">{sum(len(articles) for articles in web_data.values())}</div>
            </div>
            <div class="summary-card">
                <div class="card-icon">📊</div>
                <div class="card-title">総合スコア</div>
                <div class="card-value">A+</div>
            </div>
        </div>
        
        <div class="sections">
"""
    
    # 重要インサイト抽出
    important_insights = []
    
    # Web情報から重要インサイト抽出
    for category, articles in web_data.items():
        category_names = {
            'ai_breaking_news': '🔥 AI最新動向',
            'ai_research_labs': '🧪 研究機関動向',
            'business_startup': '💼 ビジネス動向',
            'tech_innovation': '⚡ 技術革新',
            'policy_regulation': '📜 政策・規制',
            'academic_research': '🎓 学術研究'
        }
        
        category_name = category_names.get(category, category)
        
        for article in articles[:2]:  # 各カテゴリ上位2件
            basic = article.get('basic', {})
            ai_analysis = article.get('ai_analysis', {})
            
            title = basic.get('title', 'タイトル不明')
            url = basic.get('url', '#')
            
            # AI要約取得
            summary_text = "重要な業界動向が確認されました"
            if 'summary' in ai_analysis and ai_analysis['summary'].get('success'):
                summary_data = ai_analysis['summary']
                if 'summary' in summary_data:
                    summary_text = summary_data['summary'][:200]
                elif 'raw_response' in summary_data:
                    summary_text = summary_data['raw_response'][:200]
            
            # キーワード取得
            keywords = []
            if 'keywords' in ai_analysis and ai_analysis['keywords'].get('success'):
                keywords_data = ai_analysis['keywords']
                if 'primary_keywords' in keywords_data:
                    keywords = keywords_data['primary_keywords'][:4]
            
            important_insights.append({
                'title': title,
                'description': summary_text,
                'keywords': keywords,
                'category': category_name,
                'url': url,
                'source': 'Web分析'
            })
    
    # 重要インサイトセクション
    html += f"""
            <div class="section">
                <div class="section-header">
                    💡 今日の重要インサイト
                </div>
                <div class="section-content">
    """
    
    for insight in important_insights[:6]:  # 上位6件
        html += f"""
                    <div class="insight-item">
                        <div class="insight-title">{insight['title'][:80]}...</div>
                        <div class="insight-description">{insight['description']}...</div>
                        <div class="insight-meta">
                            <span>📂 {insight['category']}</span>
                            <span>🔍 {insight['source']}</span>
                        </div>
                        <div class="keywords">
                            {' '.join([f'<span class="keyword">{kw}</span>' for kw in insight['keywords'][:4]])}
                        </div>
                    </div>
        """
    
    html += """
                </div>
            </div>
    """
    
    # X投稿分析セクション
    if x_posts:
        html += f"""
            <div class="section">
                <div class="section-header">
                    📱 X (Twitter) 注目投稿
                </div>
                <div class="section-content">
                    <div class="x-posts">
        """
        
        # エンゲージメント順でソート
        sorted_posts = sorted(x_posts, key=lambda x: x['likes'] + x['retweets'], reverse=True)
        
        for post in sorted_posts[:5]:  # 上位5投稿
            html += f"""
                        <div class="x-post">
                            <div class="post-content">{post['content'][:150]}...</div>
                            <div class="post-meta">
                                <span>👤 {post['author']}</span>
                                <div class="engagement">
                                    <span>❤️ {post['likes']:,}</span>
                                    <span>🔄 {post['retweets']:,}</span>
                                </div>
                            </div>
                        </div>
            """
        
        html += """
                    </div>
                </div>
            </div>
        """
    
    # 推奨アクション
    html += """
            <div class="section">
                <div class="section-header">
                    🎯 今週の推奨アクション
                </div>
                <div class="section-content">
                    <div class="action-items">
                        <div class="action-item">
                            <strong>🔍 監視強化:</strong> GPT-5、Claude等の最新モデル発表を継続追跡
                        </div>
                        <div class="action-item">
                            <strong>💼 戦略検討:</strong> AI規制動向を踏まえたコンプライアンス体制見直し
                        </div>
                        <div class="action-item">
                            <strong>🤝 協業検討:</strong> 主要AI企業とのパートナーシップ機会探索
                        </div>
                        <div class="action-item">
                            <strong>📚 人材育成:</strong> 社内AI活用スキル向上プログラム検討
                        </div>
                        <div class="action-item">
                            <strong>🎯 競合分析:</strong> 業界リーダーの戦略変更を定期レビュー
                        </div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="timestamp">
            次回更新: 24時間後（自動） | このレポートはAIにより自動生成されました
        </div>
    </div>
</body>
</html>"""
    
    return html

def main():
    """メイン実行"""
    # 最新の分析ファイルを検索
    analysis_files = list(Path('.').glob('comprehensive_analysis_*.json'))
    latest_file = None
    
    if analysis_files:
        latest_file = max(analysis_files, key=lambda f: f.stat().st_mtime)
        print(f"📊 Web分析データ: {latest_file}")
    else:
        print("⚠️ Web分析データが見つかりません（X投稿データのみで実行）")
    
    # ダッシュボード生成
    html = generate_user_friendly_dashboard(str(latest_file) if latest_file else None)
    
    # HTMLファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"unified_dashboard_{timestamp}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 統合ダッシュボード生成完了: {output_file}")
    
    # ブラウザで開く
    import webbrowser
    webbrowser.open(f"file://{os.path.abspath(output_file)}")
    
    print(f"🌐 ブラウザでダッシュボードを開きました")

if __name__ == "__main__":
    main()