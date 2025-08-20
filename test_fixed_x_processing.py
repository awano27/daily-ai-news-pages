#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Fixed X Processing - 修正版X投稿処理のテスト
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
    """修正版テスト"""
    print("🧪 Fixed X Processing Test - CSV列名修正版テスト")
    print("=" * 60)
    
    # 環境変数読み込み
    load_env()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✅ GEMINI_API_KEY: {api_key[:10]}...{api_key[-4:]}")
    else:
        print("⚠️ GEMINI_API_KEY not set")
    
    try:
        from enhanced_x_processor import EnhancedXProcessor
        
        processor = EnhancedXProcessor()
        print("✅ Enhanced X Processor initialized")
        
        # Google Sheets URL
        csv_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
        
        print(f"\n📡 Processing X posts from CSV...")
        posts = processor.process_x_posts(csv_url, max_posts=5)
        
        if posts:
            print(f"\n✅ Successfully processed {len(posts)} posts")
            
            # build形式に変換
            build_items = processor.convert_to_build_format(posts)
            
            print(f"\n📝 Sample processed posts:")
            for i, item in enumerate(build_items[:3], 1):
                summary = item.get('_summary', '')
                title = item.get('title', '')
                enhanced = item.get('_enhanced', False)
                
                print(f"\n{i}. {title}")
                print(f"   Enhanced: {'✅' if enhanced else '❌'}")
                print(f"   Summary length: {len(summary)} chars")
                print(f"   Summary: {summary[:100]}...")
                
                if len(summary) > 300:
                    print(f"   ⚠️ Over 300 chars! ({len(summary)} chars)")
                else:
                    print(f"   ✅ Within 300 chars")
        else:
            print("❌ No posts processed - check debug output above")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")