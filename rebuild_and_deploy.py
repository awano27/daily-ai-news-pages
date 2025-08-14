#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rebuild with updated X posts processing and deploy
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("Rebuilding with Updated X Posts Processing")
    print("=" * 60)
    
    # Set environment variables for testing
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '48'  # Look back 48 hours for more X posts
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    
    print("Environment settings:")
    print(f"  HOURS_LOOKBACK: {os.environ['HOURS_LOOKBACK']}")
    print(f"  MAX_ITEMS_PER_CATEGORY: {os.environ['MAX_ITEMS_PER_CATEGORY']}")
    
    try:
        # Import and run updated build.py
        print("\nRunning updated build.py...")
        import build
        build.main()
        
        # Check if index.html was created
        if Path('index.html').exists():
            size = Path('index.html').stat().st_size
            print(f"\n✓ index.html generated ({size:,} bytes)")
            
            # Show timestamp
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                if '最終更新：' in content:
                    start = content.find('最終更新：') + 5
                    end = content.find('</div>', start)
                    timestamp = content[start:end].strip()
                    print(f"✓ Updated timestamp: {timestamp}")
        else:
            print("✗ index.html was NOT generated")
            return False
            
        # Git operations
        print("\nCommitting changes...")
        try:
            subprocess.run(['git', 'add', 'index.html', 'build.py'], check=True)
            subprocess.run(['git', 'commit', '-m', 'fix: Update X posts to use real timestamps from CSV'], check=True)
            subprocess.run(['git', 'push'], check=True)
            print("✓ Changes pushed to GitHub")
            
            print("\n" + "=" * 60)
            print("REBUILD AND DEPLOY SUCCESSFUL!")
            print("Site URL: https://awano27.github.io/daily-ai-news/")
            print("X posts should now show with correct timestamps!")
            print("=" * 60)
            
        except subprocess.CalledProcessError as e:
            print(f"Git operation failed: {e}")
            print("Please run git commands manually:")
            print("  git add index.html build.py")
            print("  git commit -m 'fix: Update X posts with real timestamps'")
            print("  git push")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()