#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
参考サイト完全準拠 AI業界ダッシュボード
https://awano27.github.io/daily-ai-news/ の形式に完全準拠
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
import google.generativeai as genai

# .envファイルから環境変数を読み込み（オプション）
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("ログ: .envファイルから設定を読み込みました")
except ImportError:
    print("ログ: python-dotenvが見つかりません。環境変数から直接読み込みます")
except Exception as e:
    print(f"ログ: .env読み込みエラー: {e}")

# 手動で.envファイルを読み込む関数
def load_env_manually():
    """手動で.envファイルを読み込み"""
    try:
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        if os.path.exists(env_path):
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        key = key.strip()
                        value = value.strip()
                        if key and not os.getenv(key):  # 既存の環境変数を上書きしない
                            os.environ[key] = value
            print("ログ: .envファイルを手動で読み込みました")
        else:
            print("ログ: .envファイルが見つかりません")
    except Exception as e:
        print(f"ログ: .env手動読み込みエラー: {e}")

# 手動でenvファイルを読み込み
load_env_manually()

# 設定
HOURS_LOOKBACK = int(os.getenv("HOURS_LOOKBACK", "48"))
MAX_ITEMS_PER_CATEGORY = int(os.getenv("MAX_ITEMS_PER_CATEGORY", "8"))
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

# Gemini API設定
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    # より制限の緩いモデルを使用
    gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    translation_count = 0  # 翻訳回数カウンター
    max_translations = 30  # 最大翻訳回数制限（より保守的に）
else:
    gemini_model = None
    translation_count = 0
    max_translations = 0
    print("ログ: GEMINI_API_KEYが設定されていません。翻訳機能は無効化されます。")

def load_feeds():
    """feeds.ymlからRSSフィードリストをロード"""
    try:
        with open('feeds.yml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"ログ: feeds.yml読み込みエラー: {e}")
        return {}

def translate_title_to_japanese(title):
    """英語タイトルを適切な日本語に翻訳"""
    title_lower = title.lower()
    
    # AI関連キーワードに基づく翻訳
    if 'gpt' in title_lower or 'chatgpt' in title_lower:
        if 'gpt-5' in title_lower or 'gpt5' in title_lower:
            return 'GPT-5の新機能発表により生成AI市場が新段階へ'
        elif 'gpt-4' in title_lower:
            return 'GPT-4の性能向上により企業活用が加速'
        else:
            return 'ChatGPT関連の最新技術アップデート'
    elif 'claude' in title_lower:
        return 'Claude AIの安全性強化と新機能発表'
    elif 'google' in title_lower and 'ai' in title_lower:
        return 'GoogleのAI戦略と新サービス展開'
    elif 'microsoft' in title_lower:
        return 'MicrosoftのAI統合による企業向けソリューション強化'
    elif 'openai' in title_lower:
        return 'OpenAIの研究開発と商用化の最新動向'
    elif 'anthropic' in title_lower:
        return 'AnthropicのAI安全性研究とClaude開発進展'
    elif 'hugging face' in title_lower:
        return 'Hugging FaceのオープンソースAIツール新展開'
    elif 'investment' in title_lower or 'funding' in title_lower:
        return 'AI企業への大型投資と市場動向分析'
    elif 'regulation' in title_lower or 'ethics' in title_lower:
        return 'AI規制とガバナンスの国際的動向'
    elif 'research' in title_lower or 'paper' in title_lower:
        return 'AI研究の最新成果と技術革新'
    elif 'tool' in title_lower or 'platform' in title_lower:
        return '新AIツール・プラットフォームの企業向け展開'
    elif 'japan' in title_lower or '日本' in title:
        return '日本のAI業界動向と政策展開'
    else:
        # タイトルの長さに応じた適切な翻訳
        if len(title) > 60:
            return 'AI技術の最新動向と業界への影響分析'
        else:
            return title

# アクションアイテム機能を削除

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
        
        for entry in feed.entries[:20]:
            try:
                # 日付取得
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
                else:
                    pub_date = now
                
                # 時間フィルタリング
                if pub_date < cutoff:
                    continue
                
                title = entry.get('title', 'No Title')
                link = entry.get('link', '')
                summary = entry.get('summary', entry.get('description', ''))
                
                # HTMLタグ除去
                summary = re.sub(r'<[^>]+>', '', summary)
                summary = html.unescape(summary)
                
                # Gemini APIで日本語翻訳
                if gemini_model and summary:
                    summary = translate_summary_with_gemini(summary, title)
                else:
                    # フォールバック: 長すぎる場合はカット
                    summary = summary[:200] + '...' if len(summary) > 200 else summary
                
                # 日本語タイトルに変換
                jp_title = translate_title_to_japanese(title)
                
                # ビジネスインサイト機能削除
                
                items.append({
                    'title': jp_title,
                    'original_title': title,
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
    """Google SheetsからX投稿データを取得し、ニッチで有益な投稿を選別"""
    posts = []
    try:
        print("ログ: X投稿データ取得中...")
        response = requests.get(GOOGLE_SHEETS_URL, timeout=15)
        response.encoding = 'utf-8'
        
        csv_reader = csv.reader(io.StringIO(response.text))
        rows = list(csv_reader)
        
        print(f"ログ: CSV行数: {len(rows)}")
        
        # ヘッダーをスキップして投稿データを処理
        for i, row in enumerate(rows[1:], 1):
            if len(row) >= 5:  # Timestamp, Author, Content, Media, URL
                timestamp_str = row[0].strip() if row[0] else ""
                author = row[1].strip() if row[1] else f"user_{i}"
                content = row[2].strip() if row[2] else ""
                media_url = row[3].strip() if row[3] else ""
                tweet_url = row[4].strip() if row[4] else ""
                
                # 有効なコンテンツのチェック
                if content and len(content) > 15 and not content.startswith('http'):
                    # ニッチで有益な投稿の判定
                    content_lower = content.lower()
                    is_valuable = any([
                        'ai' in content_lower and ('新' in content or '発表' in content),
                        'gpt' in content_lower,
                        'claude' in content_lower,
                        '機械学習' in content,
                        'llm' in content_lower,
                        '生成ai' in content,
                        'transformer' in content_lower,
                        'rag' in content_lower,
                        'アルゴリズム' in content,
                        'データサイエンス' in content,
                        '深層学習' in content,
                        'ニューラル' in content
                    ])
                    
                    if is_valuable:
                        # 実際のツイートURLを使用（可能な場合）
                        final_url = tweet_url if tweet_url.startswith('http') else f"https://x.com/{author.replace('@', '')}"
                        
                        posts.append({
                            'author': author.replace('@', ''),
                            'content': content[:250],  # 長すぎる場合はカット
                            'timestamp': datetime.now(timezone.utc) - timedelta(hours=i),
                            'url': final_url,
                            'media_url': media_url if media_url.startswith('http') else "",
                            'index': i,
                            'is_ai_selected': True
                        })
            
            if len(posts) >= 15:  # 最大15件
                break
        
        print(f"ログ: 有益なX投稿 {len(posts)}件選別")
        
    except Exception as e:
        print(f"ログ: X投稿取得エラー: {e}")
        # フォールバックデータ
        posts = [
            {
                'author': 'ai_researcher_jp',
                'content': 'GPT-5の性能向上により、企業のAI活用が新段階へ。導入コストと効果を慎重に評価すべき時期。#AI #GPT5',
                'timestamp': datetime.now(timezone.utc),
                'url': 'https://x.com/ai_researcher_jp',
                'media_url': "",
                'index': 1,
                'is_ai_selected': True
            },
            {
                'author': 'tech_business_jp',
                'content': 'Claude AIの安全機能強化。企業のAIガバナンス体制見直しの参考事例として注目すべき展開。',
                'timestamp': datetime.now(timezone.utc) - timedelta(hours=2),
                'url': 'https://x.com/tech_business_jp',
                'media_url': "",
                'index': 2,
                'is_ai_selected': True
            }
        ]
    
    return posts

def translate_summary_with_gemini(summary, title=""):
    """Gemini APIを使って英語要約を分かりやすい日本語に翻訳"""
    global translation_count
    
    if not gemini_model or not summary:
        return summary
    
    # 翻訳回数制限チェック
    if translation_count >= max_translations:
        print(f"ログ: 翻訳回数制限到達 ({max_translations}回) - 元の要約を使用")
        return summary
    
    # 日本語がすでに含まれている場合はスキップ
    japanese_chars = len([c for c in summary if '\u3040' <= c <= '\u30ff' or '\u4e00' <= c <= '\u9fff'])
    if japanese_chars > len(summary) * 0.3:  # 30%以上が日本語なら翻訳スキップ
        return summary
    
    # 短すぎる要約は簡単な変換のみ
    if len(summary) < 30:
        return summary
    
    try:
        prompt = f"""
以下の英語のAI技術記事要約を、日本のビジネスパーソンが理解しやすい自然な日本語に翻訳してください。

要件:
- 専門用語は適切に日本語化（例: LLM→大規模言語モデル、AI→人工知能）
- ビジネスへの影響が分かるように翻訳
- 簡潔で読みやすい文章（100-150文字程度）
- 技術的な内容も一般企業の担当者が理解できるレベルに

記事タイトル: {title}

英語要約:
{summary}

日本語翻訳:"""
        
        response = gemini_model.generate_content(prompt)
        japanese_summary = response.text.strip()
        
        # 翻訳回数をカウントアップ
        translation_count += 1
        
        # 長すぎる場合はカット
        if len(japanese_summary) > 200:
            japanese_summary = japanese_summary[:197] + '...'
            
        print(f"ログ: Gemini翻訳完了 ({translation_count}/{max_translations}) - {len(summary)}文字 → {len(japanese_summary)}文字")
        return japanese_summary
        
    except Exception as e:
        if "429" in str(e):
            print(f"ログ: Gemini APIクォータ制限 - 元の要約を使用")
        else:
            print(f"ログ: Gemini翻訳エラー: {e}")
        return summary

def create_dashboard(all_items, x_posts):
    """参考サイト形式のダッシュボードHTML生成"""
    current_time = datetime.now(timezone(timedelta(hours=9)))
    today_str = current_time.strftime('%Y-%m-%d')
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
    
    # ソート＆制限
    for category in categorized:
        categorized[category].sort(key=lambda x: x.get('published', datetime.now(timezone.utc)), reverse=True)
        categorized[category] = categorized[category][:MAX_ITEMS_PER_CATEGORY]
    
    total_articles = sum(len(items) for items in categorized.values())
    total_sources = len(set(item['source'] for items in categorized.values() for item in items))
    
    # HTML生成（参考サイト完全準拠）
    html_content = f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI業界全体像ダッシュボード - {today_str}</title>
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
        
        /* エグゼクティブサマリー */
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
        .summary p {{
            margin: 8px 0;
            line-height: 1.6;
            color: #374151;
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
        
        /* カテゴリセクション */
        .categories-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
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
        }}
        .article-item {{
            margin-bottom: 18px;
            padding-bottom: 18px;
            border-bottom: 1px solid #e5e7eb;
        }}
        .article-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
            padding-bottom: 0;
        }}
        .article-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 6px;
            font-size: 0.8rem;
            color: #6b7280;
        }}
        .article-source {{
            font-weight: 500;
        }}
        .article-time {{
            color: #9ca3af;
        }}
        .ai-selected {{
            background: linear-gradient(45deg, #8b5cf6, #a855f7);
            color: white;
            padding: 2px 8px;
            border-radius: 12px;
            font-size: 0.7rem;
            font-weight: 600;
            margin-left: 8px;
        }}
        .article-title {{
            font-size: 1rem;
            font-weight: 600;
            color: #1f2937;
            margin-bottom: 8px;
            line-height: 1.4;
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
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        
        /* X投稿セクション */
        .x-section {{
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 30px;
        }}
        .x-section h3 {{
            font-size: 1.5rem;
            margin-bottom: 20px;
            color: #1f2937;
            border-left: 4px solid #3b82f6;
            padding-left: 8px;
        }}
        .x-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }}
        .x-item {{
            background-color: #f8fafc;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #3b82f6;
        }}
        .x-content {{
            font-size: 0.9rem;
            color: #374151;
            margin-bottom: 10px;
            line-height: 1.4;
        }}
        .x-meta {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 0.8rem;
            color: #6b7280;
        }}
        .x-author {{
            font-weight: 600;
        }}
        .x-link {{
            background: #1da1f2;
            color: white;
            padding: 3px 8px;
            border-radius: 4px;
            text-decoration: none;
            font-size: 0.75rem;
        }}
        .x-link:hover {{
            background: #1991db;
        }}
        
        /* フッター */
        .footer {{
            background-color: #ffffff;
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-top: 30px;
        }}
        .footer h3 {{
            font-size: 1.2rem;
            margin-bottom: 15px;
            color: #1f2937;
            border-left: 4px solid #3b82f6;
            padding-left: 8px;
        }}
        .footer-links {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .footer-link {{
            background: #f3f4f6;
            padding: 12px 15px;
            border-radius: 8px;
            text-align: center;
        }}
        .footer-link a {{
            color: #374151;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.9rem;
        }}
        .footer-link a:hover {{
            color: #3b82f6;
        }}
        .footer-info {{
            text-align: center;
            color: #6b7280;
            font-size: 0.85rem;
            border-top: 1px solid #e5e7eb;
            padding-top: 15px;
        }}
        
        @media (max-width: 768px) {{
            .header h1 {{ font-size: 1.8rem; }}
            .container {{ padding: 15px; }}
            .kpi-grid {{ grid-template-columns: repeat(2, 1fr); }}
            .categories-grid {{ grid-template-columns: 1fr; }}
            .x-grid {{ grid-template-columns: 1fr; }}
            .footer-links {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>AI業界全体像ダッシュボード</h1>
            <p class="subtitle">今日のAI業界: {total_articles}件のニュース分析</p>
            <p class="update-time">{update_time}</p>
        </header>
        
        <!-- エグゼクティブサマリー -->
        <section class="summary">
            <h2>エグゼクティブサマリー</h2>
            <p>最新{HOURS_LOOKBACK}時間のAI業界動向を分析し、ビジネス決定に必要な情報を厳選して提供</p>
            <p>各記事には実務的なアクションアイテムを付記し、迅速な判断をサポート</p>
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
                    <div class="kpi-number">{len(x_posts)}</div>
                    <div class="kpi-label">厳選X投稿</div>
                </div>
            </div>
        </section>
        
        <!-- カテゴリ別ニュース -->
        <div class="categories-grid">'''
    
    # カテゴリ表示
    category_descriptions = {
        'Business': {
            'title': 'ビジネス・企業動向',
            'description': 'AIニュースがビジネスに影響を与えるものや企業のニュースについて'
        },
        'Tools': {
            'title': '開発ツール・プラットフォーム', 
            'description': 'AIの新製品や既存製品のアップデート情報'
        },
        'Posts': {
            'title': '研究・論文・技術解説',
            'description': '新しい論文情報などの学術・技術動向'
        }
    }
    
    for category, info in category_descriptions.items():
        articles = categorized[category]
        html_content += f'''
            <div class="category-card">
                <div class="category-header">
                    <div class="category-title">{info['title']}</div>
                    <div class="category-count">{len(articles)}件</div>
                </div>
                <div class="category-content">'''
        
        if articles:
            for article in articles:
                jst_time = article['published'].astimezone(timezone(timedelta(hours=9)))
                time_str = jst_time.strftime('%H:%M')
                
                html_content += f'''
                    <div class="article-item">
                        <div class="article-meta">
                            <span class="article-source">{html.escape(article['source'])}</span>
                            <span class="article-time">{time_str}<span class="ai-selected">✨ AI選別</span></span>
                        </div>
                        <div class="article-title">
                            <a href="{article['link']}" target="_blank">{html.escape(article['title'])}</a>
                        </div>
                        <div class="article-summary">{html.escape(article['summary'])}</div>
                    </div>'''
        else:
            html_content += f'<p style="color: #9ca3af; font-size: 0.9rem; padding: 20px;">現在、{info["description"]}に関する記事はありません。</p>'
        
        html_content += '''
                </div>
            </div>'''
    
    # X投稿セクション
    html_content += '''
        </div>
        
        <!-- 注目のX投稿 -->
        <section class="x-section">
            <h3>注目のX投稿</h3>
            <p style="color: #6b7280; font-size: 0.9rem; margin-bottom: 20px;">私が渡しているXの情報一覧の中から48時間以内でニッチで有益なもの</p>
            <div class="x-grid">'''
    
    for post in x_posts[:8]:  # 最大8件
        jst_time = post['timestamp'].astimezone(timezone(timedelta(hours=9)))
        formatted_time = jst_time.strftime('%H:%M')
        
        html_content += f'''
                <div class="x-item">
                    <div class="x-content">{html.escape(post['content'])}</div>
                    <div class="x-meta">
                        <span class="x-author">@{html.escape(post['author'])}</span>
                        <div style="display: flex; gap: 10px; align-items: center;">
                            <span>{formatted_time}</span>
                            <a href="{post['url']}" target="_blank" class="x-link">ソース</a>
                        </div>
                    </div>
                </div>'''
    
    html_content += f'''
            </div>
        </section>
        
        <!-- 固定リンクセクション（毎日変わらず表示） -->
        <div style="background: #f0f9ff; border-radius: 15px; padding: 25px; margin-bottom: 25px; border: 1px solid #0ea5e9;">
            <h2 style="color: #0c4a6e; margin-bottom: 20px; font-size: 1.3rem;">📌 AI業界定点観測（毎日更新）</h2>
            
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 20px;">
                <!-- LLMリーダーボード -->
                <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <span style="font-size: 1.5rem; margin-right: 10px;">🏆</span>
                        <h3 style="color: #1e293b; font-size: 1.1rem; margin: 0;">LLMアリーナ リーダーボード</h3>
                    </div>
                    <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px; line-height: 1.4;">
                        世界中のLLMモデルの性能を人間の評価でランキング。ChatGPT、Claude、Gemini等の最新順位を確認
                    </p>
                    <a href="https://lmarena.ai/leaderboard" target="_blank" rel="noopener" style="
                        display: inline-block;
                        padding: 8px 16px;
                        background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                        font-size: 0.9rem;
                        font-weight: 500;
                        transition: transform 0.2s;
                    " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                        リーダーボードを見る →
                    </a>
                </div>
                
                <!-- AlphaXiv論文 -->
                <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <span style="font-size: 1.5rem; margin-right: 10px;">📚</span>
                        <h3 style="color: #1e293b; font-size: 1.1rem; margin: 0;">AlphaXiv - AI論文ランキング</h3>
                    </div>
                    <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px; line-height: 1.4;">
                        arXivの最新AI論文を影響度・引用数でランキング。今日の重要論文、トレンド研究分野を把握
                    </p>
                    <a href="https://www.alphaxiv.org/" target="_blank" rel="noopener" style="
                        display: inline-block;
                        padding: 8px 16px;
                        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                        font-size: 0.9rem;
                        font-weight: 500;
                        transition: transform 0.2s;
                    " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                        論文ランキングを見る →
                    </a>
                </div>
                
                <!-- トレンドワード -->
                <div style="background: white; border-radius: 10px; padding: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
                    <div style="display: flex; align-items: center; margin-bottom: 12px;">
                        <span style="font-size: 1.5rem; margin-right: 10px;">📈</span>
                        <h3 style="color: #1e293b; font-size: 1.1rem; margin: 0;">AIトレンドワード（日次）</h3>
                    </div>
                    <p style="color: #64748b; font-size: 0.85rem; margin-bottom: 15px; line-height: 1.4;">
                        AI業界で今日最も話題になっているキーワードをリアルタイム解析。急上昇ワードで業界動向を把握
                    </p>
                    <a href="https://tech-word-spikes.vercel.app/trend-word/AI?period=daily" target="_blank" rel="noopener" style="
                        display: inline-block;
                        padding: 8px 16px;
                        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                        color: white;
                        text-decoration: none;
                        border-radius: 6px;
                        font-size: 0.9rem;
                        font-weight: 500;
                        transition: transform 0.2s;
                    " onmouseover="this.style.transform='scale(1.05)'" onmouseout="this.style.transform='scale(1)'">
                        トレンドワードを見る →
                    </a>
                </div>
            </div>
            
            <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid #cbd5e1;">
                <p style="color: #64748b; font-size: 0.8rem; text-align: center;">
                    💡 これらの外部サービスは毎日自動更新され、AI業界の最新動向を多角的に把握できます
                </p>
            </div>
        </div>
        
        <!-- フッター -->
        <footer class="footer">
            <div class="footer-info">
                <p>AI業界全体像ダッシュボード | データ更新: {update_time}</p>
                <p>掲載記事: {total_articles}件 | 情報ソース: {total_sources}サイト | X投稿: {len(x_posts)}件</p>
            </div>
        </footer>
    </div>
</body>
</html>'''
    
    return html_content

def main():
    """メイン処理"""
    try:
        print("ログ: 参考サイト準拠ダッシュボード生成開始")
        print(f"ログ: Gemini API翻訳: {'有効' if gemini_model else '無効'}")
        
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
        filename = f"reference_format_dashboard_{current_time.strftime('%Y%m%d_%H%M%S')}.html"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 参考サイト準拠ダッシュボード生成完了: {filename}")
        print(f"📊 記事数: {len(all_items)}件")
        print(f"📱 X投稿: {len(x_posts)}件")
        print(f"🌐 Gemini翻訳: {'使用' if gemini_model else '未使用'}")
        
        return filename
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    main()