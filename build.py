name: Daily build

on:
  schedule:
    - cron: '0 22 * * *'   # 07:00 JST
  workflow_dispatch:

permissions:
  contents: write   # ← push する権限

jobs:
  build:
    runs-on: ubuntu-latest
    env:
      TZ: Asia/Tokyo
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          python -V
          pip install --upgrade pip
          pip install feedparser pyyaml
          python -c "import yaml,sys;print('YAML OK', yaml.__version__)"

      - name: Build HTML
        shell: bash
        run: |
          set -euxo pipefail
          ls -la
          python build.py
          echo "----- build.py done -----"
          ls -la
          test -f index.html && echo "index.html exists" || (echo "::error::index.html not found" && exit 1)
          head -n 20 index.html || true

      - name: Commit and push
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add -A
          git commit -m "chore: update index.html [skip ci]" || echo "no changes"
          git push

      # 失敗時に index.html を拾えるように
      - name: Upload page as artifact (for debug)
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: page
          path: index.html
          if-no-files-found: warn
