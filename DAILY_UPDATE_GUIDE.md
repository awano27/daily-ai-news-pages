# 毎日の AI ニュースダッシュボード更新ガイド

## 📋 概要
このガイドは、AI業界ダッシュボード（https://awano27.github.io/daily-ai-news/）の毎日の更新作業で発生する可能性のある問題を防ぐためのチェックリストです。

## ⚠️ 今日発生した問題と解決策

### 問題1: GitHub Actionsが古いスクリプトを実行
**症状**: 新しい機能（Gemini翻訳等）を実装してもサイトに反映されない  
**原因**: `.github/workflows/build.yml`が古いスクリプトを実行している  
**解決**: ワークフローファイルを新しいスクリプトに更新する

### 問題2: 依存関係不足
**症状**: `ModuleNotFoundError: No module named 'dotenv'` エラー  
**原因**: GitHub Actionsで必要なライブラリがインストールされていない  
**解決**: `build.yml`の依存関係に `python-dotenv` を追加

## 🔄 毎日の更新チェックリスト

### 1. 自動更新の確認（毎朝8:00頃）

```bash
# サイトが更新されているか確認
curl -I https://awano27.github.io/daily-ai-news/
```

- [ ] サイトの日付が今日の日付になっている
- [ ] 記事数が適切（20件以上）
- [ ] X投稿が表示されている
- [ ] 日本語翻訳が正常に動作している

### 2. GitHub Actions の確認

1. https://github.com/awano27/daily-ai-news/actions にアクセス
2. 最新のワークフロー実行を確認
3. エラーがないか確認

- [ ] ワークフローが正常完了（緑色のチェックマーク）
- [ ] ビルド時間が10分以内
- [ ] エラーメッセージがない

### 3. 手動更新が必要な場合

#### 3.1 GitHub Actions での手動実行
```
1. https://github.com/awano27/daily-ai-news/actions
2. "Daily build (JA summaries fixed)" を選択
3. "Run workflow" → "Run workflow" をクリック
4. 5-10分待ってサイト確認
```

#### 3.2 ローカルでの緊急更新
```bash
# 環境確認
cd C:\Users\yoshitaka\daily-ai-news
python -c "import google.generativeai; print('Gemini API OK')"

# 翻訳付きダッシュボード生成
python generate_reference_format_dashboard.py

# 生成されたファイルを確認
# reference_format_dashboard_YYYYMMDD_HHMMSS.html

# 手動デプロイ（緊急時のみ）
copy reference_format_dashboard_*.html index.html
git add index.html
git commit -m "chore: manual update for emergency deployment"
git push origin main
```

## 🛠️ 新機能追加時の注意点

### スクリプト追加・変更時
1. **新しいPythonスクリプトを作成した場合**:
   - `.github/workflows/build.yml` を更新
   - 依存関係を `pip install` 行に追加
   - タイムアウト設定を適切に設定

2. **環境変数が必要な場合**:
   - GitHub Secrets に追加
   - `build.yml` の `env` セクションに追加

3. **新しいライブラリを使用する場合**:
   - `requirements.txt` を更新
   - `build.yml` の pip install に追加

### デプロイ前チェック
```bash
# ローカルテスト
python your_new_script.py

# Gitコミット
git add your_new_script.py
git add .github/workflows/build.yml  # 忘れがち！
git commit -m "feat: add new feature"
git push origin main
```

## 📞 トラブルシューティング

### 🚨 サイトが更新されない
1. GitHub Actions を確認
2. ワークフローを手動実行
3. エラーログを確認
4. 必要に応じてローカル生成→手動デプロイ

### 🚨 翻訳が動作しない
1. Gemini APIキーが設定されているか確認
2. API制限に達していないか確認
3. ログで翻訳エラーメッセージを確認

### 🚨 X投稿データが取得できない
1. Google Sheets URLが正しいか確認
2. CSV形式でアクセスできるか確認
3. フォールバックデータが表示されているか確認

## 📝 ログ確認コマンド

```bash
# 最新のコミット確認
git log --oneline -5

# 現在の状態確認
git status

# リモートとの差分確認
git fetch && git status
```

## ⏰ 重要なタイミング

- **7:00 JST**: 自動更新時刻
- **8:00 JST**: 更新確認推奨時刻
- **9:00 JST**: 問題があれば手動対応開始

## 🔧 緊急時連絡先

- GitHub Repository: https://github.com/awano27/daily-ai-news
- Live Site: https://awano27.github.io/daily-ai-news/
- Actions: https://github.com/awano27/daily-ai-news/actions

---

## 📚 関連ファイル

- `generate_reference_format_dashboard.py` - メイン生成スクリプト
- `.github/workflows/build.yml` - 自動更新設定
- `feeds.yml` - RSS フィード設定
- `.env` - API キー等の環境変数

**このガイドを定期的に更新して、新しい問題と解決策を追加してください。**