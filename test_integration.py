#!/usr/bin/env python3
"""
Enhanced System Test - Gemini URL context統合のテスト
"""
import os
from pathlib import Path

def test_gemini_integration():
    """Gemini統合のテスト"""
    print("🧪 Gemini URL Context統合テスト")
    
    # 環境変数チェック
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY が設定されていません")
        return False
    
    try:
        from gemini_url_context import GeminiURLContextClient
        
        client = GeminiURLContextClient()
        print("✅ Geminiクライアント初期化成功")
        
        # 簡単なテスト
        test_urls = ["https://ai.google.dev/"]
        result = client.generate_from_urls(
            "このページの要点を1文で教えてください",
            test_urls
        )
        
        if result.get("text"):
            print("✅ URL解析テスト成功")
            print(f"📝 結果: {result['text'][:100]}...")
            return True
        else:
            print("❌ URL解析テスト失敗")
            return False
            
    except Exception as e:
        print(f"❌ テスト失敗: {e}")
        return False

def test_enhanced_collector():
    """強化版収集システムのテスト"""
    print("\n📰 Enhanced News Collector テスト")
    
    try:
        from enhanced_news_collector import EnhancedNewsCollector
        
        collector = EnhancedNewsCollector()
        print("✅ Enhanced Collector初期化成功")
        
        # feeds.ymlの存在確認
        if not Path("feeds.yml").exists():
            print("⚠️ feeds.yml が見つかりません（テスト継続）")
        
        return True
        
    except Exception as e:
        print(f"❌ Enhanced Collector テスト失敗: {e}")
        return False

def test_integration():
    """統合テスト"""
    print("\n🔗 統合テスト")
    
    try:
        from enhanced_build import enhanced_build_process
        print("✅ enhanced_build モジュール読み込み成功")
        return True
        
    except Exception as e:
        print(f"❌ 統合テスト失敗: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Enhanced AI News System - Integration Test\n")
    
    results = []
    results.append(test_gemini_integration())
    results.append(test_enhanced_collector())
    results.append(test_integration())
    
    print(f"\n📊 テスト結果: {sum(results)}/{len(results)} 成功")
    
    if all(results):
        print("✅ すべてのテストに合格しました！")
        print("\n🎉 次のステップ:")
        print("1. pip install -r requirements.txt")
        print("2. .envファイルにGEMINI_API_KEYを設定")
        print("3. python enhanced_build.py を実行")
    else:
        print("❌ 一部のテストが失敗しました")
        print("エラー内容を確認して設定を見直してください")
