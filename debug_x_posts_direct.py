#!/usr/bin/env python3
"""
Direct debug of X posts CSV and processing
"""
import os
import requests
import csv
import io
from datetime import datetime
from dateutil import parser

# 環境変数
X_POSTS_CSV = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
HOURS_LOOKBACK = 48

def is_recent(published_str, hours_lookback):
    """記事が指定時間内に公開されたかチェック"""
    try:
        pub_time = datetime.strptime(published_str, '%Y-%m-%d %H:%M:%S')
        from datetime import timezone
        pub_time = pub_time.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        diff = now - pub_time
        return diff.total_seconds() <= hours_lookback * 3600
    except:
        return False

def debug_x_posts():
    """X投稿のデバッグ"""
    print("🔍 X投稿 直接デバッグ")
    print("=" * 50)
    
    try:
        print(f"📱 CSV URL: {X_POSTS_CSV}")
        
        # CSVダウンロード
        response = requests.get(X_POSTS_CSV, timeout=30)
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ HTTPエラー: {response.status_code}")
            return
        
        # CSVパース
        csv_content = response.text
        print(f"CSV Content Length: {len(csv_content)} chars")
        
        # 最初の500文字を表示
        print("\n📄 CSV Content Preview:")
        print("-" * 30)
        print(csv_content[:500])
        print("-" * 30)
        
        reader = csv.DictReader(io.StringIO(csv_content))
        
        print("\n📋 CSV Headers:")
        headers = reader.fieldnames
        print(headers)
        
        posts = []
        total_rows = 0
        recent_count = 0
        
        print("\n📊 Processing rows:")
        print("-" * 40)
        
        for row in reader:
            total_rows += 1
            print(f"\nRow {total_rows}:")
            
            # 各列の内容を表示
            for header in headers:
                value = row.get(header, '').strip()
                print(f"  {header}: {value[:50]}{'...' if len(value) > 50 else ''}")
            
            # データ処理テスト
            tweet_content = row.get('Tweet Content', '').strip()
            username = row.get('Username', '').strip()
            timestamp_str = row.get('Timestamp', '').strip()
            
            if not tweet_content:
                print("  ❌ Empty tweet content - skipping")
                continue
                
            # タイムスタンプ処理テスト
            try:
                post_date = parser.parse(timestamp_str)
                print(f"  📅 Parsed date: {post_date}")
                
                if is_recent(post_date.strftime('%Y-%m-%d %H:%M:%S'), HOURS_LOOKBACK):
                    recent_count += 1
                    print(f"  ✅ Recent post (within {HOURS_LOOKBACK}h)")
                    
                    # PostオブジェクトをUUID
                    post_url = row.get('Source Link 1', '').strip() or row.get('Source Link 2', '').strip()
                    title = tweet_content[:100] + '...' if len(tweet_content) > 100 else tweet_content
                    
                    post = {
                        'title': title,
                        'url': post_url,
                        'summary': f"@{username}: {tweet_content}",
                        'published': timestamp_str,
                        'source': 'X (Twitter)'
                    }
                    posts.append(post)
                    print(f"  ✅ Added to posts list")
                else:
                    print(f"  ⏰ Too old - skipping")
                    
            except Exception as e:
                print(f"  ❌ Date parse error: {e}")
                
            # 最初の5行だけ詳細表示
            if total_rows >= 5:
                print(f"\n... (showing first 5 rows only, total: {total_rows})")
                break
        
        print(f"\n📈 Summary:")
        print(f"Total rows in CSV: {total_rows}")
        print(f"Recent posts (within {HOURS_LOOKBACK}h): {recent_count}")
        print(f"Valid posts to add: {len(posts)}")
        
        if posts:
            print(f"\n🎯 Posts to be added:")
            for i, post in enumerate(posts[:3]):
                print(f"{i+1}. {post['title']}")
                print(f"   Source: {post['source']}")
                print(f"   URL: {post['url']}")
        
        return posts
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    debug_x_posts()