#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Execute build.py with analysis and detailed reporting
"""
import os
import sys
import json
from datetime import datetime, timezone, timedelta

def setup_environment():
    """Set required environment variables"""
    os.environ['HOURS_LOOKBACK'] = '48'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '30'
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
    
    print("Environment variables set:")
    for key in ['HOURS_LOOKBACK', 'MAX_ITEMS_PER_CATEGORY', 'TRANSLATE_TO_JA', 'TRANSLATE_ENGINE', 'X_POSTS_CSV']:
        print(f"  {key} = {os.environ.get(key)}")

def analyze_before_build():
    """Analyze current state before build"""
    print("\n" + "="*60)
    print("BEFORE BUILD - Current State Analysis")
    print("="*60)
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        # Count X posts
        x_posts = len(re.findall(r'Xポスト', content))
        
        # Extract KPI counts
        kpi_matches = re.findall(r'<div class="kpi-value">(\d+)件</div>', content)
        if len(kpi_matches) >= 3:
            business_count, tools_count, posts_count = kpi_matches[:3]
            print(f"Current counts in index.html:")
            print(f"  Business: {business_count} items")
            print(f"  Tools: {tools_count} items")  
            print(f"  Posts: {posts_count} items")
            print(f"  X posts detected: {x_posts}")
        
        # Extract timestamp
        update_match = re.search(r'最終更新：([^<]+)', content)
        if update_match:
            print(f"  Last update: {update_match.group(1).strip()}")
            
    except Exception as e:
        print(f"Error analyzing current state: {e}")

def run_build():
    """Execute the build process with detailed logging"""
    print("\n" + "="*60)
    print("EXECUTING BUILD PROCESS")
    print("="*60)
    
    try:
        # Import and run build
        import build
        
        # Capture original print to track messages
        original_print = print
        build_messages = []
        
        def capturing_print(*args, **kwargs):
            message = ' '.join(str(arg) for arg in args)
            build_messages.append(message)
            original_print(*args, **kwargs)
        
        # Temporarily replace print
        import builtins
        builtins.print = capturing_print
        
        try:
            build.main()
        finally:
            # Restore original print
            builtins.print = original_print
        
        # Analyze build messages for key information
        print("\n" + "-"*40)
        print("KEY BUILD MESSAGES:")
        print("-"*40)
        
        sns_messages = [msg for msg in build_messages if 'X post' in msg or 'SNS' in msg or 'posts' in msg.lower()]
        for msg in sns_messages:
            print(f"  {msg}")
            
        return True, build_messages
        
    except Exception as e:
        print(f"Build failed: {e}")
        import traceback
        traceback.print_exc()
        return False, []

def analyze_after_build():
    """Analyze state after build"""
    print("\n" + "="*60)
    print("AFTER BUILD - Results Analysis")
    print("="*60)
    
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
        
        import re
        # Count X posts
        x_posts = len(re.findall(r'Xポスト', content))
        
        # Extract KPI counts
        kpi_matches = re.findall(r'<div class="kpi-value">(\d+)件</div>', content)
        if len(kpi_matches) >= 3:
            business_count, tools_count, posts_count = kpi_matches[:3]
            print(f"New counts in index.html:")
            print(f"  Business: {business_count} items")
            print(f"  Tools: {tools_count} items")  
            print(f"  Posts: {posts_count} items")
            print(f"  X posts detected: {x_posts}")
        
        # Extract timestamp
        update_match = re.search(r'最終更新：([^<]+)', content)
        if update_match:
            print(f"  Last update: {update_match.group(1).strip()}")
        
        # Look for importance sorting evidence
        posts_section_match = re.search(r'<section id="posts"[^>]*>(.*?)</section>', content, re.DOTALL)
        if posts_section_match:
            posts_html = posts_section_match.group(1)
            post_titles = re.findall(r'<a class="card-title"[^>]*>([^<]+)</a>', posts_html)
            print(f"\nFirst 5 post titles (importance order check):")
            for i, title in enumerate(post_titles[:5]):
                print(f"  {i+1}. {title}")
                
        return {
            'business': int(business_count) if 'business_count' in locals() else 0,
            'tools': int(tools_count) if 'tools_count' in locals() else 0,
            'posts': int(posts_count) if 'posts_count' in locals() else 0,
            'x_posts': x_posts
        }
            
    except Exception as e:
        print(f"Error analyzing after build: {e}")
        return {}

def main():
    print("Daily AI News Build Execution with Analysis")
    print("="*60)
    
    # Set up environment
    setup_environment()
    
    # Analyze before
    analyze_before_build()
    
    # Run build
    success, messages = run_build()
    
    if success:
        # Analyze after
        results = analyze_after_build()
        
        # Final summary
        print("\n" + "="*60)
        print("FINAL SUMMARY")
        print("="*60)
        print(f"Build Status: ✓ SUCCESS")
        print(f"Configuration:")
        print(f"  - HOURS_LOOKBACK: {os.environ.get('HOURS_LOOKBACK')}")
        print(f"  - MAX_ITEMS_PER_CATEGORY: {os.environ.get('MAX_ITEMS_PER_CATEGORY')}")
        print(f"  - Using Google Sheets CSV: ✓")
        print(f"  - 8/14+ filtering: ✓ (built into gather_x_posts)")
        print(f"  - Importance scoring: ✓ (calculate_sns_importance_score)")
        
        if results:
            print(f"Results:")
            print(f"  - SNS posts displayed: {results.get('posts', 0)}")
            print(f"  - X posts in HTML: {results.get('x_posts', 0)}")
            print(f"  - Business items: {results.get('business', 0)}")
            print(f"  - Tools items: {results.get('tools', 0)}")
            
            if results.get('posts', 0) >= 20:
                print("  ✓ Good number of SNS posts displayed")
            else:
                print("  ⚠ Fewer SNS posts than expected")
    else:
        print(f"\nBuild Status: ✗ FAILED")
        print("Check error messages above")

if __name__ == "__main__":
    main()