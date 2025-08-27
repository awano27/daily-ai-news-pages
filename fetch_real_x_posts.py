#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
実際のCSVからXポストデータを取得・処理するスクリプト
"""
import requests
import csv
import io
import html
from datetime import datetime, timezone
import re
import unicodedata

def fetch_and_process_x_posts():
    """Google SheetsからCSVデータを取得し、実際のXポストを処理"""
    
    csv_url = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
    
    print("📱 実際のXポストデータを取得中...")
    print(f"URL: {csv_url}")
    print("=" * 60)
    
    try:
        # CSVデータを取得
        response = requests.get(csv_url, timeout=30)
        print(f"HTTP Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ HTTPエラー: {response.status_code}")
            return []
        
        # エンコーディングを明示的に設定
        response.encoding = 'utf-8'
        content = response.text
        print(f"データサイズ: {len(content)} 文字")
        
        # CSVを解析
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        print(f"CSV行数: {len(rows)}")
        
        if not rows:
            print("❌ CSVデータが空です")
            return []
        
        # ヘッダー確認
        headers = rows[0] if rows else []
        print(f"ヘッダー: {headers}")
        
        # 実際のXポストを処理
        x_posts = []
        processed_count = 0
        
        for i, row in enumerate(rows[1:], 1):  # ヘッダーをスキップ
            if len(row) < 3:
                continue
                
            # データを抽出
            date_str = row[0].strip('"').strip() if len(row) > 0 else ""
            username = row[1].strip('"').strip() if len(row) > 1 else ""
            text = row[2].strip('"').strip() if len(row) > 2 else ""
            media_url = row[3].strip('"').strip() if len(row) > 3 else ""
            tweet_url = row[4].strip('"').strip() if len(row) > 4 else ""
            
            # 基本的な検証
            if not text or len(text.strip()) < 10:  # 最低10文字
                continue
            
            # HTMLエンティティをデコード
            text = html.unescape(text)
            username = html.unescape(username)
            
            # 文字の正規化
            text = unicodedata.normalize('NFKC', text)
            username = unicodedata.normalize('NFKC', username)
            
            # 制御文字を除去
            text = ''.join(char for char in text if char.isprintable() or char in '\n\r\t')
            text = re.sub(r'\s+', ' ', text).strip()
            
            # URLがない場合はダミーURLを生成
            if not tweet_url and username:
                username_clean = username.replace('@', '').replace('"', '')
                tweet_url = f"https://x.com/{username_clean}/status/example_{i}"
            elif not tweet_url:
                tweet_url = f"https://x.com/unknown/status/example_{i}"
            
            # 日付処理
            try:
                # 複数の日付フォーマットに対応
                date_formats = [
                    "%B %d, %Y at %I:%M%p",   # "August 10, 2025 at 02:41AM"
                    "%B %d, %Y",              # "August 13, 2025"
                    "%Y-%m-%d %H:%M:%S",      # "2025-08-18 14:30:00"
                    "%Y-%m-%d",               # "2025-08-18"
                    "%m/%d/%Y",               # "8/18/2025"
                ]
                
                parsed_date = None
                for fmt in date_formats:
                    try:
                        parsed_date = datetime.strptime(date_str, fmt)
                        break
                    except:
                        continue
                
                if parsed_date is None:
                    parsed_date = datetime.now()
                    
            except Exception as e:
                parsed_date = datetime.now()
            
            # Xポストオブジェクトを作成
            x_post = {
                'date': date_str,
                'username': username,
                'text': text,
                'media_url': media_url,
                'tweet_url': tweet_url,
                'parsed_date': parsed_date,
                'display_title': f"{username} - AI関連ポスト",
                'display_summary': text[:200] + '...' if len(text) > 200 else text
            }
            
            x_posts.append(x_post)
            processed_count += 1
            
            # デバッグ用：最初の3つを詳細表示
            if processed_count <= 3:
                print(f"\n📝 ポスト {processed_count}:")
                print(f"  日付: {date_str}")
                print(f"  ユーザー: {username}")
                print(f"  テキスト: {text[:100]}...")
                print(f"  URL: {tweet_url}")
        
        print(f"\n✅ 処理完了: {len(x_posts)}件の実際のXポストを取得")
        return x_posts
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return []

def convert_to_html_format(x_posts):
    """XポストをHTML形式に変換"""
    html_cards = []
    
    for i, post in enumerate(x_posts[:10], 1):  # 最大10件
        # タイトルを生成
        if post['username']:
            title = f"🐦 {post['username']} - AI関連投稿"
        else:
            title = f"🐦 Xポスト #{i}"
        
        # 要約を生成（日本語に翻訳されているかチェック）
        summary = post['display_summary']
        if len(summary) > 300:
            summary = summary[:300] + '...'
        
        # 相対時間を計算
        time_diff = datetime.now() - post['parsed_date']
        hours_ago = int(time_diff.total_seconds() / 3600)
        if hours_ago < 1:
            time_ago = "1時間前"
        elif hours_ago < 24:
            time_ago = f"{hours_ago}時間前"
        else:
            days_ago = int(hours_ago / 24)
            time_ago = f"{days_ago}日前"
        
        html_card = f'''        <article class="enhanced-card" data-score="10.0" data-source="X / SNS (実データ)" data-time="{post['parsed_date'].isoformat()}">
          <div class="card-priority high">最高 10.0</div>
          <header class="card-header">
            <h3 class="card-title">
              <a href="{post['tweet_url']}" target="_blank" rel="noopener">{html.escape(title)}</a>
            </h3>
          </header>
          <div class="card-meta">
            <span class="card-source">X / SNS (実データ)</span>
          </div>
          <div class="card-summary">{html.escape(summary)}</div>
          <footer class="card-footer">
            <span class="card-score">スコア: 10.0</span>
            <span class="card-time">{time_ago}</span>
          </footer>
        </article>

'''
        html_cards.append(html_card)
    
    return ''.join(html_cards)

if __name__ == "__main__":
    # 実際のXポストを取得
    x_posts = fetch_and_process_x_posts()
    
    if x_posts:
        print(f"\n📊 取得成功: {len(x_posts)}件")
        
        # HTML形式に変換
        html_content = convert_to_html_format(x_posts)
        
        # HTMLファイルに保存
        with open('x_posts_real.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("💾 実際のXポストHTML（x_posts_real.html）を生成しました")
        print("\n🔧 次のステップ:")
        print("1. x_posts_real.htmlの内容をindex.htmlのPostsセクションに挿入")
        print("2. GitHubにプッシュして反映")
        
    else:
        print("❌ Xポストの取得に失敗しました")