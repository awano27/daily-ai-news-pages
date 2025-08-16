#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple runner for the comprehensive dashboard
"""
import os
import sys

# Set up environment
os.chdir(r'C:\Users\yoshitaka\daily-ai-news')
sys.path.insert(0, r'C:\Users\yoshitaka\daily-ai-news')

# Environment variables
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google'
os.environ['HOURS_LOOKBACK'] = '24'
os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'

# Import and run
try:
    import generate_comprehensive_dashboard
    print("🔄 Starting comprehensive AI dashboard generation...")
    result = generate_comprehensive_dashboard.main()
    if result:
        print("✅ Dashboard generation completed successfully!")
    else:
        print("❌ Dashboard generation failed!")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()