#!/usr/bin/env python3
"""
Gemini API機能のテストスクリプト
"""
import os
import sys
from gemini_analyzer import GeminiAnalyzer

def test_gemini_functionality():
    """Gemini APIの機能をテスト"""
    print("🧪 Gemini API機能テスト中...")
    
    # Gemini APIキーの確認
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key or api_key == 'your_gemini_api_key_here':
        print("❌ GEMINI_API_KEY環境変数が設定されていません")
        print("\n📝 設定方法:")
        print("1. Google AI StudioでAPIキーを取得: https://makersuite.google.com/app/apikey")
        print("2. 環境変数を設定:")
        print("   Windows: set GEMINI_API_KEY=your_actual_api_key")
        print("   macOS/Linux: export GEMINI_API_KEY=your_actual_api_key")
        print("3. または.envファイルに追加:")
        print("   GEMINI_API_KEY=your_actual_api_key")
        return False
    
    # GeminiAnalyzerを初期化
    analyzer = GeminiAnalyzer(api_key)
    
    if not analyzer.enabled:
        print("❌ Gemini APIが初期化できませんでした")
        return False
    
    print("✅ Gemini API初期化成功")
    
    # テスト用ニュースデータ
    test_news = [
        {
            'title': 'OpenAI announces GPT-5 with revolutionary capabilities',
            'summary': 'OpenAI has unveiled GPT-5, featuring unprecedented reasoning abilities and multimodal understanding...',
            'source': 'TechCrunch',
            'importance': 70
        },
        {
            'title': 'Meta launches new AI safety protocols',
            'summary': 'Meta introduces comprehensive safety measures for AI development and deployment...',
            'source': 'VentureBeat',
            'importance': 60
        }
    ]
    
    # ニュース重要度分析のテスト
    print("\n🔍 ニュース重要度分析をテスト...")
    try:
        enhanced_news = analyzer.analyze_news_importance(test_news)
        
        for i, item in enumerate(enhanced_news[:2]):
            print(f"\n📰 ニュース {i+1}:")
            print(f"   タイトル: {item['title'][:50]}...")
            print(f"   Geminiスコア: {item.get('gemini_score', 'N/A')}")
            print(f"   理由: {item.get('gemini_reason', 'N/A')}")
            print(f"   カテゴリ: {item.get('gemini_category', 'N/A')}")
            print(f"   キーワード: {item.get('gemini_keywords', [])}")
        
        print("✅ ニュース重要度分析テスト成功")
    except Exception as e:
        print(f"❌ ニュース重要度分析テスト失敗: {e}")
        return False
    
    # 市場洞察生成のテスト
    print("\n📊 市場洞察生成をテスト...")
    try:
        test_data = {
            'categories': {
                'business': {
                    'featured_topics': enhanced_news[:3]
                }
            }
        }
        
        insights = analyzer.generate_market_insights(test_data)
        print(f"   市場センチメント: {insights.get('market_sentiment', 'N/A')}")
        print(f"   主要トレンド: {insights.get('key_trends', [])}")
        print(f"   投資分野: {insights.get('investment_focus', [])}")
        print(f"   主要企業: {insights.get('major_players', [])}")
        print(f"   見通し: {insights.get('outlook', 'N/A')}")
        
        print("✅ 市場洞察生成テスト成功")
    except Exception as e:
        print(f"❌ 市場洞察生成テスト失敗: {e}")
        return False
    
    # エグゼクティブサマリー強化のテスト
    print("\n📋 エグゼクティブサマリー強化をテスト...")
    try:
        test_dashboard = {
            'stats': {
                'total_items': 100,
                'active_companies': 5
            },
            'market_insights': insights,
            'executive_summary': {}
        }
        
        enhanced_summary = analyzer.enhance_executive_summary(test_dashboard)
        print(f"   ヘッドライン: {enhanced_summary.get('headline', 'N/A')}")
        print(f"   キーポイント: {enhanced_summary.get('key_points', [])}")
        print(f"   重要トピック: {enhanced_summary.get('important_topic', 'N/A')}")
        print(f"   明日の注目点: {enhanced_summary.get('tomorrow_focus', 'N/A')}")
        
        print("✅ エグゼクティブサマリー強化テスト成功")
    except Exception as e:
        print(f"❌ エグゼクティブサマリー強化テスト失敗: {e}")
        return False
    
    print("\n🎉 すべてのGemini API機能テストが正常に完了しました!")
    print("\n📋 利用可能な機能:")
    print("✅ AIによるニュース重要度評価 (1-100スコア)")
    print("✅ 市場動向の洞察分析")
    print("✅ エグゼクティブサマリーの強化")
    print("✅ 技術トレンドの予測")
    print("✅ 重要度に基づく自動ソート")
    
    return True

if __name__ == "__main__":
    success = test_gemini_functionality()
    
    if success:
        print("\n🚀 Gemini API機能が正常に動作しています")
        print("💡 generate_comprehensive_dashboard.pyでGemini機能を有効化できます")
    else:
        print("\n⚠️ Gemini API設定を確認してください")
        sys.exit(1)