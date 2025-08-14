#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run build.py with proper environment settings
"""
import os
import sys
from pathlib import Path

# Set environment variables
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google'
os.environ['HOURS_LOOKBACK'] = '24'
os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'

print("=" * 60)
print("Building Daily AI News Site")
print("=" * 60)
print(f"Settings:")
print(f"  HOURS_LOOKBACK: {os.environ['HOURS_LOOKBACK']}")
print(f"  MAX_ITEMS_PER_CATEGORY: {os.environ['MAX_ITEMS_PER_CATEGORY']}")
print(f"  TRANSLATE_TO_JA: {os.environ['TRANSLATE_TO_JA']}")
print(f"  TRANSLATE_ENGINE: {os.environ['TRANSLATE_ENGINE']}")
print("=" * 60)

try:
    # Import and run build.py
    import build
    build.main()
    
    # Check if index.html was created
    if Path('index.html').exists():
        size = Path('index.html').stat().st_size
        print("\n" + "=" * 60)
        print(f"SUCCESS: index.html generated ({size:,} bytes)")
        print("=" * 60)
        
        # Read first few lines to verify content
        with open('index.html', 'r', encoding='utf-8') as f:
            lines = f.readlines()[:10]
            if len(lines) > 5:
                print("\nFirst few lines of index.html:")
                print("-" * 40)
                for line in lines[:5]:
                    print(line.rstrip())
                print("-" * 40)
    else:
        print("\nERROR: index.html was not generated!")
        sys.exit(1)
        
except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)