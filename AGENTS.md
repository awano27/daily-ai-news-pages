# Repository Guidelines

## プロジェクト構成とモジュール配置
- 主要スクリプト: ルート直下の Python に集約。`build.py`（サイト生成）、`build_simple_ranking.py`（ランキング）、`deploy_*.py`（デプロイ）、`enhanced_x_processor.py`/`gemini_*`（拡張機能）。
- 設定/アセット: `feeds.yml`（RSS 定義）、`style.css`（スタイル）。
- 生成物: `index.html`、`*_latest.html`、キャッシュ `_cache/translations.json`。
- CI/CD: `.github/workflows/*.yml` で定期ビルドと GitHub Pages デプロイ。
- テスト: 実行可能な `test_*.py`（例: `test_build.py`、`comprehensive_enhanced_test.py`）と `tests/`（pytest）。

## ビルド/テスト/開発コマンド
- 仮想環境: Windows `python -m venv .venv && .venv\Scripts\activate`／Unix `python -m venv .venv && source .venv/bin/activate`
- 依存関係: `pip install -r requirements.txt`
- ローカルビルド: 環境変数を設定して `python build.py`
  - PowerShell 例: `$env:TRANSLATE_TO_JA='1'; $env:HOURS_LOOKBACK='24'; python build.py`
  - Bash 例: `TRANSLATE_TO_JA=1 HOURS_LOOKBACK=24 python build.py`
- 簡易確認: `python test_build.py` または `python comprehensive_enhanced_test.py`
- プレビュー: 生成後に `index.html` をブラウザで開く。

## コーディング規約と命名
- Python 3.11+/PEP 8/インデント 4 スペース。
- 命名: 変数/関数は `snake_case`、ファイルは `lower_snake_case.py`（例: `deploy_latest_changes.py`）。
- モジュールは単一責務を意識し、import 時の副作用を最小化。
- 可能な範囲で型ヒントを使用（例: `list[dict]`）。

## テスト指針
- 小さく焦点の定まった `test_*.py` を機能近傍に配置し、`python file.py` で実行可能に。
- pytest（任意）: `tests/` 配下に `test_*.py` を置き、`pytest -q` で実行。
- 出力検証: `index.html` の生成、タブ/検索 UI の表示、翻訳有効時は `_cache/translations.json` の更新を確認。

## コミット/プルリクガイドライン
- コミットメッセージ: Conventional Commits（`feat:`/`fix:`/`chore:`/`docs:` など）。例: `fix: tab の動作をテンプレート修正で復元`。
- PR 要件:
  - 目的と要約、関連 Issue のリンク。
  - 環境変数や設定変更点（`TRANSLATE_TO_JA`、`HOURS_LOOKBACK` など）。
  - UI 影響は before/after スクリーンショット（`index.html`）。
  - テスト手順（実行コマンド/期待結果）。

## セキュリティ/設定の注意
- Secrets は GitHub Actions の Secrets に保存（`DEEPL_API_KEY`/`GEMINI_API_KEY`）。キーはコミット禁止。
- 主な環境変数: `TRANSLATE_TO_JA`、`TRANSLATE_ENGINE`、`HOURS_LOOKBACK`、`MAX_ITEMS_PER_CATEGORY`、`X_POSTS_CSV`、`TZ`。
- 生成物（`index.html`、`_cache/`）は CI でコミット対象になる場合あり。ローカルの `.venv/` は除外。
