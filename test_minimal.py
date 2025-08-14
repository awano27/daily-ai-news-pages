#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Minimal test to check if build.py can run
"""
import os
import sys

# Set environment variables
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google'
os.environ['HOURS_LOOKBACK'] = '48'  # Look back 48 hours for more content
os.environ['MAX_ITEMS_PER_CATEGORY'] = '2'  # Limit items for testing

print("=" * 60)
print("Running build.py with test parameters")
print("=" * 60)
print(f"HOURS_LOOKBACK: {os.environ['HOURS_LOOKBACK']}")
print(f"MAX_ITEMS_PER_CATEGORY: {os.environ['MAX_ITEMS_PER_CATEGORY']}")
print(f"TRANSLATE_TO_JA: {os.environ['TRANSLATE_TO_JA']}")
print(f"TRANSLATE_ENGINE: {os.environ['TRANSLATE_ENGINE']}")
print("=" * 60)

try:
    # Import and run build.py
    import build
    build.main()
    print("\n" + "=" * 60)
    print("SUCCESS: build.py completed")
    
    # Check if index.html was created
    from pathlib import Path
    if Path('index.html').exists():
        size = Path('index.html').stat().st_size
        print(f"✓ index.html generated ({size:,} bytes)")
        
        # Show first 500 characters
        content = Path('index.html').read_text(encoding='utf-8')
        print(f"\nFirst 500 characters of index.html:")
        print("-" * 40)
        print(content[:500])
        print("-" * 40)
    else:
        print("✗ index.html was NOT generated")
        
except Exception as e:
    print("\n" + "=" * 60)
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)