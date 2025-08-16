#!/usr/bin/env python3
"""
403 Forbiddenエラー修正のテスト
"""
import sys
import os

# プロジェクトディレクトリに移動
os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

try:
    print("🔧 403 Forbiddenエラー修正をテスト中...")
    
    import build
    import yaml
    
    # feeds.ymlを読み込み
    with open('feeds.yml', 'r', encoding='utf-8') as f:
        feeds_config = yaml.safe_load(f)
    
    # 各カテゴリのフィード数をカウント
    total_feeds = 0
    success_count = 0
    
    for category, feeds in feeds_config.items():
        print(f"\n📂 {category}カテゴリ: {len(feeds)}個のフィード")
        category_items = build.gather_items(feeds, category)
        if category_items:
            success_count += len([f for f in feeds if f.get('url')])
            print(f"✅ {len(category_items)}件のニュースを取得")
        total_feeds += len([f for f in feeds if f.get('url')])
    
    print(f"\n📊 結果サマリー:")
    print(f"・総フィード数: {total_feeds}")
    print(f"・成功率: {success_count}/{total_feeds} ({success_count/total_feeds*100:.1f}%)")
    
    # 修正されたダッシュボードを生成
    print("\n🔄 修正版ダッシュボードを生成中...")
    from generate_comprehensive_dashboard import analyze_ai_landscape, generate_comprehensive_dashboard_html
    
    data = analyze_ai_landscape()
    html_content = generate_comprehensive_dashboard_html(data)
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ 403エラー修正版ダッシュボード生成完了!")
    print(f"📊 総ニュース数: {data['stats']['total_items']}")
    print(f"🗣️ SNS投稿数: {data['x_posts']['total_count']}")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()