#!/usr/bin/env python3
"""
Gemini API機能のテストスクリプト - 修正版
"""
import os
import sys

# 手動で.envファイルを読み込み
try:
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()
        print("✅ .envファイル読み込み完了")
except Exception as e:
    print(f"⚠️ .envファイル読み込みエラー: {e}")

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
    
    # 基本的なAPIリクエストテスト
    print("\n🔍 基本的なAPIリクエストをテスト...")
    try:
        test_prompt = """
タイトル: OpenAI releases GPT-5
ソース: TechCrunch

ビジネス・投資カテゴリに適した記事か評価してください。

JSON形式で回答:
{
  "valuable": true,
  "importance_score": 8,
  "reason": "重要なAIニュース"
}
"""
        result = analyzer._make_request(test_prompt)
        
        if result:
            print(f"✅ APIレスポンス取得成功: {result[:100]}...")
        else:
            print("❌ APIレスポンス取得失敗")
            return False
        
        print("✅ 基本APIテスト成功")
    except Exception as e:
        print(f"❌ 基本APIテスト失敗: {e}")
        return False
    
    print("\n🎉 Gemini API基本テストが正常に完了しました!")
    print("\n📋 修正点:")
    print("✅ gemini-1.5-flash-latest モデルに変更")
    print("✅ レスポンス処理を簡素化")
    print("✅ プロンプトを短縮")
    print("✅ エラーハンドリング強化")
    
    return True

if __name__ == "__main__":
    success = test_gemini_functionality()
    
    if success:
        print("\n🚀 Gemini API機能が正常に動作しています")
        print("💡 generate_comprehensive_dashboard.pyでGemini機能を有効化できます")
    else:
        print("\n⚠️ Gemini API設定を確認してください")
        sys.exit(1)