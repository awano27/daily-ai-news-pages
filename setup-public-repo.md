# GitHub Pages 公開用リポジトリのセットアップ手順

## 1. Personal Access Token の作成

1. GitHubの設定ページへアクセス: https://github.com/settings/tokens
2. "Generate new token (classic)" をクリック
3. 以下の権限を付与:
   - `repo` (Full control of private repositories)
   - `workflow` (Update GitHub Action workflows)
4. トークンを生成してコピー

## 2. Private リポジトリ (daily-ai-news) の設定

1. リポジトリの Settings → Secrets and variables → Actions へ移動
2. "New repository secret" をクリック
3. 名前: `PERSONAL_TOKEN`
4. 値: 先ほど作成したトークンを貼り付け
5. "Add secret" をクリック

## 3. 公開用リポジトリの作成

1. 新しいリポジトリを作成: https://github.com/new
   - Repository name: `daily-ai-news-pages`
   - Public を選択（GitHub Pages無料版で公開するため）
   - Initialize with README はチェックしない
2. リポジトリ作成後、Settings → Pages へ移動
3. Source: Deploy from a branch
4. Branch: `gh-pages` / `/ (root)`
5. Save をクリック

## 4. ワークフローの実行

### 自動実行
- `main` ブランチにHTMLファイルの変更がプッシュされた時
- "Daily build (JA summaries fixed)" ワークフローが成功した時

### 手動実行
1. Private リポジトリの Actions タブへ移動
2. "Deploy to Public Pages Repo" ワークフローを選択
3. "Run workflow" → "Run workflow" をクリック

## 5. 確認

デプロイ完了後、以下のURLでサイトが公開されます:
- https://awano27.github.io/daily-ai-news-pages/

## ディレクトリ構造

```
daily-ai-news (Private)
├── .github/
│   └── workflows/
│       ├── build.yml (既存のビルドワークフロー)
│       └── deploy-to-public.yml (新規追加)
├── build.py
├── generate_comprehensive_dashboard.py
├── index.html (生成されるダッシュボード)
└── その他のファイル...

daily-ai-news-pages (Public)
└── gh-pages ブランチ
    ├── index.html (デプロイされたダッシュボード)
    ├── dashboard.html (もしあれば)
    └── assets/ (もしあれば)
```

## メリット

1. **セキュリティ**: ソースコードや設定ファイルは Private リポジトリに保持
2. **無料公開**: Public リポジトリで GitHub Pages を無料で利用
3. **自動化**: ビルド成功後に自動的に公開サイトを更新
4. **分離**: 開発と公開が明確に分離される

## トラブルシューティング

### デプロイが失敗する場合
1. `PERSONAL_TOKEN` が正しく設定されているか確認
2. トークンに `repo` 権限があるか確認
3. 公開リポジトリ名が正しいか確認

### サイトが表示されない場合
1. GitHub Pages の設定を確認（gh-pages ブランチ）
2. デプロイ完了から数分待つ（初回は時間がかかる）
3. ブラウザのキャッシュをクリア