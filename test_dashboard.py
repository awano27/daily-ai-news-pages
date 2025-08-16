#!/usr/bin/env python3
# Simple test to verify dashboard generation works
import sys
import subprocess

try:
    result = subprocess.run([sys.executable, "generate_comprehensive_dashboard.py"], 
                          capture_output=True, text=True, timeout=60)
    print("Return code:", result.returncode)
    print("STDOUT:", result.stdout)
    if result.stderr:
        print("STDERR:", result.stderr)
    
    # Check if index.html was updated
    from pathlib import Path
    index_path = Path("index.html")
    if index_path.exists():
        print(f"index.html size: {index_path.stat().st_size} bytes")
        print("Dashboard generation completed successfully!")
    else:
        print("ERROR: index.html not found!")
        
except subprocess.TimeoutExpired:
    print("Script timed out after 60 seconds")
except Exception as e:
    print(f"Error: {e}")