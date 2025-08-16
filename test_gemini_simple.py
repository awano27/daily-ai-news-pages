#!/usr/bin/env python3
"""
Gemini APIの簡単なテスト
"""
import os
from dotenv import load_dotenv

# .envファイルを読み込み
load_dotenv()

# APIキーの確認
api_key = os.getenv('GEMINI_API_KEY')
if api_key and api_key != 'あなたのAPIキーをここに入力':
    print(f"✅ Gemini APIキーが設定されています: {api_key[:10]}...")
    
    # Gemini APIのテスト
    from gemini_analyzer import GeminiAnalyzer
    analyzer = GeminiAnalyzer()
    
    if analyzer.enabled:
        print("✅ Gemini API接続成功！")
        print("\n🧪 簡単なテストを実行...")
        
        test_news = [{
            'title': 'Test News',
            'summary': 'This is a test',
            'source': 'Test Source',
            'importance': 50
        }]
        
        result = analyzer.analyze_news_importance(test_news)
        if result:
            print("✅ ニュース分析テスト成功！")
            print(f"   Geminiスコア: {result[0].get('gemini_score', 'N/A')}")
    else:
        print("❌ Gemini API接続失敗")
else:
    print("❌ APIキーが設定されていません")
    print("   .envファイルのGEMINI_API_KEYを確認してください")