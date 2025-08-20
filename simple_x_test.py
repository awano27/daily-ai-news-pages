#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
シンプルなX投稿取得テスト
"""
import requests
import csv
import io
from datetime import datetime

def simple_test():
    """最小限のX投稿取得テスト"""
    print("🚀 シンプルX投稿取得テスト")
    
    # Google Sheets URL
    url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    
    try:
        # CSVデータ取得
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        content = response.content.decode('utf-8-sig', errors='ignore')
        
        print(f"✅ CSV取得成功: {len(content)} characters")
        
        # CSV解析
        reader = csv.reader(io.StringIO(content))
        posts = []
        
        row_count = 0
        for row in reader:
            row_count += 1
            if row_count == 1:  # ヘッダースキップ
                print(f"📋 ヘッダー: {row}")
                continue
            
            if len(row) >= 3:
                date_str = row[0].strip('"').strip() if len(row) > 0 else ""
                username = row[1].strip('"').strip() if len(row) > 1 else ""
                text = row[2].strip('"').strip() if len(row) > 2 else ""
                
                if text and len(text) > 5:  # 5文字以上
                    posts.append({
                        'username': username,
                        'text': text[:100],  # 最初の100文字
                        'date': date_str,
                        'quality_score': min(10, max(1, len(text) // 10))  # 簡易品質スコア
                    })
                    
                    if len(posts) <= 5:  # 最初の5件を表示
                        print(f"📝 投稿{len(posts)}: @{username}")
                        print(f"    内容: {text[:60]}...")
                        print(f"    日付: {date_str}")
        
        print(f"\n📊 総投稿数: {len(posts)}件")
        
        # 簡易分類テスト
        influencer_posts = []
        tech_discussions = []
        
        # すべての投稿を注目投稿として扱う（まずは表示を優先）
        for i, post in enumerate(posts[:10]):  # 最初の10件
            if i < 5:  # 最初の5件を注目投稿
                influencer_posts.append(post)
            else:  # 残りを技術ディスカッション
                tech_discussions.append(post)
        
        print(f"\n🎯 分類結果:")
        print(f"   注目投稿: {len(influencer_posts)}件")
        print(f"   技術ディスカッション: {len(tech_discussions)}件")
        
        if influencer_posts:
            print("\n📢 注目投稿（最初の3件）:")
            for i, post in enumerate(influencer_posts[:3], 1):
                print(f"   {i}. @{post['username']}")
                print(f"      {post['text'][:50]}...")
        
        return len(posts) > 0
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = simple_test()
    if success:
        print("\n✅ 基本的なX投稿取得は成功しています")
        print("💡 次は generate_comprehensive_dashboard.py の修正が必要です")
    else:
        print("\n❌ X投稿取得に問題があります")
    
    input("Press Enter to exit...")