#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test CSV Fix - CSV構造修正のテスト
"""
import os
from pathlib import Path

def load_env():
    """環境変数を.envファイルから読み込み"""
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def main():
    """CSV修正版テスト"""
    print("🔧 CSV Structure Fix Test")
    print("=" * 50)
    
    # 環境変数読み込み
    load_env()
    
    try:
        from enhanced_x_processor import EnhancedXProcessor
        
        processor = EnhancedXProcessor()
        print("✅ Enhanced X Processor initialized")
        
        # Google Sheets URL
        csv_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
        
        print(f"\n📡 Testing CSV structure fix...")
        posts = processor.process_x_posts(csv_url, max_posts=3)  # 少数でテスト
        
        if posts:
            print(f"\n🎉 Success! Processed {len(posts)} posts")
            
            # build形式に変換
            build_items = processor.convert_to_build_format(posts)
            
            print(f"\n📝 Processed posts:")
            for i, item in enumerate(build_items, 1):
                summary = item.get('_summary', '')
                title = item.get('title', '')
                
                print(f"\n{i}. {title}")
                print(f"   Summary: {summary[:100]}...")
                print(f"   Length: {len(summary)} chars ({'✅' if len(summary) <= 300 else '❌'})")
        else:
            print("❌ Still no posts processed")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()