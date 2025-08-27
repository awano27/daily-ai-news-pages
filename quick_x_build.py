#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Xポスト専用の軽量ビルダー
"""
import os
import requests
import csv
import io
import re
import html
from datetime import datetime, timezone, timedelta

def quick_build_x_posts():
    """Xポストを素早くビルド"""
    print("⚡ 軽量Xポストビルド開始")
    print("=" * 40)
    
    # CSV URL
    csv_url = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
    
    try:
        # CSVデータを取得（タイムアウト短縮）
        print("📡 CSV取得中...")
        response = requests.get(csv_url, timeout=10)
        
        if response.status_code != 200:
            print(f"❌ HTTPエラー: {response.status_code}")
            return []
        
        content = response.text
        print(f"📊 データサイズ: {len(content)} 文字")
        
        # CSVを解析（簡易版）
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        
        if not rows:
            print("❌ CSVが空です")
            return []
        
        print(f"📋 CSV行数: {len(rows)}")
        print(f"📋 ヘッダー: {rows[0] if rows else 'なし'}")
        
        # Xポストを抽出（最大5件、高速処理）
        x_posts_html = []
        post_count = 0
        
        for row_idx, row in enumerate(rows[1:6], 1):  # 最初の5行のみ
            if len(row) < 3:
                continue
            
            # 基本データ抽出
            date_str = row[0].strip('"').strip() if row[0] else f"2025-08-{25+row_idx}"
            username = row[1].strip('"').strip() if row[1] else f"user_{row_idx}"
            text = row[2].strip('"').strip() if row[2] else "No content"
            
            # テキストが短すぎる場合はスキップ
            if len(text) < 10:
                continue
            
            # HTMLエンティティをデコード
            text = html.unescape(text)
            
            # 長すぎる場合は切り詰め
            if len(text) > 200:
                text = text[:200] + "..."
            
            # URLを検索（全ての列から）
            tweet_url = ""
            for col in row:
                if 'x.com' in col or 'twitter.com' in col:
                    url_match = re.search(r'https?://(?:x\.com|twitter\.com)/[^\s,"\']+', col)
                    if url_match:
                        tweet_url = url_match.group(0)
                        break
            
            # URLがない場合はプロフィールページ
            if not tweet_url:
                clean_user = username.replace('@', '').replace(' ', '')
                tweet_url = f"https://x.com/{clean_user}" if clean_user else "https://x.com"
            
            post_count += 1
            
            # HTML生成
            card_html = f'''        <article class="enhanced-card" data-score="10.0" data-source="X / SNS (CSV実データ)" data-time="{datetime.now().isoformat()}">
          <div class="card-priority high">最高 10.0</div>
          <header class="card-header">
            <h3 class="card-title">
              <a href="{tweet_url}" target="_blank" rel="noopener">🐦 {username} - X投稿</a>
            </h3>
          </header>
          <div class="card-meta">
            <span class="card-source">X / SNS (CSV実データ)</span>
          </div>
          <div class="card-summary">{html.escape(text)}</div>
          <footer class="card-footer">
            <span class="card-score">スコア: 10.0</span>
            <span class="card-time">数時間前</span>
          </footer>
        </article>

'''
            x_posts_html.append(card_html)
            
            print(f"✅ 投稿 {post_count}: {username} -> {tweet_url[:50]}...")
            print(f"   テキスト: {text[:50]}...")
        
        print(f"\n📊 処理結果: {len(x_posts_html)}件のXポスト生成")
        
        # HTMLファイルを読み込み（簡易版）
        if not os.path.exists('index.html'):
            print("❌ index.htmlが見つかりません")
            return []
        
        with open('index.html', 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Postsセクションを見つけて置換
        posts_start = html_content.find('<section class="tab-panel hidden" data-category="posts">')
        if posts_start == -1:
            print("❌ Postsセクションが見つかりません")
            return []
        
        # セクション内のコンテンツを置換
        content_start = html_content.find('<div class="tab-content">', posts_start)
        content_end = html_content.find('</div>', content_start) + 6
        
        if content_start == -1 or content_end == -1:
            print("❌ Postsセクションの構造が不正です")
            return []
        
        # 新しいコンテンツを挿入
        new_content = f'''<div class="tab-content">

{(''.join(x_posts_html))}        <!-- Xポスト以降は他のポスト -->'''
        
        new_html = html_content[:content_start] + new_content + html_content[content_end:]
        
        # ファイルに保存
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(new_html)
        
        print("💾 index.html更新完了")
        
        return x_posts_html
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return []

if __name__ == "__main__":
    posts = quick_build_x_posts()
    
    if posts:
        print(f"\n🎉 成功: {len(posts)}件のXポストを生成")
        print("\n次のステップ:")
        print("git add index.html")
        print("git commit -m 'fix: Add real X posts from CSV with lightweight builder'")
        print("git push origin main")
    else:
        print("\n❌ Xポストの生成に失敗しました")