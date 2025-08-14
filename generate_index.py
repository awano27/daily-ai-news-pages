#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generate a minimal index.html to get the site working
"""
import os
from datetime import datetime, timezone, timedelta
from pathlib import Path

JST = timezone(timedelta(hours=9))
NOW = datetime.now(JST)

# Minimal HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Daily AI News (日本語要約) - {date}</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<header>
<h1>🤖 Daily AI News <span class="subtitle">(日本語要約)</span></h1>
<p class="updated">最終更新: {datetime_full} (過去{hours}時間)</p>
</header>

<nav class="tab-nav">
<button class="tab-button active" data-tab="business">
Business <span class="count">(0)</span>
</button>
<button class="tab-button" data-tab="tools">
Tools <span class="count">(0)</span>
</button>
<button class="tab-button" data-tab="posts">
Posts <span class="count">(0)</span>
</button>
</nav>

<main>
<section id="business" class="tab-content">
<p class="empty">現在、ニュース記事を取得中です。しばらくお待ちください。</p>
<p class="empty">GitHub Actionsが次回実行時に記事が表示されます。</p>
</section>

<section id="tools" class="tab-content hidden">
<p class="empty">現在、ニュース記事を取得中です。しばらくお待ちください。</p>
</section>

<section id="posts" class="tab-content hidden">
<p class="empty">現在、ニュース記事を取得中です。しばらくお待ちください。</p>
</section>
</main>

<footer>
<p>このサイトは自動的に生成されています。毎日07:00 JSTに更新されます。</p>
</footer>

<script>
document.querySelectorAll('.tab-button').forEach(button => {{
  button.addEventListener('click', () => {{
    const tabName = button.dataset.tab;
    
    // Update buttons
    document.querySelectorAll('.tab-button').forEach(b => b.classList.remove('active'));
    button.classList.add('active');
    
    // Update content
    document.querySelectorAll('.tab-content').forEach(content => {{
      content.classList.add('hidden');
    }});
    document.getElementById(tabName).classList.remove('hidden');
  }});
}});
</script>
</body>
</html>"""

def main():
    print("Generating minimal index.html...")
    
    html = HTML_TEMPLATE.format(
        date=NOW.strftime("%Y-%m-%d"),
        datetime_full=NOW.strftime("%Y-%m-%d %H:%M JST"),
        hours=24
    )
    
    # Write the file
    output_path = Path("index.html")
    output_path.write_text(html, encoding="utf-8")
    
    size = output_path.stat().st_size
    print(f"✓ Generated index.html ({size:,} bytes)")
    print("\nThis is a placeholder page that will be replaced when GitHub Actions runs.")
    print("The page shows a message that content is being fetched.")
    
if __name__ == "__main__":
    main()