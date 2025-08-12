# 日本語要約対応（DeepL）版
- ソースリンクは原文のまま、ページに掲載する **要約のみ日本語化** します（DeepL API Free/Pro）。
- 一般ニュースは `general: true` で AI 関連キーワードにマッチしたものだけ採用します。

## セットアップ
1. **DeepL APIキー** を取得して GitHub Secrets に `DEEPL_API_KEY` として登録  
   - Repository → *Settings → Secrets and variables → Actions* → **New repository secret**
2. 本リポジトリに `build.py`（本ファイル）と `style.css`、`feeds.yml` を置く
3. 同梱の `.github/workflows/build.yml` を使う（`TRANSLATE_TO_JA='1'` が有効）

## ローカル実行
```bash
pip install feedparser pyyaml deepl
set DEEPL_API_KEY=xxxxxxxxxxxxxxxx  # Windows PowerShell は $env:DEEPL_API_KEY="..."
set TRANSLATE_TO_JA=1               # PowerShell: $env:TRANSLATE_TO_JA="1"
python build.py
```

## キャッシュ
- `_cache/translations.json` に英→日訳を保存し、次回以降は再利用します（Actions のコミットに含めます）。
