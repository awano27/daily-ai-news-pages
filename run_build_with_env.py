#!/usr/bin/env python3
import os
import subprocess
import sys

# Set environment variables
os.environ['HOURS_LOOKBACK'] = '48'
os.environ['MAX_ITEMS_PER_CATEGORY'] = '30'
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google'
os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'

# Import and run build.py
try:
    import build
    build.main()
except Exception as e:
    print(f"Error running build.py: {e}")
    sys.exit(1)