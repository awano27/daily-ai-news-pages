#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X投稿の取得状況をチェックするテスト
"""
import os
import requests
import csv
import io
from datetime import datetime, timezone

# 環境変数設定
os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'

def test_x_posts():
    """X投稿データの取得テスト"""
    url = os.environ['X_POSTS_CSV']
    
    print("🔍 X投稿データ取得テスト開始")
    print(f"URL: {url}")
    print("=" * 60)
    
    try:
        # CSVデータ取得
        response = requests.get(url, timeout=30)
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ HTTPエラー: {response.status_code}")
            return False
        
        # エンコーディング設定
        response.encoding = 'utf-8'
        content = response.text
        print(f"データサイズ: {len(content)} 文字")
        
        # 先頭データ表示
        print("\n📋 CSV先頭データ:")
        lines = content.strip().split('\n')
        for i, line in enumerate(lines[:5], 1):
            print(f"  {i}: {line[:100]}{'...' if len(line) > 100 else ''}")
        
        # CSV解析
        print("\n📊 CSV構造分析:")
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        print(f"総行数: {len(rows)}")
        
        if not rows:
            print("❌ CSVデータが空です")
            return False
        
        # ヘッダー確認
        headers = rows[0] if rows else []
        print(f"列数: {len(headers)}")
        print(f"ヘッダー: {headers}")
        
        # データ行を分析
        valid_posts = 0
        empty_text = 0
        
        for i, row in enumerate(rows[1:], 1):  # ヘッダーをスキップ
            if len(row) >= 3:
                date_col = row[0].strip() if len(row) > 0 else ""
                user_col = row[1].strip() if len(row) > 1 else ""
                text_col = row[2].strip() if len(row) > 2 else ""
                
                if text_col and len(text_col.strip()) > 5:
                    valid_posts += 1
                    
                    # 最初の3つの有効な投稿を表示
                    if valid_posts <= 3:
                        print(f"\n📝 投稿 {valid_posts}:")
                        print(f"  日付: {date_col}")
                        print(f"  ユーザー: {user_col}")
                        print(f"  テキスト: {text_col[:100]}{'...' if len(text_col) > 100 else ''}")
                        if len(row) > 4:
                            print(f"  URL: {row[4]}")
                else:
                    empty_text += 1
        
        print(f"\n📈 統計:")
        print(f"  有効な投稿: {valid_posts}")
        print(f"  空のテキスト: {empty_text}")
        print(f"  成功率: {valid_posts / (len(rows) - 1) * 100:.1f}%")
        
        # build.pyの形式で変換をテスト
        print("\n🔄 build.py形式への変換テスト:")
        
        build_items = []
        for row in rows[1:]:
            if len(row) >= 3:
                text = row[2].strip() if len(row) > 2 else ""
                if text and len(text.strip()) > 5:
                    username = row[1].strip() if len(row) > 1 else ""
                    url = row[4].strip() if len(row) > 4 else "https://x.com/unknown"
                    
                    item = {
                        "title": f"Xポスト {username}",
                        "link": url,
                        "_summary": text[:150] + '...' if len(text) > 150 else text,
                        "_full_text": text,
                        "_source": "X / SNS",
                        "_dt": datetime.now(timezone.utc)
                    }
                    build_items.append(item)
        
        print(f"変換された投稿数: {len(build_items)}")
        
        if build_items:
            print("\n📋 変換例:")
            for i, item in enumerate(build_items[:3], 1):
                print(f"  {i}. タイトル: {item['title']}")
                print(f"     URL: {item['link']}")
                print(f"     要約: {item['_summary'][:50]}...")
        
        return valid_posts > 0
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_x_posts()
    print("\n" + "=" * 60)
    if success:
        print("✅ X投稿取得テスト: 成功")
    else:
        print("❌ X投稿取得テスト: 失敗")