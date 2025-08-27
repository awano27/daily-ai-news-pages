#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSVの構造を詳細分析してX投稿のURL抽出方法を特定
"""
import requests
import csv
import io
import re

def analyze_csv_structure():
    """CSVの構造を詳細分析"""
    csv_url = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
    
    print("🔍 CSV構造の詳細分析")
    print("=" * 50)
    
    try:
        response = requests.get(csv_url, timeout=30)
        if response.status_code != 200:
            print(f"❌ HTTPエラー: {response.status_code}")
            return
        
        content = response.text
        print(f"データサイズ: {len(content)} 文字")
        
        # CSVをパース
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        
        print(f"総行数: {len(rows)}")
        
        if rows:
            # ヘッダー分析
            headers = rows[0]
            print(f"\nヘッダー（{len(headers)}列）:")
            for i, header in enumerate(headers):
                print(f"  [{i}]: '{header}'")
            
            # サンプルデータ行を分析
            print(f"\n最初の3つのデータ行:")
            for row_num, row in enumerate(rows[1:4], 1):
                print(f"\n--- 行 {row_num} ({len(row)}列) ---")
                for i, cell in enumerate(row):
                    if i < len(headers):
                        header = headers[i]
                    else:
                        header = f"Column_{i}"
                    
                    # URLを検出
                    if re.search(r'https?://[^\s]+', cell):
                        print(f"  [{i}] {header}: '{cell}' ← URL発見!")
                    elif len(cell) > 50:
                        print(f"  [{i}] {header}: '{cell[:50]}...'")
                    else:
                        print(f"  [{i}] {header}: '{cell}'")
            
            # URL パターンの詳細分析
            print(f"\n📊 URL パターン分析:")
            url_patterns = {}
            
            for row_num, row in enumerate(rows[1:10], 1):  # 最初の10行をチェック
                for col_num, cell in enumerate(row):
                    urls = re.findall(r'https?://[^\s,;"\']+', cell)
                    for url in urls:
                        if 'x.com' in url or 'twitter.com' in url:
                            col_name = headers[col_num] if col_num < len(headers) else f"Column_{col_num}"
                            if col_name not in url_patterns:
                                url_patterns[col_name] = []
                            url_patterns[col_name].append({
                                'row': row_num,
                                'url': url,
                                'cell_content': cell[:100] + '...' if len(cell) > 100 else cell
                            })
            
            print("X/Twitter URL が含まれる列:")
            for col_name, urls in url_patterns.items():
                print(f"\n📍 {col_name}:")
                for info in urls[:3]:  # 最初の3つを表示
                    print(f"    行{info['row']}: {info['url']}")
                    print(f"         内容: {info['cell_content']}")
                    
        print("\n✅ CSV構造分析完了")
        
        # 推奨される修正コードを生成
        print("\n🔧 推奨される修正:")
        if url_patterns:
            main_col = max(url_patterns.keys(), key=lambda k: len(url_patterns[k]))
            main_col_index = headers.index(main_col) if main_col in headers else -1
            print(f"   メインのURL列: '{main_col}' (インデックス: {main_col_index})")
            print(f"   修正コード: tweet_url = row[{main_col_index}].strip() if len(row) > {main_col_index} else \"\"")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_csv_structure()