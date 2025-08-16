#!/usr/bin/env python3
import subprocess
import sys
import os
import shutil

# Change to project directory
os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

print("🔄 Generating dashboard with clickable SNS posts...")

try:
    # Generate the dashboard
    result = subprocess.run([sys.executable, "generate_comprehensive_dashboard.py"], 
                          capture_output=True, text=True, check=True)
    print("✅ Dashboard generated successfully")
    print(result.stdout)
    
    # Copy dashboard.html to index.html
    if os.path.exists("dashboard.html"):
        shutil.copy2("dashboard.html", "index.html")
        print("✅ dashboard.html copied to index.html")
    else:
        print("❌ dashboard.html not found")
        sys.exit(1)
    
    # Git operations
    print("🔄 Committing changes...")
    subprocess.run(["git", "add", "index.html", "dashboard_data.json"], check=True)
    
    commit_message = """feat: Add clickable X/Twitter posts [skip ci]

ENHANCEMENT:
- X/Twitter posts are now clickable and link to original tweets
- Added URL support for both influencer posts and tech discussions  
- Improved user experience with hover effects (Twitter blue color)
- Maintains existing styling and layout

🤖 Generated with Claude Code

Co-Authored-By: Claude <noreply@anthropic.com>"""
    
    subprocess.run(["git", "commit", "-m", commit_message], check=True)
    print("✅ Changes committed")
    
    # Push to GitHub
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ Changes pushed to GitHub")
    
    print("\n🌐 Dashboard updated with clickable SNS posts!")
    print("🔗 URL: https://awano27.github.io/daily-ai-news/")
    print("⏰ Changes will be live in 1-5 minutes")
    
except subprocess.CalledProcessError as e:
    print(f"❌ Error: {e}")
    if hasattr(e, 'stdout') and e.stdout:
        print(f"stdout: {e.stdout}")
    if hasattr(e, 'stderr') and e.stderr:  
        print(f"stderr: {e.stderr}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Unexpected error: {e}")
    sys.exit(1)