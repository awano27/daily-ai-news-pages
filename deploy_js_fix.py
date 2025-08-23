#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy JavaScript tab fix to GitHub
"""

import os
import subprocess
import sys

def run_command(cmd):
    """Run shell command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    os.chdir(r"C:\Users\yoshitaka\daily-ai-news")
    
    print("🔧 JavaScript タブ機能修正をデプロイ中...")
    
    # Git add
    print("📝 index.htmlをコミット...")
    success, stdout, stderr = run_command("git add index.html")
    if not success:
        print(f"❌ Git add failed: {stderr}")
        return False
    
    # Git commit
    commit_msg = """fix: Add inline JavaScript for tab functionality and fix HTML structure

🔧 タブ機能修正:
✅ インラインJavaScriptでタブ切り替え機能追加
✅ HTML構造の破損修正
✅ フィルタリング機能の修正
✅ タブのアクティブ状態管理

🎯 効果:
• タブクリックで正しくコンテンツ切り替え
• Business/Tools/Postsタブの完全動作
• フィルタリング機能正常化

🧪 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
    
    success, stdout, stderr = run_command(f'git commit -m "{commit_msg}"')
    if not success:
        print(f"❌ Git commit failed: {stderr}")
        return False
    
    # Git push
    print("📤 GitHubにプッシュ...")
    success, stdout, stderr = run_command("git push origin main")
    if not success:
        print(f"❌ Git push failed: {stderr}")
        return False
    
    print("\n✅ タブ機能修正版がGitHub Pagesにデプロイ完了!")
    print("🔗 https://awano27.github.io/daily-ai-news/")
    print("\n🎉 修正内容:")
    print("• タブ切り替え完全動作")
    print("• コンテンツ表示正常化")
    print("• フィルタリング機能修復")
    print("• ユーザビリティ向上")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)