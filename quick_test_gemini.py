#!/usr/bin/env python3
"""
Quick Gemini Test - 最小限のGemini動作テスト
"""
import os
from pathlib import Path

def load_env_manual():
    """手動で.envファイルを読み込み"""
    env_path = Path('.env')
    if env_path.exists():
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def test_gemini_minimal():
    """最小限のGeminiテスト"""
    print("🔧 Quick Gemini Test")
    
    # 環境変数読み込み
    load_env_manual()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ GEMINI_API_KEY が見つかりません")
        return False
    
    print(f"✅ API Key: {api_key[:10]}...{api_key[-4:]}")
    
    try:
        from google import genai
        print("✅ google-genai インポート成功")
        
        # クライアント作成
        client = genai.Client()
        print("✅ Geminiクライアント作成成功")
        
        # シンプルなテスト（URLなし）
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents="Hello! Just say 'Hi' back."
        )
        
        if response.text:
            print(f"✅ Gemini応答成功: {response.text}")
            return True
        else:
            print("❌ 応答が空です")
            return False
            
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("💡 pip install google-genai を実行してください")
        return False
    except Exception as e:
        print(f"❌ Geminiテストエラー: {e}")
        return False

if __name__ == "__main__":
    success = test_gemini_minimal()
    if success:
        print("\n🎉 Gemini基本機能は正常に動作しています！")
        print("📋 次は python test_integration_fixed.py を実行してください")
    else:
        print("\n❌ Gemini設定に問題があります")
        print("🔧 トラブルシューティング:")
        print("1. API keyが正しいか確認")
        print("2. インターネット接続を確認") 
        print("3. pip install google-genai を再実行")