#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
修正されたX投稿機能のテスト
"""
import os
import sys
from datetime import datetime

# 環境変数設定
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google'
os.environ['HOURS_LOOKBACK'] = '24'
os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'

print("🔧 修正されたX投稿機能テスト開始")
print("=" * 50)

try:
    # build.pyから修正された関数をインポート
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from build import gather_x_posts
    
    print("📱 修正されたX投稿取得テスト...")
    x_posts = gather_x_posts(os.environ['X_POSTS_CSV'])
    
    print(f"✅ 取得されたXポスト数: {len(x_posts)}")
    
    if x_posts:
        print("\n📋 取得したXポストの詳細:")
        print("-" * 30)
        
        for i, post in enumerate(x_posts[:5], 1):
            print(f"{i}. タイトル: {post.get('title', 'N/A')}")
            print(f"   URL: {post.get('link', 'N/A')}")
            print(f"   要約: {post.get('_summary', 'N/A')[:100]}...")
            print(f"   ソース: {post.get('_source', 'N/A')}")
            print(f"   重要度スコア: {post.get('_importance_score', 'N/A')}")
            print(f"   日時: {post.get('_dt', 'N/A')}")
            print()
        
        if len(x_posts) > 5:
            print(f"... その他 {len(x_posts) - 5} 件のポスト")
        
        # スコアチェック
        high_score_count = sum(1 for post in x_posts if post.get('_importance_score', 0) >= 10.0)
        print(f"\n📊 統計:")
        print(f"   高重要度投稿（スコア10.0）: {high_score_count}/{len(x_posts)}")
        print(f"   成功率: {high_score_count / len(x_posts) * 100:.1f}%")
        
    else:
        print("❌ Xポストが取得されませんでした")
        
except Exception as e:
    print(f"❌ エラー: {e}")
    import traceback
    traceback.print_exc()

print("\n✅ テスト完了")