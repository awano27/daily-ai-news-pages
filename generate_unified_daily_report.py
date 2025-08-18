#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統合型AIデイリーレポート生成システム
RSS + SNS(X/Twitter) + 追加ソース統合版
"""

import os
import sys
import json
import csv
import io
import feedparser
import requests
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any, Tuple
import re
import warnings
from urllib.parse import urlparse

# 警告無効化
warnings.filterwarnings('ignore')

# 設定
HOURS_LOOKBACK = int(os.getenv('HOURS_LOOKBACK', '48'))  # 48時間に戻す
X_POSTS_CSV_URL = os.getenv('X_POSTS_CSV', 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0')

# 動作確認済みの信頼性高フィード（拡張版）
VERIFIED_FEEDS = {
    'tier1_official': [  # 最高信頼性
        {'name': 'TechCrunch', 'url': 'https://techcrunch.com/feed/', 'category': 'general'},
        {'name': 'VentureBeat AI', 'url': 'https://venturebeat.com/category/ai/feed/', 'category': 'strategy'},
        {'name': 'The Verge', 'url': 'https://www.theverge.com/rss/index.xml', 'category': 'general'},
        {'name': 'MIT Technology Review', 'url': 'https://www.technologyreview.com/feed/', 'category': 'strategy'},
        {'name': 'Ars Technica', 'url': 'https://feeds.arstechnica.com/arstechnica/technology-lab', 'category': 'general'},
        {'name': 'Wired', 'url': 'https://www.wired.com/feed/', 'category': 'general'},
    ],
    'tier2_specialized': [  # 高信頼性
        {'name': 'AI News', 'url': 'https://artificialintelligence-news.com/feed/', 'category': 'general'},
        {'name': 'Machine Learning Mastery', 'url': 'https://machinelearningmastery.com/feed/', 'category': 'implementation'},
        {'name': 'Analytics Vidhya', 'url': 'https://www.analyticsvidhya.com/feed/', 'category': 'implementation'},
        {'name': 'Towards AI', 'url': 'https://pub.towardsai.net/feed', 'category': 'implementation'},
        {'name': 'OpenAI Blog', 'url': 'https://openai.com/blog/rss/', 'category': 'strategy'},
    ],
    'tier3_community': [  # コミュニティソース
        {'name': 'Hacker News', 'url': 'https://hnrss.org/frontpage', 'category': 'community'},
        {'name': 'Product Hunt', 'url': 'https://www.producthunt.com/feed', 'category': 'community'},
    ],
    'japanese_sources': [  # 日本語ソース
        {'name': 'ASCII.jp AI・IoT', 'url': 'https://ascii.jp/rss.xml', 'category': 'japan_business'},
        {'name': 'ITmedia AI', 'url': 'https://rss.itmedia.co.jp/rss/2.0/ait.xml', 'category': 'japan_business'},
        {'name': 'CNET Japan', 'url': 'https://japan.cnet.com/rss/index.rdf', 'category': 'japan_business'},
    ]
}

# 許可ドメイン
ALLOWED_DOMAINS = {
    'techcrunch.com', 'theverge.com', 'venturebeat.com', 'technologyreview.com',
    'itmedia.co.jp', 'ascii.jp', 'artificialintelligence-news.com',
    'machinelearningmastery.com', 'towardsai.net', 'analyticsvidhya.com'
}

class SNSProcessor:
    """SNS(X/Twitter)データ処理クラス"""
    
    def __init__(self):
        self.now_jst = datetime.now()
        self.cutoff_time = self.now_jst - timedelta(hours=HOURS_LOOKBACK)
    
    def fetch_sns_data(self) -> List[Dict]:
        """SNS投稿データを取得"""
        print("📱 SNS投稿データを取得中...")
        
        try:
            response = requests.get(X_POSTS_CSV_URL, timeout=30)
            response.raise_for_status()
            
            # CSVパース（ヘッダーなし想定）
            csv_content = response.content.decode('utf-8-sig')
            csv_reader = csv.reader(io.StringIO(csv_content))
            
            posts = []
            for i, row in enumerate(csv_reader):
                if len(row) < 4:
                    continue
                    
                post_data = {
                    'timestamp': row[0] if len(row) > 0 else '',
                    'username': row[1] if len(row) > 1 else '',
                    'text': row[2] if len(row) > 2 else '',
                    'image_url': row[3] if len(row) > 3 else '',
                    'post_url': row[4] if len(row) > 4 else ''
                }
                posts.append(post_data)
            
            print(f"✅ SNS投稿データ取得完了: {len(posts)}件")
            return posts
            
        except Exception as e:
            print(f"[ERROR] SNS投稿データ取得エラー: {e}")
            return []
    
    def normalize_sns_posts(self, posts: List[Dict]) -> List[Dict]:
        """SNS投稿データを正規化"""
        print("🔄 SNS投稿データを正規化中...")
        
        normalized = []
        
        for post in posts:
            try:
                # タイムスタンプ処理
                timestamp = self._parse_timestamp(post.get('timestamp', ''))
                
                # 本文抽出
                text = post.get('text', '').strip()
                if not text or len(text) < 10:
                    continue
                
                # ユーザー名処理
                username = post.get('username', '').strip()
                if not username.startswith('@'):
                    username = f"@{username}" if username else "@unknown"
                
                # URL処理
                post_url = post.get('post_url', '').strip()
                if 'twitter.com' in post_url:
                    post_url = post_url.replace('twitter.com', 'x.com')
                
                normalized_post = {
                    'timestamp': timestamp,
                    'username': username,
                    'text': text,
                    'url': post_url,
                    'score': self._calculate_sns_score(text, username, timestamp),
                    'category': self._categorize_sns_post(text),
                    'source_type': 'sns'
                }
                
                normalized.append(normalized_post)
                
            except Exception as e:
                continue
        
        print(f"✅ SNS投稿正規化完了: {len(normalized)}件")
        return normalized
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """タイムスタンプ解析"""
        if not timestamp_str:
            return datetime.now()
        
        # X特有フォーマット "August 10, 2025 at 02:41AM"
        if ' at ' in timestamp_str:
            try:
                clean_timestamp = timestamp_str.replace(' at ', ' ')
                return datetime.strptime(clean_timestamp, '%B %d, %Y %I:%M%p')
            except ValueError:
                pass
        
        # その他の一般的なフォーマット
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d',
            '%m/%d/%Y %H:%M:%S',
            '%m/%d/%Y'
        ]
        
        for fmt in formats:
            try:
                return datetime.strptime(timestamp_str.split('.')[0], fmt)
            except ValueError:
                continue
        
        return datetime.now()
    
    def _calculate_sns_score(self, text: str, username: str, timestamp: datetime) -> float:
        """SNS投稿のスコア計算（緩和版）"""
        score = 1.0  # ベーススコア増加
        text_lower = text.lower()
        username_lower = username.lower()
        
        # テーママッチ（0-4点）- より多くのキーワード
        theme_keywords = [
            'ai', 'gpt', 'llm', '人工知能', '機械学習', 'chatgpt', 'claude',
            'release', 'launch', 'funding', 'investment', 'startup',
            'research', 'paper', 'breakthrough', 'model', 'tech',
            'announcement', 'new', 'update', 'feature', 'tool'
        ]
        
        theme_score = sum(1 for keyword in theme_keywords if keyword in text_lower)
        score += min(4.0, theme_score * 0.3)  # より緩い基準
        
        # 具体性（0-2点）
        if re.search(r'\$\d+[MBK]|\d+億|\d+万|¥\d+|\d+%', text):
            score += 1.5
        if re.search(r'http[s]?://\S+|\.com|\.ai', text):
            score += 0.8
        if re.search(r'AI|GPT|LLM', text, re.IGNORECASE):
            score += 0.8
        
        # 信頼性（0-2.5点）
        trusted_indicators = ['openai', 'anthropic', 'google', 'microsoft', 'meta', 'nvidia', 'deepmind']
        if any(indicator in username_lower for indicator in trusted_indicators):
            score += 2.5
        elif len(username) > 4:
            score += 1.5  # 一般アカウントのスコア増加
        
        # 鮮度（0-2点）
        if timestamp:
            hours_ago = (self.now_jst - timestamp).total_seconds() / 3600
            if hours_ago <= 6:
                score += 2.0
            elif hours_ago <= 12:
                score += 1.5
            elif hours_ago <= 24:
                score += 1.0
            elif hours_ago <= 48:
                score += 0.5
        
        # 長さボーナス（適度な長さの投稿）
        if 50 <= len(text) <= 500:
            score += 0.5
        
        return min(10.0, score)
    
    def _categorize_sns_post(self, text: str) -> str:
        """SNS投稿のカテゴリ分類"""
        text_lower = text.lower()
        
        if any(kw in text_lower for kw in ['release', 'launch', 'product']):
            return 'new_products'
        elif any(kw in text_lower for kw in ['funding', 'investment', 'raised']):
            return 'funding'
        elif any(kw in text_lower for kw in ['research', 'paper', 'study']):
            return 'research'
        elif any(kw in text_lower for kw in ['partnership', 'hiring', 'join']):
            return 'partnership'
        else:
            return 'general'
    
    def filter_sns_posts(self, posts: List[Dict]) -> List[Dict]:
        """SNS投稿のフィルタリングと選別"""
        # 48時間フィルタ
        filtered_48h = []
        all_posts = []
        
        for post in posts:
            all_posts.append(post)
            if post['timestamp'] >= self.cutoff_time:
                filtered_48h.append(post)
        
        # 48時間以内が少ない場合は全投稿から上位を選択
        if len(filtered_48h) < 15:
            print(f"📱 48時間以内の投稿が{len(filtered_48h)}件と少ないため、全期間から選択")
            # 全投稿をスコア順でソート
            all_posts.sort(key=lambda x: x['score'], reverse=True)
            # 上位30件を選択
            selected = all_posts[:30]
        else:
            # 48時間以内の投稿をスコア順でソート
            filtered_48h.sort(key=lambda x: x['score'], reverse=True)
            # 上位25件を選択
            selected = filtered_48h[:25]
        
        print(f"📱 SNS投稿選別完了: {len(selected)}件（48時間以内: {len(filtered_48h)}件、全期間: {len(all_posts)}件）")
        return selected

class RSSProcessor:
    """RSS フィード処理クラス"""
    
    def __init__(self):
        self.now_jst = datetime.now()
        self.cutoff_time = self.now_jst - timedelta(hours=HOURS_LOOKBACK)
    
    def fetch_rss_data(self) -> List[Dict]:
        """RSS データを取得"""
        print("📰 RSS フィードデータを取得中...")
        
        all_articles = []
        
        for tier_name, feeds in VERIFIED_FEEDS.items():
            print(f"  🔄 {tier_name} フィード処理中...")
            
            for feed_info in feeds:
                try:
                    print(f"    📡 {feed_info['name']} を取得中...")
                    
                    # タイムアウト設定でフィード取得
                    import socket
                    socket.setdefaulttimeout(10)
                    
                    feed = feedparser.parse(feed_info['url'])
                    
                    if not hasattr(feed, 'entries') or not feed.entries:
                        print(f"    ⚠️ {feed_info['name']}: フィードが空またはエラー")
                        continue
                    
                    processed_count = 0
                    for entry in feed.entries[:20]:  # 各フィード最大20件に増加
                        try:
                            article = self._process_rss_entry(entry, feed_info, tier_name)
                            if article:
                                all_articles.append(article)
                                processed_count += 1
                        except Exception as entry_error:
                            continue  # 個別エントリのエラーは無視
                    
                    print(f"    ✅ {feed_info['name']}: {processed_count}件")
                    
                except Exception as e:
                    print(f"    ❌ {feed_info['name']}: エラー - {str(e)[:100]}")
                    continue
        
        print(f"✅ RSS データ取得完了: {len(all_articles)}件")
        return all_articles
    
    def _process_rss_entry(self, entry, feed_info: Dict, tier_name: str) -> Dict:
        """RSS エントリを処理"""
        try:
            # タイトルとサマリーの基本チェック
            title = entry.get('title', '').strip()
            if not title:
                return None
            
            # タイムスタンプ処理（より寛容に）
            timestamp = self._parse_rss_timestamp(entry)
            if not timestamp:
                # タイムスタンプが取得できない場合は現在時刻とする（48時間フィルタを通す）
                timestamp = datetime.now()
            
            # 48時間フィルタ（緩い条件）
            if timestamp < self.cutoff_time:
                # タイムスタンプが古い場合も、重要そうな記事は含める
                text_content = f"{title} {entry.get('summary', '')}".lower()
                important_keywords = ['ai', 'artificial intelligence', 'chatgpt', 'openai', 'google', 'microsoft', 'meta', 'anthropic']
                if not any(keyword in text_content for keyword in important_keywords):
                    return None
            
            # URL取得
            url = entry.get('link', '')
            
            # タイトルとサマリー
            title = entry.get('title', '').strip()
            summary = entry.get('summary', entry.get('description', '')).strip()
            
            if not title:
                return None
            
            # HTMLタグを除去
            import re
            if summary:
                summary = re.sub(r'<[^>]+>', '', summary)
            
            return {
                'timestamp': timestamp,
                'title': title,
                'summary': summary,
                'url': url,
                'source': feed_info['name'],
                'category': feed_info['category'],
                'tier': tier_name,
                'score': self._calculate_rss_score(title, summary, feed_info['name'], tier_name),
                'source_type': 'rss'
            }
            
        except Exception as e:
            return None
    
    def _parse_rss_timestamp(self, entry) -> datetime:
        """RSS タイムスタンプ解析"""
        time_fields = ['published_parsed', 'updated_parsed']
        
        for field in time_fields:
            if hasattr(entry, field) and getattr(entry, field):
                try:
                    time_struct = getattr(entry, field)
                    return datetime(*time_struct[:6])
                except:
                    continue
        
        return None
    
    def _is_allowed_domain(self, url: str) -> bool:
        """ドメイン許可チェック（緩い条件）"""
        if not url:
            return True  # URLがない場合も許可
        try:
            domain = urlparse(url).netloc.lower()
            # 基本的に全て許可（フィルタリングは緩く）
            return True
        except:
            return True
    
    def _calculate_rss_score(self, title: str, summary: str, source: str, tier: str) -> float:
        """RSS記事のスコア計算"""
        score = 1.0  # ベーススコア
        
        # ティア別基本スコア
        tier_scores = {
            'tier1_official': 3.0,
            'tier2_specialized': 2.5,
            'tier3_community': 2.0,
            'japanese_sources': 2.0
        }
        score += tier_scores.get(tier, 1.0)
        
        # AI関連キーワード
        text = f"{title} {summary}".lower()
        ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'deep learning', 'gpt', 'llm']
        ai_score = sum(1 for kw in ai_keywords if kw in text)
        score += min(2.0, ai_score * 0.5)
        
        # ビジネス関連キーワード
        business_keywords = ['funding', 'investment', 'startup', 'company', 'partnership', 'acquisition']
        business_score = sum(1 for kw in business_keywords if kw in text)
        score += min(1.5, business_score * 0.3)
        
        return min(10.0, score)

class UnifiedReportGenerator:
    """統合レポート生成クラス"""
    
    def __init__(self):
        self.sns_processor = SNSProcessor()
        self.rss_processor = RSSProcessor()
    
    def generate_report(self) -> str:
        """統合レポート生成"""
        print("🚀 統合AIデイリーレポート生成開始")
        
        # データ取得
        sns_raw = self.sns_processor.fetch_sns_data()
        sns_posts = self.sns_processor.normalize_sns_posts(sns_raw)
        sns_selected = self.sns_processor.filter_sns_posts(sns_posts)
        
        rss_articles = self.rss_processor.fetch_rss_data()
        
        # 統合処理
        all_content = sns_selected + rss_articles
        all_content.sort(key=lambda x: x['score'], reverse=True)
        
        # カテゴリ別分類
        categorized = defaultdict(list)
        for item in all_content:
            categorized[item.get('category', 'general')].append(item)
        
        # Good News 抽出
        good_news = [item for item in all_content if item['score'] >= 6.0][:5]
        
        # HTML生成
        html_content = self._generate_html(all_content, categorized, good_news, sns_selected, rss_articles)
        
        return html_content
    
    def _generate_html(self, all_content: List[Dict], categorized: Dict, 
                      good_news: List[Dict], sns_data: List[Dict], rss_data: List[Dict]) -> str:
        """HTML レポート生成"""
        
        today = datetime.now().strftime('%Y年%m月%d日')
        
        html = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>統合AIデイリーレポート - {today}</title>
    <style>
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            background-color: #f8fafe;
            color: #2d3748;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 12px;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 2.5em;
            font-weight: 600;
        }}
        .subtitle {{
            margin: 15px 0 0 0;
            opacity: 0.9;
            font-size: 1.1em;
        }}
        .content {{
            padding: 30px;
        }}
        
        /* サマリーセクション */
        .summary {{
            background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
            border-left: 5px solid #38b2ac;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .summary h2 {{
            margin: 0 0 15px 0;
            color: #234e52;
            font-size: 1.4em;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 15px;
        }}
        .stat-item {{
            background: rgba(255,255,255,0.7);
            padding: 15px;
            border-radius: 6px;
            text-align: center;
        }}
        .stat-number {{
            font-size: 2em;
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 5px;
        }}
        .stat-label {{
            color: #4a5568;
            font-size: 0.9em;
        }}
        
        /* Good News */
        .good-news {{
            margin-bottom: 35px;
        }}
        .good-news h2 {{
            color: #2d3748;
            border-bottom: 3px solid #48bb78;
            padding-bottom: 8px;
            margin-bottom: 20px;
        }}
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 20px;
        }}
        .news-card {{
            background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
            border: 1px solid #9ae6b4;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #48bb78;
        }}
        .news-score {{
            background: #38a169;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
        }}
        .news-source {{
            background: #4299e1;
            color: white;
            padding: 3px 8px;
            border-radius: 8px;
            font-size: 0.7em;
            margin-left: 10px;
        }}
        .news-title {{
            font-weight: 600;
            color: #22543d;
            margin-bottom: 8px;
            font-size: 1.05em;
        }}
        .news-content {{
            color: #2f855a;
            font-size: 0.9em;
            margin-bottom: 12px;
        }}
        .news-meta {{
            font-size: 0.8em;
            color: #68d391;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .news-url {{
            color: #3182ce;
            text-decoration: none;
        }}
        .news-url:hover {{
            text-decoration: underline;
        }}
        
        /* タブシステム */
        .tabs {{
            display: flex;
            border-bottom: 2px solid #e2e8f0;
            margin-bottom: 20px;
        }}
        .tab {{
            padding: 12px 24px;
            background: #f7fafc;
            border: none;
            cursor: pointer;
            font-size: 1em;
            color: #4a5568;
            border-radius: 8px 8px 0 0;
            margin-right: 5px;
        }}
        .tab.active {{
            background: #4299e1;
            color: white;
        }}
        .tab-content {{
            display: none;
        }}
        .tab-content.active {{
            display: block;
        }}
        
        /* リストアイテム */
        .content-list {{
            background: #f7fafc;
            border-radius: 6px;
            overflow: hidden;
        }}
        .content-item {{
            padding: 15px 20px;
            border-bottom: 1px solid #e2e8f0;
            display: grid;
            grid-template-columns: 60px 120px 1fr 80px 100px;
            gap: 15px;
            align-items: center;
            font-size: 0.9em;
        }}
        .content-item:last-child {{
            border-bottom: none;
        }}
        .item-score {{
            background: #edf2f7;
            color: #4a5568;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            text-align: center;
        }}
        .item-source {{
            color: #4299e1;
            font-weight: 500;
            font-size: 0.8em;
        }}
        .item-title {{
            color: #2d3748;
            font-weight: 500;
        }}
        .item-time {{
            color: #718096;
            font-size: 0.8em;
        }}
        .item-url {{
            color: #3182ce;
            text-decoration: none;
            font-size: 0.8em;
        }}
        .item-url:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            background: #2d3748;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🔄 統合AIデイリーレポート</h1>
            <div class="subtitle">{today} - RSS + SNS統合分析</div>
        </div>
        
        <div class="content">
            <div class="summary">
                <h2>📊 本日のサマリー</h2>
                <div class="stats-grid">
                    <div class="stat-item">
                        <div class="stat-number">{len(sns_data)}</div>
                        <div class="stat-label">SNS投稿</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{len(rss_data)}</div>
                        <div class="stat-label">RSS記事</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{len(good_news)}</div>
                        <div class="stat-label">Good News</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-number">{len(all_content)}</div>
                        <div class="stat-label">総情報数</div>
                    </div>
                </div>
            </div>"""
        
        # Good News セクション
        if good_news:
            html += """
            <div class="good-news">
                <h2>👍 Good News（注目情報）</h2>
                <div class="news-grid">"""
            
            for item in good_news:
                source_type = "📱 SNS" if item['source_type'] == 'sns' else "📰 RSS"
                title = item.get('title', self._generate_title_from_text(item.get('text', '')))
                content = item.get('summary', item.get('text', ''))[:100] + '...'
                timestamp = item['timestamp'].strftime('%m/%d %H:%M') if item.get('timestamp') else '時刻不明'
                source_name = item.get('source', item.get('username', '不明'))
                
                html += f"""
                    <div class="news-card">
                        <div class="news-score">スコア: {item['score']:.1f}</div>
                        <span class="news-source">{source_type}</span>
                        <div class="news-title">{title}</div>
                        <div class="news-content">{content}</div>
                        <div class="news-meta">
                            <span>{source_name} | {timestamp}</span>
                            <a href="{item.get('url', '#')}" target="_blank" class="news-url">詳細</a>
                        </div>
                    </div>"""
            
            html += "</div></div>"
        
        # タブセクション
        html += """
            <h2>📋 詳細情報（カテゴリ別）</h2>
            <div class="tabs">
                <button class="tab active" onclick="openTab(event, 'all')">全て</button>
                <button class="tab" onclick="openTab(event, 'sns')">SNS投稿</button>
                <button class="tab" onclick="openTab(event, 'rss')">RSS記事</button>
            </div>"""
        
        # 全てタブ
        html += """
            <div id="all" class="tab-content active">
                <div class="content-list">"""
        
        for item in all_content[:30]:  # 上位30件
            source_type = "📱" if item['source_type'] == 'sns' else "📰"
            title = item.get('title', self._generate_title_from_text(item.get('text', '')))
            timestamp = item['timestamp'].strftime('%H:%M') if item.get('timestamp') else '--:--'
            source_name = item.get('source', item.get('username', '不明'))
            
            html += f"""
                <div class="content-item">
                    <div class="item-score">{item['score']:.1f}</div>
                    <div class="item-source">{source_type} {source_name}</div>
                    <div class="item-title">{title}</div>
                    <div class="item-time">{timestamp}</div>
                    <div><a href="{item.get('url', '#')}" target="_blank" class="item-url">詳細</a></div>
                </div>"""
        
        html += "</div></div>"
        
        # SNSタブ
        html += """
            <div id="sns" class="tab-content">
                <div class="content-list">"""
        
        for item in [x for x in all_content if x['source_type'] == 'sns'][:20]:
            title = self._generate_title_from_text(item.get('text', ''))
            timestamp = item['timestamp'].strftime('%H:%M') if item.get('timestamp') else '--:--'
            
            html += f"""
                <div class="content-item">
                    <div class="item-score">{item['score']:.1f}</div>
                    <div class="item-source">📱 {item.get('username', '不明')}</div>
                    <div class="item-title">{title}</div>
                    <div class="item-time">{timestamp}</div>
                    <div><a href="{item.get('url', '#')}" target="_blank" class="item-url">詳細</a></div>
                </div>"""
        
        html += "</div></div>"
        
        # RSSタブ
        html += """
            <div id="rss" class="tab-content">
                <div class="content-list">"""
        
        for item in [x for x in all_content if x['source_type'] == 'rss'][:20]:
            title = item.get('title', '無題')
            timestamp = item['timestamp'].strftime('%H:%M') if item.get('timestamp') else '--:--'
            
            html += f"""
                <div class="content-item">
                    <div class="item-score">{item['score']:.1f}</div>
                    <div class="item-source">📰 {item.get('source', '不明')}</div>
                    <div class="item-title">{title}</div>
                    <div class="item-time">{timestamp}</div>
                    <div><a href="{item.get('url', '#')}" target="_blank" class="item-url">詳細</a></div>
                </div>"""
        
        html += """</div></div>
        </div>
        
        <div class="footer">
            <p>🔄 統合AIデイリーレポート - RSS + SNS統合分析システム</p>
            <p>過去{HOURS_LOOKBACK}時間のデータを総合分析 | スコア重み付け評価 | エグゼクティブ最適化</p>
        </div>
    </div>
    
    <script>
        function openTab(evt, tabName) {{
            var i, tabcontent, tablinks;
            tabcontent = document.getElementsByClassName("tab-content");
            for (i = 0; i < tabcontent.length; i++) {{
                tabcontent[i].classList.remove("active");
            }}
            tablinks = document.getElementsByClassName("tab");
            for (i = 0; i < tablinks.length; i++) {{
                tablinks[i].classList.remove("active");
            }}
            document.getElementById(tabName).classList.add("active");
            evt.currentTarget.classList.add("active");
        }}
    </script>
</body>
</html>"""
        
        return html
    
    def _generate_title_from_text(self, text: str) -> str:
        """テキストからタイトルを生成"""
        if not text:
            return "無題"
        
        # 最初の文を取得
        first_sentence = text.split('。')[0].split('.')[0].split('\n')[0]
        
        # 長すぎる場合は切り詰め
        if len(first_sentence) > 60:
            return first_sentence[:60] + "..."
        
        return first_sentence

def main():
    """メイン実行関数"""
    generator = UnifiedReportGenerator()
    html_report = generator.generate_report()
    
    # ファイル保存
    today_str = datetime.now().strftime('%Y%m%d')
    report_filename = f'unified_daily_report_{today_str}.html'
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    with open('unified_daily_report_latest.html', 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"✅ 統合AIデイリーレポート生成完了: {report_filename}")

if __name__ == "__main__":
    main()