#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual enhanced build with debug output
"""

import os
import sys

# Set up environment
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google'
os.environ['HOURS_LOOKBACK'] = '24'
os.environ['MAX_ITEMS_PER_CATEGORY'] = '25'
os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'

print("🔧 Manual Enhanced Build")
print("=" * 40)

print("📋 Environment:")
print(f"   HOURS_LOOKBACK: {os.environ.get('HOURS_LOOKBACK')}")
print(f"   MAX_ITEMS_PER_CATEGORY: {os.environ.get('MAX_ITEMS_PER_CATEGORY')}")
print(f"   X_POSTS_CSV: Set")

# Import and run
try:
    print("\n🚀 Starting build...")
    from build_simple_ranking import main
    
    all_items = main()
    
    if all_items:
        print(f"\n✅ Build completed with {len(all_items)} total items")
        
        # Analyze by category
        categories = {}
        for item in all_items:
            cat = item.get('category', 'Unknown')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(item)
        
        print(f"\n📊 Category breakdown:")
        for cat, items in categories.items():
            print(f"   {cat}: {len(items)} items")
            
            # Show sample from Posts category
            if cat == 'Posts':
                print(f"     Posts samples:")
                for i, item in enumerate(items[:3]):
                    is_x = "🐦" if item.get('is_x_post') else "📑"
                    print(f"       {is_x} {item.get('title', '')[:50]}...")
        
        # Check if HTML was generated
        if os.path.exists('index.html'):
            print(f"\n📄 index.html generated successfully")
            
            # Quick check for Posts content
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                
            has_posts_tab = 'id="posts"' in content
            has_twitter_badge = 'post-type-badge twitter' in content
            has_arxiv_badge = 'post-type-badge arxiv' in content
            
            print(f"   Posts tab: {'✅' if has_posts_tab else '❌'}")
            print(f"   Twitter badge: {'✅' if has_twitter_badge else '❌'}")
            print(f"   arXiv badge: {'✅' if has_arxiv_badge else '❌'}")
            
        else:
            print(f"\n❌ index.html not generated")
            
    else:
        print("❌ Build returned no items")
        
except Exception as e:
    print(f"❌ Build error: {e}")
    import traceback
    traceback.print_exc()

print("\n🏁 Manual build completed")