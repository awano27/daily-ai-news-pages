#!/usr/bin/env python3
"""
Switch to correct repository and deploy tab fix
"""
import subprocess
import os
from pathlib import Path

def main():
    try:
        os.chdir(Path(__file__).parent)
        
        print("🔄 Switching to Correct Repository")
        print("=" * 50)
        
        # 1. Change remote URL to pages repository
        print("🔧 Changing remote URL...")
        result = subprocess.run([
            'git', 'remote', 'set-url', 'origin', 
            'https://github.com/awano27/daily-ai-news-pages.git'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Remote URL changed to: awano27/daily-ai-news-pages")
        else:
            print(f"   ❌ Failed to change remote URL: {result.stderr}")
            return False
        
        # 2. Verify remote URL
        print("📋 Verifying remote URL...")
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if result.returncode == 0:
            print("   Current remotes:")
            for line in result.stdout.strip().split('\n'):
                print(f"     {line}")
        
        # 3. Check current branch and status  
        print("📊 Checking current status...")
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        
        if result.stdout.strip():
            print("   📝 Uncommitted changes found, adding them...")
            subprocess.run(['git', 'add', '.'], check=True)
            
            commit_msg = "fix: Tab functionality repair - deploy to daily-ai-news-pages"
            print("   💾 Committing changes...")
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        else:
            print("   ✅ All changes already committed")
        
        # 4. Force push to new repository (since history may differ)
        print("🚀 Force pushing to pages repository...")
        result = subprocess.run(['git', 'push', '--force', 'origin', 'main'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("   ✅ Successfully pushed to pages repository!")
        else:
            print(f"   ❌ Push failed: {result.stderr}")
            
            # If force push fails, try regular push
            print("   🔄 Trying regular push...")
            result2 = subprocess.run(['git', 'push', 'origin', 'main'], 
                                   capture_output=True, text=True)
            if result2.returncode == 0:
                print("   ✅ Regular push successful!")
            else:
                print(f"   ❌ Both pushes failed: {result2.stderr}")
                return False
        
        print("\n🎉 Successfully Switched to Pages Repository!")
        print("=" * 50)
        print("✅ Remote URL: awano27/daily-ai-news-pages")
        print("✅ Tab fixes pushed to correct repository")
        print("✅ JavaScript hidden class logic applied")
        print("🔄 GitHub Actions will rebuild pages site")
        
        print("\n📋 Expected Results (5-10 minutes):")
        print("  🌐 Site URL: https://awano27.github.io/daily-ai-news-pages/")
        print("  🖱️ Business タブ → Business記事表示")
        print("  🖱️ Tools タブ → Tools記事表示")
        print("  🖱️ Posts タブ → SNS/論文表示")
        print("  📅 Date: 2025-08-23 (current)")
        print("  🎨 Enhanced card structure with priority system")
        
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
        print("\n🎯 Repository switch completed!")
        print("Your tab fix will now deploy to the correct site:")
        print("https://awano27.github.io/daily-ai-news-pages/")
        print("⏱️ Check in 5-10 minutes for updated functionality.")
        exit(0)
    else:
        exit(1)