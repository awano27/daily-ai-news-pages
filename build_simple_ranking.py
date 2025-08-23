# -*- coding: utf-8 -*-
"""
Simple Enhanced Daily AI News - 確実に動作するランキングシステム
元の build.py をベースに、情報量を維持しつつランキング機能を追加

HTML Structure Fix Applied: 2025-08-23
- Enhanced card template with priority system
- Proper HTML tag structure and closure
- CSS generation included for styling
- Force GitHub Actions to use this updated version
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

# 基本設定
HOURS_LOOKBACK = int(os.getenv('HOURS_LOOKBACK', '24'))
MAX_ITEMS_PER_CATEGORY = int(os.getenv('MAX_ITEMS_PER_CATEGORY', '25'))
TRANSLATE_TO_JA = os.getenv('TRANSLATE_TO_JA', '1') == '1'
TRANSLATE_ENGINE = os.getenv('TRANSLATE_ENGINE', 'google')
X_POSTS_CSV = os.getenv('X_POSTS_CSV', 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0')

# 翻訳機能
try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
    TRANSLATE_AVAILABLE = True
    print("✅ 翻訳機能: 利用可能")
except ImportError:
    print("⚠️ 翻訳機能: deep-translator未インストール")
    TRANSLATE_AVAILABLE = False

class SimpleEngineerRanking:
    """シンプルなエンジニア関連度ランキング"""
    
    # エンジニア重要キーワード（重み付き）
    TECH_KEYWORDS = {
        # 高優先度 (3.0倍)
        'code': 3.0, 'api': 3.0, 'sdk': 3.0, 'github': 3.0, 'implementation': 3.0,
        'tutorial': 3.0, 'framework': 3.0, 'library': 3.0,
        
        # AI/ML (2.5倍)
        'pytorch': 2.5, 'tensorflow': 2.5, 'huggingface': 2.5, 'gpt': 2.5, 
        'llm': 2.5, 'openai': 2.5, 'anthropic': 2.5, 'model': 2.5, 'ai': 2.5,
        
        # インフラ (2.0倍)
        'docker': 2.0, 'kubernetes': 2.0, 'aws': 2.0, 'azure': 2.0, 'gcp': 2.0,
        'deployment': 2.0, 'production': 2.0, 'mlops': 2.0,
        
        # パフォーマンス (1.8倍)
        'performance': 1.8, 'benchmark': 1.8, 'optimization': 1.8, 'speed': 1.8,
        'memory': 1.8, 'gpu': 1.8, 'cuda': 1.8,
        
        # 研究 (1.5倍) 
        'research': 1.5, 'paper': 1.5, 'arxiv': 1.5, 'algorithm': 1.5,
        'method': 1.5, 'evaluation': 1.5
    }
    
    # 信頼できるソース
    TRUSTED_DOMAINS = [
        'arxiv.org', 'github.com', 'pytorch.org', 'tensorflow.org', 
        'huggingface.co', 'openai.com', 'anthropic.com', 'deepmind.com',
        'ai.googleblog.com', 'research.facebook.com'
    ]
    
    @classmethod
    def calculate_score(cls, item):
        """エンジニア関連度スコアを計算 (0-10)"""
        title = item.get('title', '').lower()
        summary = item.get('summary', '').lower()
        url = item.get('url', '').lower()
        
        content = f"{title} {summary}"
        score = 0.0
        
        # キーワードマッチング
        for keyword, weight in cls.TECH_KEYWORDS.items():
            if keyword in content:
                score += weight
                # タイトルにある場合は追加ボーナス
                if keyword in title:
                    score += weight * 0.5
        
        # 信頼できるソースボーナス
        domain = urlparse(url).netloc.lower()
        for trusted in cls.TRUSTED_DOMAINS:
            if trusted in domain:
                score *= 1.3
                break
        
        # コード・実装の特別ボーナス
        if any(indicator in content for indicator in ['```', 'code example', 'implementation', 'github.com']):
            score *= 1.2
            
        # 数値・ベンチマークボーナス
        if re.search(r'\d+[%x]|\d+ms|\d+gb|benchmark', content):
            score *= 1.1
            
        return min(score, 10.0)
    
    @classmethod
    def get_priority(cls, score):
        """スコアから優先度情報を取得"""
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

def load_feeds():
    """フィード設定を読み込み（簡素版）"""
    feeds_file = Path('feeds.yml')
    if not feeds_file.exists():
        # デフォルト設定
        return {
            'Business': [
                'https://venturebeat.com/ai/feed/',
                'https://techcrunch.com/category/artificial-intelligence/feed/',
                'https://www.reddit.com/r/artificial/.rss'
            ],
            'Tools': [
                'https://huggingface.co/blog/feed.xml',
                'https://pytorch.org/blog/rss.xml',
                'https://www.reddit.com/r/MachineLearning/.rss'
            ],
            'Posts': []  # X/Twitter posts + arXiv papers
        }
    
    # 既存のfeeds.ymlを読み込み、URL形式に変換
    with open(feeds_file, 'r', encoding='utf-8') as f:
        feeds_data = yaml.safe_load(f)
    
    processed_feeds = {}
    for category, feed_list in feeds_data.items():
        processed_feeds[category] = []
        for feed_entry in feed_list:
            if isinstance(feed_entry, dict) and 'url' in feed_entry:
                # 無効化されていないもののみ追加
                if not feed_entry.get('disabled', False):
                    processed_feeds[category].append(feed_entry['url'])
            elif isinstance(feed_entry, str):
                processed_feeds[category].append(feed_entry)
    
    return processed_feeds

def fetch_articles():
    """記事を取得してランキング"""
    feeds = load_feeds()
    all_items = []
    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=HOURS_LOOKBACK)
    
    print(f"📰 記事取得開始: {HOURS_LOOKBACK}時間以内、最大{MAX_ITEMS_PER_CATEGORY}件/カテゴリ")
    
    for category, urls in feeds.items():
        if category == 'Posts':
            continue  # X posts + arXiv papersは後で処理
            
        print(f"📂 {category}")
        category_items = []
        
        for url in urls[:10]:  # 最大10フィード/カテゴリ
            try:
                print(f"  🔄 {url}")
                feed = feedparser.parse(url)
                
                for entry in feed.entries[:MAX_ITEMS_PER_CATEGORY]:
                    pub_date = datetime.now(timezone.utc)
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                    
                    if pub_date < cutoff_time:
                        continue
                    
                    item = {
                        'title': entry.get('title', 'No title'),
                        'url': entry.get('link', ''),
                        'summary': clean_text(entry.get('summary', '')),
                        'published': pub_date,
                        'source': get_source_name(url),
                        'category': category,
                        'is_x_post': False
                    }
                    
                    # ランキングスコア計算
                    item['score'] = SimpleEngineerRanking.calculate_score(item)
                    icon, cls, text = SimpleEngineerRanking.get_priority(item['score'])
                    item['priority_icon'] = icon
                    item['priority_class'] = cls  
                    item['priority_text'] = text
                    
                    category_items.append(item)
                    
            except Exception as e:
                print(f"    ❌ エラー: {e}")
        
        # カテゴリ内でスコア順ソート
        category_items.sort(key=lambda x: x['score'], reverse=True)
        all_items.extend(category_items[:MAX_ITEMS_PER_CATEGORY])
    
    # X posts + arXiv papersを追加
    try:
        x_posts = fetch_x_posts()
        arxiv_papers = fetch_arxiv_papers()
        posts_items = x_posts + arxiv_papers
        
        # Posts categoryでスコア順ソート
        for item in posts_items:
            item['category'] = 'Posts'
        posts_items.sort(key=lambda x: x['score'], reverse=True)
        
        all_items.extend(posts_items[:MAX_ITEMS_PER_CATEGORY])
        print(f"✅ X posts: {len(x_posts)}件, arXiv papers: {len(arxiv_papers)}件")
    except Exception as e:
        print(f"❌ Posts取得エラー: {e}")
    
    # 全体でスコア順ソート
    all_items.sort(key=lambda x: x['score'], reverse=True)
    
    print(f"📊 総記事数: {len(all_items)}件")
    high_priority = len([x for x in all_items if x['score'] >= 4.0])
    medium_priority = len([x for x in all_items if x['score'] >= 2.5])
    print(f"🔥 高優先度: {high_priority}件")
    print(f"📖 中優先度: {medium_priority}件")
    
    return all_items

def fetch_x_posts():
    """X postsを取得（簡素版）"""
    if not X_POSTS_CSV:
        return []
        
    posts = []
    try:
        # Enhanced X Processorが利用可能な場合はそれを使用
        try:
            from enhanced_x_processor import EnhancedXProcessor
            processor = EnhancedXProcessor()
            raw_posts = processor.process_x_posts(X_POSTS_CSV, max_posts=15)
            enhanced_posts = processor.convert_to_build_format(raw_posts)
            
            for post in enhanced_posts:
                item = {
                    'title': post.get('title', ''),
                    'summary': post.get('_summary', ''),
                    'url': post.get('link', ''),
                    'published': post.get('_dt', datetime.now(timezone.utc)),
                    'source': 'X (Twitter)',
                    'category': 'Posts',
                    'is_x_post': True
                }
                
                # ランキングスコア計算
                item['score'] = SimpleEngineerRanking.calculate_score(item)
                icon, cls, text = SimpleEngineerRanking.get_priority(item['score'])
                item['priority_icon'] = icon
                item['priority_class'] = cls
                item['priority_text'] = text
                
                posts.append(item)
                
        except ImportError:
            # フォールバック処理
            response = requests.get(X_POSTS_CSV, timeout=10)
            response.encoding = 'utf-8'
            
            reader = csv.DictReader(io.StringIO(response.text))
            for i, row in enumerate(reader):
                if i >= 15:  # 最大15件
                    break
                    
                if not row.get('content'):
                    continue
                    
                item = {
                    'title': (row.get('content', '') or '')[:100] + '...',
                    'summary': row.get('content', ''),
                    'url': row.get('url', ''),
                    'published': datetime.now(timezone.utc),
                    'source': 'X (Twitter)',
                    'category': 'Posts',
                    'is_x_post': True
                }
                
                # ランキングスコア計算
                item['score'] = SimpleEngineerRanking.calculate_score(item)
                icon, cls, text = SimpleEngineerRanking.get_priority(item['score'])
                item['priority_icon'] = icon
                item['priority_class'] = cls
                item['priority_text'] = text
                
                posts.append(item)
            
    except Exception as e:
        print(f"X posts取得失敗: {e}")
        
    return posts

def fetch_arxiv_papers():
    """arXiv論文を取得（AI/ML関連）"""
    papers = []
    arxiv_feeds = [
        'https://arxiv.org/rss/cs.AI',  # Artificial Intelligence
        'https://arxiv.org/rss/cs.LG',  # Machine Learning
        'https://arxiv.org/rss/cs.CL',  # Computation and Language
        'https://arxiv.org/rss/cs.CV',  # Computer Vision
    ]
    
    try:
        for feed_url in arxiv_feeds:
            try:
                print(f"  🔄 arXiv: {feed_url}")
                feed = feedparser.parse(feed_url)
                
                for entry in feed.entries[:5]:  # 最大5件/フィード
                    pub_date = datetime.now(timezone.utc)
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        pub_date = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                    
                    # 24時間以内の論文のみ
                    cutoff_time = datetime.now(timezone.utc) - timedelta(hours=HOURS_LOOKBACK)
                    if pub_date < cutoff_time:
                        continue
                    
                    item = {
                        'title': entry.get('title', 'No title'),
                        'url': entry.get('link', ''),
                        'summary': clean_text(entry.get('summary', '')),
                        'published': pub_date,
                        'source': 'arXiv',
                        'category': 'Posts',
                        'is_x_post': False
                    }
                    
                    # ランキングスコア計算（研究論文なので+1.2倍ボーナス）
                    base_score = SimpleEngineerRanking.calculate_score(item)
                    item['score'] = min(base_score * 1.2, 10.0)  # 研究論文ボーナス
                    icon, cls, text = SimpleEngineerRanking.get_priority(item['score'])
                    item['priority_icon'] = icon
                    item['priority_class'] = cls
                    item['priority_text'] = text
                    
                    papers.append(item)
                    
            except Exception as e:
                print(f"    ❌ arXiv取得エラー: {e}")
                
    except Exception as e:
        print(f"arXiv feeds処理エラー: {e}")
        
    return papers

def translate_items(items):
    """要約を翻訳（キャッシュ付き）"""
    if not TRANSLATE_AVAILABLE or not TRANSLATE_TO_JA:
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
    
    # 翻訳エンジン
    translator = GoogleTranslator(source='en', target='ja')
    translated = 0
    
    for item in items:
        summary = item.get('summary', '')
        if len(summary) < 10:
            continue
            
        cache_key = f"google:{hash(summary)}"
        
        if cache_key in cache:
            item['summary'] = cache[cache_key]
        else:
            try:
                translated_text = translator.translate(summary)
                item['summary'] = translated_text
                cache[cache_key] = translated_text
                translated += 1
                
                if translated % 5 == 0:
                    time.sleep(0.5)  # レート制限
                    
            except Exception as e:
                print(f"翻訳エラー: {e}")
    
    # キャッシュ保存
    try:
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(cache, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"キャッシュ保存エラー: {e}")
    
    print(f"🔤 新規翻訳: {translated}件")

def generate_html(items):
    """HTML生成"""
    # カテゴリ別に分類（スコア順維持）
    categories = {}
    for item in items:
        cat = item['category']
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(item)
    
    # 統計
    total = len(items)
    hot = len([x for x in items if x['score'] >= 6.0])
    high = len([x for x in items if x['score'] >= 4.0 and x['score'] < 6.0])
    medium = len([x for x in items if x['score'] >= 2.5 and x['score'] < 4.0])
    
    now = datetime.now().strftime("%Y-%m-%d %H:%M JST")
    
    html = f'''<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Daily AI News — {now}</title>
  <link rel="stylesheet" href="style.css"/>
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
        豊富な情報量（{total}件）を維持しつつ、重要度で整理表示。
    </p>

    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-value">{total}件</div>
        <div class="kpi-label">総記事数</div>
        <div class="kpi-note">情報量維持</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{hot + high}件</div>
        <div class="kpi-label">高優先度記事</div>
        <div class="kpi-note">スコア4.0以上</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{medium}件</div>
        <div class="kpi-label">中優先度記事</div>
        <div class="kpi-note">スコア2.5以上</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{now}</div>
        <div class="kpi-label">最終更新</div>
        <div class="kpi-note">自動更新</div>
      </div>
    </section>
    
    <div class="filter-controls">
      <div class="filter-group">
        <label>優先度フィルター:</label>
        <button class="filter-btn active" data-filter="all">すべて ({total})</button>
        <button class="filter-btn" data-filter="hot">🔥 最高優先 ({hot})</button>
        <button class="filter-btn" data-filter="high">⚡ 高優先 ({high})</button>
        <button class="filter-btn" data-filter="medium">📖 中優先 ({medium})</button>
      </div>
      <div class="search-container">
        <input id="searchBox" type="text" placeholder="🔍 技術、企業、キーワードで検索..." />
      </div>
    </div>

    <nav class="tabs" role="tablist">'''
    
    # タブ生成
    for i, (cat, cat_items) in enumerate(categories.items()):
        active = 'active' if i == 0 else ''
        icon = get_category_icon(cat)
        html += f'''
      <button class="tab {active}" data-target="#{cat.lower()}" aria-selected="{str(i==0).lower()}">
        {icon} {cat} ({len(cat_items)})
      </button>'''
    
    html += '''
    </nav>

'''
    
    # タブコンテンツ
    for i, (cat, cat_items) in enumerate(categories.items()):
        active = 'active' if i == 0 else ''
        html += f'''    <section id="{cat.lower()}" class="tab-panel {active}">
'''
        
        for item in cat_items:
            html += generate_card_html(item)
        
        html += '''    </section>

'''
    
    html += '''  </main>

  <footer class="site-footer">
    <div class="footer-content">
      <p>© 2025 Daily AI News - Enhanced with Simple Engineer Ranking</p>
      <p>情報量を維持しつつエンジニア向けランキングを実現</p>
    </div>
  </footer>

  <script>
    // タブ切り替え機能
    document.addEventListener('DOMContentLoaded', function() {
      const tabs = document.querySelectorAll('.tab');
      const panels = document.querySelectorAll('.tab-panel');
      
      tabs.forEach(tab => {
        tab.addEventListener('click', function() {
          // すべてのタブとパネルをリセット
          tabs.forEach(t => {
            t.classList.remove('active');
            t.setAttribute('aria-selected', 'false');
          });
          panels.forEach(p => {
            p.classList.remove('active');
          });
          
          // クリックされたタブをアクティブに
          this.classList.add('active');
          this.setAttribute('aria-selected', 'true');
          
          // 対応するパネルをアクティブに
          const targetId = this.getAttribute('data-target');
          const targetPanel = document.querySelector(targetId);
          if (targetPanel) {
            targetPanel.classList.add('active');
          }
        });
      });
      
      // フィルタ機能
      const searchBox = document.getElementById('searchBox');
      const filterBtns = document.querySelectorAll('.filter-btn');
      
      if (searchBox) {
        searchBox.addEventListener('input', function() {
          filterCards();
        });
      }
      
      filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
          filterBtns.forEach(b => b.classList.remove('active'));
          this.classList.add('active');
          filterCards();
        });
      });
      
      function filterCards() {
        const query = searchBox ? searchBox.value.toLowerCase() : '';
        const activeFilter = document.querySelector('.filter-btn.active');
        const filterType = activeFilter ? activeFilter.getAttribute('data-filter') : 'all';
        const activePanel = document.querySelector('.tab-panel.active');
        
        if (activePanel) {
          const cards = activePanel.querySelectorAll('.card');
          cards.forEach(card => {
            const title = card.querySelector('.card-title');
            const summary = card.querySelector('.card-summary');
            const titleText = title ? title.textContent.toLowerCase() : '';
            const summaryText = summary ? summary.textContent.toLowerCase() : '';
            
            const matchesSearch = !query || titleText.includes(query) || summaryText.includes(query);
            
            let matchesFilter = true;
            if (filterType !== 'all') {
              const priority = card.getAttribute('data-priority') || '';
              matchesFilter = priority === filterType;
            }
            
            if (matchesSearch && matchesFilter) {
              card.style.display = '';
            } else {
              card.style.display = 'none';
            }
          });
        }
      }
    });
  </script>
</body>
</html>'''
    
    return html

def generate_card_html(item):
    """記事カードHTML生成（SNS/論文対応）"""
    time_ago = format_time_ago(item.get('published', datetime.now(timezone.utc)))
    
    # 要約を適切な長さに調整
    summary = item.get('summary', '')
    if len(summary) > 200:
        summary = summary[:197] + '...'
    
    # Posts（SNS/論文）特有の表示
    post_type_indicator = ""
    if item.get('category') == 'Posts':
        if item.get('is_x_post', False):
            post_type_indicator = '<span class="post-type-badge twitter">🐦 Twitter</span>'
        elif 'arxiv' in item.get('source', '').lower():
            post_type_indicator = '<span class="post-type-badge arxiv">📑 arXiv</span>'
    
    return f'''
<article class="card enhanced-card" data-score="{item.get('score', 0):.1f}" data-priority="{item.get('priority_class', 'minimal')}">
  <div class="card-header">
    <div class="priority-indicator {item.get('priority_class', 'minimal')}">
      <span class="priority-icon">{item.get('priority_icon', '📄')}</span>
      <span class="priority-text">{item.get('priority_text', '参考')}</span>
      <span class="score-badge">スコア: {item.get('score', 0):.1f}</span>
    </div>
    <div class="card-meta">
      <span class="meta-time">📅 {time_ago}</span>
      <span class="meta-source">📖 {item.get('source', '')}</span>
      {post_type_indicator}
    </div>
  </div>
  
  <div class="card-body">
    <a class="card-title" href="{item.get('url', '')}" target="_blank" rel="noopener">
      {item.get('title', 'No title')}
    </a>
    <p class="card-summary">{summary}</p>
  </div>
  
  <div class="card-footer">
    <div class="card-actions">
      <a href="{item.get('url', '')}" class="action-btn primary" target="_blank">📖 詳細を読む</a>
      <button class="action-btn bookmark" data-url="{item.get('url', '')}">🔖 ブックマーク</button>
    </div>
  </div>
</article>
'''

# ユーティリティ関数
def clean_text(text):
    """テキストクリーニング"""
    if not text:
        return ''
    text = re.sub(r'<[^>]+>', '', text)
    text = html.unescape(text)
    return text.strip()

def get_source_name(url):
    """URLからソース名抽出"""
    domain = urlparse(url).netloc
    return domain.replace('www.', '').replace('.com', '').replace('.org', '').title()

def get_category_icon(category):
    """カテゴリアイコン"""
    icons = {
        'Business': '🏢', 
        'Tools': '⚡', 
        'Posts': '🧪'  # SNS/論文ポスト
    }
    return icons.get(category, '📄')

def format_time_ago(dt):
    """相対時間表示"""
    if not dt:
        return "不明"
    diff = datetime.now(timezone.utc) - dt
    hours = int(diff.total_seconds() / 3600)
    if hours < 1:
        return "今"
    elif hours < 24:
        return f"{hours}時間前"
    else:
        return f"{hours // 24}日前"

def generate_css():
    """CSSファイルを生成"""
    css_content = '''/* Digital.gov compliance deployed at 2025-08-20 23:07:20 JST */
:root{
  /* Digital.gov準拠: WCAG AAA対応カラーシステム */
  --fg:#0f172a; --bg:#ffffff; --muted:#475569; --line:#e2e8f0;
  --brand:#1e40af; --brand-weak:#f1f5f9; --chip:#f8fafc;
  --brand-hover:#1e3a8a; --brand-light:#bfdbfe; --brand-dark:#1e3a8a;
  --success:#15803d; --warning:#ca8a04; --danger:#dc2626;
  --info:#0369a1; --neutral:#64748b;
  
  /* 段階的背景色（彩度を下げた背景） */
  --bg-subtle:#f8fafc; --bg-muted:#f1f5f9; --bg-emphasis:#e2e8f0;
  
  /* グラデーション（彩度調整済み） */
  --gradient:linear-gradient(135deg, #1e40af 0%, #1e3a8a 100%);
  --gradient-subtle:linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
  
  /* シャドウ */
  --shadow:0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg:0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  
  /* レイアウト変数 */
  --border-radius: 12px;
  --spacing-xs: 4px; --spacing-sm: 8px; --spacing-md: 16px; 
  --spacing-lg: 24px; --spacing-xl: 32px; --spacing-2xl: 48px;
  
  /* タイポグラフィ */
  --font-size-xs: 12px; --font-size-sm: 14px; --font-size-base: 16px;
  --font-size-lg: 18px; --font-size-xl: 20px; --font-size-2xl: 24px;
  --font-size-3xl: 32px; --font-size-4xl: 36px;
  
  /* フォーカス表示 */
  --focus-ring: 0 0 0 3px rgba(59, 130, 246, 0.5);
  --focus-ring-offset: 2px;
}
*{box-sizing:border-box}
body{
  margin:0;
  background:var(--bg);
  color:var(--fg);
  font-family:system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,'Noto Sans JP',sans-serif;
  font-size:var(--font-size-base);
  line-height:1.6;
  scroll-behavior:smooth;
}
.container{
  max-width:1000px;
  margin:0 auto;
  padding:var(--spacing-lg) var(--spacing-md);
  display:flex;
  flex-direction:column;
  gap:var(--spacing-lg);
}

/* ヘッダー */
.site-header{
  display:flex;
  justify-content:space-between;
  align-items:center;
  padding:var(--spacing-md);
  background:var(--bg-subtle);
  border-bottom:1px solid var(--line);
  margin-bottom:var(--spacing-lg);
}
.brand{
  font-size:var(--font-size-xl);
  font-weight:700;
  color:var(--brand);
}
.updated{
  color:var(--muted);
  font-size:var(--font-size-sm);
}

/* タイトル */
.page-title{
  font-size:var(--font-size-3xl);
  font-weight:700;
  margin:0 0 var(--spacing-md) 0;
  text-align:center;
  background:var(--gradient);
  -webkit-background-clip:text;
  -webkit-text-fill-color:transparent;
  background-clip:text;
}
.lead{
  font-size:var(--font-size-lg);
  color:var(--muted);
  text-align:center;
  margin-bottom:var(--spacing-xl);
  line-height:1.7;
}

/* KPI Grid */
.kpi-grid{
  display:grid;
  grid-template-columns:repeat(auto-fit, minmax(200px, 1fr));
  gap:var(--spacing-md);
  margin-bottom:var(--spacing-xl);
}
.kpi-card{
  background:var(--bg-subtle);
  padding:var(--spacing-md);
  border-radius:var(--border-radius);
  text-align:center;
  border:1px solid var(--line);
}
.kpi-value{
  font-size:var(--font-size-2xl);
  font-weight:700;
  color:var(--brand);
}
.kpi-label{
  font-size:var(--font-size-sm);
  color:var(--muted);
  margin-top:var(--spacing-xs);
}
.kpi-note{
  font-size:var(--font-size-xs);
  color:var(--neutral);
  margin-top:var(--spacing-xs);
}

/* タブ */
.tabs{
  display:flex;
  border-bottom:2px solid var(--line);
  margin-bottom:var(--spacing-lg);
  gap:var(--spacing-sm);
}
.tab{
  background:none;
  border:none;
  padding:var(--spacing-md) var(--spacing-lg);
  font-size:var(--font-size-base);
  cursor:pointer;
  border-bottom:3px solid transparent;
  transition:all 0.3s ease;
  color:var(--muted);
}
.tab.active{
  color:var(--brand);
  border-bottom-color:var(--brand);
  font-weight:600;
}
.tab:hover{
  color:var(--brand-hover);
  background:var(--bg-subtle);
  border-radius:var(--border-radius) var(--border-radius) 0 0;
}

/* タブパネル */
.tab-panel{
  display:block;
}
.tab-panel.hidden{
  display:none;
}

/* 検索・フィルター */
.search-container{
  margin-bottom:var(--spacing-lg);
}
.search-header{
  display:flex;
  flex-direction:column;
  gap:var(--spacing-sm);
  margin-bottom:var(--spacing-md);
}
#searchBox{
  padding:var(--spacing-md);
  border:1px solid var(--line);
  border-radius:var(--border-radius);
  font-size:var(--font-size-base);
  width:100%;
}
#searchBox:focus{
  outline:none;
  border-color:var(--brand);
  box-shadow:var(--focus-ring);
}
.search-info{
  font-size:var(--font-size-sm);
  color:var(--muted);
  text-align:center;
}
.filter-controls{
  display:flex;
  gap:var(--spacing-sm);
  flex-wrap:wrap;
}
.filter-controls select{
  padding:var(--spacing-sm) var(--spacing-md);
  border:1px solid var(--line);
  border-radius:var(--border-radius);
  background:var(--bg);
}

/* カード */
.card{
  background:var(--bg);
  border:1px solid var(--line);
  border-radius:var(--border-radius);
  margin-bottom:var(--spacing-md);
  overflow:hidden;
  box-shadow:var(--shadow);
  transition:all 0.3s ease;
}
.card:hover{
  box-shadow:var(--shadow-lg);
  transform:translateY(-2px);
}
.card-header{
  padding:var(--spacing-md);
  background:var(--bg-subtle);
  border-bottom:1px solid var(--line);
}
.card-title{
  font-size:var(--font-size-lg);
  font-weight:600;
  color:var(--brand);
  text-decoration:none;
  display:block;
  line-height:1.4;
}
.card-title:hover{
  color:var(--brand-hover);
  text-decoration:underline;
}
.card-body{
  padding:var(--spacing-md);
}
.card-summary{
  color:var(--fg);
  line-height:1.6;
  margin:0 0 var(--spacing-md) 0;
}
.card-footer{
  padding:var(--spacing-md);
  background:var(--bg-muted);
  border-top:1px solid var(--line);
  font-size:var(--font-size-sm);
  color:var(--muted);
}
.card-footer a{
  color:var(--brand);
  text-decoration:none;
}
.card-footer a:hover{
  text-decoration:underline;
}

/* チップ */
.chips{
  display:flex;
  gap:var(--spacing-sm);
  flex-wrap:wrap;
}
.chip{
  background:var(--chip);
  color:var(--brand);
  padding:var(--spacing-xs) var(--spacing-sm);
  border-radius:var(--border-radius);
  font-size:var(--font-size-xs);
  border:1px solid var(--line);
}
.chip.ghost{
  background:transparent;
  color:var(--muted);
}

/* フッター */
.site-footer{
  margin-top:var(--spacing-2xl);
  padding:var(--spacing-lg);
  background:var(--bg-subtle);
  border-top:1px solid var(--line);
  text-align:center;
  font-size:var(--font-size-sm);
  color:var(--muted);
}
.site-footer a{
  color:var(--brand);
  text-decoration:none;
}
.site-footer a:hover{
  text-decoration:underline;
}

/* ノート */
.note{
  background:var(--bg-emphasis);
  border:1px solid var(--line);
  border-radius:var(--border-radius);
  padding:var(--spacing-md);
  margin-top:var(--spacing-xl);
  font-size:var(--font-size-sm);
  color:var(--muted);
  text-align:center;
}

/* レスポンシブ */
@media (max-width: 768px) {
  .container{
    padding:var(--spacing-md) var(--spacing-sm);
  }
  .site-header{
    flex-direction:column;
    gap:var(--spacing-sm);
    text-align:center;
  }
  .tabs{
    flex-direction:column;
  }
  .tab{
    border-bottom:none;
    border-left:3px solid transparent;
  }
  .tab.active{
    border-left-color:var(--brand);
    background:var(--bg-subtle);
  }
  .kpi-grid{
    grid-template-columns:1fr;
  }
  .filter-controls{
    flex-direction:column;
  }
  .chips{
    justify-content:center;
  }
}

/* アクセシビリティ */
.tab:focus{
  outline:none;
  box-shadow:var(--focus-ring);
}
#searchBox:focus{
  outline:none;
  box-shadow:var(--focus-ring);
}
.card-title:focus{
  outline:none;
  box-shadow:var(--focus-ring);
}'''
    
    return css_content

def main():
    """メイン処理"""
    print("🚀 Simple Enhanced Daily AI News")
    print("=" * 40)
    print(f"⚙️ {HOURS_LOOKBACK}時間、最大{MAX_ITEMS_PER_CATEGORY}件/カテゴリ")
    
    # 記事取得
    items = fetch_articles()
    
    # 翻訳
    translate_items(items)
    
    # HTML生成
    html_content = generate_html(items)
    
    # ファイル出力
    output_file = Path('index.html')
    output_file.write_text(html_content, encoding='utf-8')
    
    # CSS生成
    css_content = generate_css()
    css_file = Path('style.css')
    css_file.write_text(css_content, encoding='utf-8')
    print("✅ CSS file generated")
    
    print(f"✅ 生成完了: {output_file}")
    print("📊 ランキング完了")

if __name__ == "__main__":
    main()