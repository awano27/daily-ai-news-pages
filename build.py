# -*- coding: utf-8 -*-
import feedparser
from datetime import datetime, timedelta, timezone
import yaml
import sys

MAX_ITEMS_PER_CATEGORY = 6
HOURS_LOOKBACK = 24
JST = timezone(timedelta(hours=9))

def load_feeds():
    with open("feeds.yml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}

def fetch_items(url):
    try:
        return feedparser.parse(url).entries
    except Exception as e:
        print(f"[WARN] feed parse failed: {url} -> {e}", file=sys.stderr)
        return []

def within_lookback(entry, cutoff):
    # published_parsed または updated_parsed を見る。無ければ True（採用）
    for key in ("published_parsed", "updated_parsed"):
        t = getattr(entry, key, None) or entry.get(key)
        if t:
            dt = datetime(*t[:6], tzinfo=timezone.utc).astimezone(JST)
            return dt >= cutoff
    return True

def main():
    now = datetime.now(JST)
    cutoff = now - timedelta(hours=HOURS_LOOKBACK)
    feeds = load_feeds()

    html = []
    html.append(f"<!doctype html><html lang='ja'><head><meta charset='utf-8'>"
                f"<title>Daily AI News — {now.strftime('%Y-%m-%d %H:%M %Z')}</title>"
                f"<meta name='viewport' content='width=device-width, initial-scale=1'>"
                f"</head><body>")
    html.append(f"<h1>Daily AI News</h1><p>最終更新：{now.strftime('%Y-%m-%d %H:%M %Z')}</p>")

    if not feeds:
        html.append("<p>feeds.yml が空です。</p>")
    else:
        for category, urls in feeds.items():
            html.append(f"<h2>{category}</h2><ul>")
            shown = 0
            for url in urls:
                for entry in fetch_items(url):
                    if not within_lookback(entry, cutoff):
                        continue
                    title = getattr(entry, "title", "(no title)")
                    link = getattr(entry, "link", "#")
                    html.append(f"<li><a href='{link}' target='_blank' rel='noopener'>{title}</a> "
                                f"<small>出典: <a href='{link}' target='_blank' rel='noopener'>{link}</a></small></li>")
                    shown += 1
                    if shown >= MAX_ITEMS_PER_CATEGORY:
                        break
                if shown >= MAX_ITEMS_PER_CATEGORY:
                    break
            if shown == 0:
                html.append("<li>新着なし（期間を広げるかフィードを追加してください）</li>")
            html.append("</ul>")

    html.append("</body></html>")

    with open("index.html", "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    print("wrote index.html")

if __name__ == "__main__":
    main()
