#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix "要約: ○○" chips in index.html by detecting whether each card's summary text
contains Japanese characters. If so -> 日本語, else -> 英語.

Usage:
  python fix_lang_chips.py [path/to/index.html]

Notes:
- Non-destructive: writes a backup file next to the input as index.html.bak
- Requires beautifulsoup4 (already present in your environment via deep-translator)
"""

import sys
import re
from bs4 import BeautifulSoup
from pathlib import Path

JP_RE = re.compile(r'[\u3040-\u30ff\u3400-\u9fff\uF900-\uFAFF]')

def looks_japanese(s: str) -> bool:
    return bool(JP_RE.search(s or ""))

def main():
    html_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("index.html")
    if not html_path.exists():
        print(f"[ERROR] File not found: {html_path}")
        sys.exit(1)

    raw = html_path.read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(raw, "html.parser")

    changed = 0
    total = 0

    # Each news item card
    for art in soup.select("article.card"):
        total += 1
        # get summary text
        summ = art.select_one(".card-summary")
        if not summ:
            continue
        text = summ.get_text(" ", strip=True)
        lang = "日本語" if looks_japanese(text) else "英語"

        # find existing chip like "要約: ..."
        # Prefer spans inside the same card
        chips = art.select(".chips span.chip.ghost")
        target = None
        for sp in chips:
            if (sp.get_text() or "").strip().startswith("要約:"):
                target = sp
                break

        if target is None:
            # add a new chip into the chips container
            chips_container = art.select_one(".chips")
            if chips_container:
                new_span = soup.new_tag("span", **{"class":"chip ghost"})
                new_span.string = f"要約: {lang}"
                chips_container.append(new_span)
                changed += 1
        else:
            current = (target.get_text() or "").strip()
            desired = f"要約: {lang}"
            if current != desired:
                target.string = desired
                changed += 1

    if changed:
        # backup
        bak = html_path.with_suffix(html_path.suffix + ".bak")
        bak.write_text(raw, encoding="utf-8", errors="ignore")
        html_path.write_text(str(soup), encoding="utf-8")
        print(f"[OK] Updated chips in {html_path} (changed {changed}/{total} cards). Backup -> {bak.name}")
    else:
        print(f"[OK] No changes needed ({total} cards scanned).")

if __name__ == "__main__":
    main()
