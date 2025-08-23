#!/usr/bin/env python3
"""
Trigger GitHub Actions workflow to deploy the site
"""
import requests
import os
import json

def trigger_workflow():
    """Trigger the GitHub Actions workflow"""
    # GitHub API endpoint for workflow dispatch
    url = "https://api.github.com/repos/awano27/daily-ai-news-pages/actions/workflows/deploy-pages.yml/dispatches"
    
    # Headers for the request
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {os.environ.get('GITHUB_TOKEN', '')}",
        "User-Agent": "Python-Deploy-Script"
    }
    
    # Payload for manual trigger
    payload = {
        "ref": "main",
        "inputs": {}
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 204:
            print("✅ GitHub Actions workflow triggered successfully!")
            print("🌐 Check: https://github.com/awano27/daily-ai-news-pages/actions")
            print("🕐 Site will update in 2-5 minutes")
        else:
            print(f"❌ Failed to trigger workflow: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Error triggering workflow: {e}")

if __name__ == "__main__":
    print("🚀 Triggering GitHub Actions deployment...")
    trigger_workflow()