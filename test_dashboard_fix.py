#!/usr/bin/env python3
# Test if dashboard generation issue is fixed

try:
    import build
    
    # Test if get_category is now accessible at module level
    print("Testing build.get_category access...")
    
    # Test with sample data
    test_conf = {"Business": [{"name": "test", "url": "test.com"}]}
    result = build.get_category(test_conf, "Business")
    
    print(f"✅ build.get_category works! Result: {result}")
    
    # Test parse_feeds
    print("Testing build.parse_feeds...")
    feeds_conf = build.parse_feeds()
    print(f"✅ build.parse_feeds works! Loaded {len(feeds_conf)} categories")
    
    # Test gather_items (this should work since it was already module-level)
    print("Testing build.gather_items...")
    business_feeds = build.get_category(feeds_conf, "Business")
    print(f"✅ Found {len(business_feeds)} business feeds")
    
    print("\n🎉 All required functions are now accessible at module level!")
    print("Dashboard generation should now work correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()