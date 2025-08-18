#!/usr/bin/env python3
"""
Simple script to push the build.py duplicate removal fix
"""
import subprocess
import os
import sys

def run_cmd(cmd, description=""):
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8', errors='ignore')
        if result.stdout:
            print(f"✅ {result.stdout.strip()}")
        if result.stderr:
            print(f"⚠️ stderr: {result.stderr.strip()}")
        if result.returncode != 0:
            print(f"❌ Command failed with return code {result.returncode}")
            return False
        return True
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

def main():
    # Change to project directory
    os.chdir(r"C:\Users\yoshitaka\daily-ai-news")
    
    print("🚀 Pushing build.py duplicate removal fix to GitHub...")
    
    # Fetch latest changes
    run_cmd("git fetch origin", "Fetching latest changes")
    
    # Pull with merge (handle conflicts automatically)
    run_cmd("git pull origin main --no-edit", "Pulling and merging changes")
    
    # Check status
    run_cmd("git status", "Checking Git status")
    
    # Add build.py 
    run_cmd("git add build.py", "Staging build.py changes")
    
    # Commit the fix
    commit_msg = """fix: add comprehensive duplicate removal to build.py

- Add global deduplication across all categories (Business, Tools, Posts)
- Remove duplicates by both URL and title before category processing
- Prevent same articles from appearing in multiple categories
- Maintain original X posts integration with duplicate checking
- This should finally resolve the duplicate article issue

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"""
    
    if run_cmd(f'git commit -m "{commit_msg}"', "Committing duplicate removal fix"):
        print("✅ Commit successful!")
        
        # Push to remote
        if run_cmd("git push origin main", "Pushing to GitHub"):
            print("\n🎉 SUCCESS! build.py duplicate removal fix pushed to GitHub!")
            print("📋 Next GitHub Actions run should eliminate duplicate articles.")
            print("🔗 Check the results at: https://awano27.github.io/daily-ai-news/")
            return True
        else:
            print("❌ Push failed")
            return False
    else:
        print("⚠️ Commit failed or no changes to commit")
        # Try to push anyway in case changes are already staged
        if run_cmd("git push origin main", "Attempting to push existing changes"):
            print("✅ Push successful!")
            return True
        return False

if __name__ == "__main__":
    success = main()
    input("Press Enter to exit...")
    sys.exit(0 if success else 1)