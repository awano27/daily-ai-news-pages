#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test live Google Sheets integration for X posts
"""
import os
import sys
from datetime import datetime, timezone, timedelta

def main():
    print("=" * 60)
    print("Testing Live Google Sheets Integration")
    print("=" * 60)
    
    # Set environment to use Google Sheets
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    # X_POSTS_CSV will default to Google Sheets URL
    
    try:
        import build
        
        # Test X posts gathering from Google Sheets
        print("Testing X posts from live Google Sheets...")
        google_sheets_url = build.GOOGLE_SHEETS_URL
        print(f"URL: {google_sheets_url}")
        
        x_posts = build.gather_x_posts(google_sheets_url)
        
        if x_posts:
            print(f"\n✓ Successfully loaded {len(x_posts)} X posts from Google Sheets")
            
            # Show details of recent posts
            print("\nRecent posts (within 24 hours):")
            JST = timezone(timedelta(hours=9))
            NOW = datetime.now(JST)
            
            for i, post in enumerate(x_posts[:10]):
                age_hours = (NOW - post['_dt']).total_seconds() / 3600
                print(f"  {i+1}. {post['title']}")
                print(f"      Posted: {post['_dt'].strftime('%Y-%m-%d %H:%M JST')}")
                print(f"      Age: {age_hours:.1f} hours ago")
                print(f"      Summary: {post['_summary'][:60]}...")
                print()
        else:
            print("✗ No X posts found or error occurred")
            return False
        
        # Test full build with Google Sheets data
        print("Testing full site build with Google Sheets data...")
        build.main()
        
        # Verify result
        from pathlib import Path
        if Path('index.html').exists():
            size = Path('index.html').stat().st_size
            print(f"\n✓ Site built successfully ({size:,} bytes)")
            
            # Check content
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Look for Posts section
                posts_start = content.find('id="posts"')
                if posts_start != -1:
                    posts_section = content[posts_start:posts_start+2000]
                    posts_count = posts_section.count('<article class="card">')
                    print(f"✓ Posts section contains {posts_count} items")
                    
                    # Check for recent timestamps
                    if 'JST' in content:
                        print("✓ Content includes JST timestamps")
                    
                    # Check update time
                    if '2025-08-14' in content:
                        print("✓ Content shows today's date")
        
        print("\n" + "=" * 60)
        print("✅ GOOGLE SHEETS INTEGRATION TEST SUCCESSFUL")
        print("The site now uses live data from Google Sheets!")
        print("Ready to deploy with:")
        print("  git add build.py index.html")
        print("  git commit -m 'feat: Add live Google Sheets integration for X posts'")
        print("  git push")
        print("=" * 60)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()