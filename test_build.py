#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script to validate build.py execution
"""
import os
import sys
import subprocess
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    print("[TEST] Checking dependencies...")
    required = ['feedparser', 'yaml', 'deep_translator']
    missing = []
    
    for module in required:
        try:
            if module == 'yaml':
                __import__('yaml')
            elif module == 'deep_translator':
                from deep_translator import GoogleTranslator
            else:
                __import__(module)
            print(f"  ✓ {module}")
        except ImportError:
            print(f"  ✗ {module} - MISSING")
            missing.append(module)
    
    if missing:
        print(f"\n[ERROR] Missing dependencies: {', '.join(missing)}")
        print(f"Install with: pip install feedparser pyyaml deep-translator==1.11.4")
        return False
    return True

def check_files():
    """Check if required files exist"""
    print("\n[TEST] Checking required files...")
    required_files = ['build.py', 'feeds.yml', 'style.css']
    missing = []
    
    for file in required_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} - MISSING")
            missing.append(file)
    
    if missing:
        print(f"\n[ERROR] Missing files: {', '.join(missing)}")
        return False
    return True

def run_build():
    """Run build.py with test parameters"""
    print("\n[TEST] Running build.py with test parameters...")
    
    # Set test environment variables
    env = os.environ.copy()
    env['HOURS_LOOKBACK'] = '48'  # Look back 48 hours for more content
    env['MAX_ITEMS_PER_CATEGORY'] = '3'  # Limit to 3 items for testing
    env['TRANSLATE_TO_JA'] = '1'
    env['TRANSLATE_ENGINE'] = 'google'
    
    try:
        result = subprocess.run(
            [sys.executable, 'build.py'],
            env=env,
            capture_output=True,
            text=True,
            timeout=60
        )
        
        print("\n=== STDOUT ===")
        print(result.stdout)
        
        if result.stderr:
            print("\n=== STDERR ===")
            print(result.stderr)
        
        if result.returncode != 0:
            print(f"\n[ERROR] build.py exited with code {result.returncode}")
            return False
            
    except subprocess.TimeoutExpired:
        print("\n[ERROR] build.py timed out after 60 seconds")
        return False
    except Exception as e:
        print(f"\n[ERROR] Failed to run build.py: {e}")
        return False
    
    return True

def check_output():
    """Check if index.html was generated"""
    print("\n[TEST] Checking output...")
    
    if not Path('index.html').exists():
        print("  ✗ index.html - NOT GENERATED")
        return False
    
    size = Path('index.html').stat().st_size
    print(f"  ✓ index.html - Generated ({size:,} bytes)")
    
    # Check if file has content
    if size < 1000:
        print("  ⚠ Warning: index.html seems too small")
        return False
    
    # Check if cache was created
    cache_file = Path('_cache/translations.json')
    if cache_file.exists():
        print(f"  ✓ Translation cache exists")
    else:
        print(f"  ⚠ Translation cache not found (may be normal on first run)")
    
    return True

def main():
    print("=" * 60)
    print("Daily AI News Build Test")
    print("=" * 60)
    
    tests = [
        ("Dependencies", check_dependencies),
        ("Required Files", check_files),
        ("Build Execution", run_build),
        ("Output Validation", check_output)
    ]
    
    failed = []
    for name, test_func in tests:
        if not test_func():
            failed.append(name)
            print(f"\n[FAIL] {name} test failed")
            # Continue to run other tests for diagnosis
    
    print("\n" + "=" * 60)
    if failed:
        print(f"FAILED: {len(failed)} test(s) failed: {', '.join(failed)}")
        print("\nPlease fix the issues above and try again.")
        sys.exit(1)
    else:
        print("SUCCESS: All tests passed!")
        print("\nYou can now:")
        print("1. Open index.html in a browser to view the generated site")
        print("2. Commit and push changes to deploy to GitHub Pages")
        sys.exit(0)

if __name__ == "__main__":
    main()