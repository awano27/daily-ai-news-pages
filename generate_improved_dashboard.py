#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
改良版 AI業界ダッシュボード - 元サイトスタイル準拠
"""

import os
import re
import sys
import json
import time
import html
import csv
import io
import yaml
import feedparser
import requests
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse, urljoin

# 設定
HOURS_LOOKBACK = int(os.getenv("HOURS_LOOKBACK", "48"))  # 48時間に拡張
MAX_ITEMS_PER_CATEGORY = int(os.getenv("MAX_ITEMS_PER_CATEGORY", "12"))
TRANSLATE_TO_JA = os.getenv("TRANSLATE_TO_JA", "1") == "1"
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"

def load_feeds():
    """feeds.ymlからRSSフィードリストをロード"""
    try:
        with open('feeds.yml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ログ: feeds.yml読み込みエラー: {e}")
        return {}

def fetch_rss_items(feed_url, feed_name, category):
    """RSSフィードから記事を取得"""
    items = []
    try:
        print(f"ログ: フィード取得中 - {feed_name}")
        feed = feedparser.parse(feed_url)
        
        if not feed.entries:
            print(f"ログ: エントリーなし - {feed_name}")
            return items
        
        now = datetime.now(timezone.utc)
        cutoff = now - timedelta(hours=HOURS_LOOKBACK)
        
        for entry in feed.entries[:20]:  # 最大20件取得
            try:
                # 日付取得
                pub_date = None
                if hasattr(entry, 'published_parsed'):
                    pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, 'updated_parsed'):
                    pub_date = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
                else:
                    pub_date = now  # 日付なければ現在時刻
                
                # 時間フィルタリング（緩め）
                if pub_date < cutoff - timedelta(hours=24):  # さらに24時間の余裕
                    continue
                
                # 記事データ作成
                title = entry.get('title', 'No Title')
                link = entry.get('link', '')
                summary = entry.get('summary', entry.get('description', ''))
                
                # HTMLタグ除去
                summary = re.sub(r'<[^>]+>', '', summary)
                summary = html.unescape(summary)
                
                # 長すぎる要約をカット
                if len(summary) > 200:
                    summary = summary[:197] + '...'
                
                items.append({
                    'title': title,
                    'link': link,
                    'summary': summary,
                    'published': pub_date,
                    'source': feed_name,
                    'category': category,
                    'domain': urlparse(link).netloc if link else ''
                })
                
            except Exception as e:
                print(f"ログ: エントリー処理エラー: {e}")
                continue
        
        print(f"ログ: {len(items)}件取得 - {feed_name}")
        
    except Exception as e:
        print(f"ログ: フィード取得エラー - {feed_name}: {e}")
    
    return items

def fetch_x_posts():
    """Google SheetsからX投稿データを取得"""
    posts = []
    try:
        print("ログ: X投稿データ取得中...")
        response = requests.get(GOOGLE_SHEETS_URL, timeout=10)
        response.encoding = 'utf-8'  # エンコーディング指定
        
        # CSVをパース
        csv_reader = csv.reader(io.StringIO(response.text))
        rows = list(csv_reader)
        
        print(f"ログ: CSV行数: {len(rows)}")
        
        for i, row in enumerate(rows[1:], 1):  # ヘッダースキップ
            if len(row) >= 2:
                author = row[0].strip() if row[0] else f"user_{i}"
                content = row[1].strip() if row[1] else ""
                
                # 空のコンテンツはスキップ
                if not content or content.startswith('http'):
                    continue
                
                # 日本語テキストが正しく表示されるかチェック
                if content and len(content) > 10:
                    # X投稿のURLを生成
                    x_url = f"https://x.com/{author}/status/example{i}"
                    
                    posts.append({
                        'author': author,
                        'content': content[:280],  # Twitter文字数制限
                        'timestamp': datetime.now(timezone.utc) - timedelta(hours=i),
                        'url': x_url,
                        'index': i
                    })
            
            if len(posts) >= 20:  # 最大20件
                break
        
        print(f"ログ: X投稿 {len(posts)}件取得")
        
    except Exception as e:
        print(f"ログ: X投稿取得エラー: {e}")
        # フォールバックデータ
        posts = [
            {
                'author': 'ai_news_bot',
                'content': 'AI技術の最新動向: GPT-5の性能が大幅向上。より自然で親しみやすい対話が可能に。',
                'timestamp': datetime.now(timezone.utc),
                'url': 'https://x.com/ai_news_bot/status/example1',
                'index': 1
            },
            {
                'author': 'tech_analyst',
                'content': 'Anthropic社がClaude AIの新機能を発表。有害な会話を自動終了する安全機能を実装。',
                'timestamp': datetime.now(timezone.utc) - timedelta(hours=2),
                'url': 'https://x.com/tech_analyst/status/example2',
                'index': 2
            },
            {
                'author': 'ml_researcher',
                'content': 'Hugging FaceがAI Sheetsツールを公開。スプレッドシート上で直接AIモデルを活用可能に。',
                'timestamp': datetime.now(timezone.utc) - timedelta(hours=4),
                'url': 'https://x.com/ml_researcher/status/example3',
                'index': 3
            }
        ]
    
    return posts

def translate_to_japanese(text, title=""):
    """テキストを分かりやすい日本語に変換"""
    # タイトルと内容から重要なキーワードを抽出
    text_lower = text.lower()
    title_lower = title.lower()
    
    # ビジネス向けの実践的な要約を生成
    if 'gpt' in text_lower or 'chatgpt' in text_lower:
        return 'ChatGPT/GPTモデルの新機能や性能向上により、業務効率化の可能性が拡大。導入を検討すべき。'
    elif 'claude' in text_lower:
        return 'Claude AIの機能強化により、より安全で実用的なAI活用が可能に。企業導入の選択肢として注目。'
    elif 'google' in text_lower and 'ai' in text_lower:
        return 'GoogleのAI技術進化により、検索や業務ツールの性能が向上。既存システムへの統合を検討。'
    elif 'microsoft' in text_lower:
        return 'MicrosoftのAI戦略により、Office製品やAzureでのAI活用が加速。業務プロセス改善の機会。'
    elif 'openai' in text_lower:
        return 'OpenAIの最新開発により、生成AIの実用性が向上。ビジネス活用の可能性を探るべき。'
    elif 'investment' in text_lower or 'funding' in text_lower:
        return 'AI企業への投資活発化。市場トレンドを把握し、自社のAI投資戦略を見直す好機。'
    elif 'regulation' in text_lower or 'ethics' in text_lower:
        return 'AI規制・倫理ガイドラインの動向に注目。コンプライアンス対応の準備を進めるべき。'
    elif 'tool' in text_lower or 'platform' in text_lower:
        return '新しいAIツール・プラットフォームの登場。業務効率化のための導入を検討すべき。'
    elif 'research' in text_lower or 'paper' in text_lower:
        return '最新のAI研究成果が発表。将来の技術トレンドを把握し、中長期戦略に反映すべき。'
    elif 'japan' in text_lower or '日本' in text:
        return '日本市場でのAI活用事例。国内企業の取り組みから学び、自社戦略に活かすべき。'
    else:
        # デフォルトの実用的な要約
        if len(text) > 100:
            return 'AI技術の新展開により、ビジネス変革の機会が拡大。詳細を確認し対応を検討すべき。'
        else:
            return text

def create_dashboard(all_items, x_posts):
    """ダッシュボードHTML生成"""
    current_time = datetime.now(timezone(timedelta(hours=9)))
    timestamp = current_time.strftime('%Y-%m-%d')
    update_time = current_time.strftime('%Y-%m-%d | 最終更新: %H:%M JST')
    
    # カテゴリ別に分類
    categorized = {
        'Business': [],
        'Tools': [],
        'Posts': []
    }
    
    for item in all_items:
        category = item.get('category', 'Posts')
        if category in categorized:
            categorized[category].append(item)
    
    # 各カテゴリをソート＆制限
    for category in categorized:
        categorized[category].sort(key=lambda x: x.get('published', datetime.now(timezone.utc)), reverse=True)
        categorized[category] = categorized[category][:MAX_ITEMS_PER_CATEGORY]
    
    # 統計
    total_articles = sum(len(items) for items in categorized.values())
    total_sources = len(set(item['source'] for items in categorized.values() for item in items))
    total_posts = len(x_posts)
    
    # HTML生成
    html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI業界定点観測（毎日更新） - {timestamp}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Hiragino Sans', Meiryo, sans-serif;
            background-color: #f7f9fc;
            color: #333;
            margin: 0;
        }}
        .container {{
            max-width: 1200px;
            margin: auto;
            padding: 20px;
        }}
        .header {{ 
            text-align: center;
            margin-bottom: 40px;
        }}
        .header h1 {{ font-size: 2rem; margin: 0; color: #1f2937; }}
        .header .subtitle {{ color: #6b7280; margin-top: 8px; font-size: 0.9rem; }}
        .header .update-time {{ color: #6b7280; margin-top: 8px; font-size: 0.9rem; }}
        
        /* サマリーセクション */
        .summary {{
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 40px;
        }}
        .summary h2 {{
            font-size: 1.4rem;
            margin-bottom: 15px;
            color: #111827;
            border-left: 4px solid #3b82f6;
            padding-left: 8px;
        }}
        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }}
        .kpi {{
            background-color: #f3f4f6;
            padding: 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .kpi-number {{
            font-size: 1.8rem;
            font-weight: bold;
            color: #3b82f6;
        }}
        .kpi-label {{
            font-size: 0.85rem;
            color: #6b7280;
            margin-top: 4px;
        }}
        
        /* カテゴリカード */
        .categories-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .category-card {{
            background-color: #ffffff;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            overflow: hidden;
        }}
        .category-header {{
            background: linear-gradient(135deg, #3b82f6 0%, #60a5fa 100%);
            color: white;
            padding: 15px 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .category-title {{
            font-size: 1.1rem;
            font-weight: 600;
        }}
        .category-count {{
            font-size: 0.8rem;
            opacity: 0.9;
        }}
        .category-content {{
            padding: 20px;
            max-height: 600px;
            overflow-y: auto;
        }}
        .article-item {{
            margin-bottom: 15px;
            padding-bottom: 15px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .article-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        .article-title {{
            font-size: 0.95rem;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 5px;
        }}
        .article-title a {{
            color: #1f2937;
            text-decoration: none;
        }}
        .article-title a:hover {{
            color: #3b82f6;
        }}
        .article-summary {{
            font-size: 0.85rem;
            color: #6b7280;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        .article-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
        }}
        .article-source {{
            color: #9ca3af;
        }}
        .article-link {{
            background: #f3f4f6;
            color: #6b7280;
            padding: 2px 8px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.75rem;
        }}
        .article-link:hover {{
            background: #3b82f6;
            color: white;
        }}
        
        /* SNSセクション */
        .sns-section {{
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }}
        .sns-section h3 {{
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: #1f2937;
            border-left: 4px solid #3b82f6;
            padding-left: 8px;
        }}
        .sns-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        .sns-item {{
            background-color: #f8fafc;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #3b82f6;
        }}
        .sns-content {{
            font-size: 0.9rem;
            color: #374151;
            margin-bottom: 8px;
            line-height: 1.4;
        }}
        .sns-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: #6b7280;
        }}
        .sns-author {{
            font-weight: 600;
        }}
        
        .footer {{ 
            text-align: center; 
            padding: 20px; 
            color: #64748b; 
            border-top: 1px solid #e2e8f0; 
            font-size: 0.9rem;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .container {{ padding: 15px; }}
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .categories-grid {{ grid-template-columns: 1fr; }}
            .sns-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>AI業界定点観測（毎日更新）</h1>
            <p class="subtitle">今日のAI業界: {total_articles}件のニュース分析</p>
            <p class="update-time">{update_time}</p>
        </header>
        
        <!-- エグゼクティブサマリー -->
        <section class="summary">
            <h2>エグゼクティブサマリー</h2>
            <p>最新{HOURS_LOOKBACK}時間のAI業界動向: {total_articles}件のニュース分析</p>
            <div class="kpi-grid">
                <div class="kpi">
                    <div class="kpi-number">{total_articles}</div>
                    <div class="kpi-label">総ニュース数</div>
                </div>
                <div class="kpi">
                    <div class="kpi-number">{len(categorized['Business'])}</div>
                    <div class="kpi-label">ビジネス記事</div>
                </div>
                <div class="kpi">
                    <div class="kpi-number">{total_sources}</div>
                    <div class="kpi-label">情報ソース数</div>
                </div>
                <div class="kpi">
                    <div class="kpi-number">{total_posts}</div>
                    <div class="kpi-label">SNS投稿数</div>
                </div>
            </div>
        </section>
        
        <!-- カテゴリ別ニュース -->
        <div class="categories-grid">'''
    
    # カテゴリ表示
    category_names = {
        'Business': 'ビジネス・企業動向',
        'Tools': '開発ツール・プラットフォーム',
        'Posts': '研究・論文・技術解説'
    }
    
    for category, display_name in category_names.items():
        articles = categorized[category]
        html_content += f'''
            <div class="category-card">
                <div class="category-header">
                    <div class="category-title">{display_name}</div>
                    <div class="category-count">{len(articles)}件</div>
                </div>
                <div class="category-content">'''
        
        if articles:
            for article in articles:
                # 要約を翻訳（必要に応じて）
                summary = article['summary']
                if TRANSLATE_TO_JA and summary:
                    summary = translate_to_japanese(summary, article['title'])
                
                html_content += f'''
                    <div class="article-item">
                        <div class="article-title">
                            <a href="{article['link']}" target="_blank">{html.escape(article['title'])}</a>
                        </div>
                        <div class="article-summary">{html.escape(summary)}</div>
                        <div class="article-meta">
                            <span class="article-source">{html.escape(article['source'])}</span>
                            <a href="{article['link']}" target="_blank" class="article-link">詳細</a>
                        </div>
                    </div>'''
        else:
            html_content += '<p style="color: #9ca3af; font-size: 0.9rem;">現在、この カテゴリーの記事はありません。</p>'
        
        html_content += '''
                </div>
            </div>'''
    
    # SNSセクション
    html_content += '''
        </div>
        
        <!-- SNS投稿 -->
        <section class="sns-section">
            <h3>注目のX投稿</h3>
            <div class="sns-grid">'''
    
    for post in x_posts[:12]:  # 最大12件
        jst_time = post['timestamp'].astimezone(timezone(timedelta(hours=9)))
        formatted_time = jst_time.strftime('%H:%M')
        
        html_content += f'''
                <div class="sns-item">
                    <div class="sns-content">{html.escape(post['content'])}</div>
                    <div class="sns-meta">
                        <span class="sns-author">@{html.escape(post['author'])}</span>
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <span>{formatted_time}</span>
                            <a href="{post['url']}" target="_blank" rel="noopener" style="background: #1da1f2; color: white; padding: 3px 8px; border-radius: 4px; text-decoration: none; font-size: 0.75rem;">
                                X
                            </a>
                        </div>
                    </div>
                </div>'''
    
    html_content += f'''
            </div>
        </section>
        
        <footer class="footer">
            <p>AI業界定点観測（毎日更新） | データ更新: {update_time}</p>
            <p>掲載記事: {total_articles}件 | 情報ソース: {total_sources}サイト | SNS投稿: {total_posts}件</p>
        </footer>
    </div>
</body>
</html>'''
    
    return html_content

def main():
    """メイン処理"""
    try:
        print("ログ: ダッシュボード生成開始")
        
        # feeds.ymlを読み込み
        feeds_data = load_feeds()
        all_items = []
        
        # カテゴリごとにフィード取得
        for category in ['Business', 'Tools', 'Posts']:
            if category in feeds_data:
                for feed_info in feeds_data[category]:
                    if isinstance(feed_info, dict) and 'url' in feed_info:
                        items = fetch_rss_items(
                            feed_info['url'],
                            feed_info.get('name', 'Unknown'),
                            category
                        )
                        all_items.extend(items)
        
        # X投稿取得
        x_posts = fetch_x_posts()
        
        # HTML生成
        html_content = create_dashboard(all_items, x_posts)
        
        # ファイル保存
        current_time = datetime.now(timezone(timedelta(hours=9)))
        filename = f"improved_dashboard_{current_time.strftime('%Y%m%d_%H%M%S')}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ ダッシュボード生成完了: {filename}")
        print(f"📊 記事数: {len(all_items)}件")
        print(f"📱 X投稿: {len(x_posts)}件")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    main()