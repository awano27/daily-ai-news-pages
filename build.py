# -*- coding: utf-8 -*-
"""
AIニュース HTML 生成スクリプト（UI強化＋一般ニュースからAI記事のみ抽出）
- カードUI / タブ / KPI / 相対時刻
- Business / Tools で一般ニュース（general: true）は AI関連キーワードにマッチした記事のみ採用
- 期間: 環境変数 HOURS_LOOKBACK（既定: 24 時間）
- 件数: 環境変数 MAX_ITEMS_PER_CATEGORY（既定: 8 件）
- テンプレート: string.Template を使用（JS/CSSの{}と衝突しない）
"""
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse
from string import Template
import os, re, sys, html
import yaml, feedparser

# ===== 基本設定 =====
JST = timezone(timedelta(hours=9))
HOURS_LOOKBACK = int(os.environ.get("HOURS_LOOKBACK", "24"))
MAX_ITEMS_PER_CATEGORY = int(os.environ.get("MAX_ITEMS_PER_CATEGORY", "8"))

# ===== AI関連キーワード =====
KEYWORDS_COMMON = [
    "AI","人工知能","生成AI","生成型AI","大規模言語モデル","LLM","機械学習","深層学習",
    "chatgpt","gpt","openai","anthropic","claude","llama","gemini","copilot",
    "stable diffusion","midjourney","mistral","cohere","perplexity","hugging face","langchain",
    "rag","ベンチマーク","推論","微調整","ファインチューニング","画像生成","動画生成","sora","nemo","nim","blackwell"
]
KEYWORDS_BUSINESS = [
    "規制","法規制","ガイドライン","政府","省庁","投資","資金調達","ipo","買収","m&a",
    "提携","合意","価格","料金","企業導入","商用利用","市場","売上","収益","雇用","監督","規制当局","コンプライアンス"
]
KEYWORDS_TOOLS = [
    "api","sdk","モデル","リリース","アップデート","ベータ","プレビュー","オープンソース","oss",
    "サンプル","チュートリアル","パッケージ","ライブラリ","バージョン","benchmark","throughput","latency","性能","推論速度"
]
NEGATIVE_HINTS = ["スポーツ","天気","為替","相場","観光","レシピ","占い"]

# ===== ユーティリティ =====
def strip_tags(s: str) -> str:
    if not s: return ""
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

def humanize(dt: datetime, now: datetime) -> str:
    delta = now - dt
    sec = int(delta.total_seconds())
    if sec < 60:   return "たった今"
    if sec < 3600: return f"{sec // 60}分前"
    if sec < 86400:return f"{sec // 3600}時間前"
    days = sec // 86400
    return f"{days}日前"

def parse_dt(entry):
    for key in ("published_parsed", "updated_parsed"):
        t = getattr(entry, key, None) or entry.get(key)
        if t:
            return datetime(*t[:6], tzinfo=timezone.utc).astimezone(JST)
    return None

def domain_of(link: str) -> str:
    try:
        host = urlparse(link).netloc
        return host.replace("www.", "")
    except Exception:
        return ""

def normalize_feeds(feeds_yaml: dict) -> dict:
    norm = {"business": [], "tools": [], "posts": []}
    for k, v in (feeds_yaml or {}).items():
        lk = (k or "").strip().lower()
        if lk in norm:
            norm[lk] = v or []
    # 互換: 先頭大文字キーに対応
    for old, new in (("Business","business"),("Tools","tools"),("Posts","posts")):
        if old in (feeds_yaml or {}):
            norm[new] = feeds_yaml.get(old) or norm[new]
    return norm

def matches_keywords(text: str, keywords: list[str]) -> bool:
    s = text.lower()
    for kw in keywords:
        if kw.lower() in s:
            return True
    return False

# ===== 収集（AIフィルタ対応） =====
def collect(feeds_cfg: dict) -> dict:
    cutoff = datetime.now(JST) - timedelta(hours=HOURS_LOOKBACK)
    result = {"business": [], "tools": [], "posts": []}
    seen_links = set()

    for cat in result.keys():
        for item in feeds_cfg.get(cat, []):
            # feeds.yml: 文字列URL or {name,url,general,include}
            if isinstance(item, dict):
                name = item.get("name") or ""
                url  = item.get("url") or ""
                is_general = bool(item.get("general", False))
                include_extra = item.get("include") or []
            else:
                name, url, is_general, include_extra = "", str(item), False, []

            try:
                parsed = feedparser.parse(url)
            except Exception as e:
                print(f"[WARN] parse error: {url} -> {e}", file=sys.stderr)
                continue

            if cat == "business":
                kw = KEYWORDS_COMMON + KEYWORDS_BUSINESS + include_extra
            elif cat == "tools":
                kw = KEYWORDS_COMMON + KEYWORDS_TOOLS + include_extra
            else:
                kw = KEYWORDS_COMMON + include_extra

            for e in parsed.entries:
                dt = parse_dt(e) or datetime.now(JST)
                if dt < cutoff:
                    continue

                title = getattr(e, "title", "(no title)")
                link  = getattr(e, "link", "#")
                summary_raw = getattr(e, "summary", "")
                text = f"{title} {strip_tags(summary_raw)}"

                # 一般ニュースは AI キーワードにヒットしたものだけ採用
                if is_general:
                    if any(neg in text for neg in NEGATIVE_HINTS):
                        continue
                    if not matches_keywords(text, kw):
                        continue

                if link in seen_links:
                    continue
                seen_links.add(link)

                summary = strip_tags(summary_raw)
                if len(summary) > 220:
                    summary = summary[:220] + "…"

                result[cat].append({
                    "title": html.escape(title),
                    "link": link,
                    "summary": html.escape(summary),
                    "dt": dt,
                    "source": name or domain_of(link),
                })

    for cat in result:
        result[cat].sort(key=lambda x: x["dt"], reverse=True)
        result[cat] = result[cat][:MAX_ITEMS_PER_CATEGORY]
    return result

# ===== HTMLレンダリング =====
PAGE_TMPL = Template("""<!doctype html>
<html lang="ja">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>Daily AI News — ${updated}</title>
  <link rel="stylesheet" href="style.css"/>
</head>
<body>
  <header class="site-header">
    <div class="brand">📰 Daily AI News</div>
    <div class="updated">最終更新：${updated}</div>
  </header>

  <main class="container">
    <h1 class="page-title">今日の最新AI情報</h1>
    <p class="lead">ビジネスニュース・ツール情報・SNS/論文ポストに分け、直近${hours}時間の更新を配信します。</p>

    <section class="kpi-grid">
      <div class="kpi-card">
        <div class="kpi-value">${n_business}件</div>
        <div class="kpi-label">ビジネスニュース</div>
        <div class="kpi-note">重要度高め</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">${n_tools}件</div>
        <div class="kpi-label">ツールニュース</div>
        <div class="kpi-note">開発者向け</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">${n_posts}件</div>
        <div class="kpi-label">SNS/論文ポスト</div>
        <div class="kpi-note">検証系</div>
      </div>
      <div class="kpi-card">
        <div class="kpi-value">${date_jst}</div>
        <div class="kpi-label">最終更新</div>
        <div class="kpi-note">JST</div>
      </div>
    </section>

    <nav class="tabs" role="tablist">
      <button class="tab active" data-target="#business" aria-selected="true">🏢 ビジネスニュース</button>
      <button class="tab" data-target="#tools" aria-selected="false">⚡ ツールニュース</button>
      <button class="tab" data-target="#posts" aria-selected="false">🧪 SNS/論文ポスト</button>
    </nav>

    ${sections}

    <section class="note">
      <p>方針：一次情報（公式ブログ/プレス/論文）を優先。一般ニュースは AI キーワードで抽出。各カード末尾に<strong>出典URL</strong>を明記。</p>
    </section>
  </main>

  <footer class="site-footer">
    <div>Generated by <code>build.py</code> · Timezone: JST</div>
    <div><a href="https://github.com/">Hosted on GitHub Pages</a></div>
  </footer>

  <script>
    // タブ切替（依存ライブラリなし）
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(btn => btn.addEventListener('click', () => {
      tabs.forEach(b => { b.classList.remove('active'); b.setAttribute('aria-selected','false'); });
      btn.classList.add('active'); btn.setAttribute('aria-selected','true');
      document.querySelectorAll('.tab-panel').forEach(p => p.classList.add('hidden'));
      const target = document.querySelector(btn.dataset.target);
      if (target) target.classList.remove('hidden');
    }));
  </script>
</body>
</html>""")

SECTION_TMPL = Template("""
<section id="${id}" class="tab-panel ${hidden}">
  ${cards}
</section>""")

CARD_TMPL = Template("""
<article class="card">
  <div class="card-header">
    <a class="card-title" href="${link}" target="_blank" rel="noopener">${title}</a>
  </div>
  <div class="card-body">
    <p class="card-summary">${summary}</p>
    <div class="chips">
      <span class="chip">${source}</span>
      <span class="chip ghost">${timeago}</span>
    </div>
  </div>
  <div class="card-footer">
    出典: <a href="${link}" target="_blank" rel="noopener">${link}</a>
  </div>
</article>""")

EMPTY_TMPL = '<div class="empty">新着なし（期間を広げるかフィードを追加してください）</div>'

def render_cards(items, now) -> str:
    if not items:
        return EMPTY_TMPL
    htmls = []
    for it in items:
        htmls.append(CARD_TMPL.substitute(
            link=it["link"],
            title=it["title"],
            summary=it["summary"],
            source=html.escape(it["source"] or ""),
            timeago=humanize(it["dt"], now),
        ))
    return "\n".join(htmls)

def render_page(collected: dict) -> str:
    now = datetime.now(JST)
    sections = []
    sections.append(SECTION_TMPL.substitute(id="business", hidden="", cards=render_cards(collected["business"], now)))
    sections.append(SECTION_TMPL.substitute(id="tools", hidden="hidden", cards=render_cards(collected["tools"], now)))
    sections.append(SECTION_TMPL.substitute(id="posts", hidden="hidden", cards=render_cards(collected["posts"], now)))
    return PAGE_TMPL.substitute(
        updated=now.strftime("%Y-%m-%d %H:%M JST"),
        hours=HOURS_LOOKBACK,
        n_business=len(collected["business"]),
        n_tools=len(collected["tools"]),
        n_posts=len(collected["posts"]),
        date_jst=now.strftime("%Y年%m月%d日 %H:%M"),
        sections="\n".join(sections)
    )

def main():
    with open("feeds.yml", "r", encoding="utf-8") as f:
        raw = yaml.safe_load(f) or {}
    feeds = normalize_feeds(raw)
    data = collect(feeds)
    html_out = render_page(data)
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_out)
    print("wrote index.html")

if __name__ == "__main__":
    main()
