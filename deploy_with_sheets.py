#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy with live Google Sheets integration
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("Deploying with Live Google Sheets Integration")
    print("=" * 60)
    
    # Set environment for production
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    
    try:
        # Step 1: Test Google Sheets access
        print("Step 1: Testing Google Sheets access...")
        import build
        
        google_sheets_url = build.GOOGLE_SHEETS_URL
        print(f"Google Sheets URL: {google_sheets_url}")
        
        # Quick test of data access
        try:
            x_posts = build.gather_x_posts(google_sheets_url)
            if x_posts:
                print(f"✓ Successfully accessed Google Sheets with {len(x_posts)} posts")
                
                # Show most recent post
                if x_posts:
                    latest = max(x_posts, key=lambda x: x['_dt'])
                    print(f"✓ Latest post: {latest['title']} ({latest['_dt'].strftime('%Y-%m-%d %H:%M')})")
            else:
                print("⚠ Warning: No posts found in Google Sheets")
        except Exception as e:
            print(f"⚠ Warning: Google Sheets access issue: {e}")
            print("Proceeding with build anyway...")
        
        # Step 2: Build site
        print("\nStep 2: Building site with live Google Sheets data...")
        build.main()
        
        # Step 3: Verify build
        if Path('index.html').exists():
            size = Path('index.html').stat().st_size
            print(f"\n✓ Site built successfully ({size:,} bytes)")
            
            # Quick content check
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Count content sections
                business_cards = content.count('<article class="card">', 0, content.find('id="tools"'))
                tools_cards = content.count('<article class="card">', content.find('id="tools"'), content.find('id="posts"'))
                posts_cards = content.count('<article class="card">', content.find('id="posts"'))
                
                print(f"✓ Content summary:")
                print(f"  - Business: {business_cards} articles")
                print(f"  - Tools: {tools_cards} articles")
                print(f"  - Posts/SNS: {posts_cards} items (from Google Sheets)")
                
                # Check timestamp
                if '最終更新：' in content:
                    start = content.find('最終更新：') + 5
                    end = content.find('</div>', start)
                    timestamp = content[start:end].strip()
                    print(f"✓ Updated: {timestamp}")
        else:
            print("✗ Build failed - index.html not created")
            return False
        
        # Step 4: Deploy to GitHub
        print("\nStep 3: Deploying to GitHub...")
        try:
            subprocess.run(['git', 'add', 'build.py', 'index.html'], check=True)
            subprocess.run(['git', 'commit', '-m', 'feat: Add live Google Sheets integration for X posts data'], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            print("\n" + "=" * 60)
            print("🎉 DEPLOYMENT WITH GOOGLE SHEETS SUCCESSFUL!")
            print("Site: https://awano27.github.io/daily-ai-news/")
            print("")
            print("✅ Features added:")
            print("- Live data from Google Sheets")
            print("- Automatic updates when you edit the spreadsheet")
            print("- Real-time X/SNS posts without manual CSV updates")
            print("")
            print("📝 To add new X posts:")
            print("1. Edit the Google Sheets directly")
            print("2. Run GitHub Actions or wait for daily auto-update")
            print("3. Site will automatically include new posts!")
            print("=" * 60)
            
        except subprocess.CalledProcessError as e:
            print(f"Git operation failed: {e}")
            print("\nManual deployment:")
            print("git add build.py index.html")
            print("git commit -m 'feat: Add Google Sheets integration'")
            print("git push")
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()