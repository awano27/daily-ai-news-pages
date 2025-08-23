#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Force build update script to fix CSS/JS references
"""

import subprocess
import sys
import os
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return the result"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=Path(__file__).parent)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            if result.stdout.strip():
                print(f"Output: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} failed")
            if result.stderr.strip():
                print(f"Error: {result.stderr.strip()}")
            return False
    except Exception as e:
        print(f"❌ {description} failed with exception: {e}")
        return False

def main():
    print("🚀 Force Build Update - Fixing CSS/JS References")
    print("=" * 50)
    
    # Check if build_simple_ranking.py exists and has correct references
    build_script = Path("build_simple_ranking.py")
    if not build_script.exists():
        print("❌ build_simple_ranking.py not found!")
        return False
    
    # Read the build script to verify CSS reference
    with open(build_script, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if 'style_enhanced_ranking.css' in content:
        print("❌ Found incorrect CSS reference in build script!")
        print("Need to fix CSS reference to style.css")
        
        # Fix the CSS reference
        content = content.replace('style_enhanced_ranking.css', 'style.css')
        
        with open(build_script, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ Fixed CSS reference in build script")
    else:
        print("✅ CSS reference is already correct")
    
    if 'script_enhanced_ranking.js' in content:
        print("❌ Found external JS reference in build script!")
        print("JavaScript should be inline")
    else:
        print("✅ JavaScript is inline as expected")
    
    # Stage and commit the build script
    print("\n📝 Committing build script changes...")
    if not run_command("git add build_simple_ranking.py", "Stage build script"):
        return False
    
    if not run_command('git commit -m "fix: Correct CSS reference in build_simple_ranking.py"', "Commit changes"):
        print("ℹ️ No changes to commit or commit failed")
    
    # Push changes
    print("\n📤 Pushing to GitHub...")
    if not run_command("git push origin main", "Push changes"):
        return False
    
    # Try to trigger GitHub Actions workflow
    print("\n🎯 Triggering GitHub Actions workflow...")
    workflows = [
        "enhanced-daily-build.yml",
        "build.yml",
        ".github/workflows/enhanced-daily-build.yml"
    ]
    
    for workflow in workflows:
        if run_command(f"gh workflow run {workflow}", f"Trigger {workflow}"):
            print(f"✅ Successfully triggered {workflow}")
            break
        else:
            print(f"⚠️ Failed to trigger {workflow}, trying next...")
    
    print("\n🎉 Force build update completed!")
    print("🔗 Check: https://awano27.github.io/daily-ai-news-pages/")
    print("⏳ GitHub Actions may take a few minutes to complete")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)