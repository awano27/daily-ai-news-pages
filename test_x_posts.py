#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test X posts processing with real dates
"""
import os
import sys
from datetime import datetime, timezone, timedelta

# Set environment variables
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google'
os.environ['HOURS_LOOKBACK'] = '48'  # 48 hours as requested
os.environ['MAX_ITEMS_PER_CATEGORY'] = '30'  # 30 items as requested
os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'

print("=" * 60)
print("Testing X Posts Processing")
print("=" * 60)

try:
    import build
    
    # Test gather_x_posts function directly
    print("Testing gather_x_posts function...")
    csv_url = os.environ.get('X_POSTS_CSV', '_sources/x_favorites.csv')
    print(f"Using CSV source: {csv_url}")
    x_posts = build.gather_x_posts(csv_url)
    
    print(f"\nFound {len(x_posts)} X posts:")
    print("-" * 40)
    
    for i, post in enumerate(x_posts[:10]):  # Show first 10
        print(f"{i+1}. {post['title']}")
        print(f"   Date: {post['_dt']}")
        print(f"   Summary: {post['_summary'][:80]}...")
        print(f"   URL: {post['link']}")
        print()
    
    if len(x_posts) > 10:
        print(f"... and {len(x_posts) - 10} more posts")
    
    # Test age calculation
    print("\nAge calculation test:")
    print("-" * 40)
    JST = timezone(timedelta(hours=9))
    NOW = datetime.now(JST)
    
    for post in x_posts[:5]:
        age = NOW - post['_dt']
        hours_ago = age.total_seconds() / 3600
        print(f"Post: {post['title']}")
        print(f"  Posted: {post['_dt']}")
        print(f"  Age: {hours_ago:.1f} hours ago")
        print()

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()

print("=" * 60)
print("Test completed")