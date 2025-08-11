import feedparser
from datetime import datetime, timedelta, timezone
import yaml
import os

# 設定
MAX_ITEMS_PER_CATEGORY = 6
HOURS_LOOKBACK = 24
JST = timezone(timedelta(hours=9))
now = datetime.now(JST)
cutoff = now - timedelta(hours=HOURS_LOOKBACK)

# フィード読み込み
with open("feeds.yml", "r", encoding="utf-8") as f:
    feeds = yaml.safe_load(f)

html_parts = []
html_parts.append(f"<!doctype html><html lang='ja'><head><meta charset='utf-8'><title>Daily AI News — {now.strftime('%Y-%m-%d %H:%M %Z')}</title></head><body>")
html_parts.append(f"<h1>Daily AI News</h1><p>最終更新：{now.strftime('%Y-%m-%d %H:%M %Z')}</p>")

for category, urls in feeds.items():
    html_parts.append(f"<h2>{category}</h2><ul>")
    count = 0
    for url in urls:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            if hasattr(entry, 'published_parsed'):
                published_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc).astimezone(JST)
                if published_dt < cutoff:
                    continue
            title = entry.title
            link = entry.link
            html_parts.append(f"<li><a href='{link}' target='_blank'>{title}</a></li>")
            count += 1
            if count >= MAX_ITEMS_PER_CATEGORY:
                break
    html_parts.append("</ul>")

html_parts.append("</body></html>")

# index.html 出力
with open("index.html", "w", encoding="utf-8") as f:
    f.write("\n".join(html_parts))
