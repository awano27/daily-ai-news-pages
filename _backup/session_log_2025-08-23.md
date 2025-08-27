# Session Log — Daily AI News (2025-08-23)

このファイルは、AIアシスタントとの作業セッションの要約です。変更点、理由、実行手順を簡潔に記録しています。

## 概要
- GitHub Pages 更新停止の原因調査と修正
- デプロイ経路の整理と手動デプロイWFの追加
- 情報源（日本語含む）の拡充
- ランキング軸を「AIエンジニア/業務効率化の有用度」に最適化
- Top Picks（有用度上位）をページ先頭に追加
- X（Twitter）カードのタイトル/要約の可読性改善

## CI/CD の変更
- `.github/workflows/build.yml`
  - スケジュールを 21:55 UTC（JST 06:55）に前倒し
  - コミットメッセージから `[skip ci]` を削除（push トリガーが発火）
- `.github/workflows/deploy-to-public.yml`
  - 自動起動（push/workflow_run）を停止し手動実行専用に変更
- `.github/workflows/manual-deploy.yml`（新規）
  - 手動実行で Pages デプロイ（build → artifact → deploy）
  - Inputs: `hours_lookback`、`max_items_per_category`、`top_picks_count`
  - 依存: `python-dateutil` を追加
  - 安定化: まず `build_simple_ranking.py` を実行、失敗時のみ `build.py` へフォールバック

## 情報源（feeds.yml）の拡充
- 日本語: TechCrunch Japan（AI）, CNET Japan, GIGAZINE, Publickey
- コミュニティ: Qiita（AIタグ）, Zenn（AIトピック）, はてなブックマーク IT
- 研究: arXiv（cs.AI/cs.LG/cs.CL/stat.ML）, Google Research Blog, Keras Blog, Lightning AI Blog

## ランキング/表示ロジックの改善（build_simple_ranking.py）
- 有用度スコア（AIエンジニア/業務効率化）に最適化
  - 追加加点: 自動化/効率化（自動化/効率化/ワークフロー/Copilot/Zapier/Notion/Excel/GAS/Power Automate 等）
  - ハウツー/実装: how to/手順/チュートリアル/導入・活用事例/コード例 で加点
  - 信頼ドメインを拡張（learn.microsoft.com、zapier.com、notion.so 等）
- Top Picks を追加
  - 環境変数 `TOP_PICKS_COUNT`（既定 10）で制御
  - 全カテゴリ横断でスコア上位を重複除去して表示
- 表示文言
  - リード: 「有用度スコア（AIエンジニア/業務効率化向け）」
  - カード: 「スコア」→「有用度」に変更

## X（Twitter）カードの可読性改善
- 投稿本文のクリーニング（URL/末尾ハッシュタグ/末尾メンション除去、空白整形）
- 外部リンク検出（x.com/twitter/t.co を除外）→ OGP の `og:title` / `<title>` を取得
- タイトル: `記事タイトル（ドメイン）` へ置換（なければ整形済み本文）
- 要約: `[カテゴリ] 記事タイトル ｜ 投稿要約: … ｜ 出典: ドメイン` に統一（カテゴリは実装/効率化/研究/発表を推定）
- ソース表記: `X @username`
- 生成結果でスコアを再計算

## 実行手順（手動デプロイ）
1. GitHub → Actions → 「Manual Deploy AI News to GitHub Pages」
2. Run workflow（Branch: `main`）
   - 例: `hours_lookback=48`, `max_items_per_category=30`, `top_picks_count=15`
3. 反映確認: https://awano27.github.io/daily-ai-news/

## 既知の注意点
- 追加した日本語ソースは一般テック記事も含むため、ノイズが増える場合は個別に調整可能
- 外部サイトの OGP 取得は失敗する場合あり（その場合は整形本文で代替）

## 次の改善候補
- ドメイン別アイコン表示（GitHub/ArXiv/Medium等）
- カードチップ（読了時間/実装難易度/カテゴリ）
- Xを別タブ分離 or Top Picks への昇格ロジック追加

