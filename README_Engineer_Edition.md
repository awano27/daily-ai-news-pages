# AI Tech Radar - Engineer Edition

エンジニアのための最新AI技術情報サイト

## 🎯 主な改善点

### デザイン・UX改善
- **モダンなインターフェース**: グラスモーフィズム、アニメーション効果
- **ダークモード対応**: 眼に優しい開発者向けテーマ
- **レスポンシブデザイン**: モバイル・タブレット完全対応
- **アクセシビリティ強化**: キーボードナビゲーション、ARIA対応

### エンジニア向け機能
- **技術スコアリング**: 0.6以上の高品質技術コンテンツのみ表示
- **実装難易度表示**: 初級・中級・上級の3段階で分類
- **技術スタック検出**: Python、JavaScript、CUDA等を自動識別
- **コード例ハイライト**: 実装可能なコード片を優先表示
- **読了時間推定**: 技術文書の読解時間を考慮した精密計算

### インタラクティブ要素
- **リアルタイム検索**: キーワード、技術、企業名でフィルタリング
- **スマートタグ**: LLM、Computer Vision、MLOps等のカテゴリ
- **ブックマーク機能**: ローカルストレージで記事保存
- **トレンド表示**: 注目度上位20%を自動選定

### コンテンツ最適化
- **高品質フィード**: arXiv、GitHub、主要テック企業ブログ
- **重複除去**: コンテンツ類似度による自動フィルタリング
- **翻訳キャッシュ**: API呼び出し最適化で高速化
- **パフォーマンス指標**: ベンチマーク結果やメトリクス表示

## 🚀 使用方法

### 基本実行
```bash
# エンジニア版ビルド実行
python build_engineer_focused.py

# Windows用バッチファイル
test_engineer_build.bat
```

### 環境変数設定
```bash
# 翻訳設定
set TRANSLATE_TO_JA=1
set TRANSLATE_ENGINE=google

# 収集範囲設定
set HOURS_LOOKBACK=24
set MAX_ITEMS_PER_CATEGORY=15
```

## 📁 ファイル構成

```
AI Tech Radar/
├── index_engineer_focused.html    # エンジニア版メインHTML
├── style_engineer.css             # モダンCSS（ダークモード対応）
├── script_engineer.js             # インタラクティブ機能
├── build_engineer_focused.py      # エンジニア向けビルドスクリプト
├── feeds_engineer.yml             # 高品質フィード設定
├── test_engineer_build.bat        # Windows用テストスクリプト
└── _cache/                        # 翻訳・データキャッシュ
```

## 🔧 技術仕様

### フロントエンド
- **CSS Grid/Flexbox**: モダンレイアウト
- **CSS Custom Properties**: テーマ切り替え対応
- **Intersection Observer**: 遅延読み込み・アニメーション
- **Web Storage API**: ブックマーク・設定保存
- **Service Worker**: オフライン対応（実装予定）

### バックエンド
- **Python 3.8+**: 非同期処理対応
- **feedparser**: RSS/Atom フィード解析
- **deep-translator**: 多言語対応翻訳
- **PyYAML**: 設定ファイル管理
- **dataclasses**: 型安全なデータ構造

### データ処理
- **技術関連度スコアリング**: キーワード重み付け
- **実装難易度推定**: ML分類アルゴリズム
- **トレンド検出**: 時系列解析
- **重複除去**: コンテンツハッシュ化

## 🎨 デザインシステム

### カラーパレット
- **プライマリ**: #6366f1 (Indigo)
- **セカンダリ**: #22d3ee (Cyan)
- **アクセント**: #f59e0b (Amber)
- **成功**: #10b981 (Emerald)
- **警告**: #f59e0b (Orange)
- **エラー**: #ef4444 (Red)

### タイポグラフィ
- **本文**: Inter, system-ui
- **コード**: 'Fira Code', 'JetBrains Mono'
- **サイズ**: fluid typography (clamp)

## 📊 品質指標

### パフォーマンス目標
- **First Contentful Paint**: < 1.5s
- **Largest Contentful Paint**: < 2.5s
- **Cumulative Layout Shift**: < 0.1
- **First Input Delay**: < 100ms

### アクセシビリティ
- **WCAG 2.1 AA準拠**
- **カラーコントラスト比**: 4.5:1以上
- **キーボードナビゲーション**: 完全対応
- **スクリーンリーダー**: ARIA属性完備

## 🔄 デプロイメント

### GitHub Pages対応
```bash
# 自動デプロイ用設定
cp index_engineer_focused.html index.html
git add .
git commit -m "Update to Engineer Edition"
git push origin main
```

### 継続的統合
```yaml
# .github/workflows/build-engineer.yml
name: Build Engineer Edition
on:
  schedule:
    - cron: '0 */2 * * *'  # 2時間ごと
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Setup Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Build site
        run: python build_engineer_focused.py
      - name: Deploy
        run: |
          cp index_engineer_focused.html index.html
          git config --local user.email "action@github.com"
          git config --local user.name "GitHub Action"
          git add .
          git commit -m "Auto-build: $(date)" || exit 0
          git push
```

## 🛠️ カスタマイズ

### 新しいフィードソース追加
```yaml
# feeds_engineer.yml
new_category:
  - https://example.com/feed.xml
```

### 技術スコア調整
```python
# build_engineer_focused.py
TECH_KEYWORDS = {
    'custom_category': ['keyword1', 'keyword2']
}
```

### UI テーマカスタマイズ
```css
/* style_engineer.css */
:root {
  --primary: #your-color;
  --secondary: #your-color;
}
```

## 🧪 テスト

### ローカル開発
```bash
# 開発サーバー起動
python -m http.server 8000

# ブラウザでアクセス
open http://localhost:8000/index_engineer_focused.html
```

### 品質チェック
```bash
# HTML検証
html5validator index_engineer_focused.html

# CSS検証
csslint style_engineer.css

# JavaScript検証
eslint script_engineer.js

# アクセシビリティチェック
pa11y http://localhost:8000/index_engineer_focused.html
```

## 📈 今後の拡張予定

### v2.0 機能
- [ ] **AIキュレーション**: GPT-4による記事要約・評価
- [ ] **パーソナライゼーション**: ユーザー興味プロファイル
- [ ] **マルチ言語対応**: 英語・中国語・韓国語
- [ ] **PWA化**: オフライン閲覧、プッシュ通知

### 技術的改善
- [ ] **GraphQL API**: 高速データ取得
- [ ] **CDN統合**: グローバル配信
- [ ] **A/Bテスト**: UI最適化
- [ ] **分析ダッシュボード**: 利用統計

## 🤝 コントリビュート

1. **Issue報告**: バグ・改善提案
2. **Pull Request**: 機能追加・修正
3. **フィードバック**: UX改善提案

## 📝 ライセンス

MIT License - 詳細は`LICENSE`ファイルを参照

## 📞 サポート

- **GitHub Issues**: 技術的な問題
- **Discussion**: 機能リクエスト・質問
- **Email**: engineer-edition@aitechradar.dev

---

🚀 **エンジニアによる、エンジニアのための最高のAI情報体験を提供します**