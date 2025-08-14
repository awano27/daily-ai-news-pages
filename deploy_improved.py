#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy improved Daily AI News with enhanced features
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("=" * 60)
    print("Deploying Enhanced Daily AI News")
    print("=" * 60)
    
    # Set environment
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    
    try:
        # Step 1: Test improvements
        print("Step 1: Testing improvements...")
        import test_improvements
        if not test_improvements.main():
            print("❌ Tests failed!")
            return False
        
        # Step 2: Build with improvements
        print("\nStep 2: Building enhanced site...")
        import build
        build.main()
        
        # Step 3: Verify output
        if Path('index.html').exists():
            size = Path('index.html').stat().st_size
            print(f"\n✅ Enhanced site built ({size:,} bytes)")
            
            # Quick content verification
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Check for improvements
                checks = [
                    ('gradient', 'Modern header design'),
                    ('box-shadow', 'Enhanced card styling'),
                    ('Anthropic', 'New AI news sources'),
                    ('DeepMind', 'Additional research sources'),
                    ('2025-08-14', 'Current date content')
                ]
                
                print("\n✅ Verification results:")
                for check, description in checks:
                    if check in content:
                        print(f"  ✓ {description}")
                    else:
                        print(f"  ⚠ {description} not found")
        else:
            print("❌ Build failed - no index.html")
            return False
        
        # Step 4: Deploy to GitHub
        print("\nStep 3: Deploying to GitHub...")
        try:
            # Add all improved files
            subprocess.run(['git', 'add', 'feeds.yml', 'build.py', 'style.css', 'index.html'], check=True)
            
            # Create comprehensive commit message
            commit_msg = """feat: Major improvements to Daily AI News

✨ Enhanced news sources:
- Added Anthropic, DeepMind, AWS AI blogs
- Added LangChain, Papers With Code, Towards Data Science
- Improved Google News queries

🧠 Smart content filtering:
- AI relevance scoring system
- Advanced keyword filtering
- Exclusion of irrelevant content

🎨 Modern UI/UX:
- Gradient header design
- Card hover effects and shadows
- Improved typography and responsive design

🔧 Technical improvements:
- Live Google Sheets integration
- Better error handling and logging
- Enhanced caching system"""
            
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            subprocess.run(['git', 'push'], check=True)
            
            print("\n" + "=" * 60)
            print("🎉 ENHANCED DAILY AI NEWS DEPLOYED!")
            print("=" * 60)
            print("🌟 Major Improvements:")
            print("  📰 Higher quality news sources")
            print("  🤖 Smarter AI content filtering")
            print("  🎨 Modern, professional design")
            print("  📱 Mobile-responsive interface")
            print("  ⚡ Live Google Sheets integration")
            print("")
            print("🌍 Live site: https://awano27.github.io/daily-ai-news/")
            print("📊 More valuable AI news, better user experience!")
            print("=" * 60)
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Git operation failed: {e}")
            print("\n📋 Manual deployment commands:")
            print("git add feeds.yml build.py style.css index.html")
            print("git commit -m 'feat: Major improvements to Daily AI News'")
            print("git push")
            return False
    
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == "__main__":
    main()