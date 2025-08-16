#!/usr/bin/env python3
"""Minimal test for dashboard generation"""
import os
import sys
from pathlib import Path

print("Testing basic imports...")

try:
    import json
    print("✅ json imported")
except Exception as e:
    print(f"❌ json failed: {e}")

try:
    from datetime import datetime
    print("✅ datetime imported")
except Exception as e:
    print(f"❌ datetime failed: {e}")

try:
    from collections import Counter
    print("✅ collections imported")
except Exception as e:
    print(f"❌ collections failed: {e}")

try:
    import url_filter
    print("✅ url_filter imported")
except Exception as e:
    print(f"❌ url_filter failed: {e}")

try:
    import gemini_analyzer
    print("✅ gemini_analyzer imported")
except Exception as e:
    print(f"❌ gemini_analyzer failed: {e}")

# Try to import the main dashboard module
try:
    import generate_comprehensive_dashboard
    print("✅ generate_comprehensive_dashboard imported")
    
    # Check if main function exists
    if hasattr(generate_comprehensive_dashboard, 'main'):
        print("✅ main function found")
    else:
        print("❌ main function not found")
        
except Exception as e:
    print(f"❌ generate_comprehensive_dashboard failed: {e}")
    import traceback
    traceback.print_exc()

print("Basic import tests completed.")