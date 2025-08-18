#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
対象URL設定とバッチ処理
"""

import sys
import os
from pathlib import Path

# .envファイルを読み込み
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenvがない場合は手動で.envを読み込み
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from scrapers.beautifulsoup_scraper import BeautifulSoupScraper
from scrapers.gemini_extractor import GeminiExtractor

# 対象URLリスト（カテゴリ別）
TARGET_URLS = {
    "ai_news": [
        "https://techcrunch.com/category/artificial-intelligence/",
        "https://venturebeat.com/ai/",
        "https://www.theverge.com/ai-artificial-intelligence",
    ],
    
    "ai_research": [
        "https://openai.com/blog/",
        "https://blog.google/technology/ai/",
        "https://www.anthropic.com/news",
    ],
    
    "tech_news": [
        "https://news.ycombinator.com/",
        "https://techcrunch.com/",
        "https://www.producthunt.com/",
    ],
    
    "business": [
        "https://techcrunch.com/category/startups/",
        "https://www.crunchbase.com/",
        "https://pitchbook.com/news",
    ]
}

def scrape_category(category: str, max_urls: int = 3):
    """カテゴリ別スクレイピング実行"""
    if category not in TARGET_URLS:
        print(f"❌ カテゴリ '{category}' が見つかりません")
        print(f"利用可能: {list(TARGET_URLS.keys())}")
        return
    
    urls = TARGET_URLS[category][:max_urls]
    print(f"🎯 カテゴリ '{category}' のスクレイピング開始")
    print(f"📊 対象URL: {len(urls)}件")
    
    scraper = BeautifulSoupScraper()
    extractor = GeminiExtractor()
    
    results = []
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] {url}")
        
        try:
            # 基本スクレイピング
            basic_result = scraper.scrape(url)
            
            if basic_result['success']:
                # AI要約
                ai_result = extractor.extract(
                    basic_result['content'], 
                    "summary"
                )
                
                result = {
                    'url': url,
                    'title': basic_result['title'],
                    'content_length': len(basic_result['content']),
                    'ai_summary': ai_result.get('summary', 'AI要約失敗') if ai_result['success'] else 'AI要約失敗'
                }
                
                results.append(result)
                
                print(f"✅ 完了: {basic_result['title']}")
                print(f"📝 要約: {result['ai_summary'][:100]}...")
            else:
                print(f"❌ スクレイピング失敗: {basic_result.get('error', '不明')}")
                
        except Exception as e:
            print(f"❌ エラー: {e}")
    
    scraper.close()
    
    # 結果保存
    import json
    from datetime import datetime
    
    output_file = f"results_{category}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ 結果保存: {output_file}")
    print(f"📊 成功: {len(results)}件")

def main():
    """メイン実行"""
    print("🚀 対象URL設定バッチ処理")
    print("\n利用可能カテゴリ:")
    for category in TARGET_URLS.keys():
        print(f"  - {category}")
    
    if len(sys.argv) > 1:
        category = sys.argv[1]
        max_urls = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        scrape_category(category, max_urls)
    else:
        print("\n使用方法:")
        print("  python target_urls.py <category> [max_urls]")
        print("  例: python target_urls.py ai_news 2")

if __name__ == "__main__":
    main()