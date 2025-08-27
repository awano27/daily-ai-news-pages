#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CSVから実際のXポストを直接抽出
"""
import requests
import re
from datetime import datetime
import html

def extract_real_x_posts():
    """CSVから実際のXポストを抽出"""
    
    csv_url = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
    
    try:
        print("📱 実際のCSVデータを取得中...")
        response = requests.get(csv_url, timeout=30)
        
        if response.status_code != 200:
            print(f"❌ HTTPエラー: {response.status_code}")
            return []
        
        content = response.text
        print(f"データサイズ: {len(content)} 文字")
        
        # テキストから投稿を抽出（August 2025の日付パターンを使用）
        x_posts = []
        
        # August XX, 2025 at XX:XXAM/PM 形式の日付パターン
        date_pattern = r'(August \d{1,2}, 2025 at \d{1,2}:\d{2}[AP]M)'
        
        # テキストを分割して処理
        lines = content.split('\n')
        current_post = {}
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
                
            # 日付を検出
            date_match = re.search(date_pattern, line)
            if date_match:
                # 前の投稿があれば保存
                if current_post.get('text') and len(current_post['text'].strip()) > 20:
                    x_posts.append(current_post.copy())
                
                # 新しい投稿を開始
                current_post = {
                    'date': date_match.group(1),
                    'username': '',
                    'text': '',
                    'urls': []
                }
                continue
            
            # @ユーザー名を検出
            username_matches = re.findall(r'@([a-zA-Z0-9_]+)', line)
            if username_matches and not current_post.get('username'):
                current_post['username'] = username_matches[0]
            
            # URLを検出
            url_matches = re.findall(r'https?://[^\s,"\'"]+', line)
            for url in url_matches:
                if url not in current_post.get('urls', []):
                    current_post.setdefault('urls', []).append(url)
            
            # テキストコンテンツを蓄積（日付行以外）
            if not re.search(date_pattern, line) and len(line) > 10:
                # CSVの引用符を除去
                cleaned_line = line.strip('"').strip()
                if cleaned_line:
                    if current_post.get('text'):
                        current_post['text'] += ' ' + cleaned_line
                    else:
                        current_post['text'] = cleaned_line
        
        # 最後の投稿も追加
        if current_post.get('text') and len(current_post['text'].strip()) > 20:
            x_posts.append(current_post)
        
        print(f"抽出された投稿数: {len(x_posts)}")
        
        # 重複除去と品質フィルタリング
        filtered_posts = []
        seen_texts = set()
        
        for post in x_posts:
            # テキストの正規化
            normalized_text = re.sub(r'\s+', ' ', post['text'].lower().strip())
            
            # 重複チェック
            text_signature = normalized_text[:100]  # 最初の100文字で重複判定
            if text_signature in seen_texts:
                continue
            seen_texts.add(text_signature)
            
            # 品質フィルタリング
            if (len(post['text']) > 30 and  # 30文字以上
                post.get('username') and    # ユーザー名が存在
                not post['text'].startswith('RT')):  # RTではない
                
                # URLの優先順位付け
                tweet_url = ""
                if post.get('urls'):
                    # Twitter/X URLを優先
                    for url in post['urls']:
                        if 'twitter.com' in url or 'x.com' in url:
                            tweet_url = url
                            break
                    if not tweet_url:
                        tweet_url = post['urls'][0]
                
                # URLがない場合はダミーURL
                if not tweet_url:
                    username_clean = post['username'].replace('@', '')
                    tweet_url = f"https://x.com/{username_clean}/status/example_{len(filtered_posts)+1}"
                
                filtered_posts.append({
                    'date': post['date'],
                    'username': f"@{post['username']}" if not post['username'].startswith('@') else post['username'],
                    'text': html.unescape(post['text'].strip()),
                    'tweet_url': tweet_url,
                    'display_summary': post['text'][:250] + '...' if len(post['text']) > 250 else post['text']
                })
        
        print(f"フィルタリング後: {len(filtered_posts)}件")
        
        # 最初の5件を詳細表示
        print("\n📋 抽出されたXポスト（最初の5件）:")
        print("=" * 60)
        
        for i, post in enumerate(filtered_posts[:5], 1):
            print(f"\n{i}. 日付: {post['date']}")
            print(f"   ユーザー: {post['username']}")
            print(f"   URL: {post['tweet_url']}")
            print(f"   テキスト: {post['text'][:150]}...")
            print(f"   文字数: {len(post['text'])}")
        
        return filtered_posts[:10]  # 最大10件を返す
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return []

def create_html_from_real_posts(posts):
    """実際のXポストからHTML形式を生成"""
    if not posts:
        return ""
    
    html_cards = []
    
    for i, post in enumerate(posts, 1):
        # タイトルを生成
        title = f"🐦 {post['username']} - AI関連投稿"
        
        # 要約を生成
        summary = post['display_summary']
        
        # 時間表示（簡易版）
        time_ago = "数時間前"
        
        html_card = f'''        <article class="enhanced-card" data-score="10.0" data-source="X / SNS (実データ)" data-time="{datetime.now().isoformat()}">
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
    # 実際のXポストを抽出
    real_posts = extract_real_x_posts()
    
    if real_posts:
        # HTML生成
        html_content = create_html_from_real_posts(real_posts)
        
        # ファイルに保存
        with open('real_x_posts.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"\n✅ 成功: {len(real_posts)}件の実際のXポストを抽出")
        print("💾 real_x_posts.htmlに保存しました")
        
        # 統計情報
        usernames = set(post['username'] for post in real_posts)
        print(f"\n📊 統計:")
        print(f"   投稿数: {len(real_posts)}")
        print(f"   ユニークユーザー: {len(usernames)}")
        print(f"   主要ユーザー: {', '.join(list(usernames)[:5])}")
        
    else:
        print("❌ Xポストの抽出に失敗しました")