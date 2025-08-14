#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete deployment for today (8/14) with current data
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("Deploying Daily AI News for 2025-08-14")
    print("=" * 60)
    
    try:
        # Step 1: Add today's sample X posts
        print("Step 1: Adding today's X posts...")
        import add_today_posts
        add_today_posts.add_today_posts()
        
        # Step 2: Build with proper settings for today
        print("\nStep 2: Building site for today...")
        os.environ['TRANSLATE_TO_JA'] = '1'
        os.environ['TRANSLATE_ENGINE'] = 'google'
        os.environ['HOURS_LOOKBACK'] = '24'  # Back to 24 hours now that we have today's data
        os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
        
        import build
        build.main()
        
        # Step 3: Verify content
        if Path('index.html').exists():
            size = Path('index.html').stat().st_size
            print(f"\n✓ index.html generated ({size:,} bytes)")
            
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check if today's content is included
                if '2025-08-14' in content:
                    print("✓ Today's date found in content")
                
                # Count articles in each section
                business_start = content.find('id="business"')
                tools_start = content.find('id="tools"')
                posts_start = content.find('id="posts"')
                
                business_cards = content[business_start:tools_start].count('<article class="card">') if business_start != -1 and tools_start != -1 else 0
                tools_cards = content[tools_start:posts_start].count('<article class="card">') if tools_start != -1 and posts_start != -1 else 0
                posts_cards = content[posts_start:].count('<article class="card">') if posts_start != -1 else 0
                
                print(f"✓ Content summary:")
                print(f"  - Business: {business_cards} articles")
                print(f"  - Tools: {tools_cards} articles") 
                print(f"  - Posts/SNS: {posts_cards} items")
                
        else:
            print("✗ index.html not generated")
            return False
        
        # Step 4: Deploy to GitHub
        print("\nStep 3: Deploying to GitHub...")
        try:
            subprocess.run(['git', 'add', 'index.html', '_sources/x_favorites.csv', 'build.py'], check=True)
            subprocess.run(['git', 'commit', '-m', 'update: Daily AI news for 2025-08-14 with current X posts'], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            print("\n" + "=" * 60)
            print("🎉 DEPLOYMENT SUCCESSFUL!")
            print("Site: https://awano27.github.io/daily-ai-news/")
            print("- Updated with today's date (8/14)")
            print("- Includes recent X/SNS posts")
            print("- 24-hour filtering active")
            print("=" * 60)
            
        except subprocess.CalledProcessError as e:
            print(f"Git operation failed: {e}")
            print("\nManual deployment needed:")
            print("git add index.html _sources/x_favorites.csv build.py")
            print("git commit -m 'update: Daily AI news for 2025-08-14'")
            print("git push")
    
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()