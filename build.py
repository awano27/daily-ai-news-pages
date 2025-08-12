# -*- coding: utf-8 -*-
"""
Daily AI News - static site generator (JST)
- Summaries are translated to Japanese (no API key) using deep-translator.
- Primary engine: GoogleTranslator (unofficial). Fallback: MyMemory (ja-JP).
- Caches translations to _cache/translations.json to avoid repeated calls.
- Reads RSS list from feeds.yml with categories: Business, Tools, Posts.

Env (optional):
  HOURS_LOOKBACK=24        # Fetch window in hours
  MAX_ITEMS_PER_CATEGORY=8 # Max cards per tab
  TRANSLATE_TO_JA=1        # 1=enable JA summaries, 0=disable
  TRANSLATE_ENGINE=google  # google|mymemory
  TZ=Asia/Tokyo            # for timestamps
"""
import os, re, sys, json, time, html
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml
import feedparser

# ---------- config ----------
HOURS_LOOKBACK = int(os.getenv("HOURS_LOOKBACK", "24"))
MAX_ITEMS_PER_CATEGORY = int(os.getenv("MAX_ITEMS_PER_CATEGORY", "8"))
TRANSLATE_TO_JA = os.getenv("TRANSLATE_TO_JA", "1") == "1"
TRANSLATE_ENGINE = os.getenv("TRANSLATE_ENGINE", "google").lower()

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

def within_window(published_parsed):
    if not published_parsed: 
        return True  # keep if unknown
    dt = datetime.fromtimestamp(time.mktime(published_parsed), tz=timezone.utc).astimezone(JST)
    return (NOW - dt) <= timedelta(hours=HOURS_LOOKBACK), dt

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

        if TRANSLATE_TO_JA and raw_summary and not looks_japanese(raw_summary):
            # cache key: stable on link+hash(summary)
            cache_key = f"{link}::{hash(raw_summary)}"
            cached = TRANSLATION_CACHE.get(cache_key)
            if cached:
                ja_summary = cached
                did_translate = True
            else:
                ja = translator.translate(raw_summary)
                if ja and ja != raw_summary:
                    ja_summary = ja
                    TRANSLATION_CACHE[cache_key] = ja_summary
                    did_translate = True

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
    for f in feeds:
        url = f.get("url")
        name = f.get("name", url)
        if not url: 
            continue
        try:
            d = feedparser.parse(url)
        except Exception as e:
            print(f"[WARN] feed parse error: {name}: {e}")
            continue
        for e in d.entries:
            ok, dt = within_window(e.get("published_parsed") or e.get("updated_parsed"))
            if not ok:
                continue
            items.append({
                "title": e.get("title", ""),
                "link": e.get("link", ""),
                "_summary": pick_summary(e),
                "_source": name,
                "_dt": dt,
            })
    # sort by time desc
    items.sort(key=lambda x: x["_dt"], reverse=True)
    return items

def main():
    global TRANSLATION_CACHE
    TRANSLATION_CACHE = load_cache()

    feeds_conf = parse_feeds()
    business = gather_items(feeds_conf.get("Business", []), "Business")
    tools    = gather_items(feeds_conf.get("Tools", []), "Tools")
    posts    = gather_items(feeds_conf.get("Posts", []), "Posts")

    translator = JaTranslator(engine=TRANSLATE_ENGINE)

    sections_html = []
    sections_html.append(SECTION_TMPL.format(
        sec_id="business",
        extra_class="",
        cards=build_cards(business, translator)
    ))
    sections_html.append(SECTION_TMPL.format(
        sec_id="tools",
        extra_class="hidden",
        cards=build_cards(tools, translator)
    ))
    sections_html.append(SECTION_TMPL.format(
        sec_id="posts",
        extra_class="hidden",
        cards=build_cards(posts, translator)
    ))

    html_out = PAGE_TMPL.format(
        updated_title=NOW.strftime("%Y-%m-%d %H:%M JST"),
        updated_full=NOW.strftime("%Y-%m-%d %H:%M JST"),
        lookback=HOURS_LOOKBACK,
        cnt_business=len(business[:MAX_ITEMS_PER_CATEGORY]),
        cnt_tools=len(tools[:MAX_ITEMS_PER_CATEGORY]),
        cnt_posts=len(posts[:MAX_ITEMS_PER_CATEGORY]),
        sections="".join(sections_html)
    )

    Path("index.html").write_text(html_out, encoding="utf-8")
    save_cache(TRANSLATION_CACHE)
    print("wrote index.html")

if __name__ == "__main__":
    main()
