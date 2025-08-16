#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google SheetsのCSVから日付を確認して問題を診断
"""
import csv
import io
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen

def check_dates():
    """CSVの日付フォーマットと8/13の投稿を確認"""
    
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    JST = timezone(timedelta(hours=9))
    NOW = datetime.now(JST)
    aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=JST)
    
    print("📊 Google SheetsのCSVを確認中...")
    print("=" * 60)
    
    try:
        # CSVを取得
        with urlopen(GOOGLE_SHEETS_URL) as r:
            raw = r.read()
        
        # UTF-8でデコード
        txt = raw.decode('utf-8-sig', errors='ignore')
        
        # CSV読み込み
        rdr = csv.reader(io.StringIO(txt))
        
        print("🔍 CSVデータの分析:\n")
        
        row_count = 0
        problem_dates = []
        aug13_posts = []
        
        for row in rdr:
            row_count += 1
            
            # 最初の5行を表示
            if row_count <= 5:
                print(f"行{row_count}: {row[:2] if len(row) >= 2 else row}")  # 日付とユーザー名のみ表示
            
            if len(row) >= 5:
                date_str = row[0].strip('"')
                username = row[1].strip('"')
                tweet_url = row[4].strip('"')
                
                # pop_ikedaの投稿を探す
                if 'pop_ikeda' in username and '1955419027209326985' in tweet_url:
                    print(f"\n⚠️ 問題の投稿を発見:")
                    print(f"   ユーザー: {username}")
                    print(f"   日付文字列: '{date_str}'")
                    print(f"   URL: {tweet_url}")
                
                # 日付パースを試みる
                try:
                    # "August 10, 2025 at 02:41AM" -> datetime
                    dt = datetime.strptime(date_str, "%B %d, %Y at %I:%M%p")
                    dt = dt.replace(tzinfo=JST)
                    
                    # 8/13以前の投稿をチェック
                    if dt < aug14_jst:
                        aug13_posts.append({
                            'date': dt.strftime('%Y-%m-%d %H:%M'),
                            'user': username,
                            'url': tweet_url
                        })
                except Exception as e:
                    # パースに失敗した日付を記録
                    problem_dates.append({
                        'original': date_str,
                        'user': username,
                        'error': str(e)
                    })
        
        print(f"\n📈 統計:")
        print(f"   総行数: {row_count}")
        print(f"   8/14より前の投稿: {len(aug13_posts)}件")
        print(f"   日付パースエラー: {len(problem_dates)}件")
        
        if aug13_posts:
            print(f"\n❌ 8/14より前の投稿（除外されるべき）:")
            for post in aug13_posts[:5]:  # 最初の5件を表示
                print(f"   - {post['date']} | {post['user']}")
        
        if problem_dates:
            print(f"\n⚠️ 日付パースに失敗した投稿（現在時刻として扱われる）:")
            for prob in problem_dates[:5]:  # 最初の5件を表示
                print(f"   - '{prob['original']}' | {prob['user']}")
                print(f"     エラー: {prob['error']}")
        
        # 日付フォーマットの診断
        print("\n🔧 診断結果:")
        if problem_dates:
            print("   ⚠️ 日付パースエラーが発生しています")
            print("   → これらの投稿は現在時刻（NOW）として扱われ、フィルタを通過してしまいます")
            print("   → 日付フォーマットの修正が必要です")
        else:
            print("   ✅ 日付パースは正常です")
            
        if aug13_posts:
            print("   ❌ 8/14より前の投稿が含まれています")
            print("   → フィルタリングロジックを確認する必要があります")
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_dates()