#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Build Template - build.pyのテンプレートからダッシュボードリンクを削除
"""
import subprocess
from pathlib import Path
from datetime import datetime
import re

def fix_build_py():
    """build.pyのHTMLテンプレートを修正"""
    print("🔧 Fixing build.py template")
    print("-" * 30)
    
    if Path('build.py').exists():
        print("📝 build.py を修正中...")
        
        with open('build.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # HTMLテンプレート内のダッシュボードリンクを削除
        # パターン1: nav要素全体を削除
        nav_patterns = [
            r'<nav class="nav-links">.*?</nav>',
            r'<nav class="nav-links">[^<]*<a href="ai_news_dashboard\.html"[^>]*>.*?</a>[^<]*</nav>',
        ]
        
        for pattern in nav_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # パターン2: ダッシュボードリンクのみを削除
        dashboard_patterns = [
            r'<a href="ai_news_dashboard\.html"[^>]*>.*?</a>',
            r'<a href="ai_news_dashboard\.html" class="nav-link">📊 ダッシュボード</a>',
        ]
        
        for pattern in dashboard_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # パターン3: 空になったnav要素を削除
        empty_nav_patterns = [
            r'<nav class="nav-links">\s*</nav>',
            r'<nav class="nav-links">\s*\n\s*</nav>',
        ]
        
        for pattern in empty_nav_patterns:
            content = re.sub(pattern, '', content, flags=re.DOTALL)
        
        # ファイル保存
        with open('build.py', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ build.py テンプレート修正完了")
        return True
    else:
        print("❌ build.py が見つかりません")
        return False

def verify_build_template():
    """build.pyの修正確認"""
    print("\n🔍 Verify build.py template")
    print("-" * 30)
    
    if Path('build.py').exists():
        with open('build.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # ダッシュボード関連要素をチェック
        dashboard_indicators = [
            'ai_news_dashboard.html',
            '📊 ダッシュボード',
            'nav-link.*ダッシュボード',
        ]
        
        found_count = 0
        for indicator in dashboard_indicators:
            if re.search(indicator, content):
                found_count += 1
                print(f"⚠️ Found: {indicator}")
        
        if found_count == 0:
            print("✅ build.py: No dashboard references found")
            return True
        else:
            print(f"❌ build.py: Still contains {found_count} dashboard references")
            return False
    else:
        print("❌ build.py not found")
        return False

def rebuild_site():
    """修正されたbuild.pyでサイトを再生成"""
    print("\n🚀 Rebuild site with fixed template")
    print("-" * 30)
    
    import os
    
    # 環境変数設定
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    
    try:
        import subprocess
        result = subprocess.run([
            'python', 'build.py'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Site rebuild successful")
            
            # index.htmlにコピー
            if Path('news_detail.html').exists():
                import shutil
                shutil.copy('news_detail.html', 'index.html')
                print("✅ index.html updated")
            
            return True
        else:
            print(f"❌ Build failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Rebuild error: {e}")
        return False

def commit_and_push():
    """修正をコミット・プッシュ"""
    print("\n📤 Commit and push template fix")
    print("-" * 30)
    
    try:
        # Git設定
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=False)
        subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], check=False)
        
        # ファイル追加
        subprocess.run(['git', 'add', 'build.py'], check=True)
        subprocess.run(['git', 'add', '*.html'], check=True)
        
        # コミット
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M JST')
        commit_msg = f"""fix: Remove dashboard link from build.py template - {timestamp}

🔧 BUILD TEMPLATE FIX:
✅ Removed dashboard link from HTML template in build.py
✅ Prevents regeneration of unused navigation links
✅ Ensures clean navigation on every rebuild
✅ Applied to both template and current HTML files

🎯 Result: No more dashboard links in future builds
🧹 Permanent fix for navigation cleanup

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
                print(f"⚠️ Push failed: {push_result.stderr}")
                
                # リベース後に再プッシュ
                print("🔄 Retrying after rebase...")
                subprocess.run(['git', 'pull', 'origin', 'main', '--rebase'], check=False)
                
                retry_result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                            capture_output=True, text=True)
                
                if retry_result.returncode == 0:
                    print("✅ Retry push successful")
                    return True
                else:
                    print(f"❌ Retry push failed: {retry_result.stderr}")
                    return False
        else:
            print("⚠️ Nothing to commit or commit failed")
            return False
            
    except Exception as e:
        print(f"❌ Git operation failed: {e}")
        return False

def main():
    """メイン処理"""
    print("🔧 Fix Build Template - build.pyテンプレート修正")
    print("=" * 60)
    print(f"開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # 1. build.pyテンプレート修正
    if fix_build_py():
        
        # 2. 修正確認
        if verify_build_template():
            
            # 3. サイト再生成
            if rebuild_site():
                
                # 4. コミット・プッシュ
                if commit_and_push():
                    print("\n" + "=" * 60)
                    print("🎉 Build Template Fix Complete!")
                    print("=" * 60)
                    print("✅ build.py template fixed")
                    print("✅ Dashboard links permanently removed")
                    print("✅ Site rebuilt with clean navigation")
                    print("✅ Changes pushed to GitHub")
                    print()
                    print("🌐 Site will update with:")
                    print("- Clean header without dashboard link")
                    print("- Simple 'Daily AI News' branding only")
                    print("- No broken or unused navigation")
                    print()
                    print("⏰ Site update: 2-3 minutes")
                    print("🔗 URL: https://awano27.github.io/daily-ai-news/")
                else:
                    print("❌ Push failed")
            else:
                print("❌ Rebuild failed")
        else:
            print("⚠️ Template still contains dashboard references")
    else:
        print("❌ Template fix failed")

if __name__ == "__main__":
    main()