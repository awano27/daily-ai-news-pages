#!/usr/bin/env python3
"""
403エラー根本修正のテスト
"""
from dotenv import load_dotenv
load_dotenv()

def test_403_fix():
    print("🧪 403エラー根本修正をテスト中...")
    
    # URL フィルターテスト
    try:
        from url_filter import is_403_url, filter_403_urls
        
        test_url = "https://news.google.com/rss/articles/CBMijwFBVV95cUxPZFprVjVNbUFEa25tZXJfbzlyd1hiSEEyRmR1dlFIQUdCRzI0MTJSR3l6elFyUXBlTVdhQkhQY2ZSdDZmbXR0YlFMdmZjMHpTNFVZczZTb1lVWVJkWDJCdlhHeHZMdnlmT3Z3dEJjem1SaV85aWdfLWxyUjdydGNqQVhyeGpjem5fd1NLcC0xSQ?oc=5"
        
        print(f"🔍 テストURL: {test_url[:50]}...")
        print(f"🚫 403判定: {is_403_url(test_url)}")
        
        if is_403_url(test_url):
            print("✅ 403 URLが正しく検出されました")
        else:
            print("❌ 403 URL検出に失敗")
            
    except ImportError as e:
        print(f"❌ URL フィルターインポートエラー: {e}")
        return False
    
    # ダッシュボード生成テスト
    try:
        from generate_comprehensive_dashboard import analyze_ai_landscape
        
        print("\n📊 ダッシュボード生成テスト...")
        data = analyze_ai_landscape()
        
        print("✅ ダッシュボード生成成功")
        print(f"📊 総アイテム数: {data['stats']['total_items']}")
        
        # 403 URLが含まれていないかチェック
        problem_urls = []
        for category in data['categories'].values():
            for topic in category.get('featured_topics', []):
                url = topic.get('url', '')
                if is_403_url(url):
                    problem_urls.append(url)
        
        if problem_urls:
            print(f"❌ {len(problem_urls)}件の403 URLが残っています:")
            for url in problem_urls[:3]:
                print(f"  🚫 {url[:50]}...")
        else:
            print("✅ 403 URLは完全に除外されました")
            
        return len(problem_urls) == 0
        
    except Exception as e:
        print(f"❌ ダッシュボード生成エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_403_fix()
    print(f"\n🎯 結果: {'成功' if success else '失敗'}")
    
    if success:
        print("🎉 403エラーが根本的に解決されました！")
        print("🚀 GitHub Pagesにデプロイ準備完了")
    else:
        print("⚠️ まだ問題が残っています")