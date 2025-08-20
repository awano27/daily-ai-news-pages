#!/usr/bin/env python3
"""
Enhanced System Test - Gemini URL context統合のテスト（修正版）
"""
import os
import sys
from pathlib import Path

# .envファイルから環境変数を明示的にロード
def load_env_file():
    """環境変数を.envファイルから読み込み"""
    env_path = Path('.env')
    if env_path.exists():
        print("🔧 .envファイルから環境変数を読み込み中...")
        try:
            from dotenv import load_dotenv
            load_dotenv()
            print("✅ python-dotenvで読み込み完了")
        except ImportError:
            print("⚠️ python-dotenvが利用できません、手動で読み込み...")
            # 手動で.envファイルを読み込み
            with open(env_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
            print("✅ 手動読み込み完了")
    else:
        print("❌ .envファイルが見つかりません")

def test_env_setup():
    """環境設定のテスト"""
    print("🔧 環境設定テスト")
    
    # .env読み込み
    load_env_file()
    
    # API key確認
    api_key = os.getenv("GEMINI_API_KEY")
    if api_key:
        masked_key = f"{api_key[:10]}...{api_key[-4:]}" if len(api_key) > 14 else "設定済み"
        print(f"✅ GEMINI_API_KEY: {masked_key}")
        return True
    else:
        print("❌ GEMINI_API_KEY が設定されていません")
        return False

def test_gemini_integration():
    """Gemini統合のテスト"""
    print("\n🧪 Gemini URL Context統合テスト")
    
    # 環境変数チェック
    if not os.getenv("GEMINI_API_KEY"):
        print("❌ GEMINI_API_KEY が設定されていません")
        return False
    
    try:
        from gemini_url_context import GeminiURLContextClient
        
        print("📡 Geminiクライアント初期化中...")
        client = GeminiURLContextClient()
        print("✅ Geminiクライアント初期化成功")
        
        # 簡単なテスト（軽量なURL）
        test_urls = ["https://www.google.com/"]
        print(f"🔍 テストURL解析: {test_urls[0]}")
        
        result = client.generate_from_urls(
            "このサイトの名前を1語で答えてください",
            test_urls
        )
        
        if result.get("text") and "error" not in result:
            print("✅ URL解析テスト成功")
            print(f"📝 結果: {result['text'][:100]}...")
            
            # 使用量情報
            usage = result.get("usage_metadata")
            if usage:
                print(f"📊 使用量: {getattr(usage, 'total_token_count', '不明')} tokens")
            
            return True
        else:
            print(f"❌ URL解析テスト失敗: {result.get('error', '不明なエラー')}")
            return False
            
    except ImportError as e:
        print(f"❌ インポートエラー: {e}")
        print("💡 'pip install google-genai' を実行してください")
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
        else:
            print("✅ feeds.yml 確認完了")
        
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

def create_sample_feeds():
    """サンプルfeeds.ymlを作成"""
    print("\n📝 サンプルfeeds.yml作成")
    
    if not Path("feeds.yml").exists():
        sample_feeds = """business:
  - url: "https://techcrunch.com/feed/"
    name: "TechCrunch"
  - url: "https://venturebeat.com/feed/"
    name: "VentureBeat"

tech:
  - url: "https://www.reddit.com/r/MachineLearning/.rss"
    name: "Reddit ML"

posts:
  - url: "https://www.reddit.com/r/artificial/.rss"
    name: "Reddit AI"
"""
        
        with open("feeds.yml", "w", encoding="utf-8") as f:
            f.write(sample_feeds)
        
        print("✅ サンプルfeeds.yml作成完了")
    else:
        print("✅ feeds.yml既存確認")

def main():
    """メインテスト実行"""
    print("🚀 Enhanced AI News System - Integration Test (Fixed)\n")
    
    # サンプルファイル作成
    create_sample_feeds()
    
    # テスト実行
    results = []
    results.append(test_env_setup())
    results.append(test_gemini_integration())
    results.append(test_enhanced_collector())
    results.append(test_integration())
    
    print(f"\n📊 テスト結果: {sum(results)}/{len(results)} 成功")
    
    if all(results):
        print("✅ すべてのテストに合格しました！")
        print("\n🎉 システム準備完了:")
        print("1. python enhanced_build.py で強化版ビルド実行")
        print("2. python enhanced_news_collector.py で単体テスト")
        print("3. Gemini URL context機能をフル活用可能")
    elif sum(results) >= 3:
        print("✅ 基本機能は動作します")
        print("一部の高度な機能に問題がありますが、システムは使用可能です")
    else:
        print("❌ 重要な機能に問題があります")
        print("\n🔧 トラブルシューティング:")
        print("1. GEMINI_API_KEYが正しく設定されているか確認")
        print("2. pip install google-genai を再実行")
        print("3. インターネット接続を確認")

if __name__ == "__main__":
    main()