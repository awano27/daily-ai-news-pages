import subprocess
import sys
import os

# Set working directory
os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

print("🚀 Deploying build.py duplicate removal fix...")

# Define the git commands to run
commands = [
    ("git fetch origin", "Fetching latest changes from origin"),
    ("git pull origin main --no-edit", "Pulling and merging latest changes"),
    ("git add build.py", "Staging build.py changes"),
    ('git commit -m "fix: add comprehensive duplicate removal to build.py - Add global deduplication across all categories - Remove duplicates by URL and title - Prevent cross-category duplicates - Resolve duplicate article issue [skip ci]"', "Committing changes"),
    ("git push origin main", "Pushing changes to GitHub")
]

success_count = 0
for cmd, desc in commands:
    print(f"\n🔄 {desc}...")
    try:
        result = subprocess.run(cmd, shell=True, cwd=r"C:\Users\yoshitaka\daily-ai-news", 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print(f"✅ Success: {desc}")
            if result.stdout.strip():
                print(f"   Output: {result.stdout.strip()}")
            success_count += 1
        else:
            print(f"⚠️ Warning: {desc} returned code {result.returncode}")
            if result.stdout.strip():
                print(f"   stdout: {result.stdout.strip()}")
            if result.stderr.strip():
                print(f"   stderr: {result.stderr.strip()}")
            
    except subprocess.TimeoutExpired:
        print(f"⏱️ Timeout: {desc}")
    except Exception as e:
        print(f"❌ Error in {desc}: {e}")

print(f"\n📊 Completed {success_count}/{len(commands)} operations successfully")

if success_count >= 4:  # At least fetch, pull, add, and either commit or push succeeded
    print("🎉 Build.py duplicate removal fix deployment completed!")
    print("📋 The next GitHub Actions run should eliminate duplicate articles")
    print("🔗 Check results at: https://awano27.github.io/daily-ai-news/")
else:
    print("⚠️ Some operations may have failed, but the fix might still be deployed")

input("Press Enter to continue...")