#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Summary Length Test - 要約の文字数制限テスト
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
    """要約の文字数制限テスト"""
    print("🧪 Summary Length Test - 300文字制限の確認")
    print("=" * 60)
    
    # 環境変数読み込み
    load_env()
    
    try:
        from enhanced_x_processor import EnhancedXProcessor
        
        processor = EnhancedXProcessor()
        
        # Google Sheets URL
        csv_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
        
        print("📡 X投稿を処理中...")
        posts = processor.process_x_posts(csv_url, max_posts=5)
        
        if posts:
            build_items = processor.convert_to_build_format(posts)
            
            print(f"\n✅ 処理完了: {len(build_items)}件の投稿")
            print("\n📝 要約の文字数チェック:")
            print("-" * 60)
            
            for i, item in enumerate(build_items, 1):
                summary = item.get('_summary', '')
                title = item.get('title', '')
                enhanced = item.get('_enhanced', False)
                
                print(f"\n{i}. {title}")
                print(f"   強化済み: {'✅' if enhanced else '❌'}")
                print(f"   要約文字数: {len(summary)}文字")
                
                if len(summary) > 300:
                    print(f"   ⚠️ 300文字を超えています！")
                else:
                    print(f"   ✅ 300文字以内")
                
                print(f"   要約: {summary[:100]}...")
                
                if len(summary) > 300:
                    print(f"   📊 超過文字数: {len(summary) - 300}文字")
            
            # 統計情報
            over_limit = [item for item in build_items if len(item.get('_summary', '')) > 300]
            print(f"\n📊 統計:")
            print(f"   総投稿数: {len(build_items)}件")
            print(f"   300文字以内: {len(build_items) - len(over_limit)}件")
            print(f"   300文字超過: {len(over_limit)}件")
            
            if len(over_limit) == 0:
                print("\n🎉 すべての要約が300文字以内です！")
            else:
                print(f"\n⚠️ {len(over_limit)}件の要約が300文字を超えています")
                print("修正が必要です。")
        
        else:
            print("❌ 投稿の処理に失敗しました")
        
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")