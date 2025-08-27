# Conversation Log (Markdown)

- Repo: `awano27/daily-ai-news`
- Public site: https://awano27.github.io/daily-ai-news/
- Date: 2025-08-23 (JST)

## Summary
- Pages 更新が止まった原因を調査し、`[skip ci]` とスケジュール競合を解消。
- デプロイ経路を整理し、手動実行の Pages デプロイを追加。
- 日本語RSSを拡充、ビルドの安定化（simple優先）。
- スコア軸を「AIエンジニア/業務効率化の有用度」に最適化、Top Picks 追加。
- X（Twitter）カードのタイトル/要約を読みやすく整形（OGP活用・カテゴリ推定）。

---

## Transcript (key turns)

> User: 最新が更新されなくなりました。コードの確認をしてください。

> Assistant: リポジトリとワークフローを確認します。`[skip ci]` により push トリガーが抑止されており、`build.yml` と `deploy-pages.yml` が同刻で競合しています。

> Assistant: `.github/workflows/build.yml` のコミットメッセージから `[skip ci]` を除去し、スケジュールを 21:55 UTC に前倒し。`deploy-to-public.yml` は手動実行専用に変更。

> User: はい。

> Assistant: コミットしようとしたところ、競合（`.claude/settings.local.json`, `news_detail.html`）。HEAD 版（ours）を採用して解消し、修正を反映しました。

> User: 手動実行したい。

> Assistant: 「Manual Deploy AI News to GitHub Pages」を新規追加。Actionsから実行可能にしました。

> User: Githubにあがっていますか？

> Assistant: 先の push は `daily-ai-news-pages` に出ていました。正リポ `daily-ai-news` を新規クローンし、同じ修正（build前倒し/[skip ci]除去/手動WF追加）を `main` にプッシュしました。

> User: サイトを再ビルド。

> Assistant: 手動ワークフローで実行可能です。`hours_lookback`/`max_items` を指定可能。

> User: 実行すると？

> Assistant: `build_simple_ranking.py` で `index.html` を生成→Pagesに即時デプロイ。リポのソースコミットは発生しません。

> User: 成功。どこが更新？

> Assistant: `index.html`（＋`style.css`/`.nojekyll`）が更新。タブ/検索/翻訳も反映。

> User: 情報内容も更新して。

> Assistant: `feeds.yml` を拡充（日本語含む）。手動WFに `hours_lookback`/`max_items_per_category` の入力を追加。

> User: Manual Deploy でエラー。

> Assistant: 安定化（simple優先＋`python-dateutil` 追加）をプッシュ。再実行を案内。

> User: 日本語記事を増やしたい。

> Assistant: 日本語RSSを追加（TechCrunch Japan/CNET Japan/GIGAZINE/Publickey/Qiita/Zenn/はてな）。プッシュ済。

> User: AIエンジニア/効率化向けに有用度順で上から表示。

> Assistant: スコア軸を「有用度」に最適化（自動化/効率化/ハウツー加点、信頼ドメイン拡張）。文言も「有用度」に変更。

> User: Top Picksを先頭に。

> Assistant: Top Picks（全カテゴリ横断、重複除去、上位N件）を追加。`TOP_PICKS_COUNT` で制御。手動WFに `top_picks_count` 入力を追加。

> User: サイトを見せて。

> Assistant: 公開URLを案内。手動実行で Top Picks と新ロジックが表示されます。

> User: Xのタイトル/要約がわかりづらい。

> Assistant: クリーニング、外部リンク抽出、OGPタイトル取得、カテゴリ推定（実装/効率化/研究/発表）、統一フォーマット要約に改善。ソースは `X @username` に。

> User: まだわかりづらい。

> Assistant: 要約ビルダーを導入し、`[カテゴリ] 記事タイトル ｜ 投稿要約: … ｜ 出典: ドメイン` の定型で生成するよう強化。

> User: 会話を保存。

> Assistant: 本ファイル（Markdown）と別途サマリー（`_backup/session_log_2025-08-23.md`）を保存。

---

## Files touched (high-level)
- `.github/workflows/build.yml`（前倒し/skip ci除去）
- `.github/workflows/deploy-to-public.yml`（手動化）
- `.github/workflows/manual-deploy.yml`（新規、inputs追加）
- `feeds.yml`（日本語/研究/コミュニティ追加）
- `build_simple_ranking.py`
  - 有用度スコア最適化、Top Picks追加
  - Xカードのタイトル/要約の整形（OGP/カテゴリ推定/統一書式）

## Runbook
1) Manual Deploy: Actions → Manual Deploy → Run workflow（`hours_lookback`, `max_items_per_category`, `top_picks_count`）
2) 確認: https://awano27.github.io/daily-ai-news/
3) 追加調整（必要なら）: フィード/重み/件数の恒久設定変更

