#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X投稿データの詳細デバッグテスト
"""
import requests
import csv
import io
from datetime import datetime

def detailed_x_test():
    """詳細なX投稿取得デバッグ"""
    print("🔍 X投稿データ詳細デバッグテスト")
    
    # Google Sheets URL
    url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    
    try:
        # CSVデータ取得
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        content = response.content.decode('utf-8-sig', errors='ignore')
        
        print(f"✅ CSV取得成功: {len(content)} characters")
        print(f"📝 最初の200文字: {content[:200]}...")
        
        # CSV解析
        reader = csv.reader(io.StringIO(content))
        posts = []
        
        row_count = 0
        for row in reader:
            row_count += 1
            if row_count == 1:  # ヘッダースキップ
                print(f"📋 ヘッダー: {row}")
                continue
            
            if row_count > 10:  # 最初の10行のみ詳細表示
                break
                
            print(f"\n--- 行 {row_count} ---")
            print(f"列数: {len(row)}")
            for i, cell in enumerate(row):
                print(f"  列{i}: '{cell[:100]}{'...' if len(cell) > 100 else ''}'")
            
            if len(row) >= 3:
                date_str = row[0].strip('"').strip() if len(row) > 0 else ""
                username = row[1].strip('"').strip() if len(row) > 1 else ""
                text = row[2].strip('"').strip() if len(row) > 2 else ""
                tweet_url = row[4].strip('"').strip() if len(row) > 4 else ""
                
                if text and len(text) > 5:
                    posts.append({
                        'username': username,
                        'text': text,
                        'date': date_str,
                        'url': tweet_url,
                        'text_length': len(text)
                    })
                    
                    print(f"✅ 有効な投稿データ:")
                    print(f"   ユーザー: {username}")
                    print(f"   テキスト長: {len(text)}文字")
                    print(f"   テキスト: {text[:100]}{'...' if len(text) > 100 else ''}")
                    print(f"   日付: {date_str}")
                    print(f"   URL: {tweet_url}")
                else:
                    print(f"❌ 無効な投稿データ（テキスト長: {len(text) if text else 0}）")
        
        print(f"\n📊 解析結果:")
        print(f"   総行数: {row_count}")
        print(f"   有効投稿数: {len(posts)}件")
        
        if posts:
            print(f"\n📝 最初の3件の詳細:")
            for i, post in enumerate(posts[:3], 1):
                print(f"   {i}. @{post['username']}")
                print(f"      テキスト: {post['text'][:150]}...")
                print(f"      文字数: {post['text_length']}文字")
        
        return len(posts) > 0
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = detailed_x_test()
    print(f"\n{'✅ 成功' if success else '❌ 失敗'}")
    input("Press Enter to exit...")