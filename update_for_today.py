#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Update the site for today (8/14) - show available content within reasonable timeframe
"""
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

def main():
    print("=" * 60)
    print("Updating Site for Today (2025-08-14)")
    print("=" * 60)
    
    # Set environment variables for today
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '96'  # 4 days to capture available X posts
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    
    print("Configuration:")
    print(f"  HOURS_LOOKBACK: {os.environ['HOURS_LOOKBACK']} hours (to include available X posts)")
    print(f"  MAX_ITEMS_PER_CATEGORY: {os.environ['MAX_ITEMS_PER_CATEGORY']}")
    
    try:
        # Import and run build.py with extended lookback
        print("\nRunning build.py with extended lookback...")
        import build
        
        # Check current time and available X posts
        JST = timezone(timedelta(hours=9))
        NOW = datetime.now(JST)
        print(f"Current time: {NOW.strftime('%Y-%m-%d %H:%M JST')}")
        
        # Test X posts processing
        if Path('_sources/x_favorites.csv').exists():
            print("\nAnalyzing available X posts...")
            x_posts = build.gather_x_posts('_sources/x_favorites.csv')
            print(f"Found {len(x_posts)} X posts within {os.environ['HOURS_LOOKBACK']} hours")
            
            if x_posts:
                print("\nMost recent X posts:")
                for i, post in enumerate(x_posts[:5]):
                    age_hours = (NOW - post['_dt']).total_seconds() / 3600
                    print(f"  {i+1}. {post['title']} ({age_hours:.1f}h ago)")
        
        # Run full build
        print("\nGenerating site...")
        build.main()
        
        # Check result
        if Path('index.html').exists():
            size = Path('index.html').stat().st_size
            print(f"\n✓ index.html generated ({size:,} bytes)")
            
            # Show what was included
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Count articles
                business_count = content.count('<section id="business"')
                tools_count = content.count('<section id="tools"')
                posts_count = content.count('<section id="posts"')
                
                print(f"✓ Content summary:")
                print(f"  - Business articles: {content.count('class=\"card\"', content.find('id=\"business\"'))}")
                print(f"  - Tools articles: {content.count('class=\"card\"', content.find('id=\"tools\"'))}")
                print(f"  - Posts/SNS: {content.count('class=\"card\"', content.find('id=\"posts\"'))}")
                
                # Show timestamp
                if '最終更新：' in content:
                    start = content.find('最終更新：') + 5
                    end = content.find('</div>', start)
                    timestamp = content[start:end].strip()
                    print(f"✓ Updated: {timestamp}")
        
        print("\n" + "=" * 60)
        print("BUILD COMPLETED FOR TODAY")
        print("Ready to deploy with:")
        print("  git add index.html build.py")
        print("  git commit -m 'Update: Daily content for 2025-08-14'")
        print("  git push")
        print("=" * 60)
        
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()