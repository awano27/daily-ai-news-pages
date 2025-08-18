# -*- coding: utf-8 -*-
"""
Daily AI News - static site generator (JST)
- Summaries are translated to Japanese (no API key) using deep-translator.
- Primary engine: GoogleTranslator (unofficial). Fallback: MyMemory (ja-JP).
- Caches translations to _cache/translations.json to avoid repeated calls.
- Reads RSS list from feeds.yml with categories: Business, Tools, Posts.
- Injects X posts from a CSV file into the 'Posts' category.

Env (optional):
  HOURS_LOOKBACK=24        # Fetch window in hours
  MAX_ITEMS_PER_CATEGORY=8 # Max cards per tab
  TRANSLATE_TO_JA=1        # 1=enable JA summaries, 0=disable
  TRANSLATE_ENGINE=google  # google|mymemory
  X_POSTS_CSV=_sources/x_favorites.csv # Path to X posts CSV
  TZ=Asia/Tokyo            # for timestamps
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
import time
from urllib.parse import urljoin

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

# ---------- config ----------
HOURS_LOOKBACK = int(os.getenv("HOURS_LOOKBACK", "24"))
MAX_ITEMS_PER_CATEGORY = int(os.getenv("MAX_ITEMS_PER_CATEGORY", "8"))
TRANSLATE_TO_JA = os.getenv("TRANSLATE_TO_JA", "1") == "1"
TRANSLATE_ENGINE = os.getenv("TRANSLATE_ENGINE", "google").lower()
# Google Sheets CSV URL for live X posts data
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
X_POSTS_CSV = os.getenv("X_POSTS_CSV", GOOGLE_SHEETS_URL)

JST = timezone(timedelta(hours=9))
NOW = datetime.now(JST)

CACHE_DIR = Path("_cache")
CACHE_DIR.mkdir(exist_ok=True)
CACHE_FILE = CACHE_DIR / "translations.json"

def load_cache():
    try:
        if CACHE_FILE.exists():
            return json.loads(CACHE_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}

def save_cache(cache):
    try:
        CACHE_DIR.mkdir(exist_ok=True)
        CACHE_FILE.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding="utf-8")
    except Exception:
        pass

def advanced_feed_fetch(url, name):
    """高度なHTTPリクエストでフィード取得 - Google News 403エラー対策"""
    
    # 複数のUser-Agentを用意
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/121.0'
    ]
    
    for i, user_agent in enumerate(user_agents):
        try:
            print(f"[INFO] Advanced fetch attempt {i+1}/{len(user_agents)} for {name}")
            
            # セッションを作成して詳細ヘッダーを設定
            session = requests.Session()
            session.headers.update({
                'User-Agent': user_agent,
                'Accept': 'application/rss+xml, application/xml, text/xml, */*',
                'Accept-Language': 'ja,en-US;q=0.9,en;q=0.8',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Cache-Control': 'max-age=0'
            })
            
            # Google NewsまたはGoogle系のURLの場合、追加のヘッダーを設定
            if 'google.com' in url or 'news.google.com' in url:
                session.headers.update({
                    'Referer': 'https://news.google.com/',
                    'Origin': 'https://news.google.com',
                    'Sec-Fetch-User': '?1'
                })
            
            # Google系サービスの場合、追加の遅延
            if 'google.com' in url:
                delay = random.uniform(2, 5)  # 2-5秒のランダム遅延
                print(f"[INFO] Google service detected, applying {delay:.1f}s delay")
                time.sleep(delay)
            
            # リクエスト実行
            response = session.get(url, timeout=30, allow_redirects=True)
            
            if response.status_code == 200:
                print(f"[SUCCESS] {name} fetched successfully with User-Agent {i+1}")
                # feedparserに渡すためにBytesIOオブジェクトを作成
                import io
                feed_data = io.BytesIO(response.content)
                d = feedparser.parse(feed_data)
                return d
            elif response.status_code == 403:
                print(f"[WARN] 403 Forbidden with User-Agent {i+1} for {name}")
                continue
            else:
                print(f"[WARN] HTTP {response.status_code} with User-Agent {i+1} for {name}")
                continue
                
        except Exception as e:
            print(f"[WARN] Exception with User-Agent {i+1} for {name}: {e}")
            continue
    
    print(f"[ERROR] All advanced fetch attempts failed for {name}")
    
    # 最後の手段: Gemini Web Fetcherを使用
    try:
        from gemini_web_fetcher import GeminiWebFetcher
        fetcher = GeminiWebFetcher()
        if fetcher.analyzer.enabled:
            print(f"[INFO] Trying Gemini Web Fetcher for {name}...")
            news_items = fetcher.fetch_from_problematic_source(url, name)
            if news_items:
                # feedparserライクなオブジェクトを作成
                fake_feed = type('FakeFeed', (), {})()
                fake_feed.entries = []
                
                for item in news_items:
                    entry = type('FakeEntry', (), {})()
                    entry.title = item.get('title', '')
                    entry.summary = item.get('summary', '')
                    entry.link = item.get('url', '#')
                    entry.published_parsed = item.get('_dt', datetime.now()).timetuple()
                    fake_feed.entries.append(entry)
                
                print(f"[SUCCESS] Gemini fetched {len(news_items)} items for {name}")
                return fake_feed
    except ImportError:
        print(f"[WARN] Gemini Web Fetcher not available")
    except Exception as e:
        print(f"[WARN] Gemini Web Fetcher failed: {e}")
    
    return None

# ---------- translation ----------
def looks_japanese(s: str) -> bool:
    if not s:
        return False
    # Hiragana, Katakana, CJK
    return re.search(r"[\u3040-\u30ff\u3400-\u9fff]", s) is not None

class JaTranslator:
    def __init__(self, engine="google"):
        self.engine = engine
        self._gt = None
        self._mm = None
        self.warned = False

    def _google(self, text: str) -> str:
        if self._gt is None:
            from deep_translator import GoogleTranslator
            self._gt = GoogleTranslator(source="auto", target="ja")
        return self._gt.translate(text)

    def _mymemory(self, text: str) -> str:
        # deep-translator >=1.11.0 expects region code 'ja-JP' for MyMemory
        if self._mm is None:
            from deep_translator import MyMemoryTranslator
            self._mm = MyMemoryTranslator(source="en-GB", target="ja-JP")
        return self._mm.translate(text)

    def translate(self, text: str) -> str:
        if not text or looks_japanese(text):
            return text
        try:
            if self.engine == "google":
                try:
                    return self._google(text)
                except Exception:
                    return self._mymemory(text)
            elif self.engine == "mymemory":
                try:
                    return self._mymemory(text)
                except Exception:
                    return self._google(text)
            else:
                # unknown -> google then mymemory
                try:
                    return self._google(text)
                except Exception:
                    return self._mymemory(text)
        except Exception as e:
            if not self.warned:
                print(f"[WARN] translation disabled due to error: {e.__class__.__name__}: {e}")
                self.warned = True
            return text

# ---------- X (Twitter) post injection ----------
def _read_csv_bytes(path_or_url: str) -> bytes:
    if re.match(r'^https?://', path_or_url, re.I):
        with urlopen(path_or_url) as r:
            return r.read()
    with open(path_or_url, 'rb') as f:
        return f.read()

def _extract_x_data_from_csv(raw: bytes) -> list[dict]:
    # 文字コード自動判定(UTF-8 BOM優先→UTF-8→CP932)
    for enc in ('utf-8-sig','utf-8','cp932'):
        try:
            txt = raw.decode(enc)
            break
        except Exception:
            continue
    else:
        txt = raw.decode('utf-8', errors='ignore')

    # CSV形式: "日付", "@ユーザー", "テキスト", "画像URL", "ツイートURL"
    data = []
    try:
        rdr = csv.reader(io.StringIO(txt))
        row_count = 0
        for row in rdr:
            row_count += 1
            if row_count == 1:  # ヘッダー行をスキップ
                continue
                
            if len(row) >= 3:  # 最低3列あれば処理
                date_str = row[0].strip('"').strip() if len(row) > 0 else ""
                username = row[1].strip('"').strip() if len(row) > 1 else ""
                text = row[2].strip('"').strip() if len(row) > 2 else ""
                tweet_url = row[4].strip('"').strip() if len(row) > 4 else ""
                
                # URLがない場合はダミーURLを生成
                if not tweet_url and username:
                    username_clean = username.replace('@', '').replace('"', '')
                    tweet_url = f"https://x.com/{username_clean}/status/example"
                elif not tweet_url:
                    tweet_url = "https://x.com/unknown/status/example"
                
                # 有効なテキストがあれば処理（条件を大幅に緩和）
                if text and len(text.strip()) > 5:  # 5文字以上あれば処理
                    # 日付をパース（複数フォーマットに対応）
                    dt = None
                    # 複数の日付フォーマットを試す
                    date_formats = [
                        "%B %d, %Y at %I:%M%p",  # "August 10, 2025 at 02:41AM"
                        "%B %d, %Y",             # "August 13, 2025"
                        "%Y-%m-%d %H:%M:%S",     # "2025-08-18 14:30:00"
                        "%Y-%m-%d",              # "2025-08-18"
                        "%Y年%m月%d日",           # "2025年8月18日"
                        "%m/%d/%Y",              # "8/18/2025"
                    ]
                    for fmt in date_formats:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            dt = dt.replace(tzinfo=JST)  # JSTとして扱う
                            break
                        except:
                            continue
                    
                    # パースに失敗した場合は現在時刻を使用（投稿を表示させるため）
                    if dt is None:
                        print(f"[WARN] Date parse failed for '{date_str}', using current time")
                        dt = datetime.now(JST)
                    
                    # 常に投稿を追加
                    data.append({
                        'url': tweet_url,
                        'username': username,
                        'text': text,
                        'datetime': dt
                    })
    except Exception as e:
        print(f"[WARN] CSV parsing error: {e}")
        pass

    # 古い形式のフォールバック（URL抽出のみ）
    if not data:
        urls = re.findall(r'https?://(?:x|twitter)\.com/[^\s,"]+', txt)
        for url in urls:
            data.append({
                'url': url,
                'username': '',
                'text': '',
                'datetime': NOW
            })
    
    return data

def _extract_x_urls_from_csv(raw: bytes) -> list[str]:
    # 後方互換性のため
    data = _extract_x_data_from_csv(raw)
    
    # 正規化 & 重複除去（順序維持）
    seen, out = set(), []
    for item in data:
        u = item['url'].replace('x.com/','twitter.com/')  # 正規化
        if u not in seen:
            seen.add(u); out.append(u)
    return out

def _author_from_url(u: str) -> str:
    try:
        p = urlparse(u)
        parts = p.path.strip('/').split('/')
        return '@'+parts[0] if parts and parts[0] else 'X'
    except Exception:
        return 'X'

def gather_x_posts(csv_path: str) -> list[dict]:
    # Check if it's a URL or local file
    is_url = csv_path.startswith('http')
    
    if not is_url and not Path(csv_path).exists():
        print(f"[INFO] X posts CSV not found at: {csv_path}")
        return []
    
    if is_url:
        print(f"[INFO] Loading X posts from Google Sheets: {csv_path}")
    else:
        print(f"[INFO] Loading X posts from local file: {csv_path}")
    items = []
    try:
        raw = _read_csv_bytes(csv_path)
        x_data = _extract_x_data_from_csv(raw)
        print(f"[INFO] Extracted {len(x_data)} X posts from CSV.")
        
        for data in x_data:
            url = data['url']
            username = data['username'] or _author_from_url(url)
            post_date = data['datetime']
            # フルテキストも保持（プレビューとは別に）
            full_text = data['text']
            text_preview = data['text'][:150] + '...' if len(data['text']) > 150 else data['text']
            
            # X投稿は時間フィルター無効化（すべての投稿を含める）
            # if (NOW - post_date) <= timedelta(days=7):  # 時間フィルター無効化
            if True:  # すべての投稿を処理
                items.append({
                    "title": f"Xポスト {username}",
                    "link": url,
                    "_summary": text_preview or "X投稿データ",
                    "_full_text": full_text,  # フルテキストを追加
                    "_source": "X / SNS", 
                    "_dt": post_date,  # 実際の投稿日時を使用
                })
        
        print(f"[INFO] Created {len(items)} X post items (time filter disabled).")
    except Exception as e:
        print(f"[WARN] Failed to process X posts CSV: {e}")
    return items

# ---------- HTML template ----------
PAGE_TMPL = """<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Daily AI News — {updated_title}</title>
  <link rel="stylesheet" href="style.css"/>
</head>
<body>
  <header class="site-header">
    <div class="brand">📰 Daily AI News</div>
    <nav class="nav-links">
      <a href="ai_news_dashboard.html" class="nav-link">📊 ダッシュボード</a>
    </nav>
    <div class="updated">最終更新：{updated_full}</div>
  </header>

  <main class="container">
    <h1 class="page-title">今日の最新AI情報</h1>
    <p class="lead">
        世界のAI業界の最新動向を24時間365日モニタリング。OpenAI、Google、Meta、Anthropicなど主要企業の公式発表から、
        arXiv論文、開発者コミュニティの技術討論まで幅広く収集。ビジネス（資金調達・M&A・戦略提携）、
        テクノロジー（新モデル・API・フレームワーク）、研究（論文・ブレークスルー）の3カテゴリで整理し、
        重要度順にランキング。各記事の要約は日本語に自動翻訳、原文リンクで詳細確認可能。
        エンジニア、研究者、投資家、経営者など、AI業界のプロフェッショナル向けの包括的情報源として、
        直近{lookback}時間の重要ニュースを厳選配信。ダッシュボードでは業界全体像の俯瞰分析も提供。
    </p>

    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-value">{cnt_business}件</div>
        <div class="kpi-label">ビジネスニュース</div>
        <div class="kpi-note">重要度高め</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{cnt_tools}件</div>
        <div class="kpi-label">ツールニュース</div>
        <div class="kpi-note">開発者向け</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{cnt_posts}件</div>
        <div class="kpi-label">SNS/論文ポスト</div>
        <div class="kpi-note">検証系</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">{updated_full}</div>
        <div class="kpi-label">最終更新</div>
        <div class="kpi-note">JST</div>
      </div>
    </section>

    <nav class="tabs" role="tablist">
      <button class="tab active" data-target="#business" aria-selected="true">🏢 ビジネスニュース</button>
      <button class="tab" data-target="#tools" aria-selected="false">⚡ ツールニュース</button>
      <button class="tab" data-target="#posts" aria-selected="false">🧪 SNS/論文ポスト</button>
    </nav>

    <!-- 検索ボックス: タイトルや要約に含まれるキーワードでフィルタリングします -->
    <div class="search-container">
      <input id="searchBox" type="text" placeholder="キーワードで記事を検索..." aria-label="検索" />
    </div>

    {sections}
    <section class="note">
      <p>方針：一次情報（公式ブログ/プレス/論文）を優先。一般ニュースは AI キーワードで抽出。要約は日本語化し、<strong>出典リンクは原文</strong>のまま。</p>
    </section>
  </main>

  <footer class="site-footer">
    <div>Generated by <code>build.py</code> · Timezone: JST</div>
    <div><a href="https://github.com/">Hosted on GitHub Pages</a></div>
  </footer>

  <script>
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(btn => btn.addEventListener('click', () => {{
      tabs.forEach(b => {{ b.classList.remove('active'); b.setAttribute('aria-selected','false'); }});
      btn.classList.add('active'); btn.setAttribute('aria-selected','true');
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
      const target = document.querySelector(btn.dataset.target);
      if (target) target.classList.remove('hidden');
    }}));

    // 検索ボックスの入力に応じてカードをフィルタリングする
    const searchBox = document.getElementById('searchBox');
    if (searchBox) {{
      searchBox.addEventListener('input', () => {{
        const query = searchBox.value.toLowerCase();
        // すべてのカードを対象にキーワードを検索
        document.querySelectorAll('.card').forEach(card => {{
          const titleEl = card.querySelector('.card-title');
          const summaryEl = card.querySelector('.card-summary');
          const title = titleEl ? titleEl.textContent.toLowerCase() : '';
          const summary = summaryEl ? summaryEl.textContent.toLowerCase() : '';
          if (!query || title.includes(query) || summary.includes(query)) {{
            card.style.display = '';
          }} else {{
            card.style.display = 'none';
          }}
        }});
      }});
    }}
  </script>
</body>
</html>
"""

SECTION_TMPL = """
<section id="{sec_id}" class="tab-panel {extra_class}">
{cards}
</section>
"""

CARD_TMPL = """
<article class="card">
  <div class="card-header">
    <a class="card-title" href="{link}" target="_blank" rel="noopener">{title}</a>
  </div>
  <div class="card-body">
    <p class="card-summary">{summary}</p>
    <div class="chips">
      <span class="chip">{source_name}</span>
      <span class="chip ghost">{summary_lang}</span>
      <span class="chip ghost">{ago}</span>
    </div>
  </div>
  <div class="card-footer">
    出典: <a href="{link}" target="_blank" rel="noopener">{link}</a>
  </div>
</article>
"""

EMPTY_TMPL = '<div class="empty">新着なし（期間を広げるかフィードを追加してください）</div>'

def ago_str(dt: datetime) -> str:
    delta = NOW - dt
    secs = int(delta.total_seconds())
    if secs < 60: return f"{secs}秒前"
    mins = secs // 60
    if mins < 60: return f"{mins}分前"
    hrs = mins // 60
    if hrs < 24: return f"{hrs}時間前"
    days = hrs // 24
    return f"{days}日前"

def clean_html(s: str) -> str:
    if not s: return ""
    # strip tags very lightly
    s = re.sub(r"<.*?>", "", s)
    s = s.replace("&nbsp;", " ").strip()
    return html.escape(s, quote=False)

def pick_summary(entry) -> str:
    for key in ("summary", "subtitle", "description"):
        if key in entry and entry[key]:
            return clean_html(entry[key])
    return clean_html(entry.get("title", ""))

def parse_feeds():
    raw = yaml.safe_load(Path("feeds.yml").read_text(encoding="utf-8"))
    return raw or {}

def get_category(conf, category_name):
    """Case-insensitive category lookup"""
    # Try exact match first
    if category_name in conf:
        return conf[category_name]
    # Try case-insensitive match
    for key, value in conf.items():
        if key.lower() == category_name.lower():
            return value
    return []

def categorize_business_news(item, feeds_info):
    """ビジネスニュースをサブカテゴリに分類"""
    business_category = feeds_info.get('business_category', 'general')
    title = item.get('title', '').lower()
    summary = item.get('_summary', '').lower()
    
    # キーワードベースの分類
    if business_category == 'strategy':
        return 'strategy'  # 戦略・経営
    elif business_category == 'investment':
        return 'investment'  # 投資・M&A
    elif business_category == 'japan_business':
        return 'japan_business'  # 日本企業
    elif business_category == 'governance':
        return 'governance'  # 規制・ガバナンス
    else:
        # キーワードで自動分類
        investment_keywords = ['funding', 'investment', 'ipo', 'venture', 'capital', 'm&a', 'acquisition', '投資', '資金調達', 'IPO']
        strategy_keywords = ['strategy', 'executive', 'ceo', 'leadership', 'transformation', '戦略', '経営', 'CEO']
        governance_keywords = ['regulation', 'policy', 'compliance', 'ethics', 'governance', '規制', '政策', 'ガバナンス']
        
        for keyword in investment_keywords:
            if keyword in title or keyword in summary:
                return 'investment'
        for keyword in strategy_keywords:
            if keyword in title or keyword in summary:
                return 'strategy'
        for keyword in governance_keywords:
            if keyword in title or keyword in summary:
                return 'governance'
                
        return 'general'

def within_window(published_parsed):
    if not published_parsed: 
        return True, NOW  # keep if unknown, use current time
    dt = datetime.fromtimestamp(time.mktime(published_parsed), tz=timezone.utc).astimezone(JST)
    return (NOW - dt) <= timedelta(hours=HOURS_LOOKBACK), dt

def is_ai_relevant(title: str, summary: str) -> bool:
    """
    AIに関連性の高いコンテンツかどうかを判定
    より厳格なフィルタリングで質の高いニュースのみを選別
    """
    content = f"{title} {summary}".lower()
    
    # 高関連度キーワード（これらがあれば必ず含める）
    high_relevance = [
        'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
        'gpt', 'llm', 'large language model', 'transformer', 'bert', 'claude',
        'chatgpt', 'gemini', 'copilot', 'anthropic', 'openai', 'deepmind',
        'computer vision', 'natural language processing', 'nlp', 'reinforcement learning',
        'generative ai', 'ai model', 'ai research', 'ai breakthrough',
        '人工知能', '機械学習', 'ディープラーニング', 'ニューラルネット',
                '人工知能', '機械学習', 'ディープラーニング', 'ニューラルネット',
        'ＡＩ', 'AI', 'ML', 'DL', '生成AI', 'ジェネレーティブAI',
        'チャットGPT', 'ChatGPT', 'GPT', 'LLM', '大規模言語モデル',
        'Claude', 'Gemini', 'Copilot', 'Bard',
        '自然言語処理', 'コンピュータビジョン', '画像認識', '音声認識',
        'ロボティクス', '自動運転', '予測分析', 'データサイエンス',
        'アルゴリズム', '最適化', 'レコメンデーション',
        'スタートアップ', '資金調達', '投資', 'ファンド', 'IPO', 'M&A',
        'ソフトバンク', 'トヨタ', 'NTT', 'ソニー', '日立', '富士通', 'NEC',
        'パナソニック', '楽天', 'リクルート', 'メルカリ', 'LINE',
    ]
    
    # 中関連度キーワード（複数あれば含める）
    medium_relevance = [
        'algorithm', 'automation', 'robot', 'autonomous', 'prediction',
        'data science', 'analytics', 'intelligent', 'smart system',
        'cognitive', 'inference', 'classification', 'recognition',
        'generation', 'synthesis', 'optimization', 'recommendation',
        'アルゴリズム', '自動化', 'ロボット', '自律', '予測',
        'データサイエンス', '分析', 'インテリジェント', 'スマート',
        '認識', '生成', '最適化', 'レコメンド'
    ]
    
    # 除外キーワード（これらがあれば除外）
    exclude_keywords = [
        'cryptocurrency', 'crypto', 'blockchain', 'bitcoin', 'nft',
        'gaming', 'game', 'sports', 'entertainment', 'music', 'movie',
        'politics', 'political', 'election', 'government policy',
        'weather', 'climate change', 'environmental',
        '暗号通貨', 'ゲーム', 'スポーツ', '娯楽', '音楽', '映画',
                '暗号通貨', 'ゲーム', 'スポーツ', '娯楽', '音楽', '映画',
        '政治', '選挙', '天気', '気候変動', '環境',
        'アニメ', 'マンガ', '芸能', 'タレント', 'アイドル',
        '恋愛', '結婚', 'グルメ', '料理', '旅行', 'ファッション'
    ]
    
    # 除外キーワードチェック
    for keyword in exclude_keywords:
        if keyword in content:
            return False
    
    # 高関連度キーワードチェック
    high_score = sum(1 for keyword in high_relevance if keyword in content)
    if high_score >= 1:
        return True
    
    # 中関連度キーワードチェック（2つ以上で採用）
    medium_score = sum(1 for keyword in medium_relevance if keyword in content)
    if medium_score >= 2:
        return True
    
    return False


def calculate_importance_score(item):
    """
    ニュースの重要度スコアを計算
    大きなニュースほど高いスコアを返す
    """
    title = item.get("title", "").lower()
    summary = item.get("_summary", "").lower()
    source = item.get("_source", "").lower()
    content = f"{title} {summary}"
    
    score = 0
    
    # 1. 企業・組織の重要度（大手企業ほど高スコア）
    major_companies = {
        'openai': 100, 'anthropic': 100, 'google': 90, 'microsoft': 90,
        'meta': 85, 'nvidia': 85, 'apple': 80, 'amazon': 80,
        'tesla': 75, 'deepmind': 95, 'cohere': 70, 'hugging face': 70,
        'mistral': 65, 'stability ai': 65, 'midjourney': 60
    }
    
    for company, points in major_companies.items():
        if company in content:
            score += points
            break  # 最高スコアのみ適用
    
    # 2. 重要キーワード（画期的な発表ほど高スコア）
    high_impact_keywords = {
        'breakthrough': 80, 'launch': 70, 'release': 65, 'announce': 60,
        'unveil': 75, 'introduce': 60, 'partnership': 55, 'acquisition': 85,
        'funding': 70, 'investment': 65, 'ipo': 90, 'valuation': 60,
        'gpt-5': 100, 'gpt-4': 80, 'claude': 70, 'gemini': 70,
        'billion': 75, 'million': 50, 'record': 65, 'first': 60
    }
    
    for keyword, points in high_impact_keywords.items():
        if keyword in content:
            score += points * 0.5  # 重複を避けるため0.5倍
    
    # 3. ソースの信頼性・影響力
    source_credibility = {
        'techcrunch': 80, 'bloomberg': 90, 'reuters': 85, 'wsj': 85,
        'financial times': 80, 'the verge': 70, 'wired': 70,
        'mit technology review': 85, 'nature': 95, 'science': 95,
        'anthropic': 90, 'openai': 90, 'google': 85, 'meta': 80
    }
    
    for src, points in source_credibility.items():
        if src in source:
            score += points * 0.3  # ソース信頼性は30%の重み
            break
    
    # 4. 技術的重要度
    tech_importance = {
        'artificial general intelligence': 100, 'agi': 100,
        'multimodal': 70, 'reasoning': 60, 'safety': 65,
        'alignment': 70, 'robotics': 60, 'autonomous': 55,
        'quantum': 70, 'neural network': 50, 'transformer': 60
    }
    
    for tech, points in tech_importance.items():
        if tech in content:
            score += points * 0.4
    
    # 5. 新鮮度ボーナス（新しいニュースにボーナス）
    dt = item.get("_dt")
    if dt:
        hours_old = (NOW - dt).total_seconds() / 3600
        if hours_old < 6:  # 6時間以内
            score += 30
        elif hours_old < 12:  # 12時間以内
            score += 20
        elif hours_old < 24:  # 24時間以内
            score += 10
    
    # 6. タイトルの長さ（詳細なタイトルほどニュース価値高い）
    title_length = len(item.get("title", ""))
    if title_length > 80:
        score += 15
    elif title_length > 50:
        score += 10
    
    return max(score, 0)  # 負のスコアは0に

def calculate_sns_importance_score(item):
    """
    SNSポストの重要度スコアを計算（8/14以降の新しい情報用）
    企業アカウント、インフルエンサー、内容の重要度で判定
    """
    title = item.get("title", "").lower()
    summary = item.get("_summary", "").lower()
    username = ""
    
    # ユーザー名を抽出
    if "xポスト" in title:
        username = title.replace("xポスト", "").strip().lower()
    
    content = f"{title} {summary}"
    score = 0
    
    # 1. 企業・組織アカウントの重要度（公式アカウントほど高スコア）
    enterprise_accounts = {
        '@openai': 100, '@anthropic': 100, '@google': 90, '@microsoft': 90,
        '@meta': 85, '@nvidia': 85, '@apple': 80, '@amazon': 80,
        '@deepmind': 95, '@huggingface': 80, '@langchainai': 75,
        '@cohereai': 70, '@stabilityai': 70, '@midjourney': 65,
        # 日本企業アカウント  
        '@softbank': 80, '@toyota': 75, '@nttcom': 70, '@sony': 70,
        '@hitachi_ltd': 65, '@fujitsu_global': 65, '@nec_corp': 65,
        '@rakuten': 60, '@recruit_jp': 55, '@mercari_jp': 50,
        # AI研究者・インフルエンサー
        '@ylecun': 90, '@karpathy': 90, '@jeffdean': 85, '@goodfellow_ian': 85,
        '@elonmusk': 75, '@satyanadella': 80, '@sundarpichai': 80,
        '@sama': 95, '@darioacemoglu': 80, '@fchollet': 85,
        '@hardmaru': 75, '@adcock_brett': 70, '@minimaxir': 65,
        # 日本のAI研究者・インフルエンサー
        '@karaage0703': 70, '@shi3z': 65, '@yukihiko_n': 60,
        '@npaka': 65, '@ohtaman': 60, '@toukubo': 55,
        # その他の著名人
        '@windsurf': 60, '@oikon48': 55, '@godofprompt': 50,
        '@newsfromgoogle': 70, '@suh_sunaneko': 50, '@pop_ikeda': 45
    }
    
    for account, points in enterprise_accounts.items():
        if account in username or account.replace('@', '') in username:
            score += points
            break  # 最高スコアのみ適用
    
    # 2. コンテンツの重要度（技術的な内容ほど高スコア）
    high_value_keywords = {
        'breakthrough': 50, 'release': 40, 'launch': 40, 'announce': 35,
        'gpt-5': 80, 'gpt-4': 60, 'claude': 50, 'gemini': 50,
        'research': 40, 'paper': 35, 'model': 30, 'ai': 20,
        'artificial intelligence': 40, 'machine learning': 35,
        'deep learning': 35, 'neural network': 30,
        # 日本語キーワード
        '人工知能': 35, '機械学習': 30, 'ディープラーニング': 30,
        '生成ai': 45, 'chatgpt': 40, '大規模言語モデル': 35,
        '研究': 30, '論文': 25, 'モデル': 20, 'ブレークスルー': 45,
        '資金調達': 40, '投資': 35, 'スタートアップ': 30
    }
    
    for keyword, points in high_value_keywords.items():
        if keyword in content:
            score += points * 0.3  # 重複を避けるため0.3倍
    
    # 3. エンゲージメント指標
    engagement_indicators = {
        'thread': 15, 'important': 20, 'must read': 25, 'breaking': 30,
        'update': 10, 'new': 15, 'latest': 10, 'just': 10,
        '重要': 20, '必見': 25, '最新': 10, '速報': 30, '更新': 10,
        '解決': 20, 'ついに': 15, '問題': 10
    }
    
    for indicator, points in engagement_indicators.items():
        if indicator in content:
            score += points * 0.2
    
    # 4. 投稿の新鮮度（8/14以降の新しさを重視）
    dt = item.get("_dt")
    if dt:
        aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=JST)
        hours_since_aug14 = (dt - aug14_jst).total_seconds() / 3600
        
        # 8/15の投稿に最高ボーナス
        if hours_since_aug14 >= 24:  # 8/15以降
            score += 30
        elif hours_since_aug14 >= 12:  # 8/14午後
            score += 20
        elif hours_since_aug14 >= 0:  # 8/14朝
            score += 10
    
    # 5. テキスト長ボーナス（詳細な投稿ほど高価値）
    text_length = len(summary)
    if text_length > 100:
        score += 10
    elif text_length > 50:
        score += 5
    
    return max(score, 0)  # 負のスコアは0に

def build_cards(items, translator):
    cards = []
    for it in items[:MAX_ITEMS_PER_CATEGORY]:
        title = it.get("title") or "(no title)"
        link = it.get("link") or "#"
        src  = it.get("_source") or ""
        dt   = it.get("_dt") or NOW
        raw_summary = it.get("_summary") or ""
        ja_summary = raw_summary
        did_translate = False

        if TRANSLATE_TO_JA and translator and raw_summary and not looks_japanese(raw_summary):
            # cache key: stable on link+hash(summary)
            cache_key = f"{link}::{hash(raw_summary)}"
            cached = TRANSLATION_CACHE.get(cache_key)
            if cached:
                ja_summary = cached
                did_translate = True
            else:
                try:
                    ja = translator.translate(raw_summary)
                    if ja and ja != raw_summary:
                        ja_summary = ja
                        TRANSLATION_CACHE[cache_key] = ja_summary
                        did_translate = True
                except Exception as e:
                    print(f"[WARN] Translation failed for {link[:50]}: {e}")

        cards.append(CARD_TMPL.format(
            link=html.escape(link, quote=True),
            title=html.escape(title, quote=False),
            summary=(ja_summary if did_translate else raw_summary),
            source_name=html.escape(src, quote=False),
            summary_lang=("要約: 日本語" if did_translate else "要約: 英語"),
            ago=ago_str(dt),
        ))
    return "\n".join(cards) if cards else EMPTY_TMPL

def gather_items(feeds, category_name):
    items = []
    print(f"[INFO] Processing {len(feeds)} feeds for {category_name}")
    for f in feeds:
        url = f.get("url")
        name = f.get("name", url)
        if not url: 
            print(f"[WARN] No URL for feed: {name}")
            continue
        try:
            print(f"[INFO] Fetching: {name}")
            # User-Agentを設定してアクセス拒否を回避
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
            }
            
            # 403エラー対策: リトライ機能付きでフィード取得
            retry_count = 0
            max_retries = 2
            d = None
            
            while retry_count <= max_retries:
                try:
                    # タイムアウト制限付きでフィード取得
                    import socket
                    original_timeout = socket.getdefaulttimeout()
                    socket.setdefaulttimeout(8)  # 8秒タイムアウト
                    
                    d = feedparser.parse(url, agent=headers['User-Agent'])
                    
                    socket.setdefaulttimeout(original_timeout)
                    # HTTPステータスコードチェック
                    if hasattr(d, 'status') and d.status == 403:
                        print(f"[WARN] 403 Forbidden for {name}, trying advanced fetch...")
                        # 高度なHTTPリクエストで再試行
                        d = advanced_feed_fetch(url, name)
                        if d is None:
                            print(f"[ERROR] Advanced fetch also failed for {name}")
                            break
                    break
                except Exception as retry_e:
                    retry_count += 1
                    if retry_count <= max_retries:
                        print(f"[WARN] Retry {retry_count}/{max_retries} for {name}: {retry_e}")
                        # 高度な取得を試行
                        if 'google.com' in url:
                            print(f"[INFO] Trying advanced fetch for Google service: {name}")
                            d = advanced_feed_fetch(url, name)
                            if d is not None:
                                break
                        import time
                        time.sleep(2)  # 2秒待機
                    else:
                        # 最後の手段として高度な取得を試行
                        print(f"[INFO] Final attempt with advanced fetch for {name}")
                        d = advanced_feed_fetch(url, name)
                        if d is None:
                            raise retry_e
            
            if d and d.bozo:
                print(f"[WARN] Feed parse warning for {name}: {getattr(d, 'bozo_exception', 'unknown')}")
        except Exception as e:
            print(f"[ERROR] feed parse error: {name}: {e}")
            continue
        
        # フィード取得が失敗した場合はスキップ
        if not d or not hasattr(d, 'entries'):
            print(f"[WARN] No valid feed data for {name}, skipping...")
            continue
            
        entry_count = 0
        filtered_count = 0
        for e in d.entries:
            ok, dt = within_window(e.get("published_parsed") or e.get("updated_parsed"))
            if not ok:
                continue
            
            title = e.get("title", "")
            summary = pick_summary(e)
            
            # generalフィードの場合はAI関連度をチェック
            is_general_feed = f.get("general", False)
            if is_general_feed:
                if not is_ai_relevant(title, summary):
                    filtered_count += 1
                    continue
            
            # 403エラーURLをチェック
            link_url = e.get("link", "")
            if is_403_url(link_url):
                print(f"🚫 403 URL除外: {title[:50]}...")
                continue
                
            entry_count += 1
            items.append({
                "title": title,
                "link": link_url,
                "_summary": summary,
                "_source": name,
                "_dt": dt,
            })
        if entry_count > 0:
            if filtered_count > 0:
                print(f"[INFO] Found {entry_count} recent items from {name} (filtered out {filtered_count} non-AI items)")
            else:
                print(f"[INFO] Found {entry_count} recent items from {name}")
    # スマートソート: 重要度と時刻を組み合わせて並び替え
    if category_name == "Business":
        # ビジネスニュースは重要度順でソート
        items.sort(key=lambda x: (calculate_importance_score(x), x["_dt"]), reverse=True)
        print(f"[INFO] {category_name}: Sorted by importance score")
    elif category_name == "Posts":
        # SNS/論文ポストは重要度順でソート
        items.sort(key=lambda x: (calculate_sns_importance_score(x), x["_dt"]), reverse=True)
        print(f"[INFO] {category_name}: Sorted by SNS importance score")
    else:
        # ツールカテゴリは時刻順
        items.sort(key=lambda x: x["_dt"], reverse=True)
    
    # 最終チェック: 403 URLがないことを確認
    items_before_filter = len(items)
    items = filter_403_urls(items)
    items_after_filter = len(items)
    
    if items_before_filter != items_after_filter:
        print(f"✅ {category_name}: 最終フィルターで{items_before_filter - items_after_filter}件の403 URLを除外")
    
    print(f"[INFO] {category_name}: Total {len(items)} items found")
    return items

def main():
    print(f"[INFO] Starting build at {NOW.strftime('%Y-%m-%d %H:%M JST')}")
    print(f"[INFO] HOURS_LOOKBACK={HOURS_LOOKBACK}, MAX_ITEMS_PER_CATEGORY={MAX_ITEMS_PER_CATEGORY}")
    print(f"[INFO] TRANSLATE_TO_JA={TRANSLATE_TO_JA}, TRANSLATE_ENGINE={TRANSLATE_ENGINE}")
    
    global TRANSLATION_CACHE
    TRANSLATION_CACHE = load_cache()
    print(f"[INFO] Loaded {len(TRANSLATION_CACHE)} cached translations")

    try:
        feeds_conf = parse_feeds()
        print(f"[INFO] Loaded {sum(len(v) for v in feeds_conf.values())} feeds from feeds.yml")
    except Exception as e:
        print(f"[ERROR] Failed to parse feeds.yml: {e}")
        feeds_conf = {}
    
    # Gather items with error handling
    try:
        business = gather_items(get_category(feeds_conf, "Business"), "Business")
        print(f"[INFO] Gathered {len(business)} Business items")
    except Exception as e:
        print(f"[ERROR] Failed to gather Business items: {e}")
        business = []
    
    try:
        tools = gather_items(get_category(feeds_conf, "Tools"), "Tools")
        print(f"[INFO] Gathered {len(tools)} Tools items")
    except Exception as e:
        print(f"[ERROR] Failed to gather Tools items: {e}")
        tools = []
    
    try:
        posts = gather_items(get_category(feeds_conf, "Posts"), "Posts")
        print(f"[INFO] Gathered {len(posts)} Posts items")
    except Exception as e:
        print(f"[ERROR] Failed to gather Posts items: {e}")
        posts = []
    
    # Remove global duplicates across all categories first
    print(f"[INFO] Removing duplicates across all categories...")
    all_items = business + tools + posts
    print(f"[INFO] Before deduplication: {len(all_items)} total items")
    
    seen_links = set()
    seen_titles = set()
    unique_business = []
    unique_tools = []
    unique_posts = []
    
    # Process each category and remove duplicates
    for item in business:
        link = item.get('link', '')
        title = item.get('title', '').lower().strip()
        if link not in seen_links and title not in seen_titles:
            unique_business.append(item)
            seen_links.add(link)
            seen_titles.add(title)
    
    for item in tools:
        link = item.get('link', '')
        title = item.get('title', '').lower().strip()
        if link not in seen_links and title not in seen_titles:
            unique_tools.append(item)
            seen_links.add(link)
            seen_titles.add(title)
    
    for item in posts:
        link = item.get('link', '')
        title = item.get('title', '').lower().strip()
        if link not in seen_links and title not in seen_titles:
            unique_posts.append(item)
            seen_links.add(link)
            seen_titles.add(title)
    
    # Update with deduplicated items
    business = unique_business
    tools = unique_tools  
    posts = unique_posts
    
    print(f"[INFO] After deduplication: Business={len(business)}, Tools={len(tools)}, Posts={len(posts)}")
    
    # Inject X posts
    if X_POSTS_CSV:
        try:
            x_posts = gather_x_posts(X_POSTS_CSV)
            if x_posts:
                print(f"[INFO] Adding {len(x_posts)} X posts")
                # Only add X posts that aren't already in posts
                for x_post in x_posts:
                    x_link = x_post.get('link', '')
                    x_title = x_post.get('title', '').lower().strip()
                    if x_link not in seen_links and x_title not in seen_titles:
                        posts.append(x_post)
                        seen_links.add(x_link)
                        seen_titles.add(x_title)
            else:
                print(f"[INFO] No X posts to add")
            posts = sorted(posts, key=lambda x: x.get('_dt', NOW), reverse=True)
        except Exception as e:
            print(f"[WARN] Failed to process X posts: {e}")


    try:
        translator = JaTranslator(engine=TRANSLATE_ENGINE)
    except Exception as e:
        print(f"[WARN] Failed to initialize translator: {e}")
        translator = None

    sections_html = []
    try:
        sections_html.append(SECTION_TMPL.format(
            sec_id="business",
            extra_class="",
            cards=build_cards(business[:MAX_ITEMS_PER_CATEGORY], translator)
        ))
    except Exception as e:
        print(f"[ERROR] Failed to build Business section: {e}")
        sections_html.append(SECTION_TMPL.format(sec_id="business", extra_class="", cards=EMPTY_TMPL))
    
    try:
        sections_html.append(SECTION_TMPL.format(
            sec_id="tools",
            extra_class="hidden",
            cards=build_cards(tools[:MAX_ITEMS_PER_CATEGORY], translator)
        ))
    except Exception as e:
        print(f"[ERROR] Failed to build Tools section: {e}")
        sections_html.append(SECTION_TMPL.format(sec_id="tools", extra_class="hidden", cards=EMPTY_TMPL))
    
    try:
        sections_html.append(SECTION_TMPL.format(
            sec_id="posts",
            extra_class="hidden",
            cards=build_cards(posts[:MAX_ITEMS_PER_CATEGORY], translator)
        ))
    except Exception as e:
        print(f"[ERROR] Failed to build Posts section: {e}")
        sections_html.append(SECTION_TMPL.format(sec_id="posts", extra_class="hidden", cards=EMPTY_TMPL))

    print(f"[INFO] Final counts after limiting to {MAX_ITEMS_PER_CATEGORY} per category:")
    print(f"  Business: {len(business[:MAX_ITEMS_PER_CATEGORY])} items")
    print(f"  Tools: {len(tools[:MAX_ITEMS_PER_CATEGORY])} items")
    print(f"  Posts: {len(posts[:MAX_ITEMS_PER_CATEGORY])} items")
    print(f"[INFO] Total items to display: {len(business[:MAX_ITEMS_PER_CATEGORY]) + len(tools[:MAX_ITEMS_PER_CATEGORY]) + len(posts[:MAX_ITEMS_PER_CATEGORY])}")
    html_out = PAGE_TMPL.format(
        updated_title=NOW.strftime("%Y-%m-%d %H:%M JST"),
        updated_full=NOW.strftime("%Y-%m-%d %H:%M JST"),
        lookback=HOURS_LOOKBACK,
        cnt_business=len(business[:MAX_ITEMS_PER_CATEGORY]),
        cnt_tools=len(tools[:MAX_ITEMS_PER_CATEGORY]),
        cnt_posts=len(posts[:MAX_ITEMS_PER_CATEGORY]),
        sections="".join(sections_html)
    )

    try:
        Path("news_detail.html").write_text(html_out, encoding="utf-8")
        print(f"[SUCCESS] Wrote news_detail.html ({len(html_out)} bytes)")
    except Exception as e:
        print(f"[ERROR] Failed to write news_detail.html: {e}")
        raise
    
    try:
        save_cache(TRANSLATION_CACHE)
        print(f"[SUCCESS] Saved {len(TRANSLATION_CACHE)} translations to cache")
    except Exception as e:
        print(f"[WARN] Failed to save cache: {e}")

if __name__ == "__main__":
    main()
