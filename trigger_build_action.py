#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Trigger GitHub Actions workflow manually
"""

import subprocess
import json
import requests
import os
from pathlib import Path

def trigger_with_gh_cli():
    """Try to trigger using GitHub CLI"""
    print("🎯 Attempting to trigger GitHub Actions with gh CLI...")
    
    workflows = [
        "enhanced-daily-build.yml",
        "build.yml"
    ]
    
    for workflow in workflows:
        try:
            result = subprocess.run(
                f"gh workflow run {workflow}",
                shell=True,
                capture_output=True,
                text=True,
                cwd=Path(__file__).parent
            )
            
            if result.returncode == 0:
                print(f"✅ Successfully triggered {workflow}")
                print(f"Output: {result.stdout.strip()}")
                return True
            else:
                print(f"❌ Failed to trigger {workflow}")
                print(f"Error: {result.stderr.strip()}")
        except Exception as e:
            print(f"❌ Exception triggering {workflow}: {e}")
    
    return False

def check_github_status():
    """Check GitHub Actions status"""
    print("\n📊 Checking GitHub Actions status...")
    
    try:
        result = subprocess.run(
            "gh run list --limit 5",
            shell=True,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("Recent GitHub Actions runs:")
            print(result.stdout)
        else:
            print(f"❌ Could not check status: {result.stderr}")
    except Exception as e:
        print(f"❌ Exception checking status: {e}")

def main():
    print("🚀 Triggering GitHub Actions for Build Fix")
    print("=" * 50)
    
    # Try to trigger the workflow
    success = trigger_with_gh_cli()
    
    if success:
        print("\n✅ Workflow triggered successfully!")
        print("🔗 Monitor at: https://github.com/awano27/daily-ai-news/actions")
        print("⏳ Site will be updated in a few minutes")
        print("🌐 Check result at: https://awano27.github.io/daily-ai-news-pages/")
    else:
        print("\n⚠️ Could not trigger workflow automatically")
        print("👤 Please manually trigger the workflow:")
        print("1. Go to: https://github.com/awano27/daily-ai-news/actions")
        print("2. Click on 'Enhanced Daily AI News (Full Pipeline)'")  
        print("3. Click 'Run workflow' button")
        print("4. Click 'Run workflow' to start")
    
    # Check current status
    check_github_status()
    
    return success

if __name__ == "__main__":
    main()