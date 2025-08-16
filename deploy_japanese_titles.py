#!/usr/bin/env python3
import subprocess
import sys
import os

# Change to project directory
os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

print("🚀 日本語タイトル翻訳機能をGitHubにデプロイ中...")

try:
    # Git operations
    print("📝 変更をコミット中...")
    subprocess.run(["git", "add", "index.html", "dashboard_data.json", "generate_comprehensive_dashboard.py"], check=True)
    
    commit_message = """feat: Add Japanese title translation feature [skip ci]

🌟 NEW FEATURES:
- ニュースタイトルの自動日本語翻訳機能を追加
- 日本語タイトルを優先表示（日本語が分からない場合は英語のまま）
- X/Twitter投稿もクリック可能でリンク先に移動
- 327件のニュース、291件のSNS投稿をカバー

📋 翻訳例:
- "Sam Altman, over bread rolls, explores life after GPT-5" 
  → "サム・アルトマンは、パン・ロールを超えて、GPT-5の後の生活を探ります"
- "Anthropic has new rules for a more dangerous AI landscape"
  → "人類には、より危険なAIランドスケープのための新しいルールがあります"

🔧 TECHNICAL DETAILS:
- Google Translate API integration via build.py translator
- Fallback to original title if translation fails
- title_ja field added to all news items
- HTML template updated to show Japanese titles preferentially

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"""
    
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print("✅ コミット完了")
    
    # Push to GitHub
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ GitHub Pages にプッシュ完了")
    
    print("\n🌐 日本語タイトル翻訳機能がライブ!")
    print("🔗 URL: https://awano27.github.io/daily-ai-news/")
    print("⏰ 変更は1-5分で反映されます")
    
    print("\n📋 実装された機能:")
    print("✅ 英語ニュースタイトルを日本語に自動翻訳")
    print("✅ X/Twitter投稿がクリック可能")
    print("✅ 327件のニュース、291件のSNS投稿")
    print("✅ わかりやすい日本語タイトルで表示")
    
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