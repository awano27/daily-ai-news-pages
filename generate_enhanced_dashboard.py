#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
拡張AIニュースダッシュボード
既存システム + Web分析 + X投稿を統合し、情報量を最大化
"""

import json
import os
import csv
import requests
import yaml
import feedparser
from datetime import datetime, timedelta
from pathlib import Path
import sys
import re

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

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def fetch_x_posts():
    """X投稿データをGoogle Sheetsから取得（修正版）"""
    csv_url = os.getenv('X_POSTS_CSV', 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0')
    
    try:
        print("📱 X投稿データを取得中...")
        
        # User-Agentを設定してリクエスト
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        response = requests.get(csv_url, headers=headers, timeout=30)
        response.raise_for_status()
        
        # CSVデータを解析
        lines = response.text.strip().split('\n')
        if len(lines) < 2:
            print("⚠️ CSVデータが空またはヘッダーのみです")
            return []
        
        # ヘッダー行を確認
        header_line = lines[0]
        print(f"📋 CSVヘッダー: {header_line}")
        
        csv_reader = csv.DictReader(lines)
        
        posts = []
        for i, row in enumerate(csv_reader):
            # 行の内容を確認
            if i < 3:  # 最初の3行をデバッグ出力
                print(f"🔍 行 {i+1}: {dict(row)}")
            
            # 様々な可能性のあるカラム名を試行
            content_keys = ['投稿内容', 'content', 'Content', 'Tweet', 'Text', 'Post']
            author_keys = ['ユーザー名', 'username', 'Username', 'Author', 'User', 'author']
            likes_keys = ['いいね数', 'likes', 'Likes', 'Like', 'Hearts']
            retweets_keys = ['リポスト数', 'retweets', 'Retweets', 'RT', 'Shares']
            
            content = None
            author = '不明'
            likes = 0
            retweets = 0
            
            # コンテンツを探す
            for key in content_keys:
                if key in row and row[key] and row[key].strip():
                    content = row[key].strip()
                    break
            
            # 著者を探す
            for key in author_keys:
                if key in row and row[key] and row[key].strip():
                    author = row[key].strip()
                    break
            
            # いいね数を探す
            for key in likes_keys:
                if key in row and row[key]:
                    try:
                        likes = int(row[key].replace(',', ''))
                        break
                    except (ValueError, TypeError):
                        pass
            
            # リツイート数を探す
            for key in retweets_keys:
                if key in row and row[key]:
                    try:
                        retweets = int(row[key].replace(',', ''))
                        break
                    except (ValueError, TypeError):
                        pass
            
            if content and len(content) > 10:  # 有効なコンテンツがある場合のみ追加
                posts.append({
                    'content': content,
                    'author': author,
                    'likes': likes,
                    'retweets': retweets,
                    'timestamp': row.get('投稿日時', row.get('timestamp', row.get('Date', ''))),
                    'url': row.get('URL', row.get('url', ''))
                })
        
        print(f"✅ X投稿データ取得完了: {len(posts)}件")
        
        # 投稿内容のサンプルを表示
        if posts:
            print("📄 取得された投稿例:")
            for i, post in enumerate(posts[:3]):
                print(f"   {i+1}. {post['content'][:50]}... (👤{post['author']} ❤️{post['likes']})")
        
        return posts
        
    except Exception as e:
        print(f"❌ X投稿データ取得エラー: {e}")
        print(f"🔗 試行URL: {csv_url}")
        return []

def fetch_existing_rss_feeds():
    """既存のRSSフィード設定から追加情報を取得"""
    feeds_file = 'feeds.yml'
    if not os.path.exists(feeds_file):
        print("⚠️ feeds.ymlが見つかりません")
        return []
    
    try:
        print("📡 既存RSSフィードから追加データを取得中...")
        
        with open(feeds_file, 'r', encoding='utf-8') as f:
            feeds_config = yaml.safe_load(f)
        
        hours_lookback = int(os.getenv('HOURS_LOOKBACK', 24))
        cutoff_time = datetime.now() - timedelta(hours=hours_lookback)
        
        additional_items = []
        
        for category, feeds in feeds_config.items():
            if isinstance(feeds, list):
                for feed_url in feeds[:2]:  # 各カテゴリ上位2フィード
                    try:
                        print(f"📡 {category}: {feed_url}")
                        feed = feedparser.parse(feed_url)
                        
                        for entry in feed.entries[:3]:  # 各フィード3件
                            # 日時チェック
                            entry_time = None
                            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                                entry_time = datetime(*entry.published_parsed[:6])
                            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                                entry_time = datetime(*entry.updated_parsed[:6])
                            
                            if entry_time and entry_time > cutoff_time:
                                additional_items.append({
                                    'title': entry.get('title', 'タイトルなし'),
                                    'summary': entry.get('summary', entry.get('description', ''))[:200],
                                    'link': entry.get('link', ''),
                                    'category': category,
                                    'published': entry_time.strftime('%Y-%m-%d %H:%M') if entry_time else '',
                                    'source': 'RSS Feed'
                                })
                    except Exception as e:
                        print(f"⚠️ RSS取得エラー ({feed_url}): {e}")
                        continue
        
        print(f"✅ RSS追加データ取得完了: {len(additional_items)}件")
        return additional_items
        
    except Exception as e:
        print(f"❌ RSS設定読み込みエラー: {e}")
        return []

def extract_trending_topics(web_data, x_posts, rss_items):
    """トレンドトピック抽出"""
    trending_keywords = {}
    
    # Web分析データからキーワード抽出
    for category, articles in web_data.items():
        for article in articles:
            ai_analysis = article.get('ai_analysis', {})
            if 'keywords' in ai_analysis and ai_analysis['keywords'].get('success'):
                keywords_data = ai_analysis['keywords']
                if 'primary_keywords' in keywords_data:
                    for keyword in keywords_data['primary_keywords']:
                        trending_keywords[keyword] = trending_keywords.get(keyword, 0) + 2
    
    # X投稿からキーワード抽出
    ai_terms = ['AI', 'GPT', 'Claude', 'Gemini', 'ChatGPT', 'OpenAI', 'Anthropic', 'Google', 'Microsoft', 
                '人工知能', 'LLM', 'ML', '機械学習', 'ディープラーニング', 'ニューラル']
    
    for post in x_posts:
        content = post['content'].upper()
        for term in ai_terms:
            if term.upper() in content:
                trending_keywords[term] = trending_keywords.get(term, 0) + 1
    
    # RSSアイテムからキーワード抽出
    for item in rss_items:
        title_summary = (item['title'] + ' ' + item['summary']).upper()
        for term in ai_terms:
            if term.upper() in title_summary:
                trending_keywords[term] = trending_keywords.get(term, 0) + 1
    
    return sorted(trending_keywords.items(), key=lambda x: x[1], reverse=True)[:10]

def generate_enhanced_dashboard(analysis_file: str = None):
    """拡張ダッシュボード生成"""
    
    # 各データソース取得
    web_data = {}
    if analysis_file and os.path.exists(analysis_file):
        with open(analysis_file, 'r', encoding='utf-8') as f:
            web_data = json.load(f)
    
    x_posts = fetch_x_posts()
    rss_items = fetch_existing_rss_feeds()
    trending_topics = extract_trending_topics(web_data, x_posts, rss_items)
    
    # 統計計算
    total_web_articles = sum(len(articles) for articles in web_data.values())
    total_sources = len(web_data) + (1 if x_posts else 0) + (1 if rss_items else 0)
    
    timestamp = datetime.now().strftime('%Y年%m月%d日 %H時%M分')
    
    # HTML生成
    html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI業界総合インテリジェンス | {datetime.now().strftime('%Y年%m月%d日')}</title>
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
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
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
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 20px;
            font-size: 1.5rem;
            font-weight: bold;
        }}
        
        .section-content {{
            padding: 20px;
        }}
        
        .insight-item {{
            border-bottom: 1px solid #eee;
            padding: 20px 0;
            transition: all 0.3s ease;
        }}
        
        .insight-item:last-child {{
            border-bottom: none;
        }}
        
        .insight-item:hover {{
            background: rgba(102, 126, 234, 0.05);
            border-radius: 10px;
            margin: 0 -10px;
            padding: 20px 10px;
        }}
        
        .insight-title {{
            font-size: 1.3rem;
            font-weight: bold;
            color: #333;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        
        .insight-description {{
            color: #666;
            line-height: 1.6;
            margin-bottom: 15px;
        }}
        
        .insight-meta {{
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            font-size: 0.9rem;
            color: #888;
        }}
        
        .trending-topics {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
        }}
        
        .topic-card {{
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            padding: 15px;
            border-radius: 10px;
            text-align: center;
            font-weight: bold;
        }}
        
        .topic-count {{
            font-size: 1.5rem;
            margin-bottom: 5px;
        }}
        
        .x-posts {{
            display: grid;
            gap: 15px;
        }}
        
        .x-post {{
            background: rgba(29, 161, 242, 0.1);
            border-left: 4px solid #1da1f2;
            padding: 20px;
            border-radius: 0 10px 10px 0;
            transition: all 0.3s ease;
        }}
        
        .x-post:hover {{
            background: rgba(29, 161, 242, 0.15);
            transform: translateX(5px);
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
        
        .rss-items {{
            display: grid;
            gap: 15px;
        }}
        
        .rss-item {{
            background: rgba(102, 126, 234, 0.1);
            border-left: 4px solid #667eea;
            padding: 20px;
            border-radius: 0 10px 10px 0;
            transition: all 0.3s ease;
        }}
        
        .rss-item:hover {{
            background: rgba(102, 126, 234, 0.15);
            transform: translateX(5px);
        }}
        
        @media (max-width: 768px) {{
            .stats {{
                grid-template-columns: repeat(2, 1fr);
            }}
            
            .header h1 {{
                font-size: 2rem;
            }}
        }}
        
        .timestamp {{
            color: #888;
            font-size: 0.9rem;
            margin-top: 10px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚀 AI業界総合インテリジェンス</h1>
            <p>Web分析 × X投稿 × RSS配信の統合情報ダッシュボード</p>
            <div class="timestamp">最終更新: {timestamp}</div>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="stat-number">{total_web_articles}</div>
                <div class="stat-label">Web記事分析</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(x_posts)}</div>
                <div class="stat-label">X投稿監視</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{len(rss_items)}</div>
                <div class="stat-label">RSS配信</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">{total_sources}</div>
                <div class="stat-label">総合データソース</div>
            </div>
        </div>
        
        <div class="sections">
"""
    
    # トレンドトピックセクション
    if trending_topics:
        html += f"""
            <div class="section">
                <div class="section-header">
                    🔥 トレンドキーワード
                </div>
                <div class="section-content">
                    <div class="trending-topics">
        """
        
        for keyword, count in trending_topics[:8]:
            html += f"""
                        <div class="topic-card">
                            <div class="topic-count">{count}</div>
                            <div>{keyword}</div>
                        </div>
            """
        
        html += """
                    </div>
                </div>
            </div>
        """
    
    # Web分析インサイト
    if web_data:
        html += f"""
            <div class="section">
                <div class="section-header">
                    🌐 重要Web分析結果 ({total_web_articles}件)
                </div>
                <div class="section-content">
        """
        
        category_names = {
            'ai_breaking_news': '🔥 AI最新ニュース',
            'ai_research_labs': '🧪 AI研究ラボ',
            'business_startup': '💼 ビジネス・スタートアップ',
            'tech_innovation': '⚡ 技術革新',
            'policy_regulation': '📜 政策・規制',
            'academic_research': '🎓 学術研究'
        }
        
        for category, articles in web_data.items():
            category_name = category_names.get(category, category)
            
            for article in articles[:2]:  # 各カテゴリ上位2件
                basic = article.get('basic', {})
                ai_analysis = article.get('ai_analysis', {})
                
                title = basic.get('title', 'タイトル不明')
                
                # AI要約取得
                summary_text = "ビジネス価値の高い情報が確認されました"
                if 'summary' in ai_analysis and ai_analysis['summary'].get('success'):
                    summary_data = ai_analysis['summary']
                    if 'summary' in summary_data:
                        summary_text = summary_data['summary'][:200]
                    elif 'raw_response' in summary_data:
                        summary_text = summary_data['raw_response'][:200]
                
                html += f"""
                    <div class="insight-item">
                        <div class="insight-title">{title}</div>
                        <div class="insight-description">{summary_text}...</div>
                        <div class="insight-meta">
                            <span>📂 {category_name}</span>
                            <span>🤖 AI分析済み</span>
                        </div>
                    </div>
                """
        
        html += """
                </div>
            </div>
        """
    
    # X投稿セクション
    if x_posts:
        html += f"""
            <div class="section">
                <div class="section-header">
                    📱 注目X投稿 ({len(x_posts)}件)
                </div>
                <div class="section-content">
                    <div class="x-posts">
        """
        
        # エンゲージメント順でソート
        sorted_posts = sorted(x_posts, key=lambda x: x['likes'] + x['retweets'], reverse=True)
        
        for post in sorted_posts[:8]:  # 上位8投稿
            html += f"""
                        <div class="x-post">
                            <div class="post-content">{post['content']}</div>
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
    
    # RSS追加情報セクション
    if rss_items:
        html += f"""
            <div class="section">
                <div class="section-header">
                    📡 最新RSS配信 ({len(rss_items)}件)
                </div>
                <div class="section-content">
                    <div class="rss-items">
        """
        
        for item in rss_items[:10]:  # 上位10件
            html += f"""
                        <div class="rss-item">
                            <div class="insight-title">{item['title']}</div>
                            <div class="insight-description">{item['summary']}...</div>
                            <div class="insight-meta">
                                <span>📂 {item['category']}</span>
                                <span>📅 {item['published']}</span>
                                <span>📡 {item['source']}</span>
                            </div>
                        </div>
            """
        
        html += """
                    </div>
                </div>
            </div>
        """
    
    html += """
        </div>
        
        <div class="timestamp">
            次回更新: 24時間後（自動） | このダッシュボードは複数データソースから自動生成されました
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
        print("⚠️ Web分析データが見つかりません")
    
    # ダッシュボード生成
    html = generate_enhanced_dashboard(str(latest_file) if latest_file else None)
    
    # HTMLファイル保存
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_file = f"enhanced_dashboard_{timestamp}.html"
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ 拡張ダッシュボード生成完了: {output_file}")
    
    # ブラウザで開く
    import webbrowser
    webbrowser.open(f"file://{os.path.abspath(output_file)}")
    
    print(f"🌐 ブラウザで拡張ダッシュボードを開きました")

if __name__ == "__main__":
    main()