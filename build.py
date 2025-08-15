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
        for row in rdr:
            if len(row) >= 5:
                date_str = row[0].strip('"')
                username = row[1].strip('"')
                text = row[2].strip('"')
                tweet_url = row[4].strip('"')
                
                # URLがX/Twitterのものかチェック
                if re.match(r'https?://(?:x|twitter)\.com/', tweet_url):
                    # 日付をパース（複数フォーマットに対応）
                    dt = None
                    # 複数の日付フォーマットを試す
                    date_formats = [
                        "%B %d, %Y at %I:%M%p",  # "August 10, 2025 at 02:41AM"
                        "%B %d, %Y"               # "August 13, 2025"
                    ]
                    for fmt in date_formats:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            dt = dt.replace(tzinfo=JST)  # JSTとして扱う
                            break
                        except:
                            continue
                    
                    # パースに失敗した場合はスキップ（現在時刻にしない）
                    if dt is None:
                        continue
                    
                    if dt is not None:  # 日付が正しくパースできた場合のみ追加
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
            text_preview = data['text'][:50] + '...' if len(data['text']) > 50 else data['text']
            
                        # 8/14以降の投稿のみ含める
            aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=JST)
            if post_date >= aug14_jst and (NOW - post_date) <= timedelta(hours=HOURS_LOOKBACK):
                items.append({
                    "title": f"Xポスト {username}",
                    "link": url,
                    "_summary": text_preview or "手動で「いいね」したポストから自動抽出（要約なし）",
                    "_source": "X / SNS", 
                    "_dt": post_date,  # 実際の投稿日時を使用
                })
        
        print(f"[INFO] Created {len(items)} X post items (filtered to last {HOURS_LOOKBACK} hours).")
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
    <p class="lead">ビジネスニュース・ツール情報・SNS/論文ポストに分け、直近{lookback}時間の更新を配信します。ソースは原文、要約のみ日本語化。</p>

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
        'ＡＩ', 'AI', 'ML', 'DL'
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
        '政治', '選挙', '天気', '気候変動', '環境'
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
            d = feedparser.parse(url)
            if d.bozo:
                print(f"[WARN] Feed parse warning for {name}: {getattr(d, 'bozo_exception', 'unknown')}")
        except Exception as e:
            print(f"[ERROR] feed parse error: {name}: {e}")
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
            
            entry_count += 1
            items.append({
                "title": title,
                "link": e.get("link", ""),
                "_summary": summary,
                "_source": name,
                "_dt": dt,
            })
        if entry_count > 0:
            if filtered_count > 0:
                print(f"[INFO] Found {entry_count} recent items from {name} (filtered out {filtered_count} non-AI items)")
            else:
                print(f"[INFO] Found {entry_count} recent items from {name}")
    # sort by time desc
    items.sort(key=lambda x: x["_dt"], reverse=True)
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
    
    # Inject X posts
    if X_POSTS_CSV:
        try:
            x_posts = gather_x_posts(X_POSTS_CSV)
            if x_posts:
                print(f"[INFO] Adding {len(x_posts)} X posts")
                posts.extend(x_posts)
            else:
                print(f"[INFO] No X posts to add")
            # Remove duplicates and sort again
            seen_links = set()
            unique_posts = []
            for post in posts:
                if post.get('link') and post['link'] not in seen_links:
                    unique_posts.append(post)
                    seen_links.add(post['link'])
            posts = sorted(unique_posts, key=lambda x: x.get('_dt', NOW), reverse=True)
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
        Path("index.html").write_text(html_out, encoding="utf-8")
        print(f"[SUCCESS] Wrote index.html ({len(html_out)} bytes)")
    except Exception as e:
        print(f"[ERROR] Failed to write index.html: {e}")
        raise
    
    try:
        save_cache(TRANSLATION_CACHE)
        print(f"[SUCCESS] Saved {len(TRANSLATION_CACHE)} translations to cache")
    except Exception as e:
        print(f"[WARN] Failed to save cache: {e}")

if __name__ == "__main__":
    main()
