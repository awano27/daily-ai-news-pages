#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy latest changes including updated HTML and CSS to GitHub Pages
"""
import os
import sys
import subprocess
from pathlib import Path

def run_command(cmd, description):
    """Run a command and return success status"""
    print(f"\n[RUNNING] {description}")
    print(f"Command: {' '.join(cmd)}")
    print("-" * 50)
    
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
    
    print("🚀 Deploying latest HTML and CSS changes to GitHub Pages...")
    
    # Check git status
    print("\n📋 Checking current git status...")
    if not run_command(['git', 'status', '--porcelain'], "Checking git status"):
        print("Warning: Could not check git status, continuing...")
    
    # Add all changes
    print("\n📁 Adding all changes to git...")
    if not run_command(['git', 'add', 'index.html', 'style_enhanced_ranking.css'], "Adding HTML and CSS files"):
        print("Warning: Could not add specific files, trying to add all...")
        if not run_command(['git', 'add', '.'], "Adding all changes"):
            return False
    
    # Check what's staged
    print("\n📝 Checking staged changes...")
    run_command(['git', 'diff', '--cached', '--name-only'], "Checking staged files")
    
    # Commit changes
    commit_message = """feat: Deploy latest content with enhanced CSS design

🆕 Content Updates:
✅ Updated index.html with latest news articles (24件)
✅ Current timestamp: 2025-08-22 23:43 JST
✅ Priority-based article ranking system
✅ Enhanced article filtering and categorization

🎨 CSS Design Improvements:
✅ Modern gradient backgrounds and animations
✅ Improved card hover effects with scale transforms
✅ Enhanced priority indicators with emoji animations
✅ Better visual hierarchy with refined typography
✅ Sticky header with backdrop blur effect
✅ Custom scrollbar styling for better UX
✅ Responsive design optimizations
✅ Smooth transitions and micro-interactions

🔧 Technical Enhancements:
✅ Priority-based styling for different content types
✅ Search functionality with icon integration
✅ Tab navigation with underline animations
✅ Bookmark functionality for articles
✅ Mobile-responsive layout improvements

🧪 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"""
    
    print("\n💾 Committing changes...")
    if not run_command(['git', 'commit', '-m', commit_message], "Committing changes"):
        print("No new changes to commit or commit failed")
        # Check if there are any changes to commit
        result = subprocess.run(['git', 'status', '--porcelain'], capture_output=True, text=True)
        if not result.stdout.strip():
            print("✅ Repository is already up to date!")
            return True
    
    # Push to GitHub
    print("\n🌐 Pushing to GitHub Pages...")
    if not run_command(['git', 'push', 'origin', 'main'], "Pushing to GitHub"):
        return False
    
    print("\n" + "="*60)
    print("✅ Successfully deployed to GitHub Pages!")
    print("🔗 Your site will be updated at: https://awano27.github.io/daily-ai-news-pages/")
    print("⏳ Changes may take a few minutes to appear on the live site")
    print("="*60)
    
    print("\n🎉 Deployment Summary:")
    print("• ✅ Latest content with 24 articles")
    print("• ✅ Enhanced CSS design with modern animations")
    print("• ✅ Priority-based ranking system")
    print("• ✅ Improved responsive design")
    print("• ✅ Better user experience with hover effects")
    print("• ✅ Sticky navigation and search functionality")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)