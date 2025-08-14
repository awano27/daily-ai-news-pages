#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sync with remote and deploy dashboard
"""
import subprocess
import sys
from pathlib import Path

def main():
    print("=" * 60)
    print("🔄 GitHubと同期してダッシュボードをデプロイ")
    print("=" * 60)
    
    try:
        # Step 1: Pull latest changes
        print("\n1️⃣ リモートの変更を取得中...")
        subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], check=True)
        print("✅ 最新の変更を取得しました")
        
        # Step 2: Check dashboard files exist
        dashboard_file = Path('ai_news_dashboard.html')
        if not dashboard_file.exists():
            print("❌ ai_news_dashboard.html が見つかりません")
            print("先に python run_dashboard_direct.py を実行してください")
            return False
        
        # Step 3: Push to GitHub
        print("\n2️⃣ GitHub へプッシュ中...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("\n" + "=" * 60)
        print("✅ デプロイ完了!")
        print("=" * 60)
        print("\n🌐 ダッシュボードURL:")
        print("   https://awano27.github.io/daily-ai-news/ai_news_dashboard.html")
        print("\n📊 メインサイト:")
        print("   https://awano27.github.io/daily-ai-news/")
        print("\n✨ AIニュースダッシュボードがGitHub Pagesで公開されました!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Git操作エラー: {e}")
        
        # エラー時の手動手順を提示
        print("\n📋 手動で解決する場合:")
        print("1. git pull origin main")
        print("2. コンフリクトがある場合は解決")
        print("3. git push origin main")
        
        return False
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)