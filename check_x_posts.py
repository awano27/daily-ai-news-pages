#!/usr/bin/env python3
"""
Check X posts functionality in build_simple_ranking.py
"""
import os
import sys
import subprocess

# 環境変数設定
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google'
os.environ['HOURS_LOOKBACK'] = '48'
os.environ['MAX_ITEMS_PER_CATEGORY'] = '25'
os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'

print("🔍 Xポスト機能テスト開始")
print("=" * 50)

try:
    # build_simple_ranking.pyから関数をインポート
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from build_simple_ranking import fetch_x_posts
    
    print("📱 Xポスト取得テスト...")
    x_posts = fetch_x_posts()
    
    print(f"取得されたXポスト数: {len(x_posts)}")
    
    if x_posts:
        print("\n📋 取得したXポストの詳細:")
        print("-" * 30)
        
        for i, post in enumerate(x_posts[:5]):  # 最初の5つを表示
            print(f"{i+1}. {post.get('title', 'N/A')}")
            print(f"   URL: {post.get('url', 'N/A')}")
            print(f"   Summary: {post.get('summary', 'N/A')[:100]}...")
            print(f"   Published: {post.get('published', 'N/A')}")
            print(f"   Engineer Score: {post.get('engineer_score', 'N/A')}")
            print()
        
        if len(x_posts) > 5:
            print(f"... その他 {len(x_posts) - 5} 件のポスト")
    else:
        print("⚠️ Xポストが取得されませんでした")
        
        # CSVの内容を直接確認
        print("\n🔍 CSV直接確認...")
        import requests
        import csv
        import io
        
        url = os.environ['X_POSTS_CSV']
        response = requests.get(url, timeout=30)
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code == 200:
            csv_content = response.text
            print(f"CSV Content Length: {len(csv_content)}")
            
            reader = csv.DictReader(io.StringIO(csv_content))
            rows = list(reader)
            print(f"CSV Rows: {len(rows)}")
            
            if rows:
                print("Headers:", list(rows[0].keys()))
                print("First row:", rows[0])
        
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ テスト完了")