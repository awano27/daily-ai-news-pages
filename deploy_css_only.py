#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy CSS changes only to GitHub Pages
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
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8')
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
    # Ensure we're in the right directory
    os.chdir(Path(__file__).parent)
    
    print("🎨 Deploying CSS improvements to GitHub Pages...")
    
    # Check git status
    if not run_command(['git', 'status'], "Checking git status"):
        return False
    
    # Add CSS file
    if not run_command(['git', 'add', 'style_enhanced_ranking.css'], "Adding CSS changes"):
        return False
    
    # Commit changes
    commit_message = """feat: Enhanced CSS design improvements

🎨 Visual enhancements:
✅ Gradient backgrounds and animations
✅ Improved shadows and depth
✅ Card hover scale effects
✅ Priority indicators with emoji animations

🖱️ Interaction improvements:
✅ Button hover effects with shimmer
✅ Search box with magnifying glass icon
✅ Tab underline animations
✅ Card left border hover effect

📐 Layout enhancements:
✅ KPI cards with gradient top line
✅ Filter controls with labels
✅ Sticky header with backdrop blur
✅ Custom scrollbar styling

🎯 Color and contrast:
✅ Priority-based gradient backgrounds
✅ Score badges with star icons
✅ Enhanced tech tag hover effects
✅ Improved action button depth

🧪 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
    
    if not run_command(['git', 'commit', '-m', commit_message], "Committing CSS changes"):
        print("No changes to commit or commit failed")
    
    # Push to GitHub
    if not run_command(['git', 'push', 'origin', 'main'], "Pushing to GitHub"):
        return False
    
    print("\n✅ CSS improvements deployed successfully!")
    print("🔗 https://awano27.github.io/daily-ai-news-pages/")
    print("\n🎉 Improvements include:")
    print("• Enhanced visual design with gradients")
    print("• Improved hover effects and animations")
    print("• Better layout and spacing")
    print("• Modernized UI components")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)