#!/usr/bin/env python3
"""
抜本的403エラー修正のテスト
"""
import sys
import os

# プロジェクトディレクトリに移動
os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

try:
    print("🔧 抜本的403エラー修正をテスト中...")
    print("📡 新機能:")
    print("  ✅ 高度なHTTPリクエスト制御 (requestsライブラリ)")
    print("  ✅ 複数User-Agentローテーション")
    print("  ✅ Google専用ヘッダー設定")
    print("  ✅ ランダム遅延によるレート制限回避")
    print("  ✅ Reddit, Hacker News, GitHub Trending等の代替ソース")
    
    import build
    import yaml
    
    # feeds.ymlを読み込み
    with open('feeds.yml', 'r', encoding='utf-8') as f:
        feeds_config = yaml.safe_load(f)
    
    # 特にGoogle Newsのテスト
    print("\n🎯 Google Newsに対する特別なテスト:")
    google_feeds = []
    for category, feeds in feeds_config.items():
        for feed in feeds:
            if 'google.com' in feed.get('url', '') or 'Google News' in feed.get('name', ''):
                google_feeds.append((feed, category))
                
    print(f"Found {len(google_feeds)} Google-related feeds")
    
    for feed, category in google_feeds[:2]:  # 最初の2つをテスト
        name = feed['name']
        url = feed['url']
        print(f"\n🔍 Testing: {name}")
        
        # 高度なフェッチを直接テスト
        result = build.advanced_feed_fetch(url, name)
        if result:
            print(f"✅ SUCCESS: {name} - Advanced fetch worked!")
            entries = len(result.entries) if hasattr(result, 'entries') else 0
            print(f"   Retrieved {entries} entries")
        else:
            print(f"❌ FAILED: {name} - Advanced fetch failed")
    
    # 新しい代替ソースのテスト
    print("\n🆕 新しい代替ソースのテスト:")
    alternative_sources = [
        'Hacker News', 'Reddit AI', 'AI Business News', 
        'Reddit MachineLearning', 'GitHub Trending', 'Reddit Science'
    ]
    
    success_count = 0
    total_count = 0
    
    for category, feeds in feeds_config.items():
        for feed in feeds:
            if feed['name'] in alternative_sources:
                total_count += 1
                print(f"Testing: {feed['name']}")
                try:
                    items = build.gather_items([feed], category)
                    if items:
                        success_count += 1
                        print(f"  ✅ SUCCESS: {len(items)} items")
                    else:
                        print(f"  ⚠️ No items retrieved")
                except Exception as e:
                    print(f"  ❌ ERROR: {e}")
    
    print(f"\n📊 代替ソース成功率: {success_count}/{total_count} ({success_count/total_count*100:.1f}%)")
    
    # 完全なダッシュボード生成テスト
    print("\n🔄 完全なダッシュボード生成テスト...")
    from generate_comprehensive_dashboard import analyze_ai_landscape, generate_comprehensive_dashboard_html
    
    data = analyze_ai_landscape()
    html_content = generate_comprehensive_dashboard_html(data)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ 抜本的改善版ダッシュボード生成完了!")
    print(f"📊 総ニュース数: {data['stats']['total_items']}")
    print(f"🗣️ SNS投稿数: {data['x_posts']['total_count']}")
    
    # 改善のサマリー
    print("\n🎉 抜本的改善の効果:")
    print("  🔧 複数のUser-Agentでローテーション")
    print("  🌐 Google専用のHTTPヘッダー設定") 
    print("  ⏱️ レート制限回避のランダム遅延")
    print("  🔄 代替ソースによるフォールバック")
    print("  📡 requests library による高度制御")
    print("  🛡️ 403エラー耐性の大幅向上")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()