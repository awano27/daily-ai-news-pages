#!/usr/bin/env python3
"""
Deploy script to push the working site to GitHub Pages
"""
import subprocess
import sys
import os

def run_command(cmd):
    """Run command and return success status"""
    try:
        print(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ Success: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error: {e.stderr}")
        return False

def main():
    """Deploy the working site to GitHub Pages"""
    print("🚀 Deploying working site to GitHub Pages")
    print("=" * 50)
    
    # Change to project directory
    os.chdir(r"C:\Users\yoshitaka\daily-ai-news")
    
    # Git operations
    commands = [
        "git add .",
        'git commit -m "feat: Complete tab functionality fix with working article display"',
        "git push origin main",
        "git push origin main:gh-pages --force"
    ]
    
    for cmd in commands:
        if not run_command(cmd):
            print(f"Failed at command: {cmd}")
            sys.exit(1)
    
    print("\n✅ Deployment completed!")
    print("🌐 Site will update at: https://awano27.github.io/daily-ai-news-pages/")
    print("🕐 Allow 2-5 minutes for changes to appear")

if __name__ == "__main__":
    main()