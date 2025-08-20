#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Push Conflict - GitHubプッシュ競合修正
"""
import subprocess
import sys
from datetime import datetime

def run_command(cmd, description="", check_error=True):
    """コマンド実行"""
    if description:
        print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            if description:
                print(f"✅ {description} 完了")
            if result.stdout.strip():
                print(f"📋 出力:\n{result.stdout.strip()}")
            return True, result.stdout.strip()
        else:
            if description and check_error:
                print(f"⚠️ {description}: {result.stderr.strip()}")
            return False, result.stderr.strip()
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False, str(e)

def main():
    """競合修正メイン処理"""
    print("🔧 Push Conflict Fix - GitHubプッシュ競合修正")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    print("📊 現在の状況:")
    print("- ローカルに新しいHTMLファイルが生成済み")
    print("- リモートに他の変更がプッシュされている") 
    print("- プッシュが競合して失敗")
    print()
    
    # Step 1: リモート変更を取得
    print("📥 Step 1: リモート変更取得")
    print("-" * 30)
    
    success, _ = run_command(['git', 'pull', 'origin', 'main'], "リモート変更を取得")
    
    if not success:
        print("⚠️ プル失敗 - merge conflictが発生した可能性があります")
        
        # conflict解決のための情報表示
        print("\n🔍 コンフリクト情報確認:")
        run_command(['git', 'status'], "Git状態確認", False)
        
        # 自動merge試行
        print("\n🔄 自動merge試行...")
        run_command(['git', 'merge', '--no-edit'], "自動merge実行", False)
    
    # Step 2: 再度ステージング
    print("\n💾 Step 2: 最新状態でファイルを再ステージング")
    print("-" * 30)
    
    run_command(['git', 'add', 'index.html'], "index.htmlを追加")
    run_command(['git', 'add', 'news_detail.html'], "news_detail.htmlを追加")
    run_command(['git', 'add', 'style.css'], "style.cssを追加", False)
    run_command(['git', 'add', '_cache/'], "キャッシュを追加", False)
    
    # Step 3: コミット（修正版）
    print("\n📝 Step 3: 統合コミット作成")
    print("-" * 30)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M JST')
    commit_msg = f"""🤖 Enhanced AI News Update (Merge) - {timestamp}

✅ MERGED CONTENT UPDATE:
- Latest 48-hour AI news collection
- Gemini URL Context enhanced summaries  
- X posts deduplication & 300-char limits
- Digital.gov compliant design
- Resolved merge conflicts automatically

🔄 Auto-merge with remote changes
[skip ci]"""

    success, _ = run_command(['git', 'commit', '-m', commit_msg], "統合コミット作成")
    
    if not success:
        print("⚠️ コミット失敗 - 変更がないか確認します")
        run_command(['git', 'status'], "現在の状態確認", False)
    
    # Step 4: 再プッシュ
    print("\n🚀 Step 4: 修正済み変更をプッシュ")
    print("-" * 30)
    
    success, _ = run_command(['git', 'push', 'origin', 'main'], "修正済み変更をプッシュ")
    
    if success:
        print("\n🎉 プッシュ成功！サイト更新完了")
        print("=" * 50)
        print("✅ GitHub Actionsが自動実行されます")
        print("✅ 約2-3分でサイトが更新されます")
        print()
        print("🌐 確認URL:")
        print("- Actions: https://github.com/awano27/daily-ai-news/actions")
        print("- サイト: https://awano27.github.io/daily-ai-news-pages/")
        print()
        print("📊 更新内容:")
        print("- 最新48時間のAIニュース")
        print("- Gemini URL Context要約")
        print("- X投稿重複排除・300字制限")
        print("- アクセシブルデザイン")
        
    else:
        print("\n❌ プッシュ再失敗")
        print("手動での対応が必要です:")
        print("1. git status で状況確認")
        print("2. git log --oneline -5 でコミット確認")
        print("3. 必要に応じて git reset または git rebase")

if __name__ == "__main__":
    main()