#!/usr/bin/env python3
print("=== Daily AI News Status Check ===")

from pathlib import Path
import subprocess

# 1. Check if index.html exists
if Path('index.html').exists():
    size = Path('index.html').stat().st_size
    print(f"✓ index.html exists ({size:,} bytes)")
    
    # Check timestamp
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()
        if '最終更新：' in content:
            start = content.find('最終更新：') + 5
            end = content.find('</div>', start)
            timestamp = content[start:end].strip()
            print(f"✓ Last updated: {timestamp}")
else:
    print("✗ index.html does not exist")

# 2. Check git status
try:
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if result.stdout:
        print(f"Git changes: {len(result.stdout.splitlines())} files")
        for line in result.stdout.splitlines()[:5]:
            print(f"  {line}")
    else:
        print("✓ Git working directory clean")
except:
    print("! Git status check failed")

# 3. Check Google Sheets URL
try:
    import build
    print(f"✓ Google Sheets URL configured: {build.GOOGLE_SHEETS_URL[:60]}...")
except:
    print("✗ build.py import failed")

print("=== Status Check Complete ===")
print("\nTo deploy, run:")
print("  python deploy_with_sheets.py")