#!/usr/bin/env python3
"""
Commit tab functionality fix to GitHub
"""
import subprocess
import os
from pathlib import Path

def main():
    try:
        os.chdir(Path(__file__).parent)
        
        print("🔧 Tab Functionality Fix - JavaScript hidden class logic")
        print("=" * 55)
        
        # Add files
        print("📝 Adding build_simple_ranking.py...")
        result = subprocess.run(['git', 'add', 'build_simple_ranking.py'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ File staged")
        else:
            print(f"   ❌ Add failed: {result.stderr}")
            return False
        
        # Commit
        commit_msg = """fix: Tab functionality repair - JavaScript hidden class logic 2025-08-23

✅ Fix tab switching using hidden class instead of active class
✅ Update tab panel HTML generation (hidden vs active)  
✅ Fix filterCards function to find visible panels correctly
✅ Enhanced card template with proper HTML structure
✅ CSS generation function confirmed present

Expected result: Business/Tools/Posts tabs will switch properly"""
        
        print("💾 Committing changes...")
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Committed successfully")
        else:
            print(f"   ❌ Commit failed: {result.stderr}")
            return False
        
        # Push
        print("📤 Pushing to GitHub...")
        result = subprocess.run(['git', 'push', 'origin', 'main'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("   ✅ Pushed successfully")
        else:
            print(f"   ❌ Push failed: {result.stderr}")
            return False
        
        print("\n🎉 Tab Fix Deployed Successfully!")
        print("=" * 50)
        print("✅ JavaScript tab switching logic corrected")
        print("✅ Hidden class used for panel visibility")
        print("✅ Changes pushed to GitHub")
        print("🔄 GitHub Actions will rebuild in ~30 seconds")
        print("\n📋 Expected Results (5-10 minutes):")
        print("  🖱️ タブ機能が正常に動作 (Business/Tools/Posts切り替え)")
        print("  🎨 CSS スタイリング適用")
        print("  📅 現在日付 (2025-08-23) 表示")
        print("  📰 情報量維持 + ランキングシステム")
        print(f"\n🌐 Test: https://awano27.github.io/daily-ai-news-pages/")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n⏱️ Next steps:")
        print("1. Wait 5-10 minutes for GitHub Actions to complete")
        print("2. Test tab functionality on the site")
        print("3. Verify all three tabs (Business/Tools/Posts) switch properly")
        exit(0)
    else:
        exit(1)