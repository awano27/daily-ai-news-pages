#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced X Processing Test - 強化版X投稿処理のテスト
"""
import os
import sys
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
    """メインテスト"""
    print("🚀 Enhanced X Processing - Complete Test")
    print("=" * 60)
    
    # 環境変数読み込み
    load_env()
    
    # Gemini API確認
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        print(f"✅ GEMINI_API_KEY: {api_key[:10]}...{api_key[-4:]}")
    else:
        print("⚠️ GEMINI_API_KEY not set - フォールバック処理のみ")
    
    try:
        # Enhanced X Processorをテスト
        print("\n🧪 1. Enhanced X Processor単体テスト")
        from enhanced_x_processor import EnhancedXProcessor
        
        processor = EnhancedXProcessor()
        
        csv_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
        posts = processor.process_x_posts(csv_url, max_posts=5)
        
        if posts:
            print(f"✅ X投稿処理成功: {len(posts)}件")
            build_items = processor.convert_to_build_format(posts)
            
            print("\n📝 処理結果サンプル:")
            for i, item in enumerate(build_items[:2], 1):
                print(f"\n   {i}. {item['title']}")
                print(f"      URL: {item['link']}")
                print(f"      要約: {item['_summary'][:100]}...")
                print(f"      強化済み: {'✅' if item.get('_enhanced', False) else '❌'}")
                print(f"      重要度: {item.get('_priority', 'N/A')}")
        else:
            print("❌ X投稿処理失敗")
        
        # 統合テスト
        print("\n🧪 2. Build.py統合テスト")
        from enhanced_build_integration import integrate_enhanced_x_processing
        
        integration_success = integrate_enhanced_x_processing()
        
        if integration_success:
            print("✅ build.py統合成功")
            
            # 統合された関数をテスト
            import build
            integrated_posts = build.gather_x_posts(csv_url)
            
            print(f"📊 統合テスト結果: {len(integrated_posts)}件")
            
            enhanced_count = sum(1 for p in integrated_posts if p.get('_enhanced', False))
            print(f"   🧠 Gemini強化投稿: {enhanced_count}件")
        else:
            print("❌ build.py統合失敗")
        
        print("\n" + "=" * 60)
        print("📋 テスト完了サマリー:")
        print(f"   Enhanced X Processor: {'✅' if posts else '❌'}")
        print(f"   Build.py統合: {'✅' if integration_success else '❌'}")
        print(f"   Gemini強化機能: {'✅' if api_key and enhanced_count > 0 else '❌'}")
        
        if posts and integration_success:
            print("\n🎉 Enhanced X Processing システム準備完了！")
            print("📝 次のステップ:")
            print("   1. python build.py でサイト生成")
            print("   2. 重複が解決され、より詳細な要約が提供される")
            print("   3. 重要度に基づく優先表示")
        else:
            print("\n⚠️ 一部機能に問題があります")
            
    except Exception as e:
        print(f"❌ テスト実行エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")