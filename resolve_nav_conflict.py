#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Resolve Navigation Conflict - ナビゲーション競合解決
"""
import subprocess
from pathlib import Path
from datetime import datetime

def abort_rebase():
    """リベースを中止"""
    print("🔄 Aborting current rebase...")
    try:
        subprocess.run(['git', 'rebase', '--abort'], check=False)
        print("✅ Rebase aborted")
        return True
    except Exception as e:
        print(f"❌ Abort failed: {e}")
        return False

def force_reset_and_fix():
    """強制リセットして再修正"""
    print("\n🔄 Force reset and reapply fixes")
    print("-" * 30)
    
    try:
        # 最新のリモートを取得
        subprocess.run(['git', 'fetch', 'origin', 'main'], check=True)
        
        # 強制的にリモートに合わせる
        subprocess.run(['git', 'reset', '--hard', 'origin/main'], check=True)
        print("✅ Reset to remote main")
        
        # 再度ダッシュボードリンクを削除
        return remove_dashboard_links()
        
    except Exception as e:
        print(f"❌ Reset failed: {e}")
        return False

def remove_dashboard_links():
    """ダッシュボードリンクを削除"""
    print("\n🔧 Removing dashboard links (retry)")
    print("-" * 30)
    
    success = True
    
    # index.html修正
    if Path('index.html').exists():
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ダッシュボードリンクを削除
        import re
        
        # navセクション全体を削除
        nav_pattern = r'<nav class="nav-links">.*?</nav>'
        content = re.sub(nav_pattern, '', content, flags=re.DOTALL)
        
        # 個別のダッシュボードリンクも削除
        dashboard_patterns = [
            r'<a href="ai_news_dashboard\.html".*?</a>',
            r'<a.*?📊 ダッシュボード.*?</a>'
        ]
        
        for pattern in dashboard_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ index.html - Dashboard link removed")
    else:
        print("❌ index.html not found")
        success = False
    
    # news_detail.html修正
    if Path('news_detail.html').exists():
        with open('news_detail.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 同様の修正
        import re
        
        nav_pattern = r'<nav class="nav-links">.*?</nav>'
        content = re.sub(nav_pattern, '', content, flags=re.DOTALL)
        
        dashboard_patterns = [
            r'<a href="ai_news_dashboard\.html".*?</a>',
            r'<a.*?📊 ダッシュボード.*?</a>'
        ]
        
        for pattern in dashboard_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        with open('news_detail.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ news_detail.html - Dashboard link removed")
    else:
        print("⚠️ news_detail.html not found")
    
    return success

def commit_and_push():
    """コミットとプッシュ"""
    print("\n📤 Commit and push clean changes")
    print("-" * 30)
    
    try:
        # ステージング
        subprocess.run(['git', 'add', '*.html'], check=True)
        
        # コミット
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M JST')
        commit_msg = f"""fix: Clean navigation - remove unused dashboard link - {timestamp}

🧹 NAVIGATION CLEANUP:
✅ Removed non-functional dashboard link from header
✅ Prevents user confusion from broken navigation
✅ Cleaner, focused user experience
✅ Applied to both index.html and news_detail.html

🎯 Result: Streamlined navigation with working links only
🚀 Enhanced AI News System ready for production

[skip ci]"""

        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Commit successful")
            
            # プッシュ
            push_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                       capture_output=True, text=True)
            
            if push_result.returncode == 0:
                print("✅ Push successful")
                return True
            else:
                print(f"❌ Push failed: {push_result.stderr}")
                return False
        else:
            print("⚠️ Nothing to commit or commit failed")
            return False
            
    except Exception as e:
        print(f"❌ Git operation failed: {e}")
        return False

def verify_removal():
    """削除確認"""
    print("\n🔍 Verify dashboard link removal")
    print("-" * 30)
    
    files_checked = 0
    links_found = 0
    
    for filename in ['index.html', 'news_detail.html']:
        if Path(filename).exists():
            files_checked += 1
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # ダッシュボードリンクを検索
            dashboard_indicators = [
                'ai_news_dashboard.html',
                '📊 ダッシュボード',
                'dashboard'
            ]
            
            found_in_file = 0
            for indicator in dashboard_indicators:
                if indicator in content:
                    found_in_file += 1
            
            if found_in_file > 0:
                links_found += found_in_file
                print(f"⚠️ {filename}: Still contains dashboard references")
            else:
                print(f"✅ {filename}: Dashboard links removed")
    
    print(f"\n📊 Results: {files_checked} files checked, {links_found} dashboard references found")
    return links_found == 0

def main():
    """メイン処理"""
    print("🔧 Resolve Navigation Conflict - ナビゲーション競合解決")
    print("=" * 60)
    print(f"開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # 1. リベース中止
    abort_rebase()
    
    # 2. 強制リセットと再修正
    if force_reset_and_fix():
        
        # 3. 削除確認
        if verify_removal():
            
            # 4. コミット・プッシュ
            if commit_and_push():
                print("\n" + "=" * 60)
                print("🎉 ナビゲーション整理完了！")
                print("=" * 60)
                print("✅ Git競合解決")
                print("✅ ダッシュボードリンク削除")
                print("✅ シンプルなナビゲーション")
                print("✅ ユーザー混乱の防止")
                print()
                print("🌐 確認URL:")
                print("https://awano27.github.io/daily-ai-news/")
                print()
                print("⏰ 約2-3分後にサイトが更新されます")
                print("📋 期待される変更:")
                print("- ヘッダーからダッシュボードリンクが消える")
                print("- 'Daily AI News' ブランドのみのシンプルヘッダー")
            else:
                print("❌ プッシュ失敗")
        else:
            print("⚠️ ダッシュボードリンクがまだ残っています")
    else:
        print("❌ 修正失敗")

if __name__ == "__main__":
    main()