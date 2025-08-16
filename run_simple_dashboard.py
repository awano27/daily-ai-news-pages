#!/usr/bin/env python3
"""Simple dashboard runner to avoid dependency issues"""
import os
import sys

# Set environment to disable translation
os.environ['TRANSLATE_TO_JA'] = '0'
os.environ['HOURS_LOOKBACK'] = '24'
os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'

print("Running dashboard generation...")
try:
    # Import and run directly
    import generate_comprehensive_dashboard
    print("Module imported successfully")
    generate_comprehensive_dashboard.main()
    print("✅ Dashboard generation completed")
except Exception as e:
    print(f"❌ Dashboard generation failed: {e}")
    import traceback
    traceback.print_exc()

if __name__ == "__main__":
    print("Script executed directly")