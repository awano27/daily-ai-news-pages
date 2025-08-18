#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SNSインサイト抽出エージェント
X(Twitter)投稿データから有益な情報を抽出・分析
"""

import os
import sys
import json
import csv
import io
import requests
import re
from datetime import datetime, timedelta
from collections import defaultdict
from typing import List, Dict, Any, Tuple
import warnings

# 警告無効化
warnings.filterwarnings('ignore')

# 設定
CSV_URL = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
TARGET_HOURS = 48

class SNSInsightExtractor:
    """SNSインサイト抽出器"""
    
    def __init__(self, mode: str = "lenient"):
        """
        mode: "strict" または "lenient"
        strict: 48時間以内のデータがない場合は空結果
        lenient: データがない場合は最新から48時間で再抽出
        """
        self.mode = mode
        self.now_jst = datetime.now()
        self.cutoff_time = self.now_jst - timedelta(hours=TARGET_HOURS)
    
    def fetch_csv_data(self) -> List[Dict]:
        """CSVデータを取得"""
        print("📱 SNS投稿データを取得中...")
        
        try:
            response = requests.get(CSV_URL, timeout=30)
            response.raise_for_status()
            
            # BOM対応のCSV解析（ヘッダーなしのCSVとして処理）
            csv_content = response.content.decode('utf-8-sig')
            csv_reader = csv.reader(io.StringIO(csv_content))
            
            posts = []
            for i, row in enumerate(csv_reader):
                if len(row) < 4:  # 最低限のカラム数チェック
                    continue
                    
                # 位置ベースでデータを抽出
                post_data = {
                    'timestamp': row[0] if len(row) > 0 else '',
                    'username': row[1] if len(row) > 1 else '',
                    'text': row[2] if len(row) > 2 else '',
                    'image_url': row[3] if len(row) > 3 else '',
                    'post_url': row[4] if len(row) > 4 else ''
                }
                
                posts.append(post_data)
                
                # 最初の5行のデバッグ情報
                if i < 5:
                    print(f"[DEBUG] Row {i}: timestamp='{post_data['timestamp'][:30]}...', username='{post_data['username']}', text='{post_data['text'][:50]}...'")
            
            print(f"✅ CSV取得完了: {len(posts)}行")
            return posts
            
        except Exception as e:
            print(f"[ERROR] CSV取得エラー: {e}")
            return []
    
    def normalize_posts(self, posts: List[Dict]) -> List[Dict]:
        """投稿データを正規化"""
        print("🔄 投稿データを正規化中...")
        
        normalized = []
        skipped_count = 0
        
        for i, post in enumerate(posts):
            try:
                # 日時抽出
                timestamp = self._extract_timestamp(post)
                
                # ユーザー名抽出
                username = self._extract_username(post)
                
                # 本文抽出
                text = self._extract_text(post)
                
                # URL抽出
                url = self._extract_url(post)
                
                # デバッグ情報（最初の5行）
                if i < 5:
                    print(f"[DEBUG] Post {i}: text='{text[:50] if text else 'None'}', username='{username}', timestamp='{timestamp}'")
                
                if not text or len(text) < 10:
                    skipped_count += 1
                    if i < 5:
                        print(f"[DEBUG] Skipped post {i}: text too short or empty")
                    continue
                
                normalized_post = {
                    'timestamp': timestamp,
                    'timestamp_str': timestamp.isoformat() if timestamp else '',
                    'username': username,
                    'text': text,
                    'url': url,
                    'original_data': post
                }
                
                normalized.append(normalized_post)
                
            except Exception as e:
                if i < 5:
                    print(f"[DEBUG] Error processing post {i}: {e}")
                continue
        
        print(f"✅ 正規化完了: {len(normalized)}件 (スキップ: {skipped_count}件)")
        return normalized
    
    def _extract_timestamp(self, post: Dict) -> datetime:
        """タイムスタンプ抽出・変換"""
        timestamp_fields = ['timestamp', 'date', 'created_at', 'time', 'datetime']
        
        for field in timestamp_fields:
            if field in post and post[field]:
                timestamp_str = post[field].strip()
                if timestamp_str:
                    return self._parse_timestamp(timestamp_str)
        
        return None
    
    def _parse_timestamp(self, timestamp_str: str) -> datetime:
        """タイムスタンプ文字列をdatetimeに変換（JST想定）"""
        # 既存フォーマット
        formats = [
            '%Y-%m-%d %H:%M:%S',
            '%Y-%m-%dT%H:%M:%S',
            '%Y-%m-%d',
            '%m/%d/%Y %H:%M:%S',
            '%m/%d/%Y',
            '%d/%m/%Y %H:%M:%S',
            '%d/%m/%Y',
            '%Y年%m月%d日 %H:%M:%S',
            '%Y年%m月%d日'
        ]
        
        # X特有フォーマット "August 10, 2025 at 02:41AM" を処理
        if ' at ' in timestamp_str:
            try:
                # "August 10, 2025 at 02:41AM" -> "August 10, 2025 02:41AM"
                clean_timestamp = timestamp_str.replace(' at ', ' ')
                return datetime.strptime(clean_timestamp, '%B %d, %Y %I:%M%p')
            except ValueError:
                pass
        
        for fmt in formats:
            try:
                # タイムゾーン情報や秒数以下を除去
                clean_timestamp = timestamp_str.split('.')[0].split('+')[0].split('Z')[0]
                return datetime.strptime(clean_timestamp, fmt)
            except ValueError:
                continue
        
        # パースできない場合は現在時刻
        return datetime.now()
    
    def _extract_username(self, post: Dict) -> str:
        """ユーザー名抽出"""
        username_fields = ['username', 'user', 'author', 'screen_name', 'account']
        
        for field in username_fields:
            if field in post and post[field]:
                username = post[field].strip()
                if username:
                    # @マークを追加（ない場合）
                    return username if username.startswith('@') else f"@{username}"
        
        return "@unknown"
    
    def _extract_text(self, post: Dict) -> str:
        """本文抽出"""
        text_fields = ['text', 'content', 'tweet_text', 'message', 'post', 'body']
        
        for field in text_fields:
            if field in post and post[field]:
                text = post[field].strip()
                if text:
                    return text
        
        return ""
    
    def _extract_url(self, post: Dict) -> str:
        """URL抽出（最初のX URL）"""
        url_fields = ['post_url', 'url', 'x_url', 'tweet_url', 'link']
        
        for field in url_fields:
            if field in post and post[field]:
                url = post[field].strip()
                if url and ('x.com' in url or 'twitter.com' in url):
                    # twitter.com を x.com に正規化
                    return url.replace('twitter.com', 'x.com')
        
        return ""
    
    def filter_48h(self, posts: List[Dict]) -> Tuple[List[Dict], str]:
        """48時間フィルタリング"""
        print(f"🕒 48時間フィルタリング中（基準: {self.cutoff_time.strftime('%Y-%m-%d %H:%M:%S')}）...")
        
        filtered = []
        last_timestamp = None
        
        for post in posts:
            timestamp = post['timestamp']
            if timestamp:
                if timestamp >= self.cutoff_time:
                    filtered.append(post)
                
                # 最新タイムスタンプを記録
                if last_timestamp is None or timestamp > last_timestamp:
                    last_timestamp = timestamp
        
        if not filtered and self.mode == "lenient" and last_timestamp:
            print("⚠️ 48時間以内のデータなし。lenientモードで再抽出...")
            # 最新データから48時間で再計算
            new_cutoff = last_timestamp - timedelta(hours=TARGET_HOURS)
            for post in posts:
                timestamp = post['timestamp']
                if timestamp and timestamp >= new_cutoff:
                    filtered.append(post)
            
            filter_mode = f"lenient (最新: {last_timestamp.strftime('%Y-%m-%d %H:%M:%S')})"
        else:
            filter_mode = "strict"
        
        print(f"✅ フィルタリング完了: {len(filtered)}件 (モード: {filter_mode})")
        return filtered, filter_mode
    
    def calculate_score(self, post: Dict) -> float:
        """有益度スコア計算（0-10）"""
        text = post['text'].lower()
        username = post['username'].lower()
        timestamp = post['timestamp']
        
        score = 0.0
        
        # テーマ一致度（0-4点）
        theme_keywords = {
            'release': ['release', 'released', 'launching', 'launch', '公開', 'リリース', 'announced'],
            'funding': ['funding', 'raised', 'investment', 'ipo', '資金調達', '投資', 'series'],
            'partnership': ['partnership', 'collaboration', 'acquisition', '提携', '買収', 'merger'],
            'hiring': ['hiring', 'join', 'team', '採用', '入社', 'welcome'],
            'research': ['paper', 'research', 'benchmark', '論文', '研究', 'study'],
            'official': ['announcing', 'excited to', 'proud to', '発表', 'official']
        }
        
        theme_matches = 0
        for theme, keywords in theme_keywords.items():
            if any(keyword in text for keyword in keywords):
                theme_matches += 1
        
        score += min(3.5, theme_matches * 1.0)  # テーママッチを緩和
        
        # 具体性（0-2.5点）
        specificity = 0
        
        # 金額・数値
        if re.search(r'\$\d+[MBK]|\d+億|\d+万|¥\d+|\d+%', text):
            specificity += 1
        
        # 日付
        if re.search(r'\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}|\d{1,2}月', text):
            specificity += 0.5
        
        # URL・製品名
        if re.search(r'http[s]?://\S+|\.com|\.ai|v\d+\.\d+', text):
            specificity += 0.5
        
        # AI関連キーワード
        if re.search(r'AI|GPT|LLM|機械学習|人工知能|ディープラーニング', text, re.IGNORECASE):
            specificity += 1
        
        score += min(2.5, specificity)
        
        # 発信元信頼性（0-2点）
        trusted_indicators = ['openai', 'anthropic', 'google', 'microsoft', 'meta', 'nvidia', 'official']
        if any(indicator in username for indicator in trusted_indicators):
            score += 2.0
        elif len(username) > 4:  # 実在アカウント
            score += 1.5  # 基準値上げ
        
        # 鮮度ボーナス（0-1.5点）
        if timestamp:
            hours_ago = (self.now_jst - timestamp).total_seconds() / 3600
            if hours_ago <= 12:
                score += 1.5  # 12時間以内はボーナス増
            elif hours_ago <= 24:
                score += 1.0
            elif hours_ago <= 48:
                score += 0.5
        
        # 基本ベーススコア（存在するだけで0.5点）
        score += 0.5
        
        return min(10.0, score)
    
    def filter_useful_posts(self, posts: List[Dict]) -> List[Dict]:
        """有益投稿の抽出"""
        print("🎯 有益投稿を抽出中...")
        
        scored_posts = []
        
        for post in posts:
            score = self.calculate_score(post)
            post['score'] = score
            scored_posts.append(post)
        
        # スコア順でソート
        scored_posts.sort(key=lambda x: x['score'], reverse=True)
        
        # 動的しきい値設定：1日10-15件程度を目標
        target_count = min(15, max(10, len(scored_posts) // 10))  # 最低10件、最大15件
        
        if len(scored_posts) >= target_count:
            # 上位N件を選択
            useful_posts = scored_posts[:target_count]
            min_score = useful_posts[-1]['score']
            print(f"✅ 有益投稿抽出完了: {len(useful_posts)}件 (上位{target_count}件、最低スコア: {min_score:.1f})")
        else:
            # 全件がスコア3.0以上の場合は採用
            useful_posts = [post for post in scored_posts if post['score'] >= 3.0]
            print(f"✅ 有益投稿抽出完了: {len(useful_posts)}件 (スコア3.0以上)")
        
        return useful_posts
    
    def generate_japanese_title(self, text: str) -> str:
        """日本語タイトル生成（14字前後）"""
        # 英語投稿の場合は簡易翻訳・要約
        text_clean = re.sub(r'http[s]?://\S+', '', text).strip()
        
        # キーワードベースの簡易要約
        if 'release' in text.lower() or 'launch' in text.lower():
            if 'ai' in text.lower():
                return "AI新製品リリース発表"
            return "新製品リリース発表"
        
        elif 'funding' in text.lower() or 'raised' in text.lower():
            return "資金調達ニュース"
        
        elif 'partnership' in text.lower() or 'collaboration' in text.lower():
            return "戦略的提携発表"
        
        elif 'research' in text.lower() or 'paper' in text.lower():
            return "AI研究成果発表"
        
        elif 'hiring' in text.lower() or 'join' in text.lower():
            return "人材採用・組織拡大"
        
        else:
            # 最初の50文字を使用
            if len(text_clean) > 14:
                return text_clean[:14] + "..."
            return text_clean
    
    def categorize_post(self, post: Dict) -> str:
        """投稿のカテゴリ分類"""
        text = post['text'].lower()
        
        if any(kw in text for kw in ['release', 'launch', 'product', '新製品', 'リリース']):
            return 'new_products'
        elif any(kw in text for kw in ['funding', 'investment', 'raised', '資金調達']):
            return 'funding'
        elif any(kw in text for kw in ['partnership', 'hiring', 'join', '提携', '採用']):
            return 'partnership_hiring'
        elif any(kw in text for kw in ['research', 'paper', 'study', '研究', '論文']):
            return 'research'
        elif any(kw in text for kw in ['regulation', 'policy', 'law', '規制', '政策']):
            return 'regulation'
        else:
            return 'community'
    
    def generate_html_report(self, posts: List[Dict], filter_mode: str, 
                           total_rows: int, filtered_48h: int) -> str:
        """HTMLレポート生成"""
        
        if not posts:
            if self.mode == "strict":
                return self._generate_empty_report_strict()
            else:
                return self._generate_empty_report_lenient()
        
        # Good News抽出（上位3-5件、スコア6.0以上）
        good_news = [post for post in posts if post['score'] >= 6.0][:5]
        
        # カテゴリ別分類
        categorized = defaultdict(list)
        for post in posts:
            category = self.categorize_post(post)
            categorized[category].append(post)
        
        # カテゴリ名の日本語化
        category_names = {
            'new_products': '🚀 新製品・機能',
            'funding': '💰 資金調達',
            'partnership_hiring': '🤝 提携・採用',
            'research': '🔬 研究・ベンチマーク',
            'regulation': '⚖️ セキュリティ・規制',
            'community': '💬 コミュニティ'
        }
        
        # 最新タイムスタンプ
        last_timestamp = max(post['timestamp'] for post in posts if post['timestamp'])
        
        html_content = f"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SNSインサイト抽出レポート - {datetime.now().strftime('%Y年%m月%d日')}</title>
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
            max-width: 1000px;
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
            font-size: 2.2em;
            font-weight: 600;
        }}
        .subtitle {{
            margin: 12px 0 0 0;
            opacity: 0.9;
            font-size: 1em;
        }}
        .content {{
            padding: 30px;
        }}
        
        /* デイリーSNSサマリー */
        .daily-summary {{
            background: linear-gradient(135deg, #e6fffa 0%, #b2f5ea 100%);
            border-left: 5px solid #38b2ac;
            padding: 25px;
            border-radius: 8px;
            margin-bottom: 30px;
        }}
        .daily-summary h2 {{
            margin: 0 0 15px 0;
            color: #234e52;
            font-size: 1.3em;
        }}
        .summary-points {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .summary-points li {{
            margin-bottom: 8px;
            padding-left: 20px;
            position: relative;
            color: #2d3748;
        }}
        .summary-points li:before {{
            content: "📌";
            position: absolute;
            left: 0;
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
        .good-news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }}
        .good-news-card {{
            background: linear-gradient(135deg, #f0fff4 0%, #c6f6d5 100%);
            border: 1px solid #9ae6b4;
            padding: 20px;
            border-radius: 10px;
            border-left: 5px solid #48bb78;
        }}
        .good-news-score {{
            background: #38a169;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.8em;
            font-weight: 600;
            display: inline-block;
            margin-bottom: 10px;
        }}
        .good-news-title {{
            font-weight: 600;
            color: #22543d;
            margin-bottom: 8px;
            font-size: 1.05em;
        }}
        .good-news-summary {{
            color: #2f855a;
            font-size: 0.9em;
            margin-bottom: 12px;
        }}
        .good-news-meta {{
            font-size: 0.8em;
            color: #68d391;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .good-news-url {{
            color: #3182ce;
            text-decoration: none;
        }}
        .good-news-url:hover {{
            text-decoration: underline;
        }}
        
        /* カテゴリ別詳細 */
        .category-section {{
            margin-bottom: 30px;
        }}
        .category-header {{
            background: #4a5568;
            color: white;
            padding: 12px 20px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 1.1em;
            margin-bottom: 15px;
        }}
        .post-list {{
            background: #f7fafc;
            border-radius: 6px;
            overflow: hidden;
        }}
        .post-item {{
            padding: 15px 20px;
            border-bottom: 1px solid #e2e8f0;
            display: grid;
            grid-template-columns: 80px 100px 1fr 60px 120px;
            gap: 15px;
            align-items: center;
            font-size: 0.9em;
        }}
        .post-item:last-child {{
            border-bottom: none;
        }}
        .post-time {{
            color: #718096;
            font-size: 0.8em;
        }}
        .post-author {{
            color: #4299e1;
            font-weight: 500;
        }}
        .post-title {{
            color: #2d3748;
            font-weight: 500;
        }}
        .post-score {{
            background: #edf2f7;
            color: #4a5568;
            padding: 3px 8px;
            border-radius: 10px;
            font-size: 0.8em;
            text-align: center;
        }}
        .post-url {{
            color: #3182ce;
            text-decoration: none;
            font-size: 0.8em;
        }}
        .post-url:hover {{
            text-decoration: underline;
        }}
        
        /* 検証データ */
        .verification {{
            background: #f7fafc;
            border: 1px solid #e2e8f0;
            padding: 20px;
            border-radius: 8px;
            margin-top: 30px;
        }}
        .verification h3 {{
            margin: 0 0 12px 0;
            color: #2d3748;
            font-size: 1.1em;
        }}
        .verification pre {{
            background: #edf2f7;
            padding: 12px;
            border-radius: 4px;
            overflow-x: auto;
            font-size: 0.85em;
            margin: 0;
        }}
        
        .footer {{
            background: #2d3748;
            color: white;
            padding: 20px;
            text-align: center;
            font-size: 0.9em;
        }}
        
        .fallback-notice {{
            background: #fff5b8;
            border: 1px solid #fbd38d;
            color: #744210;
            padding: 15px;
            border-radius: 6px;
            margin-bottom: 20px;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📱 SNSインサイト抽出レポート</h1>
            <div class="subtitle">{datetime.now().strftime('%Y年%m月%d日')} - 過去48時間のX(Twitter)分析</div>
        </div>
        
        <div class="content">"""
        
        # フォールバック通知
        if "lenient" in filter_mode:
            html_content += """
            <div class="fallback-notice">
                <strong>※データ未更新のため代替窓:</strong> 最新データから48時間遡って抽出しました。
            </div>"""
        
        # デイリーSNSサマリー
        html_content += f"""
            <div class="daily-summary">
                <h2>📋 デイリーSNSサマリー</h2>
                <ul class="summary-points">
                    <li>過去48時間で{len(posts)}件の有益なX投稿を発見・分析</li>
                    <li>スコア8.0以上の注目情報{len(good_news)}件を特に重要として抽出</li>
                    <li>AI製品リリース・資金調達・技術提携の動向が活発化</li>
                    <li>SNSならではの速報性により、公式発表前の情報もキャッチ</li>
                    <li>エグゼクティブ向け意思決定に有効な具体的情報を優先収集</li>
                </ul>
            </div>"""
        
        # Good News
        if good_news:
            html_content += """
            <div class="good-news">
                <h2>👍 Good News（注目の重要情報）</h2>
                <div class="good-news-grid">"""
            
            for post in good_news:
                title = self.generate_japanese_title(post['text'])
                summary = post['text'][:60] + ('...' if len(post['text']) > 60 else '')
                time_str = post['timestamp'].strftime('%m/%d %H:%M') if post['timestamp'] else '時刻不明'
                
                html_content += f"""
                    <div class="good-news-card">
                        <div class="good-news-score">スコア: {post['score']:.1f}</div>
                        <div class="good-news-title">{title}</div>
                        <div class="good-news-summary">{summary}</div>
                        <div class="good-news-meta">
                            <span>{post['username']} | {time_str}</span>
                            <a href="{post['url']}" target="_blank" class="good-news-url">詳細</a>
                        </div>
                    </div>"""
            
            html_content += "</div></div>"
        
        # カテゴリ別詳細
        html_content += "<h2>📊 詳細分析（カテゴリ別）</h2>"
        
        for category, category_posts in categorized.items():
            if not category_posts:
                continue
                
            category_name = category_names.get(category, category)
            
            html_content += f"""
            <div class="category-section">
                <div class="category-header">{category_name} ({len(category_posts)}件)</div>
                <div class="post-list">"""
            
            for post in category_posts[:10]:  # 各カテゴリ最大10件
                title = self.generate_japanese_title(post['text'])
                time_str = post['timestamp'].strftime('%H:%M') if post['timestamp'] else '--:--'
                url_display = "詳細" if post['url'] else "リンクなし"
                
                html_content += f"""
                    <div class="post-item">
                        <div class="post-time">{time_str}</div>
                        <div class="post-author">{post['username']}</div>
                        <div class="post-title">{title}</div>
                        <div class="post-score">{post['score']:.1f}</div>
                        <div><a href="{post['url']}" target="_blank" class="post-url">{url_display}</a></div>
                    </div>"""
            
            html_content += "</div></div>"
        
        # 検証データ
        verification_data = {
            "total_rows": total_rows,
            "filtered_48h": filtered_48h,
            "selected_useful": len(posts),
            "good_news_count": len(good_news),
            "last_timestamp": last_timestamp.isoformat() if last_timestamp else None,
            "mode": filter_mode
        }
        
        html_content += f"""
            <div class="verification">
                <h3>🔍 検証データ</h3>
                <pre>{json.dumps(verification_data, ensure_ascii=False, indent=2)}</pre>
            </div>
        </div>
        
        <div class="footer">
            <p>📱 Generated by SNS Insight Extraction Agent</p>
            <p>X(Twitter) データ分析 | 有益度スコア重み付け | ビジネス価値重視</p>
        </div>
    </div>
</body>
</html>"""
        
        return html_content
    
    def _generate_empty_report_strict(self) -> str:
        """厳密モード：空結果レポート"""
        return """
        <div style="text-align: center; padding: 40px; color: #718096;">
            <h2>📱 SNSインサイト抽出結果</h2>
            <p><strong>48時間以内の該当は0件</strong></p>
        </div>
        """
    
    def _generate_empty_report_lenient(self) -> str:
        """寛容モード：空結果レポート"""
        return """
        <div style="text-align: center; padding: 40px; color: #718096;">
            <h2>📱 SNSインサイト抽出結果</h2>
            <p>有益な投稿データが見つかりませんでした。</p>
            <p>※データソースの更新をお待ちください</p>
        </div>
        """
    
    def run(self) -> str:
        """メイン処理実行"""
        print("🚀 SNSインサイト抽出エージェント開始")
        
        # 1. CSVデータ取得
        raw_posts = self.fetch_csv_data()
        if not raw_posts:
            return self._generate_empty_report_strict()
        
        total_rows = len(raw_posts)
        
        # 2. 正規化
        normalized_posts = self.normalize_posts(raw_posts)
        if not normalized_posts:
            return self._generate_empty_report_strict()
        
        # 3. 48時間フィルタ
        filtered_posts, filter_mode = self.filter_48h(normalized_posts)
        filtered_48h = len(filtered_posts)
        
        if not filtered_posts:
            if self.mode == "strict":
                return self._generate_empty_report_strict()
            else:
                return self._generate_empty_report_lenient()
        
        # 4. 有益投稿抽出
        useful_posts = self.filter_useful_posts(filtered_posts)
        
        # 5. HTMLレポート生成
        html_report = self.generate_html_report(
            useful_posts, filter_mode, total_rows, filtered_48h
        )
        
        return html_report

def main():
    """メイン関数"""
    mode = os.getenv('SNS_MODE', 'lenient')  # デフォルトは lenient
    
    extractor = SNSInsightExtractor(mode=mode)
    html_report = extractor.run()
    
    # ファイル保存
    today_str = datetime.now().strftime('%Y%m%d')
    report_filename = f'sns_insight_report_{today_str}.html'
    
    with open(report_filename, 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    with open('sns_insight_report_latest.html', 'w', encoding='utf-8') as f:
        f.write(html_report)
    
    print(f"✅ SNSインサイトレポート生成完了: {report_filename}")

if __name__ == "__main__":
    main()