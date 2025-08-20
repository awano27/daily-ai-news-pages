#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete GitHub Setup - 最終GitHub設定ガイド
"""
import webbrowser
from datetime import datetime

def main():
    """最終GitHub設定ガイド"""
    print("🎯 Complete GitHub Setup - Final Steps")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    print("✅ Status Update:")
    print("- Deploy configuration: Fixed to gh-pages")
    print("- Repository sync: Ready")
    print("- Next: GitHub Pages & Secrets setup")
    print()
    
    print("=" * 60)
    print("🔧 STEP 1: Sync Repository")
    print("=" * 60)
    print("Run: final_sync_and_setup.bat")
    print("or manually:")
    print("  git pull origin main")
    print("  git push origin main")
    print()
    
    print("=" * 60)
    print("🌐 STEP 2: GitHub Pages Setup")
    print("=" * 60)
    pages_url = "https://github.com/awano27/daily-ai-news-pages/settings/pages"
    print(f"URL: {pages_url}")
    print()
    print("Settings:")
    print("✓ Source: Deploy from a branch")
    print("✓ Branch: gh-pages")
    print("✓ Folder: / (root)")
    print("✓ Click 'Save'")
    print()
    
    print("=" * 60)
    print("🔐 STEP 3: GitHub Secrets Setup")
    print("=" * 60)
    secrets_url = "https://github.com/awano27/daily-ai-news/settings/secrets/actions"
    print(f"URL: {secrets_url}")
    print()
    print("Required Secrets:")
    print("1. GEMINI_API_KEY = AIzaSyDf_VZIxpLvLZSrhPYH-0SqF7PwE2E5Cyo")
    print("2. PERSONAL_TOKEN = (Create at https://github.com/settings/tokens)")
    print("   - Permissions: repo (full control)")
    print()
    
    print("=" * 60)
    print("🚀 STEP 4: Test Execution")
    print("=" * 60)
    actions_url = "https://github.com/awano27/daily-ai-news/actions"
    print(f"URL: {actions_url}")
    print()
    print("Actions to take:")
    print("1. Select 'Enhanced Daily AI News Build (Gemini URL Context)'")
    print("2. Click 'Run workflow'")
    print("3. Branch: main → Click 'Run workflow'")
    print("4. Wait for completion (~5-10 minutes)")
    print("5. Verify deploy workflow runs automatically")
    print()
    
    print("=" * 60)
    print("🌐 STEP 5: Final Verification")
    print("=" * 60)
    site_url = "https://awano27.github.io/daily-ai-news-pages/"
    print(f"Site URL: {site_url}")
    print()
    print("Expected results:")
    print("✅ Enhanced AI News site displays")
    print("✅ X posts without duplicates")
    print("✅ Summaries within 300 characters")
    print("✅ Gemini enhancement markers (🧠)")
    print("✅ Automatic updates at 07:00 & 19:00 JST")
    print()
    
    print("🕐 Automatic Schedule:")
    print("- Daily 07:00 JST (22:00 UTC)")
    print("- Daily 19:00 JST (10:00 UTC)")
    print()
    
    # Open pages in browser
    answer = input("🌐 Open setup pages in browser? (y/n): ")
    if answer.lower() == 'y':
        print("\n🚀 Opening setup pages...")
        
        print("1. GitHub Pages settings...")
        webbrowser.open(pages_url)
        input("   Press Enter after configuring Pages settings...")
        
        print("2. GitHub Secrets settings...")
        webbrowser.open(secrets_url)
        input("   Press Enter after configuring Secrets...")
        
        print("3. GitHub Actions...")
        webbrowser.open(actions_url)
        print("   Run the Enhanced workflow manually!")
        input("   Press Enter after starting the workflow...")
        
        print("4. Final site check...")
        webbrowser.open(site_url)
        print("   ✅ All pages opened!")
    
    print("\n" + "=" * 60)
    print("🎉 SETUP COMPLETE CHECKLIST:")
    print("=" * 60)
    print("□ Repository synced")
    print("□ GitHub Pages set to gh-pages branch")
    print("□ GEMINI_API_KEY secret configured")
    print("□ PERSONAL_TOKEN secret configured")
    print("□ Enhanced workflow executed successfully")
    print("□ Site displaying at awano27.github.io/daily-ai-news-pages")
    print()
    print("When all items are checked (□ → ✅):")
    print("🚀 Enhanced AI News System will be fully operational!")
    print()
    print("Support URLs:")
    print(f"- Site: {site_url}")
    print(f"- Actions: {actions_url}")
    print(f"- Secrets: {secrets_url}")

if __name__ == "__main__":
    main()