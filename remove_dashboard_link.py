#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Remove Dashboard Link - 使用されていないダッシュボードリンクを削除
"""
import subprocess
from pathlib import Path
from datetime import datetime

def remove_dashboard_link():
    """HTMLからダッシュボードリンクを削除"""
    print("🔧 Removing Dashboard Link")
    print("-" * 30)
    
    if Path('index.html').exists():
        print("📝 index.html からダッシュボードリンクを削除中...")
        
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ダッシュボードリンクを含むnavセクションを削除
        import re
        
        # nav要素全体を削除
        nav_pattern = r'<nav class="nav-links">.*?</nav>'
        content = re.sub(nav_pattern, '', content, flags=re.DOTALL)
        
        # または、ダッシュボードリンクのみを削除
        dashboard_link_pattern = r'<a href="ai_news_dashboard\.html".*?</a>'
        content = re.sub(dashboard_link_pattern, '', content, flags=re.DOTALL)
        
        # 空になったnav要素も削除
        empty_nav_pattern = r'<nav class="nav-links">\s*</nav>'
        content = re.sub(empty_nav_pattern, '', content, flags=re.DOTALL)
        
        # ファイル保存
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ ダッシュボードリンク削除完了")
        return True
    else:
        print("❌ index.html が見つかりません")
        return False

def update_news_detail():
    """news_detail.htmlも同様に修正"""
    print("\n📝 news_detail.html も修正中...")
    
    if Path('news_detail.html').exists():
        with open('news_detail.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        
        # 同様の修正を適用
        nav_pattern = r'<nav class="nav-links">.*?</nav>'
        content = re.sub(nav_pattern, '', content, flags=re.DOTALL)
        
        dashboard_link_pattern = r'<a href="ai_news_dashboard\.html".*?</a>'
        content = re.sub(dashboard_link_pattern, '', content, flags=re.DOTALL)
        
        empty_nav_pattern = r'<nav class="nav-links">\s*</nav>'
        content = re.sub(empty_nav_pattern, '', content, flags=re.DOTALL)
        
        with open('news_detail.html', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ news_detail.html 修正完了")
        return True
    else:
        print("⚠️ news_detail.html が見つかりません")
        return False

def push_changes():
    """変更をGitHubにプッシュ"""
    print("\n📤 Push Changes to GitHub")
    print("-" * 30)
    
    try:
        # Git設定
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=False)
        subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], check=False)
        
        # ファイル追加
        subprocess.run(['git', 'add', '*.html'], check=True)
        
        # コミット
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M JST')
        commit_msg = f"""fix: Remove unused dashboard link from navigation - {timestamp}

🔧 UI CLEANUP:
✅ Removed outdated dashboard link from header navigation
✅ Prevents user confusion from non-functional links
✅ Cleaner, focused navigation experience
✅ Applied to both index.html and news_detail.html

🎯 Result: Streamlined navigation without broken links
🧹 Better user experience with working links only

[skip ci]"""

        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ コミット成功")
            
            # プッシュ
            push_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                       capture_output=True, text=True)
            
            if push_result.returncode == 0:
                print("✅ プッシュ成功")
                return True
            else:
                print(f"❌ プッシュ失敗: {push_result.stderr}")
                
                # リベース後に再プッシュ
                print("🔄 リベース後に再プッシュ...")
                subprocess.run(['git', 'pull', 'origin', 'main', '--rebase'], check=False)
                
                retry_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                            capture_output=True, text=True)
                
                if retry_result.returncode == 0:
                    print("✅ 再プッシュ成功")
                    return True
                else:
                    print(f"❌ 再プッシュ失敗: {retry_result.stderr}")
                    return False
        else:
            print("⚠️ 変更がないかコミット失敗")
            return False
            
    except Exception as e:
        print(f"❌ Git操作エラー: {e}")
        return False

def main():
    """メイン処理"""
    print("🧹 Remove Dashboard Link - ナビゲーション整理")
    print("=" * 60)
    print(f"開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # 1. ダッシュボードリンク削除
    success1 = remove_dashboard_link()
    
    # 2. news_detail.html修正
    success2 = update_news_detail()
    
    if success1:
        # 3. 変更をプッシュ
        if push_changes():
            print("\n" + "=" * 60)
            print("🎉 ナビゲーション整理完了！")
            print("=" * 60)
            print("✅ 未使用ダッシュボードリンク削除")
            print("✅ ナビゲーションを整理")
            print("✅ ユーザーの混乱を防止")
            print("✅ 動作するリンクのみに集約")
            print()
            print("🌐 確認URL:")
            print("https://awano27.github.io/daily-ai-news/")
            print()
            print("⏰ 約2-3分後にサイトが更新されます")
            print()
            print("📋 期待される結果:")
            print("- ヘッダーからダッシュボードリンクが消える")
            print("- シンプルで分かりやすいナビゲーション")
            print("- 動作するリンクのみでユーザビリティ向上")
        else:
            print("❌ プッシュ失敗 - 手動でgit pushを実行してください")
    else:
        print("❌ HTML修正失敗")

if __name__ == "__main__":
    main()