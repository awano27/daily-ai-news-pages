#!/usr/bin/env python3
"""
Test script to analyze the CSV data and understand the filtering
"""
import sys
import os
from datetime import datetime, timezone, timedelta

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

# Import build functionality
try:
    from build import gather_x_posts, _extract_x_data_from_csv, _read_csv_bytes, JST
    
    print("=== Testing CSV Data Analysis ===")
    
    # Set test configuration 
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    
    print(f"Fetching CSV from: {GOOGLE_SHEETS_URL}")
    
    # Read CSV data
    try:
        raw_data = _read_csv_bytes(GOOGLE_SHEETS_URL)
        print(f"✓ Successfully fetched {len(raw_data)} bytes from CSV")
    except Exception as e:
        print(f"✗ Failed to fetch CSV: {e}")
        sys.exit(1)
    
    # Extract data
    try:
        x_data = _extract_x_data_from_csv(raw_data)
        print(f"✓ Extracted {len(x_data)} total posts from CSV")
    except Exception as e:
        print(f"✗ Failed to extract data: {e}")
        sys.exit(1)
    
    # Analyze dates
    aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=JST)
    recent_posts = []
    
    for post in x_data:
        post_date = post.get('datetime')
        if post_date and post_date >= aug14_jst:
            recent_posts.append(post)
    
    print(f"✓ Found {len(recent_posts)} posts on or after August 14, 2025")
    
    # Test the full gathering function
    try:
        gathered_posts = gather_x_posts(GOOGLE_SHEETS_URL)
        print(f"✓ gather_x_posts() returned {len(gathered_posts)} posts")
    except Exception as e:
        print(f"✗ gather_x_posts() failed: {e}")
    
    # Show sample data
    print(f"\n=== Sample Recent Posts ===")
    for i, post in enumerate(recent_posts[:5]):
        print(f"{i+1}. {post['username']} - {post['datetime'].strftime('%Y-%m-%d %H:%M')} JST")
        print(f"   URL: {post['url']}")
        print(f"   Text: {post['text'][:100]}...")
        print()
    
    print(f"=== Summary ===")
    print(f"Total posts in CSV: {len(x_data)}")
    print(f"Posts >= Aug 14, 2025: {len(recent_posts)}")
    print(f"Posts processed by gather_x_posts(): {len(gathered_posts) if 'gathered_posts' in locals() else 'N/A'}")
    
except ImportError as e:
    print(f"Failed to import build functions: {e}")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    sys.exit(1)