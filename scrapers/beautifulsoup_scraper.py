#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BeautifulSoup ウェブスクレイパー
高速で軽量なHTML解析によるコンテンツ抽出
"""

import requests
from bs4 import BeautifulSoup
import time
from typing import Dict, Any, List
import re

class BeautifulSoupScraper:
    """BeautifulSoupベースのウェブスクレイパー"""
    
    def __init__(self, timeout: int = 10, delay: float = 1.0):
        """
        初期化
        
        Args:
            timeout: リクエストタイムアウト (秒)
            delay: リクエスト間隔 (秒)
        """
        self.timeout = timeout
        self.delay = delay
        self.session = requests.Session()
        
        # ヘッダー設定
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'ja,en-US;q=0.7,en;q=0.3',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def scrape(self, url: str) -> Dict[str, Any]:
        """
        URLからコンテンツを取得・解析
        
        Args:
            url: 対象URL
            
        Returns:
            解析結果辞書
        """
        print(f"🔍 スクレイピング開始: {url}")
        
        try:
            # HTTP リクエスト
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            
            # HTML 解析
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # コンテンツ抽出
            result = {
                'success': True,
                'url': url,
                'status_code': response.status_code,
                'title': self._extract_title(soup),
                'content': self._extract_content(soup),
                'links': self._extract_links(soup, url),
                'images': self._extract_images(soup, url),
                'meta': self._extract_meta(soup),
                'raw_html': str(soup)[:2000] + '...' if len(str(soup)) > 2000 else str(soup)
            }
            
            print(f"✅ スクレイピング完了: {len(result['content'])}文字")
            
            # 遅延
            time.sleep(self.delay)
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ リクエストエラー: {e}")
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'error_type': 'request_error'
            }
        
        except Exception as e:
            print(f"❌ 解析エラー: {e}")
            return {
                'success': False,
                'url': url,
                'error': str(e),
                'error_type': 'parsing_error'
            }
    
    def _extract_title(self, soup: BeautifulSoup) -> str:
        """タイトル抽出"""
        # <title>タグ
        if soup.title:
            return soup.title.get_text(strip=True)
        
        # h1タグ
        h1 = soup.find('h1')
        if h1:
            return h1.get_text(strip=True)
        
        return "タイトル未取得"
    
    def _extract_content(self, soup: BeautifulSoup) -> str:
        """メインコンテンツ抽出"""
        # 不要要素を削除
        for element in soup(['script', 'style', 'nav', 'footer', 'header', 'aside']):
            element.decompose()
        
        # コンテンツ候補要素
        content_selectors = [
            'article',
            'main',
            '.content',
            '.post-content',
            '.entry-content',
            '.article-content',
            '#content',
            '#main'
        ]
        
        # セレクター順にコンテンツを検索
        for selector in content_selectors:
            element = soup.select_one(selector)
            if element:
                text = element.get_text(separator=' ', strip=True)
                if len(text) > 100:  # 十分な長さがある場合
                    return text
        
        # フォールバック: body全体
        body = soup.find('body')
        if body:
            text = body.get_text(separator=' ', strip=True)
            # 短すぎる場合は最初の1000文字
            return text[:1000] if len(text) > 1000 else text
        
        return soup.get_text(separator=' ', strip=True)
    
    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[Dict[str, str]]:
        """リンク抽出"""
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            text = a_tag.get_text(strip=True)
            
            # 相対URLを絶対URLに変換
            if href.startswith('/'):
                href = base_url.rstrip('/') + href
            elif not href.startswith(('http://', 'https://')):
                continue
            
            if text and len(text) > 0:
                links.append({
                    'url': href,
                    'text': text
                })
        
        return links[:20]  # 最大20リンク
    
    def _extract_images(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """画像URL抽出"""
        images = []
        
        for img_tag in soup.find_all('img', src=True):
            src = img_tag['src']
            
            # 相対URLを絶対URLに変換
            if src.startswith('/'):
                src = base_url.rstrip('/') + src
            elif not src.startswith(('http://', 'https://')):
                continue
            
            images.append(src)
        
        return images[:10]  # 最大10画像
    
    def _extract_meta(self, soup: BeautifulSoup) -> Dict[str, str]:
        """メタデータ抽出"""
        meta = {}
        
        # description
        desc_tag = soup.find('meta', attrs={'name': 'description'})
        if desc_tag:
            meta['description'] = desc_tag.get('content', '')
        
        # keywords
        keywords_tag = soup.find('meta', attrs={'name': 'keywords'})
        if keywords_tag:
            meta['keywords'] = keywords_tag.get('content', '')
        
        # Open Graph
        og_tags = soup.find_all('meta', attrs={'property': re.compile(r'^og:')})
        for tag in og_tags:
            property_name = tag.get('property', '').replace('og:', '')
            content = tag.get('content', '')
            if property_name and content:
                meta[f'og_{property_name}'] = content
        
        return meta
    
    def scrape_multiple(self, urls: List[str]) -> List[Dict[str, Any]]:
        """複数URL一括スクレイピング"""
        results = []
        
        print(f"🔍 一括スクレイピング開始: {len(urls)}件")
        
        for i, url in enumerate(urls, 1):
            print(f"進行状況: {i}/{len(urls)}")
            result = self.scrape(url)
            results.append(result)
        
        print(f"✅ 一括スクレイピング完了")
        return results
    
    def close(self):
        """セッション終了"""
        self.session.close()

# 使用例
if __name__ == "__main__":
    scraper = BeautifulSoupScraper()
    
    # テストURL
    test_url = "https://httpbin.org/get"
    result = scraper.scrape(test_url)
    
    print("結果:", result)
    scraper.close()