#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
docs デプロイ補助スクリプト
- 既存のローカル生成物（index.html / style.css）を docs/ 配下へコピー
- Jekyll を無効化するため docs/.nojekyll を作成

使い方:
  1) 先に `python build_simple_ranking.py` もしくは `python build.py` を実行し、
     ルートに index.html / style.css を生成しておく
  2) 本スクリプトを実行: `python scripts/prepare_docs_deploy.py`
  3) GitHub Pages のソースを `main` / `docs` に設定し、コミット&プッシュ
"""

from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"

def main() -> int:
    src_index = ROOT / "index.html"
    src_css = ROOT / "style.css"

    if not src_index.exists() or not src_css.exists():
        print("❌ index.html または style.css が見つかりません。先にビルドを実行してください。")
        return 1

    DOCS.mkdir(exist_ok=True)

    # コピー
    shutil.copy2(src_index, DOCS / "index.html")
    shutil.copy2(src_css, DOCS / "style.css")

    # Jekyll 無効化
    (DOCS / ".nojekyll").write_text("", encoding="utf-8")

    # 簡易レポート
    print("✅ docs デプロイ準備が完了しました")
    print(f" - {DOCS / 'index.html'}")
    print(f" - {DOCS / 'style.css'}")
    print(f" - {DOCS / '.nojekyll'}")
    print("次のステップ:\n  1) 変更をコミット\n  2) GitHub Pages のソースを main/docs に設定\n  3) 数分後に https://awano27.github.io/daily-ai-news/ を確認")
    return 0

if __name__ == "__main__":
    sys.exit(main())

