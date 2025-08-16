#!/usr/bin/env python3
import subprocess
import sys
import os

# Change to the correct directory
os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

# Run the test script
try:
    result = subprocess.run([sys.executable, "test_x_posts.py"], 
                          capture_output=True, text=True, timeout=300)
    
    print("STDOUT:")
    print(result.stdout)
    
    if result.stderr:
        print("\nSTDERR:")
        print(result.stderr)
    
    print(f"\nReturn code: {result.returncode}")
    
except subprocess.TimeoutExpired:
    print("Script timed out after 5 minutes")
except Exception as e:
    print(f"Error running script: {e}")