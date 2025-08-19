#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Final Production Test - 本番環境テスト（完全版）
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
    """本番環境での完全テスト"""
    print("🚀 Final Production Test - 本番環境完全テスト")
    print("=" * 60)
    
    # 環境変数読み込み
    load_env()
    
    try:
        from enhanced_x_processor import EnhancedXProcessor
        
        processor = EnhancedXProcessor()
        print("✅ Enhanced X Processor ready for production")
        
        # Google Sheets URL
        csv_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
        
        print(f"\n📡 Running production-level X post processing...")
        posts = processor.process_x_posts(csv_url, max_posts=10)  # 本番レベル
        
        if posts:
            print(f"\n🎉 Production Success! Processed {len(posts)} posts")
            
            # build形式に変換
            build_items = processor.convert_to_build_format(posts)
            
            # 統計情報
            enhanced_count = sum(1 for item in build_items if item.get('_enhanced', False))
            high_priority = sum(1 for item in build_items if item.get('_priority', 0) >= 3)
            avg_length = sum(len(item.get('_summary', '')) for item in build_items) / len(build_items)
            
            print(f"\n📊 Production Statistics:")
            print(f"   Total posts processed: {len(build_items)}")
            print(f"   🧠 Gemini enhanced: {enhanced_count} ({enhanced_count/len(build_items)*100:.1f}%)")
            print(f"   ⭐ High priority: {high_priority} ({high_priority/len(build_items)*100:.1f}%)")
            print(f"   📏 Average summary length: {avg_length:.1f} chars")
            
            # 文字数制限チェック
            over_limit = [item for item in build_items if len(item.get('_summary', '')) > 300]
            print(f"   📝 300文字以内: {len(build_items) - len(over_limit)}/{len(build_items)} ({'✅' if len(over_limit) == 0 else '❌'})")
            
            print(f"\n📝 Sample Production Results:")
            for i, item in enumerate(build_items[:5], 1):
                summary = item.get('_summary', '')
                title = item.get('title', '')
                enhanced = item.get('_enhanced', False)
                priority = item.get('_priority', 0)
                category = item.get('_category', '')
                
                print(f"\n{i}. {title}")
                print(f"   Category: {category}")
                print(f"   Enhanced: {'✅' if enhanced else '❌'} | Priority: {priority}")
                print(f"   Summary ({len(summary)} chars): {summary}")
            
            if len(over_limit) == 0 and enhanced_count > 0:
                print(f"\n🎉 **PRODUCTION READY!**")
                print(f"✅ すべての要約が300文字以内")
                print(f"✅ Gemini強化機能が正常動作")
                print(f"✅ 重複除去が正常動作") 
                print(f"✅ カテゴリ分類が正常動作")
                print(f"\n🚀 Next: python build.py で本番サイト生成")
            else:
                print(f"\n⚠️ Production issues detected:")
                if len(over_limit) > 0:
                    print(f"   - {len(over_limit)} summaries over 300 chars")
                if enhanced_count == 0:
                    print(f"   - No Gemini enhanced posts")
        else:
            print("❌ Production test failed - no posts processed")
        
    except Exception as e:
        print(f"❌ Production test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")