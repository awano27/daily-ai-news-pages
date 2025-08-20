#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Enhanced Build Integration - build.pyにEnhanced X Processorを統合
"""
import os
import sys
from pathlib import Path

# Enhanced X Processorをインポート
try:
    from enhanced_x_processor import EnhancedXProcessor
    ENHANCED_X_AVAILABLE = True
    print("✅ Enhanced X Processor: 利用可能")
except ImportError:
    ENHANCED_X_AVAILABLE = False
    print("⚠️ Enhanced X Processor: 利用不可")

def enhanced_gather_x_posts(csv_path: str) -> list[dict]:
    """
    強化版X投稿収集機能 - 重複除去とGemini分析を統合
    
    従来のgather_x_postsを置き換える関数
    """
    print(f"🚀 Enhanced X Posts Collection from: {csv_path}")
    
    if ENHANCED_X_AVAILABLE:
        try:
            # Enhanced X Processorを使用
            processor = EnhancedXProcessor()
            posts = processor.process_x_posts(csv_path, max_posts=20)
            
            if posts:
                build_items = processor.convert_to_build_format(posts)
                print(f"✅ Enhanced処理完了: {len(build_items)}件の高品質X投稿")
                
                # 統計を表示
                enhanced_count = sum(1 for item in build_items if item.get('_enhanced', False))
                high_priority = sum(1 for item in build_items if item.get('_priority', 0) >= 3)
                
                print(f"   📊 Gemini強化済み: {enhanced_count}件")
                print(f"   ⭐ 高重要度: {high_priority}件")
                
                return build_items
            else:
                print("⚠️ Enhanced処理結果が空 - フォールバックを実行")
        except Exception as e:
            print(f"⚠️ Enhanced処理でエラー: {e}")
            print("🔄 従来の処理にフォールバック")
    
    # フォールバック: 従来のgather_x_posts相当の処理
    print("🔄 従来のX投稿処理を実行")
    try:
        # build.pyから従来の処理をインポート
        import build
        return build.gather_x_posts(csv_path)
    except Exception as e:
        print(f"❌ フォールバック処理でもエラー: {e}")
        return []

def integrate_enhanced_x_processing():
    """
    build.pyのgather_x_posts関数を置き換え
    """
    try:
        import build
        
        # 元の関数をバックアップ
        build.original_gather_x_posts = build.gather_x_posts
        
        # 強化版関数で置き換え
        build.gather_x_posts = enhanced_gather_x_posts
        
        print("✅ build.py のX投稿処理を強化版に置き換え完了")
        return True
        
    except Exception as e:
        print(f"❌ build.py統合でエラー: {e}")
        return False

def main():
    """統合テスト"""
    print("🧪 Enhanced Build Integration Test")
    print("=" * 50)
    
    # 統合を実行
    success = integrate_enhanced_x_processing()
    
    if success:
        print("✅ 統合成功 - build.pyで強化版X処理が利用可能")
        
        # テスト実行
        try:
            import build
            csv_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
            
            print("\n🔄 統合されたX投稿処理をテスト...")
            x_posts = build.gather_x_posts(csv_url)
            
            print(f"📊 テスト結果: {len(x_posts)}件のX投稿")
            
            if x_posts:
                enhanced_posts = [p for p in x_posts if p.get('_enhanced', False)]
                print(f"   🧠 Gemini強化済み: {len(enhanced_posts)}件")
                
                # サンプル表示
                print("\n📝 処理済み投稿サンプル:")
                for i, post in enumerate(x_posts[:3], 1):
                    print(f"\n   {i}. {post.get('title', 'N/A')}")
                    print(f"      要約: {post.get('_summary', 'N/A')[:80]}...")
                    print(f"      強化: {'✅' if post.get('_enhanced', False) else '❌'}")
            
        except Exception as e:
            print(f"⚠️ テスト実行でエラー: {e}")
    
    else:
        print("❌ 統合失敗")

if __name__ == "__main__":
    main()