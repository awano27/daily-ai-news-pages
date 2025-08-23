#!/usr/bin/env python3
"""
Manual git commit and push to trigger GitHub Actions
"""
import subprocess
import os
from pathlib import Path

def main():
    try:
        os.chdir(Path(__file__).parent)
        
        print("🔧 Manual Git Operations")
        print("=" * 40)
        
        # Check git status
        print("1. Git Status:")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("   Files to commit:")
            for line in result.stdout.strip().split('\n'):
                print(f"     {line}")
        else:
            print("   No changes detected")
        
        # Add the trigger file
        print("\n2. Adding trigger file:")
        subprocess.run(['git', 'add', 'trigger_build_20250823.txt'], 
                      capture_output=True, text=True, check=True)
        print("   ✅ Added trigger_build_20250823.txt")
        
        # Commit
        print("\n3. Committing:")
        commit_msg = "trigger: Force GitHub Actions rebuild - 2025-08-23"
        subprocess.run(['git', 'commit', '-m', commit_msg], 
                      capture_output=True, text=True, check=True)
        print(f"   ✅ Committed: {commit_msg}")
        
        # Push
        print("\n4. Pushing to GitHub:")
        subprocess.run(['git', 'push', 'origin', 'main'], 
                      capture_output=True, text=True, check=True)
        print("   ✅ Pushed to origin/main")
        
        print("\n🎉 Manual trigger completed!")
        print("🔄 GitHub Actions should start in ~30 seconds")
        print("📈 Expected result: Site updated with 2025-08-23 date")
        print("🌐 Check: https://awano27.github.io/daily-ai-news-pages/")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git command failed: {e}")
        if e.stderr:
            print(f"   Error: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n💡 Next steps:")
        print("- Wait 5-10 minutes for GitHub Actions to complete")
        print("- Check https://awano27.github.io/daily-ai-news-pages/")
        print("- Look for date 2025-08-23 in the updated site")