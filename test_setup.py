#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
システムセットアップ検証スクリプト
Free Scraping Platform with Gemini API
"""

import sys
import os

# .envファイルを読み込み
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenvがない場合は手動で.envを読み込み
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

def test_imports():
    """必要ライブラリのインポートテスト"""
    print("🔍 ライブラリインポートテスト...")
    
    try:
        import requests
        print("✅ requests: OK")
    except ImportError as e:
        print(f"❌ requests: {e}")
        return False
    
    try:
        import bs4
        print("✅ beautifulsoup4: OK")
    except ImportError as e:
        print(f"❌ beautifulsoup4: {e}")
        return False
    
    try:
        import google.generativeai as genai
        print("✅ google-generativeai: OK")
    except ImportError as e:
        print(f"❌ google-generativeai: {e}")
        return False
    
    try:
        import yaml
        print("✅ pyyaml: OK")
    except ImportError as e:
        print(f"❌ pyyaml: {e}")
        return False
    
    return True

def test_gemini_connection():
    """Gemini API接続テスト"""
    print("\n🔍 Gemini API接続テスト...")
    
    # 環境変数からAPIキーを取得
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        print("❌ GEMINI_API_KEY環境変数が設定されていません")
        print("   .envファイルにGEMINI_API_KEY=your_api_key_hereを追加してください")
        return False
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # モデル一覧取得で接続テスト
        models = list(genai.list_models())
        if models:
            print("✅ Gemini API接続: OK")
            print(f"   利用可能モデル数: {len(models)}")
            return True
        else:
            print("❌ Gemini API接続: モデル一覧が空です")
            return False
            
    except Exception as e:
        print(f"❌ Gemini API接続エラー: {e}")
        return False

def test_scraper():
    """スクレイパー基本動作テスト"""
    print("\n🔍 スクレイパー動作テスト...")
    
    try:
        from scrapers.beautifulsoup_scraper import BeautifulSoupScraper
        
        scraper = BeautifulSoupScraper()
        
        # 簡単なHTTPリクエストテスト
        test_url = "https://httpbin.org/get"
        result = scraper.scrape(test_url)
        
        if result and 'success' in result and result['success']:
            print("✅ スクレイパー動作: OK")
            return True
        else:
            print("❌ スクレイパー動作: 結果が期待通りではありません")
            return False
            
    except Exception as e:
        print(f"❌ スクレイパーテストエラー: {e}")
        return False

def test_file_structure():
    """ファイル構造確認"""
    print("\n🔍 ファイル構造確認...")
    
    required_files = [
        'requirements.txt',
        '.env',
        'scrapers/__init__.py',
        'scrapers/beautifulsoup_scraper.py',
        'scrapers/gemini_extractor.py',
        'scripts/run_scraper.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} が見つかりません")
            all_exist = False
    
    return all_exist

def main():
    """メインテスト実行"""
    print("🚀 Free Scraping Platform セットアップ検証\n")
    
    # テスト実行
    tests = [
        ("ファイル構造", test_file_structure),
        ("ライブラリインポート", test_imports),
        ("Gemini API接続", test_gemini_connection),
        ("スクレイパー動作", test_scraper)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name}テスト中にエラー: {e}")
            results.append((test_name, False))
        print()
    
    # 結果サマリー
    print("=" * 50)
    print("📋 テスト結果サマリー")
    print("=" * 50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ 合格" if result else "❌ 不合格"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n合格: {passed}/{len(results)}")
    
    if passed == len(results):
        print("\n🎉 すべてのテストが合格しました！")
        print("次のコマンドでスクレイピングを開始できます:")
        print("  python scripts/run_scraper.py https://example.com")
        print("  または run_basic_scrape.bat を実行")
    else:
        print("\n⚠️  一部のテストが失敗しました。")
        print("上記のエラーメッセージを確認して修正してください。")

if __name__ == "__main__":
    main()