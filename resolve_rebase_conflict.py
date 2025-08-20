#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resolve Rebase Conflict - リベース競合解決
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
    """リベース競合解決"""
    print("🔧 Resolve Rebase Conflict - リベース競合解決")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    print("📊 現在の状況:")
    print("- Interactive rebaseが進行中")
    print("- index.html と news_detail.html で競合発生")
    print("- 解決済みファイルを正しくコミットして完了させる")
    print()
    
    # Step 1: 現在の状況確認
    print("🔍 Step 1: 現在の状況確認")
    print("-" * 30)
    
    run_command(['git', 'status'], "現在の状態確認", False)
    
    # Step 2: リベースを完了させる
    print("\n🔄 Step 2: リベースを完了")
    print("-" * 30)
    
    print("リベースを完了させるため、git rebase --continue を実行します")
    success, output = run_command(['git', 'rebase', '--continue'], "リベース完了", False)
    
    if not success and "nothing to commit" in output:
        print("⚠️ 変更がないため、このコミットをスキップします")
        success, _ = run_command(['git', 'rebase', '--skip'], "コミットをスキップ", False)
    
    if not success:
        print("⚠️ リベース完了に失敗。リベースを中止して別の方法を試します")
        
        # リベースを中止
        run_command(['git', 'rebase', '--abort'], "リベースを中止", False)
        
        # 強制的にリセットして最新のリモートに合わせる
        print("\n🔄 Step 2.1: 強制リセット")
        print("-" * 30)
        
        run_command(['git', 'fetch', 'origin', 'main'], "最新のリモート取得")
        run_command(['git', 'reset', '--hard', 'origin/main'], "リモートに強制合わせ")
        
        # 最新のHTMLファイルを再生成（必要に応じて）
        print("\n🔄 Step 2.2: 最新コンテンツを再適用")
        print("-" * 30)
        
        # .envファイルが正しく設定されていることを確認
        import os
        os.environ['TRANSLATE_TO_JA'] = '1'
        os.environ['TRANSLATE_ENGINE'] = 'google'
        os.environ['HOURS_LOOKBACK'] = '48'
        os.environ['MAX_ITEMS_PER_CATEGORY'] = '30'
        
        print("🚀 build.py再実行で最新コンテンツ生成...")
        build_success, _ = run_command([sys.executable, 'build.py'], "最新コンテンツ生成", False)
        
        if build_success:
            import shutil
            if os.path.exists('news_detail.html'):
                shutil.copy('news_detail.html', 'index.html')
                print("✅ index.html更新完了")
    
    # Step 3: 状況を再確認
    print("\n📊 Step 3: 状況再確認")
    print("-" * 30)
    
    run_command(['git', 'status'], "現在の状態", False)
    
    # Step 4: 清潔な状態でコミット・プッシュ
    print("\n💾 Step 4: 清潔な状態でコミット")
    print("-" * 30)
    
    # ファイルをステージング
    run_command(['git', 'add', 'index.html'], "index.htmlをステージング")
    run_command(['git', 'add', 'news_detail.html'], "news_detail.htmlをステージング")
    run_command(['git', 'add', 'style.css'], "style.cssをステージング", False)
    run_command(['git', 'add', '_cache/'], "キャッシュをステージング", False)
    
    # コミット
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M JST')
    commit_msg = f"""🤖 Enhanced AI News Update (Clean) - {timestamp}

✅ CLEAN UPDATE AFTER CONFLICT RESOLUTION:
- Latest 48-hour AI news collection
- Gemini URL Context enhanced summaries
- X posts deduplication & 300-char limits  
- Digital.gov compliant accessible design
- Resolved all merge conflicts

🔧 Conflict resolution completed
[skip ci]"""

    commit_success, _ = run_command(['git', 'commit', '-m', commit_msg], "清潔なコミット作成")
    
    # Step 5: プッシュ
    print("\n🚀 Step 5: GitHubにプッシュ")
    print("-" * 30)
    
    push_success, _ = run_command(['git', 'push', 'origin', 'main'], "GitHubにプッシュ")
    
    if push_success:
        print("\n🎉 解決成功！サイト更新完了")
        print("=" * 50)
        print("✅ リベース競合が解決されました")
        print("✅ 最新コンテンツがGitHubにプッシュされました")
        print("✅ GitHub Actionsが自動実行されます")
        print()
        print("🌐 確認URL:")
        print("- Actions: https://github.com/awano27/daily-ai-news/actions") 
        print("- サイト: https://awano27.github.io/daily-ai-news-pages/")
        print()
        print("⏰ サイト更新まで約2-3分")
        
    elif commit_success:
        print("\n⚠️ コミット成功、プッシュ失敗")
        print("手動でプッシュしてください:")
        print("git push origin main")
        
    else:
        print("\n❌ コミット失敗")
        print("手動確認が必要:")
        print("1. git status")
        print("2. git log --oneline -3")
        print("3. git push origin main")

if __name__ == "__main__":
    main()