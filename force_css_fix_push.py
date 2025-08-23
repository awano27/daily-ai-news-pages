#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Force push CSS fix to GitHub and trigger workflow
"""

import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, cwd=Path(__file__).parent, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - SUCCESS")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - FAILED")
            if result.stderr.strip():
                print(f"   Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} - EXCEPTION: {e}")
        return False

def main():
    print("🚀 Force CSS Fix Push for build_simple_ranking.py")
    print("=" * 60)
    
    # Add and commit changes
    if not run_command("git add build_simple_ranking.py", "Adding build script"):
        return False
    
    commit_msg = """fix: Add CSS generation to build_simple_ranking.py

✅ Build時にstyle.cssファイルを生成するよう修正
✅ スタイル崩れの原因（CSSファイル未生成）を解決  
✅ GitHub Actionsでの自動デプロイでCSSも正しく配信
✅ https://awano27.github.io/daily-ai-news-pages/ の表示修正

[skip ci]"""
    
    if not run_command(f'git commit -m "{commit_msg}"', "Committing changes"):
        print("ℹ️ No changes to commit or commit failed")
    
    # Push to GitHub
    if not run_command("git push origin main", "Pushing to GitHub"):
        return False
    
    print("\n📤 Changes pushed to GitHub!")
    
    # Try to trigger the enhanced workflow
    print("\n🎯 Attempting to trigger enhanced-daily-build.yml...")
    if run_command("gh workflow run enhanced-daily-build.yml", "Trigger enhanced workflow"):
        print("✅ Workflow triggered successfully!")
    else:
        print("⚠️ Could not trigger workflow automatically")
        print("👤 Please manually trigger:")
        print("1. Go to: https://github.com/awano27/daily-ai-news/actions")
        print("2. Click 'Enhanced Daily AI News (Full Pipeline)'")
        print("3. Click 'Run workflow' button")
    
    print("\n🎉 CSS fix deployment process initiated!")
    print("🔗 Target: https://awano27.github.io/daily-ai-news-pages/")
    print("⏳ Check in 3-5 minutes for updated styling")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)