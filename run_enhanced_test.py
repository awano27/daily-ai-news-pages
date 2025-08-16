#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual execution of enhanced SNS test since bash is not working
"""
import os
import sys

def main():
    print("🧪 Setting up environment for enhanced SNS functionality test...")
    
    # Set environment variables
    os.environ['HOURS_LOOKBACK'] = '48'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '30'
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    print("✅ Environment variables set:")
    print(f"   HOURS_LOOKBACK: {os.environ['HOURS_LOOKBACK']}")
    print(f"   MAX_ITEMS_PER_CATEGORY: {os.environ['MAX_ITEMS_PER_CATEGORY']}")
    print(f"   TRANSLATE_TO_JA: {os.environ['TRANSLATE_TO_JA']}")
    print(f"   TRANSLATE_ENGINE: {os.environ['TRANSLATE_ENGINE']}")
    
    print(f"\n🔄 Now importing and running build.py...")
    
    # Import and run build.py directly
    try:
        import build
        print("✅ build.py imported successfully")
        
        # Call main function
        build.main()
        
        print("✅ build.py executed successfully")
        
    except Exception as e:
        print(f"❌ Error running build.py: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 Enhanced SNS functionality test completed!")
    else:
        print("\n❌ Test failed!")
        sys.exit(1)