#!/usr/bin/env python3
"""
タイトル翻訳機能のテスト
"""
import sys
import os

# プロジェクトディレクトリに移動
os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

try:
    # 翻訳機能付きダッシュボード生成を実行
    print("🔄 日本語タイトル翻訳機能付きダッシュボードを生成中...")
    
    from generate_comprehensive_dashboard import analyze_ai_landscape, generate_comprehensive_dashboard_html
    
    # ダッシュボードデータ生成
    data = analyze_ai_landscape()
    
    # HTMLファイル生成
    html_content = generate_comprehensive_dashboard_html(data)
    
    # ファイル保存
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print("✅ 日本語タイトル翻訳機能付きダッシュボード生成完了!")
    
    # 翻訳されたタイトルの例を表示
    print("\n📋 翻訳されたタイトルの例:")
    for cat_name, cat_data in data['categories'].items():
        print(f"\n{cat_data['name']}:")
        for topic in cat_data['featured_topics'][:2]:
            if topic.get('title_ja') and topic['title_ja'] != topic['title']:
                print(f"  原文: {topic['title'][:50]}...")
                print(f"  日本語: {topic['title_ja'][:50]}...")
            else:
                print(f"  未翻訳: {topic['title'][:50]}...")
    
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()