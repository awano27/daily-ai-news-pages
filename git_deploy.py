#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python script to deploy changes to GitHub using subprocess
Workaround for bash environment issues
"""
import subprocess
import sys
from datetime import datetime, timezone, timedelta

def run_cmd(cmd, description=""):
    """Run a command and return the result"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        if result.stdout:
            print(f"✅ {result.stdout.strip()}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ エラー: {e}")
        if e.stdout:
            print(f"出力: {e.stdout}")
        if e.stderr:
            print(f"エラー詳細: {e.stderr}")
        return False

def main():
    print("=" * 60)
    print("🚀 GitHub デプロイスクリプト (Python版)")
    print("=" * 60)
    
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    timestamp = now.strftime('%Y-%m-%d %H:%M JST')
    
    # Git status check
    run_cmd("git status", "Git状態確認")
    
    # Add files
    files_to_add = [
        'index.html',
        'news_detail.html', 
        'dashboard_data.json',
        'build.py',
        'generate_comprehensive_dashboard.py',
        'auto_update_all.py'
    ]
    
    print("\n📤 ファイルをステージング中...")
    for file in files_to_add:
        run_cmd(f'git add "{file}"', f"  {file} を追加")
    
    # Commit
    commit_msg = f"""feat: Force update AI news site [{timestamp}] [skip ci]

🚀 Complete Site Update:
- Updated dashboard with 312 news items
- Enhanced with 271 X/Twitter posts from Google Sheets  
- Fixed reference links (LLM Arena, AlphaXiv, Trend Words)
- Comprehensive executive summary and industry insights

📊 Key Metrics:
- Total news: 312 items across 3 categories
- SNS posts: 271 items with importance scoring
- Active companies: Meta(5), Amazon(5), NVIDIA(5), OpenAI(3)

🎯 Site Structure:
- index.html: Executive dashboard (landing page)
- news_detail.html: Detailed news articles

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"""
    
    print("\n💾 コミット中...")
    if run_cmd(f'git commit -m "{commit_msg}"', "変更をコミット"):
        print("✅ コミット成功")
    
    # Push to remote
    print("\n🌐 GitHubへプッシュ中...")
    if run_cmd("git push origin main", "リモートへプッシュ"):
        print("✅ プッシュ成功")
        
        print("\n" + "=" * 60)
        print("🎉 デプロイ完了!")
        print("=" * 60)
        print("\n🌐 サイトURL:")
        print("  https://awano27.github.io/daily-ai-news/")
        print("\n⏰ 反映時間:")
        print("  • GitHub Pages: 通常1-5分で反映")
        print("  • CDN キャッシュ: 最大10分")
        print("  • ブラウザキャッシュ: Ctrl+F5 で強制更新")
        print("\n💡 反映されない場合:")
        print("  1. 5分待ってからブラウザで Ctrl+F5")
        print("  2. シークレットモードでアクセス")
        print("  3. GitHub リポジトリの Actions タブでビルド状況を確認")
        
        return True
    else:
        print("❌ プッシュ失敗")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)