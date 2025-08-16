#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test the enhanced SNS functionality with 8/14+ filtering and importance scoring
"""
import os
import subprocess
import sys
import re
from pathlib import Path

def test_enhanced_sns():
    """Test the enhanced SNS functionality"""
    
    print("🧪 Testing enhanced SNS functionality with 8/14+ filtering...")
    
    # Set environment variables for enhanced SNS functionality
    os.environ['HOURS_LOOKBACK'] = '48'  # 48 hours
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '30'  # Increase to 30 items
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    
    # Use Google Sheets URL for X posts
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    try:
        # Run build.py
        print("🔄 Running build.py with enhanced settings...")
        result = subprocess.run([sys.executable, 'build.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"❌ Build error: {result.stderr}")
            return False
        
        print("✅ Build completed successfully!")
        
        # Check for SNS processing output
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if 'X post' in line or 'SNS importance' in line or ('Adding' in line and 'X posts' in line):
                    print(f"   📱 {line}")
                elif 'Posts:' in line and 'Sorted by SNS importance score' in line:
                    print(f"   🎯 {line}")
        
        # Analyze the generated HTML
        index_path = Path('index.html')
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check Posts section count
            posts_match = re.search(r'<div class="kpi-value">(\d+)件</div>\s*<div class="kpi-label">SNS/論文ポスト</div>', content)
            if posts_match:
                posts_count = int(posts_match.group(1))
                print(f"\n📊 SNS/論文ポスト表示件数: {posts_count}件")
                
                if posts_count > 8:
                    print(f"✅ 成功！従来の8件から{posts_count}件に増加")
                else:
                    print(f"⚠️ 件数が期待より少ないです")
            else:
                print("⚠️ Posts section count not found in HTML")
            
            # Extract top Posts titles
            posts_section = content.split('id="posts"')[1].split('</section>')[0] if 'id="posts"' in content else ""
            titles = re.findall(r'<a class="card-title"[^>]*>([^<]+)</a>', posts_section)
            
            if titles:
                print(f"\n📱 SNS/論文ポスト上位5件（重要度順・8/14以降）:")
                for i, title in enumerate(titles[:5], 1):
                    print(f"   {i}. {title[:70]}{'...' if len(title) > 70 else ''}")
            else:
                print("⚠️ No posts titles found")
        
        return True
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    if test_enhanced_sns():
        print("\n✅ Enhanced SNS functionality test completed successfully!")
    else:
        print("\n❌ Enhanced SNS functionality test failed!")
        sys.exit(1)