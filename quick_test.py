#!/usr/bin/env python3
print("=== Quick Test ===")
print("Python is working!")

try:
    import build
    print("✓ build.py imported successfully")
    
    # Test Google Sheets URL
    print(f"Google Sheets URL: {build.GOOGLE_SHEETS_URL}")
    
    # Test environment
    import os
    print(f"HOURS_LOOKBACK: {os.getenv('HOURS_LOOKBACK', '24')}")
    
    print("=== Test Complete ===")
    
except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()