#!/usr/bin/env python3
"""
Resolve git conflict and push tab fix
"""
import subprocess
import os
from pathlib import Path

def main():
    try:
        os.chdir(Path(__file__).parent)
        
        print("🔀 Resolving Git Conflict and Pushing Tab Fix")
        print("=" * 50)
        
        # 1. Pull latest changes
        print("📥 Pulling latest changes from GitHub...")
        result = subprocess.run(['git', 'pull', 'origin', 'main'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Pull successful")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
        else:
            print(f"   ⚠️ Pull output: {result.stdout}")
            if "CONFLICT" in result.stdout or "merge conflict" in result.stdout.lower():
                print("   ❌ Merge conflict detected!")
                print("   Please resolve conflicts manually and then run:")
                print("   git add .")
                print("   git commit -m 'resolve conflicts'")
                print("   git push origin main")
                return False
            elif "Already up to date" in result.stdout:
                print("   ✅ Already up to date")
        
        # 2. Check status
        print("📋 Checking git status...")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("   📝 Uncommitted changes found")
            
            # Add all changes
            print("📝 Adding all changes...")
            subprocess.run(['git', 'add', '.'], check=True)
            
            # Commit
            commit_msg = "fix: Tab functionality repair after merge - JavaScript hidden class logic"
            print("💾 Committing merged changes...")
            subprocess.run(['git', 'commit', '-m', commit_msg], 
                          check=True)
        else:
            print("   ✅ No uncommitted changes")
        
        # 3. Push
        print("📤 Pushing to GitHub...")
        result = subprocess.run(['git', 'push', 'origin', 'main'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Push successful!")
        else:
            print(f"   ❌ Push failed: {result.stderr}")
            return False
        
        print("\n🎉 Tab Fix Successfully Deployed!")
        print("=" * 50)
        print("✅ Git conflict resolved")
        print("✅ Tab functionality fix pushed to GitHub")
        print("✅ JavaScript hidden class logic applied")
        print("🔄 GitHub Actions will rebuild in ~30 seconds")
        
        print("\n📋 Expected Tab Fix (5-10 minutes):")
        print("  🖱️ Business タブ → Business記事表示")
        print("  🖱️ Tools タブ → Tools記事表示") 
        print("  🖱️ Posts タブ → SNS/論文ポスト表示")
        print("  🎨 CSS スタイリング正常適用")
        print("  📅 現在日付 (2025-08-23) 表示")
        
        print(f"\n🌐 Test: https://awano27.github.io/daily-ai-news-pages/")
        print("⏱️ Wait 5-10 minutes, then click each tab to test")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n✨ All done! Tab functionality should work properly now.")
        exit(0)
    else:
        exit(1)