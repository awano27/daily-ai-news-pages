#!/usr/bin/env python3
"""
Gemini選別処理のデバッグ用スクリプト
"""
import os

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

def debug_gemini_selection():
    print("🔍 Gemini選別処理デバッグ開始...")
    
    analyzer = GeminiAnalyzer()
    
    if not analyzer.enabled:
        print("❌ Gemini API無効")
        return
    
    # テスト用の簡単な記事データ
    test_item = {
        'title': 'Test AI News Article',
        '_source': 'Test Source',
        '_summary': 'Test summary about AI development',
        '_dt': None
    }
    
    print("📤 テスト記事でGemini選別を実行...")
    
    # 簡潔なプロンプト
    evaluation_prompt = """
タイトル: Test AI News Article
ソース: Test Source

ビジネス・投資カテゴリに適した記事か評価してください。

JSON形式で回答:
{
  "valuable": true,
  "importance_score": 8,
  "reason": "理由"
}
"""
    
    print("🔄 Gemini APIリクエスト送信中...")
    try:
        result = analyzer._make_request(evaluation_prompt)
        if result:
            print(f"✅ 成功: {result[:200]}...")
        else:
            print("❌ レスポンスなし")
    except Exception as e:
        print(f"❌ エラー: {e}")
    
    print("🔍 デバッグ完了")

if __name__ == "__main__":
    debug_gemini_selection()