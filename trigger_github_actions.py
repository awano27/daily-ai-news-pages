#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trigger GitHub Actions - GitHub Actionsを手動トリガー
"""
import subprocess
import time
from datetime import datetime

def check_git_status():
    """Git状況確認"""
    print("📊 Git Status Check")
    print("-" * 30)
    
    try:
        # 最新のコミット確認
        result = subprocess.run(['git', 'log', '--oneline', '-3'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print("📝 最新のコミット:")
            print(result.stdout)
        
        # リモートとの差分確認
        fetch_result = subprocess.run(['git', 'fetch', 'origin'], 
                                    capture_output=True, text=True)
        
        diff_result = subprocess.run(['git', 'diff', 'HEAD', 'origin/main'], 
                                   capture_output=True, text=True)
        
        if not diff_result.stdout.strip():
            print("✅ ローカルとリモートは同期済み")
        else:
            print("⚠️ ローカルとリモートに差分があります")
            
    except Exception as e:
        print(f"❌ Git確認エラー: {e}")

def trigger_workflow():
    """ワークフローを手動トリガー"""
    print("\n🚀 GitHub Actions Manual Trigger")
    print("-" * 30)
    
    # GitHub CLIを使用してワークフローをトリガー
    workflows = [
        'enhanced-daily-build.yml',
        'build.yml',
        'deploy-to-public.yml'
    ]
    
    for workflow in workflows:
        print(f"🔄 Triggering {workflow}...")
        
        try:
            result = subprocess.run([
                'gh', 'workflow', 'run', workflow
            ], capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ {workflow} triggered successfully")
            else:
                print(f"⚠️ {workflow} trigger failed: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏱️ {workflow} trigger timed out")
        except FileNotFoundError:
            print("❌ GitHub CLI (gh) not found")
            break
        except Exception as e:
            print(f"❌ {workflow} trigger error: {e}")
        
        time.sleep(2)  # 各ワークフロー間で少し待機

def create_simple_trigger():
    """シンプルなトリガーファイルを作成"""
    print("\n📄 Creating Simple Trigger")
    print("-" * 30)
    
    try:
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        trigger_file = f"trigger_{timestamp}.md"
        
        content = f"""# Manual Trigger - {timestamp}

This file triggers GitHub Actions workflows.

- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}
- Purpose: Force update Enhanced AI News site
- Target: https://awano27.github.io/daily-ai-news-pages/

## Fixes Applied:
- ✅ DOCTYPE declaration added
- ✅ Enhanced TabController with accessibility
- ✅ Digital.gov compliance metadata
- ✅ ARIA attributes for screen readers
- ✅ Keyboard navigation support

## Expected Result:
All HTML structure and tab functionality tests should pass.
"""
        
        with open(trigger_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ Created: {trigger_file}")
        
        # Git操作
        subprocess.run(['git', 'add', trigger_file], check=True)
        
        commit_msg = f"trigger: Manual update trigger - {timestamp}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Trigger file pushed to GitHub")
        
        # ファイルを削除（次回のため）
        import os
        os.remove(trigger_file)
        
        subprocess.run(['git', 'rm', trigger_file], check=True)
        subprocess.run(['git', 'commit', '-m', f'cleanup: Remove {trigger_file}'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("✅ Trigger file cleaned up")
        return True
        
    except Exception as e:
        print(f"❌ Trigger creation failed: {e}")
        return False

def show_manual_steps():
    """手動実行手順を表示"""
    print("\n📋 Manual Steps (if needed)")
    print("-" * 30)
    print("1. GitHub Actions手動実行:")
    print("   https://github.com/awano27/daily-ai-news/actions")
    print("   - 'Enhanced Daily AI News' を選択")
    print("   - 'Run workflow' ボタンをクリック")
    print()
    print("2. 別のアプローチ:")
    print("   - GitHub Pages設定確認")
    print("   - https://github.com/awano27/daily-ai-news/settings/pages")
    print()
    print("3. 直接確認:")
    print("   - https://awano27.github.io/daily-ai-news/")
    print("   - https://awano27.github.io/daily-ai-news-pages/")

def main():
    """メイン処理"""
    print("🚀 Trigger GitHub Actions - 手動更新トリガー")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # 1. Git状況確認
    check_git_status()
    
    # 2. ワークフロー手動トリガー
    trigger_workflow()
    
    # 3. シンプルトリガー作成
    if create_simple_trigger():
        print("\n🎉 Trigger Complete!")
        print("=" * 50)
        print("✅ GitHub Actionsがトリガーされました")
        print("✅ 5-10分後にサイトが更新される予定")
        print()
        print("🕐 待機中の確認方法:")
        print("1. GitHub Actions: https://github.com/awano27/daily-ai-news/actions")
        print("2. 5分後: python test_both_urls.py")
        print("3. 10分後: python install_and_test.py")
    
    # 4. 手動手順表示
    show_manual_steps()

if __name__ == "__main__":
    main()