#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check GitHub repository and Pages status
"""
import subprocess
import json
import sys

print("=" * 60)
print("GitHub Repository Status Check")
print("=" * 60)

# Check git status
print("\n[1] Git Status:")
print("-" * 40)
try:
    result = subprocess.run(['git', 'status', '--short'], capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    else:
        print("Working directory clean")
except Exception as e:
    print(f"Error: {e}")

# Check recent commits
print("\n[2] Recent Commits:")
print("-" * 40)
try:
    result = subprocess.run(['git', 'log', '--oneline', '-5'], capture_output=True, text=True)
    print(result.stdout)
except Exception as e:
    print(f"Error: {e}")

# Check if index.html exists in the repository
print("\n[3] Files in repository:")
print("-" * 40)
try:
    result = subprocess.run(['git', 'ls-files', 'index.html'], capture_output=True, text=True)
    if result.stdout.strip():
        print("✓ index.html is tracked in git")
        # Check last commit that modified index.html
        result = subprocess.run(['git', 'log', '-1', '--format=%h %s (%ar)', 'index.html'], 
                              capture_output=True, text=True)
        if result.stdout:
            print(f"  Last modified: {result.stdout.strip()}")
    else:
        print("✗ index.html is NOT in the repository")
        print("  This is why GitHub Pages shows README instead!")
except Exception as e:
    print(f"Error: {e}")

print("\n[4] Recommendation:")
print("-" * 40)
print("To fix the deployment issue:")
print("1. Run: python build.py")
print("2. Check if index.html was created")
print("3. Run: git add index.html")
print("4. Run: git commit -m 'Add index.html for GitHub Pages'")
print("5. Run: git push")
print("\nThis will deploy the generated HTML to GitHub Pages.")