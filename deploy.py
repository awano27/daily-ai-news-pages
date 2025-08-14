#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy script: Build and commit index.html to GitHub
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n[RUNNING] {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 40)
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"Stderr: {result.stderr}", file=sys.stderr)
        
        if result.returncode != 0:
            print(f"[ERROR] Command failed with code {result.returncode}")
            return False
        print(f"[SUCCESS] {description}")
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        return False

def main():
    print("=" * 60)
    print("Daily AI News - Deployment Script")
    print("=" * 60)
    
    # Step 1: Set environment variables and run build.py
    print("\n[STEP 1] Building index.html...")
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    
    print(f"Environment variables set:")
    print(f"  TRANSLATE_TO_JA={os.environ['TRANSLATE_TO_JA']}")
    print(f"  TRANSLATE_ENGINE={os.environ['TRANSLATE_ENGINE']}")
    print(f"  HOURS_LOOKBACK={os.environ['HOURS_LOOKBACK']}")
    print(f"  MAX_ITEMS_PER_CATEGORY={os.environ['MAX_ITEMS_PER_CATEGORY']}")
    
    if not run_command([sys.executable, 'build.py'], "Generate index.html"):
        print("\n[WARNING] build.py had issues, but continuing...")
    
    # Step 2: Check if index.html was created
    if not Path('index.html').exists():
        print("\n[ERROR] index.html was not created!")
        print("Please check the build.py output above for errors.")
        sys.exit(1)
    
    size = Path('index.html').stat().st_size
    print(f"\n[SUCCESS] index.html created ({size:,} bytes)")
    
    # Step 3: Run fix_lang_chips.py if it exists
    if Path('fix_lang_chips.py').exists():
        print("\n[STEP 2] Running post-processing...")
        run_command([sys.executable, 'fix_lang_chips.py'], "Fix language chips")
    
    # Step 4: Git operations
    print("\n[STEP 3] Committing to Git...")
    
    # Add files
    if not run_command(['git', 'add', 'index.html'], "Add index.html"):
        sys.exit(1)
    
    # Also add cache if it exists
    if Path('_cache/translations.json').exists():
        run_command(['git', 'add', '_cache/translations.json'], "Add translation cache")
    
    # Check if there are changes to commit
    result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
    if not result.stdout:
        print("\n[INFO] No changes to commit")
        sys.exit(0)
    
    # Commit
    commit_msg = f"chore: update index.html [manual deploy]"
    if not run_command(['git', 'commit', '-m', commit_msg], "Commit changes"):
        print("\n[WARNING] Nothing to commit or commit failed")
    
    # Step 5: Push to GitHub
    print("\n[STEP 4] Pushing to GitHub...")
    if run_command(['git', 'push'], "Push to GitHub"):
        print("\n" + "=" * 60)
        print("DEPLOYMENT SUCCESSFUL!")
        print("Your changes will be live at:")
        print("https://awano27.github.io/daily-ai-news/")
        print("(It may take a few minutes for GitHub Pages to update)")
    else:
        print("\n[ERROR] Push failed. Please run 'git push' manually.")
        sys.exit(1)

if __name__ == "__main__":
    main()