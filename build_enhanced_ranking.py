# -*- coding: utf-8 -*-
"""
Enhanced Daily AI News - with Engineer-focused Ranking System
既存の豊富な情報量を維持しつつ、エンジニア向けスマートランキングを実装

- 全記事を取得（情報量維持）
- エンジニア関連度スコアリング
- 技術的価値に基づく自動ランキング
- 優先度表示とフィルタリング機能
"""

import os, re, sys, json, time, html, csv, io
from datetime import datetime, timezone, timedelta
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import urlopen
import yaml
import feedparser
import requests
import random

# Enhanced X Processing Integration
try:
    from enhanced_x_processor import EnhancedXProcessor
    ENHANCED_X_AVAILABLE = True
    print("✅ Enhanced X Processor: Integrated")
except ImportError:
    ENHANCED_X_AVAILABLE = False
    print("⚠️ Enhanced X Processor: Using fallback")

# URL フィルター機能をインポート
try:
    from url_filter import filter_403_urls, is_403_url
    print("✅ URL フィルター機能: 有効")
except ImportError:
    print("⚠️ URL フィルター機能: 無効")
    def filter_403_urls(items):
        return items
    def is_403_url(url):
        return False

# 翻訳機能
try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
    TRANSLATE_AVAILABLE = True
    print("✅ 翻訳機能: 利用可能")
except ImportError:
    print("⚠️ 翻訳機能: deep-translator未インストール")
    TRANSLATE_AVAILABLE = False

class EngineerRankingSystem:
    """エンジニア向け記事ランキングシステム"""
    
    # エンジニア関連キーワード（重み付き）
    TECH_KEYWORDS = {
        # 実装・開発関連（高優先度）
        'implementation': {
            'keywords': ['code', 'api', 'sdk', 'library', 'framework', 'tutorial', 'example', 'github', 'implementation', 'coding'],
            'weight': 3.0
        },
        
        # AI/ML技術（高優先度）
        'ai_ml': {
            'keywords': ['pytorch', 'tensorflow', 'huggingface', 'langchain', 'openai', 'anthropic', 'gpt', 'llm', 'transformer', 'neural', 'model', 'training', 'inference'],
            'weight': 2.5
        },
        
        # インフラ・本番環境（中高優先度）
        'infrastructure': {
            'keywords': ['docker', 'kubernetes', 'aws', 'gcp', 'azure', 'production', 'deploy', 'devops', 'mlops', 'scaling'],
            'weight': 2.0
        },
        
        # パフォーマンス（中優先度）
        'performance': {
            'keywords': ['optimization', 'performance', 'benchmark', 'speed', 'latency', 'throughput', 'memory', 'gpu'],
            'weight': 1.8
        },
        
        # 研究・論文（中優先度）
        'research': {
            'keywords': ['paper', 'research', 'arxiv', 'study', 'algorithm', 'method', 'evaluation'],
            'weight': 1.5
        },
        
        # ツール・プラットフォーム（中優先度）
        'tools': {
            'keywords': ['tool', 'platform', 'service', 'database', 'vector', 'embedding', 'search'],
            'weight': 1.3
        }
    }
    
    # ビジネス関連キーワード（低優先度、但し重要なものは除外しない）
    BUSINESS_KEYWORDS = {
        'funding': ['funding', 'investment', 'series', 'valuation'],
        'partnership': ['partnership', 'acquisition', 'merger'],
        'release': ['launch', 'release', 'announce', 'unveil']
    }
    
    # 信頼できるソース（ボーナス）
    TRUSTED_SOURCES = {
        'arxiv.org': 2.0,
        'github.com': 1.8,
        'pytorch.org': 1.8,
        'tensorflow.org': 1.8,
        'huggingface.co': 1.8,
        'openai.com': 1.5,
        'anthropic.com': 1.5,
        'engineering.fb.com': 1.5,
        'ai.googleblog.com': 1.5,
        'deepmind.com': 1.5,
        'research.google.com': 1.3,
        'microsoft.com': 1.3,
        'aws.amazon.com': 1.3
    }
    
    @classmethod
    def calculate_engineer_score(cls, item):
        """エンジニア関連度スコアを計算"""
        title = item.get('title', '').lower()
        summary = item.get('summary', '').lower()
        url = item.get('url', '')
        source = item.get('source', '').lower()
        
        content = f"{title} {summary}".lower()
        score = 0.0
        
        # 技術キーワードスコア
        for category, config in cls.TECH_KEYWORDS.items():
            keywords = config['keywords']
            weight = config['weight']
            
            matches = sum(1 for keyword in keywords if keyword in content)
            if matches > 0:
                # 複数マッチにボーナス（上限あり）
                match_bonus = min(matches * 0.3, 1.0)
                score += weight * (1 + match_bonus)
        
        # ソース信頼度ボーナス
        domain = urlparse(url).netloc.lower()
        for trusted_domain, bonus in cls.TRUSTED_SOURCES.items():
            if trusted_domain in domain:
                score *= bonus
                break
        
        # コード/実装関連の特別ボーナス
        if any(indicator in content for indicator in ['```', 'github.com', 'code example', 'implementation']):
            score *= 1.5
        
        # 数値データ・ベンチマーク（エンジニアが重視）
        if re.search(r'\d+[%x]|\d+ms|\d+gb|\d+fps|benchmark|performance', content):
            score *= 1.3
        
        # 論文・研究（学術的価値）
        if 'arxiv' in url or any(word in content for word in ['paper', 'research', 'study']):
            score *= 1.2
        
        # ビジネス系でも技術的価値があるものは除外しない
        business_score = 0
        for category, keywords in cls.BUSINESS_KEYWORDS.items():
            business_matches = sum(1 for keyword in keywords if keyword in content)
            if business_matches > 0:
                business_score += 0.3
        
        # 純粋なビジネスニュースは重み軽減（ただし完全排除はしない）
        if business_score > 0.5 and score < 2.0:
            score *= 0.7
        
        return min(score, 10.0)  # 最大10点
    
    @classmethod
    def get_priority_level(cls, score):
        """スコアから優先度レベルを判定"""
        if score >= 6.0:
            return "🔥", "hot", "最高優先"
        elif score >= 4.0:
            return "⚡", "high", "高優先"
        elif score >= 2.5:
            return "📖", "medium", "中優先"
        elif score >= 1.0:
            return "📰", "low", "低優先"
        else:
            return "📄", "minimal", "参考"
    
    @classmethod
    def detect_tech_categories(cls, item):
        """記事の技術カテゴリーを検出"""
        content = f"{item.get('title', '')} {item.get('summary', '')}".lower()
        categories = []
        
        # プログラミング言語
        if re.search(r'\b(python|javascript|rust|go|c\+\+|java)\b', content):
            categories.append('Programming')
        
        # AI/ML
        if any(word in content for word in ['ai', 'ml', 'machine learning', 'deep learning', 'neural', 'gpt', 'llm']):
            categories.append('AI/ML')
        
        # インフラ
        if any(word in content for word in ['docker', 'kubernetes', 'aws', 'cloud', 'devops']):
            categories.append('Infrastructure')
        
        # Web開発
        if any(word in content for word in ['web', 'frontend', 'backend', 'api', 'react', 'vue']):
            categories.append('Web Dev')
        
        # データ
        if any(word in content for word in ['data', 'database', 'analytics', 'visualization']):
            categories.append('Data')
        
        return categories[:3]  # 最大3つまで

def load_config():
    """設定を読み込み"""
    config = {
        'HOURS_LOOKBACK': int(os.getenv('HOURS_LOOKBACK', '24')),
        'MAX_ITEMS_PER_CATEGORY': int(os.getenv('MAX_ITEMS_PER_CATEGORY', '25')),  # 増量
        'TRANSLATE_TO_JA': os.getenv('TRANSLATE_TO_JA', '1') == '1',
        'TRANSLATE_ENGINE': os.getenv('TRANSLATE_ENGINE', 'google'),
        'X_POSTS_CSV': os.getenv('X_POSTS_CSV', 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'),
        'TZ': os.getenv('TZ', 'Asia/Tokyo')
    }
    return config

def load_feeds():
    """フィード設定を読み込み"""
    feeds_file = Path('feeds.yml')
    if not feeds_file.exists():
        print(f"⚠️ {feeds_file}が見つかりません。デフォルト設定を使用します。")
        return {
            'Business': ['https://venturebeat.com/ai/feed/'],
            'Tools': ['https://huggingface.co/blog/feed.xml'],
            'Posts': []
        }
    
    with open(feeds_file, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def fetch_and_rank_articles(config, feeds):
    """記事を取得してランキング"""
    all_items = []
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=config['HOURS_LOOKBACK'])
    
    print(f"📰 記事取得開始: {config['HOURS_LOOKBACK']}時間以内")
    
    # RSS フィードから記事取得
    for category, feed_list in feeds.items():
        if category == 'Posts':  # X posts は後で処理
            continue
            
        print(f"📂 カテゴリ: {category}")
        
        for feed_entry in feed_list:
            try:
                # feed_entryが辞書形式（name, url）かURL文字列かを判定
                if isinstance(feed_entry, dict):
                    feed_url = feed_entry.get('url', '')
                    feed_name = feed_entry.get('name', 'Unknown')
                    print(f"  🔄 取得中: {feed_name} - {feed_url}")
                else:
                    feed_url = feed_entry
                    feed_name = get_source_name(feed_url)
                    print(f"  🔄 取得中: {feed_url}")
                
                if not feed_url:
                    continue
                    
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries:
                    pub_date = None
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                    
                    if pub_date and pub_date < cutoff_time:
                        continue
                    
                    item = {
                        'title': entry.get('title', 'No title'),
                        'url': entry.get('link', ''),
                        'summary': clean_html(entry.get('summary', entry.get('description', ''))),
                        'published': pub_date,
                        'source': feed_name if isinstance(feed_entry, dict) else get_source_name(feed_url),
                        'category': category,
                        'is_x_post': False
                    }
                    
                    # スコア計算
                    item['engineer_score'] = EngineerRankingSystem.calculate_engineer_score(item)
                    item['priority_icon'], item['priority_class'], item['priority_text'] = EngineerRankingSystem.get_priority_level(item['engineer_score'])
                    item['tech_categories'] = EngineerRankingSystem.detect_tech_categories(item)
                    
                    all_items.append(item)
                    
            except Exception as e:
                print(f"    ❌ エラー: {e}")
    
    # X posts を追加
    try:
        x_posts = fetch_x_posts(config['X_POSTS_CSV'])
        for post in x_posts:
            post['engineer_score'] = EngineerRankingSystem.calculate_engineer_score(post)
            post['priority_icon'], post['priority_class'], post['priority_text'] = EngineerRankingSystem.get_priority_level(post['engineer_score'])
            post['tech_categories'] = EngineerRankingSystem.detect_tech_categories(post)
        all_items.extend(x_posts)
        print(f"✅ X posts: {len(x_posts)}件追加")
    except Exception as e:
        print(f"❌ X posts取得エラー: {e}")
    
    # 403エラーURLをフィルタリング
    all_items = filter_403_urls(all_items)
    
    # ランキング（エンジニアスコア順）
    all_items.sort(key=lambda x: x['engineer_score'], reverse=True)
    
    print(f"📊 総記事数: {len(all_items)}件")
    print(f"🔥 高優先度（4.0+）: {len([x for x in all_items if x['engineer_score'] >= 4.0])}件")
    print(f"⚡ 中優先度（2.5+）: {len([x for x in all_items if x['engineer_score'] >= 2.5 and x['engineer_score'] < 4.0])}件")
    
    return all_items

def fetch_x_posts(csv_url):
    """X posts を取得"""
    if not csv_url:
        return []
    
    posts = []
    try:
        if ENHANCED_X_AVAILABLE:
            processor = EnhancedXProcessor()
            posts = processor.process_csv_posts(csv_url)
        else:
            # Fallback処理
            response = requests.get(csv_url, timeout=10)
            response.encoding = 'utf-8'
            
            reader = csv.DictReader(io.StringIO(response.text))
            for row in reader:
                if not row.get('content') or not row.get('url'):
                    continue
                
                posts.append({
                    'title': (row.get('content') or '')[:100] + '...',
                    'summary': row.get('content', ''),
                    'url': row.get('url', ''),
                    'published': datetime.now(timezone.utc),
                    'source': 'X (Twitter)',
                    'category': 'Posts',
                    'is_x_post': True
                })
    except Exception as e:
        print(f"X posts取得エラー: {e}")
    
    return posts

def clean_html(text):
    """HTMLタグを除去"""
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return text.strip()

def get_source_name(url):
    """URLからソース名を抽出"""
    domain = urlparse(url).netloc
    domain = domain.replace('www.', '').replace('.com', '').replace('.org', '')
    return domain.title()

def translate_summaries(items, config):
    """要約を翻訳"""
    if not config['TRANSLATE_TO_JA'] or not TRANSLATE_AVAILABLE:
        return
    
    cache_file = Path('_cache/translations.json')
    cache_file.parent.mkdir(exist_ok=True)
    
    # キャッシュ読み込み
    cache = {}
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                cache = json.load(f)
        except:
            cache = {}
    
    # 翻訳エンジン設定
    if config['TRANSLATE_ENGINE'] == 'mymemory':
        translator = MyMemoryTranslator(source='en', target='ja-JP')
    else:
        translator = GoogleTranslator(source='en', target='ja')
    
    translated_count = 0
    for item in items:
        summary = item.get('summary', '')
        if not summary or len(summary) < 10:
            continue
        
        cache_key = f"{config['TRANSLATE_ENGINE']}:{hash(summary)}"
        
        if cache_key in cache:
            item['summary'] = cache[cache_key]
        else:
            try:
                translated = translator.translate(summary)
                item['summary'] = translated
                cache[cache_key] = translated
                translated_count += 1
                
                # レート制限
                if translated_count % 5 == 0:
                    time.sleep(1)
                    
            except Exception as e:
                print(f"翻訳エラー: {e}")
    
    # キャッシュ保存
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"キャッシュ保存エラー: {e}")
    
    print(f"🔤 新規翻訳: {translated_count}件")

def generate_enhanced_html(items, config):
    """エンジニア向け拡張HTMLを生成"""
    
    # カテゴリ別に分類（ランキング順を維持）
    categorized = {}
    for item in items:
        category = item['category']
        if category not in categorized:
            categorized[category] = []
        categorized[category].append(item)
    
    # 統計計算
    total_items = len(items)
    high_priority = len([x for x in items if x['engineer_score'] >= 4.0])
    medium_priority = len([x for x in items if x['engineer_score'] >= 2.5 and x['engineer_score'] < 4.0])
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M JST")
    
    html = f'''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Daily AI News — {now}</title>
  <link rel="stylesheet" href="style_enhanced_ranking.css"/>
</head>
<body>
  <header class="site-header">
    <div class="brand">📰 Daily AI News</div>
    <div class="updated">最終更新：{now}</div>
  </header>

  <main class="container">
    <h1 class="page-title">今日の最新AI情報</h1>
    <p class="lead">
        エンジニア関連度スコアでランキング表示。実装可能性・技術的価値・学習効果を重視した自動ソート。
        高優先度（🔥）、中優先度（⚡📖）、参考情報（📰📄）で分類表示。
    </p>

    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-value">{total_items}件</div>
        <div class="kpi-label">総記事数</div>
        <div class="kpi-note">全情報を保持</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{high_priority}件</div>
        <div class="kpi-label">高優先度記事</div>
        <div class="kpi-note">スコア4.0以上</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{medium_priority}件</div>
        <div class="kpi-label">中優先度記事</div>
        <div class="kpi-note">スコア2.5以上</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{now}</div>
        <div class="kpi-label">最終更新</div>
        <div class="kpi-note">自動更新</div>
      </div>
    </section>

    <!-- フィルタリング機能 -->
    <div class="filter-controls">
      <div class="filter-group">
        <label>優先度フィルター:</label>
        <button class="filter-btn active" data-filter="all">すべて ({total_items})</button>
        <button class="filter-btn" data-filter="hot">🔥 最高優先 ({len([x for x in items if x['engineer_score'] >= 6.0])})</button>
        <button class="filter-btn" data-filter="high">⚡ 高優先 ({len([x for x in items if x['engineer_score'] >= 4.0 and x['engineer_score'] < 6.0])})</button>
        <button class="filter-btn" data-filter="medium">📖 中優先 ({len([x for x in items if x['engineer_score'] >= 2.5 and x['engineer_score'] < 4.0])})</button>
      </div>
      <div class="search-container">
        <input id="searchBox" type="text" placeholder="🔍 技術、企業、キーワードで検索..." />
      </div>
    </div>

    <nav class="tabs" role="tablist">'''
    
    # タブボタン生成
    for i, (category, cat_items) in enumerate(categorized.items()):
        active = 'active' if i == 0 else ''
        icon = get_category_icon(category)
        html += f'''
      <button class="tab {active}" data-target="#{category.lower()}" aria-selected="{str(i==0).lower()}">
        {icon} {category} ({len(cat_items)})
      </button>'''
    
    html += '''
    </nav>

'''
    
    # タブコンテンツ生成
    for i, (category, cat_items) in enumerate(categorized.items()):
        active = 'active' if i == 0 else ''
        html += f'''    <section id="{category.lower()}" class="tab-panel {active}">
'''
        
        for item in cat_items:
            html += generate_enhanced_article_card(item)
        
        html += '''    </section>

'''
    
    html += '''  </main>

  <footer class="site-footer">
    <div class="footer-content">
      <p>© 2025 Daily AI News - Enhanced with Engineer Ranking System</p>
      <p>技術関連度スコアリングによる自動ランキング表示</p>
    </div>
  </footer>

  <script src="script_enhanced_ranking.js"></script>
</body>
</html>'''
    
    return html

def get_category_icon(category):
    """カテゴリーアイコンを取得"""
    icons = {
        'Business': '🏢',
        'Tools': '⚡', 
        'Posts': '🧪',
        'Research': '🔬',
        'Implementation': '⚙️'
    }
    return icons.get(category, '📄')

def generate_enhanced_article_card(item):
    """拡張記事カードを生成"""
    
    # 時間表示
    time_ago = "今"
    if item.get('published'):
        diff = datetime.now(timezone.utc) - item['published']
        hours = int(diff.total_seconds() / 3600)
        if hours >= 24:
            time_ago = f"{hours // 24}日前"
        elif hours > 0:
            time_ago = f"{hours}時間前"
    
    # 技術カテゴリー
    tech_categories = item.get('tech_categories', [])
    tech_tags = ''.join(f'<span class="tech-tag">{cat}</span>' for cat in tech_categories)
    
    # 優先度表示
    priority_icon = item.get('priority_icon', '📄')
    priority_class = item.get('priority_class', 'minimal')
    priority_text = item.get('priority_text', '参考')
    engineer_score = item.get('engineer_score', 0)
    
    # 要約の長さ調整
    summary = item.get('summary', '')
    if len(summary) > 200:
        summary = summary[:197] + '...'
    
    return f'''
<article class="card enhanced-card" data-score="{engineer_score:.1f}" data-priority="{priority_class}">
  <div class="card-header">
    <div class="priority-indicator {priority_class}">
      <span class="priority-icon">{priority_icon}</span>
      <span class="priority-text">{priority_text}</span>
      <span class="score-badge">スコア: {engineer_score:.1f}</span>
    </div>
    <div class="card-meta">
      <span class="meta-time">📅 {time_ago}</span>
      <span class="meta-source">📖 {item.get('source', '')}</span>
    </div>
  </div>
  
  <div class="card-body">
    <a class="card-title" href="{item.get('url', '')}" target="_blank" rel="noopener">
      {item.get('title', 'No title')}
    </a>
    <p class="card-summary">{summary}</p>
    
    <div class="tech-categories">
      {tech_tags}
    </div>
  </div>
  
  <div class="card-footer">
    <div class="card-actions">
      <a href="{item.get('url', '')}" class="action-btn primary" target="_blank">📖 詳細を読む</a>
      <button class="action-btn bookmark" data-url="{item.get('url', '')}">🔖 ブックマーク</button>
    </div>
    <div class="source-link">
      <small>出典: <a href="{item.get('url', '')}" target="_blank">{item.get('url', '')[:50]}...</a></small>
    </div>
  </div>
</article>
'''

def main():
    """メイン処理"""
    print("🚀 Enhanced Daily AI News with Engineer Ranking")
    print("=" * 50)
    
    config = load_config()
    feeds = load_feeds()
    
    print(f"⚙️ 設定: {config['HOURS_LOOKBACK']}時間、最大{config['MAX_ITEMS_PER_CATEGORY']}件/カテゴリ")
    
    # 記事取得とランキング
    items = fetch_and_rank_articles(config, feeds)
    
    # 翻訳処理
    translate_summaries(items, config)
    
    # HTML生成
    html_content = generate_enhanced_html(items, config)
    
    # ファイル出力
    output_file = Path('index.html')
    output_file.write_text(html_content, encoding='utf-8')
    
    print(f"✅ 生成完了: {output_file}")
    print(f"📊 ランキング結果:")
    print(f"   🔥 最高優先度: {len([x for x in items if x['engineer_score'] >= 6.0])}件")
    print(f"   ⚡ 高優先度: {len([x for x in items if x['engineer_score'] >= 4.0 and x['engineer_score'] < 6.0])}件")
    print(f"   📖 中優先度: {len([x for x in items if x['engineer_score'] >= 2.5 and x['engineer_score'] < 4.0])}件")
    print(f"   📰 低優先度: {len([x for x in items if x['engineer_score'] >= 1.0 and x['engineer_score'] < 2.5])}件")
    print(f"   📄 参考: {len([x for x in items if x['engineer_score'] < 1.0])}件")

if __name__ == "__main__":
    main()