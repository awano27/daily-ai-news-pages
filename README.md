# Daily AI News（UI＋AIフィルタ版）
- 直近24時間の AI ニュースを **ビジネス / ツール / ポスト** に分類してカードUIで表示
- 一般ニュースRSSは `general: true` を付けると **AI関連キーワードにヒットした記事のみ採用**

## 使い方
1. 本リポジトリ直下に `build.py` と `style.css` を置く
2. `feeds.yml` を編集（一般ニュースは `general: true` を付ける）
3. ローカルで生成 → コミット
   ```bash
   pip install feedparser pyyaml
   python build.py
   git add build.py style.css feeds.yml index.html
   git commit -m "feat: ui + ai filter"
   git push
   ```
4. GitHub Pages は `main / /(root)` を選択
5. Actions（同梱の `build.yml`）で毎朝 07:00 JST に自動更新

## 環境変数
- `HOURS_LOOKBACK`（既定=24）
- `MAX_ITEMS_PER_CATEGORY`（既定=8）
