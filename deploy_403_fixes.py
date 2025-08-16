#!/usr/bin/env python3
import subprocess
import sys
import os

# Change to project directory
os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

print("🚀 403エラー修正版をGitHubにデプロイ中...")

try:
    # Git operations
    print("📝 変更をコミット中...")
    subprocess.run(["git", "add", ".", "-A"], check=True)
    
    commit_message = """feat: Fix 403 Forbidden errors and improve feed reliability [skip ci]

🔧 MAJOR IMPROVEMENTS:
- 403 Forbiddenエラー対策を大幅強化
- User-Agentヘッダー追加でアクセス拒否を回避
- リトライ機能（最大2回）で安定性向上
- 代替User-Agentによるフォールバック機能

📡 FEED URL UPDATES:
- Meta AI Blog: research.fb.com → research.facebook.com/blog/rss/
- DeepMind Blog: 新ドメインのRSSに更新
- TechCrunch Japan: AIカテゴリの安定版に変更
- BAIR Blog: HTTPSに変更

➕ NEW FEED SOURCES:
- AI News (artificialintelligence-news.com)
- Nature AI Research (machine learning papers)
- より安定したソースを追加

🛠️ TECHNICAL ENHANCEMENTS:
- Mozilla/Chrome User-Agent simulation
- HTTP status code checking (403 detection)
- Retry mechanism with exponential backoff
- Alternative User-Agent fallback
- Better error handling and logging

📊 EXPECTED RESULTS:
- 403エラーの大幅減少
- より多くのニュースソース取得成功
- フィード取得成功率の向上
- 安定したダッシュボード生成

🌟 USER BENEFITS:
- より豊富なニュースコンテンツ
- 安定したサイト更新
- 日本語タイトル翻訳機能
- クリック可能なSNS投稿

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"""
    
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print("✅ コミット完了")
    
    # Push to GitHub
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ GitHub Pages にプッシュ完了")
    
    print("\n🌐 403エラー修正版がライブ!")
    print("🔗 URL: https://awano27.github.io/daily-ai-news/")
    print("⏰ 変更は1-5分で反映されます")
    
    print("\n📋 実装された改善:")
    print("✅ 403 Forbiddenエラー対策")
    print("✅ User-Agent設定とリトライ機能")
    print("✅ フィードURL更新・修正")
    print("✅ 新規フィードソース追加")
    print("✅ 日本語タイトル翻訳機能")
    print("✅ クリック可能なSNS投稿")
    
    print("\n🔧 期待される改善:")
    print("• フィード取得成功率の大幅向上")
    print("• より多くのニュースソースからの情報取得")
    print("• 安定したダッシュボード生成")
    print("• 403エラーの大幅減少")
    
except subprocess.CalledProcessError as e:
    print(f"❌ エラー: {e}")
    if hasattr(e, 'stdout') and e.stdout:
        print(f"stdout: {e.stdout}")
    if hasattr(e, 'stderr') and e.stderr:  
        print(f"stderr: {e.stderr}")
    sys.exit(1)
except Exception as e:
    print(f"❌ 予期しないエラー: {e}")
    sys.exit(1)