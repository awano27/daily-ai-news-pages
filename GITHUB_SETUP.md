# GitHub自動実行セットアップガイド

## 🚀 Enhanced AI News System - GitHub Actions自動実行設定

このガイドに従って、Enhanced AI News Systemを GitHub Actions で毎日自動実行するよう設定します。

## 📋 前提条件

- GitHubアカウント
- Gemini API Key (Google AI Studio)
- このリポジトリのフォーク権限

## 🔧 セットアップ手順

### 1. リポジトリの準備

```bash
# 変更をコミット
git add -A
git commit -m "feat: Enhanced AI News System with Gemini URL Context"
git push origin main
```

### 2. GitHub Secretsの設定

1. GitHubリポジトリにアクセス
2. **Settings** → **Secrets and variables** → **Actions** を選択
3. **New repository secret** をクリック
4. 以下のシークレットを追加:

| Name | Value |
|------|-------|
| `GEMINI_API_KEY` | あなたのGemini API Key |

### 3. GitHub Pages の有効化

1. リポジトリの **Settings** に移動
2. **Pages** セクションを選択
3. Source を **"Deploy from a branch"** に設定
4. Branch を **"main"** に設定
5. **Save** をクリック

### 4. ワークフロー権限の設定

1. **Settings** → **Actions** → **General** に移動
2. **Workflow permissions** で以下を選択:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
3. **Save** をクリック

## 🕐 実行スケジュール

### 自動実行タイミング
- **毎日 07:00 JST** (22:00 UTC)
- **毎日 19:00 JST** (10:00 UTC) 

### 手動実行
- **Actions** タブから **"Enhanced Daily AI News (Full Pipeline)"** を選択
- **Run workflow** をクリック

## 🎯 機能紹介

### ✅ Enhanced Features
- **🧠 Gemini URL Context**: X投稿の高度なAI分析
- **❌ 重複除去**: ハッシュベースの重複検出
- **📝 300文字要約**: 読みやすい簡潔な要約
- **⭐ 重要度ランキング**: AI判定による優先表示
- **🔄 自動分類**: カテゴリ別の自動整理

### 📊 出力ファイル
- `index.html` - メインニュースページ
- `news_detail.html` - 詳細ニュースページ  
- `ai_news_dashboard.html` - 分析ダッシュボード

## 🔍 トラブルシューティング

### よくある問題

#### ❌ ワークフローが失敗する
**原因**: GEMINI_API_KEY が設定されていない
**解決**: GitHub Secrets に正しいAPI Keyを設定

#### ⚠️ サイトが更新されない
**原因**: GitHub Pages の設定が不適切
**解決**: Settings → Pages で正しいブランチを選択

#### 🐛 X投稿が処理されない
**原因**: CSV URLにアクセスできない
**解決**: Google Sheets の共有設定を確認

## 📈 監視とメンテナンス

### ログの確認
1. **Actions** タブで実行履歴を確認
2. 失敗した場合は詳細ログを確認
3. エラーメッセージに基づいて対応

### パフォーマンス監視
- **Gemini API使用量**: トークン消費量の監視
- **ビルド時間**: 実行時間の最適化
- **サイト品質**: 重複率と要約品質の確認

## 🎉 完了確認

✅ GitHub Actions が正常に実行される  
✅ 毎日自動でサイトが更新される  
✅ X投稿の重複が除去される  
✅ 要約が300文字以内になる  
✅ Gemini AIによる内容強化が動作する  

## 📞 サポート

問題が発生した場合:
1. GitHub Actions のログを確認
2. API Key の有効性を確認  
3. ワークフロー設定を再確認

---

**🤖 Enhanced AI News System**  
*Powered by Gemini URL Context API*