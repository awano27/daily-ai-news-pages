#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy AI News Dashboard to GitHub
"""
import subprocess
import sys
from pathlib import Path
from datetime import datetime

def main():
    print("==" * 30)
    print("🚀 AIニュースダッシュボードをGitHubにデプロイ")
    print("==" * 30)
    
    try:
        # Check if dashboard exists
        dashboard_file = Path('ai_news_dashboard.html')
        if not dashboard_file.exists():
            print("❌ ai_news_dashboard.html が見つかりません")
            return False
        
        print(f"📁 ダッシュボードファイル: {dashboard_file.stat().st_size:,} bytes")
        
        # Git add all dashboard-related files
        files_to_add = [
            'ai_news_dashboard.html',
            'dashboard_data.json',
            'generate_dashboard.py',
            'run_dashboard.py',
            'run_dashboard_direct.py',
            'test_dashboard_fix.py',
            'build.py'  # Modified with get_category fix
        ]
        
        print("\n📝 Gitに追加するファイル:")
        for file in files_to_add:
            if Path(file).exists():
                print(f"  ✓ {file}")
        
        # Add files
        print("\n🔧 Git add 実行中...")
        subprocess.run(['git', 'add'] + files_to_add, check=True)
        
        # Create commit message
        now = datetime.now()
        commit_msg = f"""feat: Add AI News Dashboard with analytics

🎯 New Features:
- Interactive AI news dashboard (ai_news_dashboard.html)
- Real-time statistics and trends analysis
- Category-wise news distribution
- Trending keywords visualization
- Top news sources tracking

🔧 Technical updates:
- Fixed build.get_category module access issue
- Added dashboard generation scripts
- Enhanced data analysis capabilities

📊 Dashboard includes:
- Total article count across all categories
- Source distribution analysis
- Keyword trending metrics
- Recent topics by category

Generated at {now.strftime('%Y-%m-%d %H:%M JST')}

[skip ci]"""
        
        # Commit
        print("\n💾 Git commit 実行中...")
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Push
        print("\n📤 GitHub へプッシュ中...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("\n" + "==" * 30)
        print("✅ デプロイ完了!")
        print("==" * 30)
        print("\n🌐 ダッシュボードURL:")
        print("   https://awano27.github.io/daily-ai-news/ai_news_dashboard.html")
        print("\n📊 メインサイト:")
        print("   https://awano27.github.io/daily-ai-news/")
        print("\n✨ AIニュースダッシュボードがGitHub Pagesで公開されました!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Git操作エラー: {e}")
        print("\n手動でデプロイする場合は以下のコマンドを実行してください:")
        print("git add ai_news_dashboard.html dashboard_data.json generate_dashboard.py run_dashboard.py run_dashboard_direct.py test_dashboard_fix.py build.py")
        print("git commit -m 'feat: Add AI News Dashboard with analytics'")
        print("git push origin main")
        return False
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)