#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy the enhanced SNS functionality (manual version since bash is not working)
"""
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

def deploy_enhanced_sns():
    """Deploy the enhanced SNS functionality"""
    
    print("📤 Deploying enhanced SNS functionality with 8/14+ filtering...")
    
    try:
        JST = timezone(timedelta(hours=9))
        now = datetime.now(JST)
        
        print("🔄 Git operations...")
        
        # Git pull
        print("  📥 Pulling latest changes...")
        result = subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"⚠️ Git pull warning: {result.stderr}")
        
        # Add files
        files_to_add = ['build.py', 'index.html']
        for file in files_to_add:
            if Path(file).exists():
                print(f"  📁 Adding {file}...")
                result = subprocess.run(['git', 'add', file], 
                                      capture_output=True, text=True)
                if result.returncode != 0:
                    print(f"❌ Failed to add {file}: {result.stderr}")
                    return False
        
        # Check status
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True)
        if not result.stdout.strip():
            print("ℹ️ No changes to commit")
            return True
        
        # Commit
        commit_msg = f"""feat: Enhanced SNS posts from 8/14+ with importance scoring (30 items) [{now.strftime('%Y-%m-%d %H:%M JST')}]

📱 Improvements:
- Focus on 8/14+ recent posts only  
- Increased to 30 SNS posts max
- Importance-based ranking
- Enterprise accounts prioritized
- No old news, fresh content only

🎯 Priority accounts: OpenAI(100), Anthropic(100), Sam Altman(95)
🤖 Tech leaders: Google(90), Yann LeCun(90), Karpathy(90)  
🇯🇵 Japanese: karaage0703(70), shi3z(65), windsurf(60)

⚡ Freshness bonus: 8/15(+30), 8/14 PM(+20), 8/14 AM(+10)"""
        
        print("  📝 Committing changes...")
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Commit failed: {result.stderr}")
            return False
        
        print("✅ Commit successful")
        
        # Push
        print("  📤 Pushing to GitHub...")
        result = subprocess.run(['git', 'push', 'origin', 'main'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Push failed: {result.stderr}")
            return False
        
        print("✅ Push successful")
        
        return True
        
    except Exception as e:
        print(f"❌ Deployment error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("📱 Enhanced SNS Posts Deployment")
    print("=" * 60)
    
    if deploy_enhanced_sns():
        print("\n" + "=" * 60)
        print("✅ Enhanced SNS functionality deployed successfully!")
        print("=" * 60)
        
        print(f"\n📱 Enhanced Features:")
        print(f"  📅 Target period: 8/14+ recent posts only")
        print(f"  📊 Display count: Up to 30 items (4x previous)")
        print(f"  🎯 Importance ranking: Enterprise accounts & influencers prioritized")
        print(f"  🚫 Old news excluded: No posts before 8/13")
        
        print(f"\n🏆 Prioritized accounts (8/14+ posts):")
        print(f"  🌟 OpenAI(100), Anthropic(100), Sam Altman(95)")
        print(f"  🤖 Google(90), Yann LeCun(90), Karpathy(90)")
        print(f"  🇯🇵 karaage0703(70), shi3z(65), windsurf(60)")
        
        print(f"\n⚡ Freshness bonus:")
        print(f"  🔥 8/15 posts: +30 points")
        print(f"  🌟 8/14 afternoon: +20 points")
        print(f"  ⭐ 8/14 morning: +10 points")
        
        print(f"\n🌐 Site URL:")
        print(f"   https://awano27.github.io/daily-ai-news/")
        print(f"\n💡 Enjoy fresh, high-quality SNS posts from 8/14 onwards!")
        
        return True
    else:
        print("\n❌ Deployment failed!")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)