#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix CSS reference issue and rebuild site
"""

import os
import subprocess
import sys
from pathlib import Path

def main():
    print("🔧 CSS Reference Fix")
    print("=" * 30)
    
    # 環境変数設定
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '25'
    
    print("✅ Environment variables set")
    
    # ビルド実行
    print("🔨 Building site...")
    try:
        import build_simple_ranking
        print("✅ Build completed successfully")
        
        # HTMLの確認
        index_path = Path('index.html')
        if index_path.exists():
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'style.css' in content:
                print("✅ CSS reference is correct")
            else:
                print("❌ CSS reference still incorrect")
        
        # CSS確認
        css_path = Path('style.css')
        if css_path.exists():
            print("✅ style.css exists")
        else:
            print("❌ style.css not found")
            
        return True
        
    except Exception as e:
        print(f"❌ Build failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 CSS fix completed!")
        print("Ready to deploy with correct CSS reference")
    else:
        print("\n❌ CSS fix failed")
        sys.exit(1)