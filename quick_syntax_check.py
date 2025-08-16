#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick syntax check for build.py
"""

try:
    print("🔍 Checking build.py syntax...")
    
    # Try to compile the build.py file
    with open('build.py', 'r', encoding='utf-8') as f:
        code = f.read()
    
    compile(code, 'build.py', 'exec')
    print("✅ build.py syntax is valid")
    
    # Try to import it
    import build
    print("✅ build.py imported successfully")
    
    # Check if our new function exists
    if hasattr(build, 'calculate_sns_importance_score'):
        print("✅ calculate_sns_importance_score function found")
    else:
        print("❌ calculate_sns_importance_score function not found")
    
except SyntaxError as e:
    print(f"❌ Syntax error in build.py: {e}")
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Other error: {e}")
    import traceback
    traceback.print_exc()