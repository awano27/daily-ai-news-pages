#!/usr/bin/env python3
"""
Force push tab fix to GitHub - overwrite remote changes
"""
import subprocess
import os
from pathlib import Path

def main():
    try:
        os.chdir(Path(__file__).parent)
        
        print("💥 FORCE PUSH - Tab Fix to GitHub")
        print("=" * 50)
        print("⚠️ WARNING: This will overwrite remote changes!")
        print()
        
        # Check current status
        print("📋 Checking current status...")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("   📝 Uncommitted changes found, adding them...")
            subprocess.run(['git', 'add', '.'], check=True)
            
            commit_msg = "fix: Tab functionality repair - FORCE UPDATE - JavaScript hidden class logic"
            print("   💾 Committing all changes...")
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        else:
            print("   ✅ All changes already committed")
        
        # Show what will be pushed
        print("\n📊 Changes to be force pushed:")
        result = subprocess.run(['git', 'log', '--oneline', '-3'], 
                              capture_output=True, text=True)
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                print(f"   {line}")
        
        print(f"\n💥 FORCE PUSHING to origin/main...")
        print("   This will overwrite any remote changes!")
        
        # Force push
        result = subprocess.run(['git', 'push', '--force', 'origin', 'main'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ FORCE PUSH SUCCESSFUL!")
        else:
            print(f"   ❌ Force push failed: {result.stderr}")
            return False
        
        print("\n🎉 Tab Fix Force Deployed!")
        print("=" * 50)
        print("💥 Remote repository overwritten with your changes")
        print("✅ Tab functionality fix is now live on GitHub")
        print("✅ JavaScript hidden class logic applied")
        print("🔄 GitHub Actions will rebuild in ~30 seconds")
        
        print("\n📋 Your Tab Fix (5-10 minutes):")
        print("  🖱️ Business タブ → Business記事表示")
        print("  🖱️ Tools タブ → Tools記事表示")
        print("  🖱️ Posts タブ → SNS/論文ポスト表示")
        print("  🎨 CSS スタイリング正常適用")
        print("  📅 現在日付 (2025-08-23) 表示")
        
        print(f"\n🌐 Test: https://awano27.github.io/daily-ai-news-pages/")
        print("⏱️ Wait 5-10 minutes, then test tab clicking")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("⚠️ FORCE PUSH WARNING")
    print("This will overwrite remote changes without merging.")
    print("Are you sure? Press Ctrl+C to cancel, or Enter to continue...")
    try:
        input()
    except KeyboardInterrupt:
        print("\n❌ Force push cancelled.")
        exit(1)
    
    success = main()
    if success:
        print("\n💪 FORCE PUSH COMPLETE!")
        print("Your tab functionality fix is now deployed.")
        exit(0)
    else:
        exit(1)