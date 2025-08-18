#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
包括的情報取得・分析スクリプト
全カテゴリの最新情報を一括取得・AI分析
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
import time

# .envファイルを読み込み
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
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

# 包括的対象URLリスト
COMPREHENSIVE_URLS = {
    "ai_breaking_news": [
        "https://techcrunch.com/category/artificial-intelligence/",
        "https://venturebeat.com/ai/",
        "https://www.theverge.com/ai-artificial-intelligence",
        "https://spectrum.ieee.org/topic/artificial-intelligence/",
        "https://www.wired.com/tag/artificial-intelligence/",
    ],
    
    "ai_research_labs": [
        "https://openai.com/blog/",
        "https://blog.google/technology/ai/",
        "https://www.anthropic.com/news",
        "https://deepmind.google/discover/blog/",
        "https://www.microsoft.com/en-us/research/research-area/artificial-intelligence/",
        "https://ai.meta.com/blog/",
        "https://blogs.nvidia.com/blog/category/deep-learning/",
    ],
    
    "business_startup": [
        "https://techcrunch.com/category/startups/",
        "https://www.crunchbase.com/",
        "https://pitchbook.com/news",
        "https://news.ycombinator.com/",
        "https://www.producthunt.com/",
        "https://techcrunch.com/category/venture/",
        "https://www.bloomberg.com/technology",
    ],
    
    "tech_innovation": [
        "https://techcrunch.com/",
        "https://arstechnica.com/",
        "https://www.technologyreview.com/",
        "https://www.engadget.com/",
        "https://thenextweb.com/",
        "https://www.zdnet.com/",
    ],
    
    "policy_regulation": [
        "https://www.politico.com/tech",
        "https://techcrunch.com/category/government-policy/",
        "https://www.reuters.com/technology/",
        "https://www.wsj.com/tech",
    ],
    
    "academic_research": [
        "https://arxiv.org/list/cs.AI/recent",
        "https://www.nature.com/subjects/machine-learning",
        "https://www.science.org/topic/computer-science",
        "https://distill.pub/",
    ]
}

def comprehensive_analysis(max_per_category: int = 5, analysis_types: list = None):
    """包括的分析実行"""
    if analysis_types is None:
        analysis_types = ["summary", "keywords", "analysis"]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    print("🚀 包括的情報取得・分析開始")
    print(f"📊 対象カテゴリ: {len(COMPREHENSIVE_URLS)}個")
    print(f"🎯 各カテゴリ最大: {max_per_category}件")
    print(f"🤖 AI分析タイプ: {', '.join(analysis_types)}")
    print("=" * 60)
    
    scraper = BeautifulSoupScraper()
    extractor = GeminiExtractor()
    
    all_results = {}
    total_processed = 0
    total_successful = 0
    
    for category, urls in COMPREHENSIVE_URLS.items():
        print(f"\n📂 カテゴリ: {category}")
        print(f"🎯 対象URL: {min(len(urls), max_per_category)}件")
        
        category_results = []
        category_urls = urls[:max_per_category]
        
        for i, url in enumerate(category_urls, 1):
            print(f"\n[{i}/{len(category_urls)}] {url}")
            total_processed += 1
            
            try:
                # 基本スクレイピング
                basic_result = scraper.scrape(url)
                
                if basic_result['success']:
                    print(f"✅ スクレイピング成功: {basic_result['title']}")
                    
                    # AI分析（複数タイプ）
                    ai_results = {}
                    for analysis_type in analysis_types:
                        try:
                            ai_result = extractor.extract(
                                basic_result['content'], 
                                analysis_type
                            )
                            ai_results[analysis_type] = ai_result
                            print(f"🤖 {analysis_type}分析: ✅")
                        except Exception as e:
                            print(f"🤖 {analysis_type}分析: ❌ {e}")
                            ai_results[analysis_type] = {'success': False, 'error': str(e)}
                    
                    # 結果統合
                    result = {
                        'url': url,
                        'category': category,
                        'timestamp': timestamp,
                        'basic': basic_result,
                        'ai_analysis': ai_results,
                        'content_stats': {
                            'character_count': len(basic_result.get('content', '')),
                            'link_count': len(basic_result.get('links', [])),
                            'image_count': len(basic_result.get('images', [])),
                            'title': basic_result.get('title', 'N/A')
                        }
                    }
                    
                    category_results.append(result)
                    total_successful += 1
                    
                else:
                    print(f"❌ スクレイピング失敗: {basic_result.get('error', '不明')}")
                
                # レート制限対応
                time.sleep(2)
                
            except Exception as e:
                print(f"❌ 処理エラー: {e}")
        
        all_results[category] = category_results
        print(f"📊 {category}: {len(category_results)}件成功")
    
    scraper.close()
    
    # 結果保存
    output_file = f"comprehensive_analysis_{timestamp}.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    
    # サマリー生成
    summary = {
        'timestamp': timestamp,
        'total_processed': total_processed,
        'total_successful': total_successful,
        'success_rate': f"{(total_successful/total_processed)*100:.1f}%" if total_processed > 0 else "0%",
        'categories': {cat: len(results) for cat, results in all_results.items()},
        'analysis_types': analysis_types,
        'output_file': output_file
    }
    
    summary_file = f"analysis_summary_{timestamp}.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 結果表示
    print("\n" + "=" * 60)
    print("📋 包括的分析完了")
    print("=" * 60)
    print(f"📊 処理済み: {total_processed}件")
    print(f"✅ 成功: {total_successful}件")
    print(f"📈 成功率: {summary['success_rate']}")
    print(f"💾 詳細結果: {output_file}")
    print(f"📄 サマリー: {summary_file}")
    
    print(f"\n📂 カテゴリ別成功件数:")
    for category, count in summary['categories'].items():
        print(f"   {category}: {count}件")
    
    return all_results, summary

def main():
    """メイン実行"""
    import argparse
    
    parser = argparse.ArgumentParser(description="包括的情報取得・分析")
    parser.add_argument('--max-per-category', type=int, default=5, help='各カテゴリの最大URL数')
    parser.add_argument('--analysis-types', nargs='+', 
                       choices=['summary', 'keywords', 'structure', 'analysis'],
                       default=['summary', 'keywords', 'analysis'],
                       help='AI分析タイプ')
    parser.add_argument('--quick', action='store_true', help='クイック実行（各カテゴリ2件、要約のみ）')
    
    args = parser.parse_args()
    
    if args.quick:
        print("⚡ クイック実行モード")
        comprehensive_analysis(max_per_category=2, analysis_types=['summary'])
    else:
        comprehensive_analysis(max_per_category=args.max_per_category, 
                             analysis_types=args.analysis_types)

if __name__ == "__main__":
    main()