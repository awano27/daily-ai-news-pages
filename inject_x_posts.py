#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
posts セクションが 0 件のときだけ、X/Twitter の URL を N 件差し込みます（再実行しても重複なし）
- 入力: index.html, CSV(ローカル or URL)。CSV から x/twitter.com の URL を抽出
- 出力: index.html を上書き（UTF-8, LF）。KPI(「SNS/論文ポスト」)も件数更新
"""
import argparse, csv, io, os, re, sys
from urllib.parse import urlparse
from urllib.request import urlopen

X_BLOCK_START = "<!-- BEGIN:X_POSTS AUTO -->"
X_BLOCK_END   = "<!-- END:X_POSTS AUTO -->"

def _read_csv_bytes(path_or_url: str) -> bytes:
    if re.match(r'^https?://', path_or_url, re.I):
        with urlopen(path_or_url) as r:
            return r.read()
    with open(path_or_url, 'rb') as f:
        return f.read()

def _extract_x_urls_from_csv(raw: bytes) -> list[str]:
    # 文字コード自動判定(UTF-8 BOM優先→UTF-8→CP932)
    for enc in ('utf-8-sig','utf-8','cp932'):
        try:
            txt = raw.decode(enc)
            break
        except Exception:
            continue
    else:
        txt = raw.decode('utf-8', errors='ignore')

    # 1) CSV列に URL があればそれを使う 2) なければ全体から正規表現抽出
    urls: list[str] = []
    try:
        rdr = csv.reader(io.StringIO(txt))
        for row in rdr:
            for cell in row:
                m = re.findall(r'https?://(?:x|twitter)\.com/[^\s,"]+', cell)
                if m: urls.extend(m)
    except Exception:
        pass

    if not urls:
        urls = re.findall(r'https?://(?:x|twitter)\.com/[^\s,"]+', txt)

    # 正規化 & 重複除去（順序維持）
    seen, out = set(), []
    for u in urls:
        u = u.replace('x.com/','twitter.com/')  # 正規化
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

def _build_card(url: str) -> str:
    author = _author_from_url(url)
    return f"""<article class="card">
  <div class="card-header">
    <a class="card-title" href="{url}" target="_blank" rel="noopener">Xポスト {author}</a>
  </div>
  <div class="card-body">
    <p class="card-summary">手動で「いいね」したポストから自動抽出（要約なし）</p>
    <div class="chips">
      <span class="chip">X / SNS</span>
      <span class="chip ghost">要約: なし</span>
      <span class="chip ghost">—</span>
    </div>
  </div>
  <div class="card-footer">
    出典: <a href="{url}" target="_blank" rel="noopener">{url}</a>
  </div>
</article>"""

def _update_kpi(html: str, new_count: int) -> str:
    # 「SNS/論文ポスト」の KPI 値だけを安全に更新
    pattern = re.compile(
        r'(<div class="kpi-label">SNS/論文ポスト</div>\s*<div class="kpi-note">.*?</div>\s*</div>)',
        re.S)
    def repl(m):
        # 直前の kpi-card を取り直して value 部分のみ置換
        card_start = html.rfind('<div class="kpi-card">', 0, m.start())
        if card_start < 0: return m.group(0)
        # そのカード領域
        card_end = m.end()
        card_html = html[card_start:card_end]
        card_html2 = re.sub(r'(<div class="kpi-value">)\d+件(</div>)',
                            rf'\1{new_count}件\2', card_html)
        return html[:card_start] + card_html2 + html[card_end:]
    # 1回だけ置換した新HTMLを返したいので、直接扱う
    pos = pattern.search(html)
    if not pos: return html
    return _update_kpi.__wrapped__(html, new_count) if hasattr(_update_kpi,'__wrapped__') else repl(pos)  # type: ignore

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i','--input', required=True, help='index.html')
    ap.add_argument('-c','--csv',   required=True, help='CSV path or URL')
    ap.add_argument('-n','--num',   type=int, default=8)
    ap.add_argument('--only-when-empty', action='store_true', help='postsが0件のときだけ挿入')
    args = ap.parse_args()

    html = open(args.input, 'r', encoding='utf-8', errors='ignore').read()

    # posts セクション抽出
    m = re.search(r'(<section id="posts"[^>]*>)(.*?)(</section>)', html, re.S)
    if not m:
        print('NG: <section id="posts"> が見つかりません'); sys.exit(1)

    head, body, tail = m.group(1), m.group(2), m.group(3)

    # 既存カード数と既存のX URL
    existing_cards = len(re.findall(r'<article class="card">', body))
    existing_urls = set(re.findall(r'https?://(?:x|twitter)\.com/[^\s"]+', body))
    existing_urls = {u.replace('x.com/','twitter.com/') for u in existing_urls}

    if args.only_when_empty and existing_cards > 0:
        print('Skip: posts は 0 件ではありません'); return

    # CSV 読み込み → URL 抽出
    raw = _read_csv_bytes(args.csv)
    urls = _extract_x_urls_from_csv(raw)
    urls = [u for u in urls if u not in existing_urls][:args.num]
    if not urls:
        print('CSVに有効なX URLが見つかりません'); return

    # 置換（idempotent: ブロックを全差し替え）
    cards = "\n".join(_build_card(u) for u in urls)
    x_block = f"{X_BLOCK_START}\n{cards}\n{X_BLOCK_END}\n"

    if X_BLOCK_START in body and X_BLOCK_END in body:
        body2 = re.sub(rf'{re.escape(X_BLOCK_START)}.*?{re.escape(X_BLOCK_END)}',
                       x_block, body, flags=re.S)
    else:
        body2 = x_block + body  # 先頭に差し込む

    # KPIも更新
    new_total = len(re.findall(r'<article class="card">', body2))
    html2 = html[:m.start()] + head + body2 + tail + html[m.end():]
    html2 = _update_kpi(html2, new_total)

    # UTF-8 LF で保存
    with open(args.input, 'w', encoding='utf-8', newline='\n') as f:
        f.write(html2)

    print(f"Injected {len(urls)} X posts. posts total = {new_total}")

if __name__ == '__main__':
    main()
