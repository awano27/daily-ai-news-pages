#!/usr/bin/env python3
"""
403エラーURLを完全に除外するフィルター機能
"""
import re
from typing import List, Dict, Any

class URLFilter:
    def __init__(self):
        # 403エラーになることが判明しているURLパターン
        self.blocked_patterns = [
            r'https://news\.google\.com/rss/articles/CBM[^?]*\?oc=5',
            r'https://news\.google\.com/articles/CBM[^?]*\?oc=5',
            r'https://news\.google\.com/.*CBM.*',
            # Google Newsの問題のあるパターン全般
        ]
        
        # 403エラーになるドメイン
        self.blocked_domains = [
            'news.google.com/rss/articles',
            'news.google.com/articles',
        ]
        
        # 403エラーになる具体的URL（過去に確認済み）
        self.blocked_urls = set([
            'https://news.google.com/rss/articles/CBMijwFBVV95cUxPZFprVjVNbUFEa25tZXJfbzlyd1hiSEEyRmR1dlFIQUdCRzI0MTJSR3l6elFyUXBlTVdhQkhQY2ZSdDZmbXR0YlFMdmZjMHpTNFVZczZTb1lVWVJkWDJCdlhHeHZMdnlmT3Z3dEJjem1SaV95aWdfLWxyUjdydGNqQVhyeGpjem5fd1NLcC0xSQ?oc=5'
        ])
    
    def is_blocked_url(self, url: str) -> bool:
        """URLが403エラーになるかどうかをチェック"""
        if not url or url == '#':
            return False
            
        # 具体的なブロックURLのチェック
        if url in self.blocked_urls:
            return True
            
        # パターンマッチング
        for pattern in self.blocked_patterns:
            if re.match(pattern, url):
                return True
                
        # ドメインチェック
        for domain in self.blocked_domains:
            if domain in url:
                return True
                
        return False
    
    def filter_items(self, items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """アイテムリストから403 URLを除外"""
        filtered_items = []
        removed_count = 0
        
        for item in items:
            url = item.get('url', item.get('link', ''))
            
            if self.is_blocked_url(url):
                removed_count += 1
                print(f"🚫 403 URL除外: {item.get('title', 'No title')[:50]}...")
            else:
                filtered_items.append(item)
        
        if removed_count > 0:
            print(f"✅ {removed_count}件の403 URLを除外しました")
            
        return filtered_items
    
    def add_blocked_url(self, url: str):
        """新しい403 URLをブロックリストに追加"""
        self.blocked_urls.add(url)
        print(f"🚫 ブロックリストに追加: {url}")

# グローバルフィルターインスタンス
url_filter = URLFilter()

def filter_403_urls(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """アイテムから403 URLを除外（外部から呼び出し用）"""
    return url_filter.filter_items(items)

def is_403_url(url: str) -> bool:
    """URLが403エラーになるかチェック（外部から呼び出し用）"""
    return url_filter.is_blocked_url(url)

if __name__ == "__main__":
    # テスト
    test_items = [
        {
            'title': 'Normal News',
            'url': 'https://techcrunch.com/some-article'
        },
        {
            'title': 'Google News 403 Error',
            'url': 'https://news.google.com/rss/articles/CBMijwFBVV95cUxPZFprVjVNbUFEa25tZXJfbzlyd1hiSEEyRmR1dlFIQUdCRzI0MTJSR3l6elFyUXBlTVdhQkhQY2ZSdDZmbXR0YlFMdmZjMHpTNFVZczZTb1lVWVJkWDJCdlhHeHZMdnlmT3Z3dEJjem1SaV95aWdfLWxyUjdydGNqQVhyeGpjem5fd1NLcC0xSQ?oc=5'
        }
    ]
    
    print("🧪 URL フィルターテスト")
    filtered = filter_403_urls(test_items)
    print(f"元: {len(test_items)}件 → フィルター後: {len(filtered)}件")