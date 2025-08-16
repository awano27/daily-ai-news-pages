#!/usr/bin/env python3
import os
import sys
import subprocess

# Set working directory
os.chdir(r'C:\Users\yoshitaka\daily-ai-news')

# Execute the comprehensive dashboard script
try:
    result = subprocess.run([sys.executable, 'generate_comprehensive_dashboard.py'], 
                          capture_output=True, text=True)
    print("STDOUT:")
    print(result.stdout)
    if result.stderr:
        print("STDERR:")
        print(result.stderr)
    print(f"Return code: {result.returncode}")
except Exception as e:
    print(f"Error executing script: {e}")