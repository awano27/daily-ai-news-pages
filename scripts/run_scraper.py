#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統合スクレイピング実行スクリプト
BeautifulSoup + Gemini AI による高度なウェブ解析
"""

import sys
import os
import argparse
import json
from pathlib import Path

# .envファイルを読み込み
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenvがない場合は手動で.envを読み込み
    env_path = os.path.join(Path(__file__).parent.parent, '.env')
    if os.path.exists(env_path):
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ[key.strip()] = value.strip()

# プロジェクトルートをパスに追加
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from scrapers.beautifulsoup_scraper import BeautifulSoupScraper
from scrapers.gemini_extractor import GeminiExtractor

def main():
    """メイン実行関数"""
    parser = argparse.ArgumentParser(
        description="Free Scraping Platform - 統合ウェブスクレイピング"
    )
    
    parser.add_argument(
        'url',
        help='スクレイピング対象URL'
    )
    
    parser.add_argument(
        '--method',
        choices=['basic', 'ai', 'full'],
        default='basic',
        help='スクレイピング方法 (basic: HTML解析のみ, ai: AI抽出のみ, full: 両方)'
    )
    
    parser.add_argument(
        '--ai-extraction',
        choices=['summary', 'keywords', 'structure', 'analysis'],
        default='summary',
        help='AI抽出タイプ'
    )
    
    parser.add_argument(
        '--output',
        help='結果出力ファイル (JSON形式)'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='詳細出力'
    )
    
    args = parser.parse_args()
    
    print("🚀 Free Scraping Platform 開始")
    print(f"🎯 対象URL: {args.url}")
    print(f"📊 方法: {args.method}")
    
    results = {}
    
    try:
        # Basic スクレイピング
        if args.method in ['basic', 'full']:
            print("\n🔍 基本スクレイピング実行中...")
            scraper = BeautifulSoupScraper()
            basic_result = scraper.scrape(args.url)
            results['basic'] = basic_result
            
            if args.verbose:
                print(f"   タイトル: {basic_result.get('title', 'N/A')}")
                print(f"   コンテンツ長: {len(basic_result.get('content', ''))}文字")
                print(f"   リンク数: {len(basic_result.get('links', []))}")
            
            scraper.close()
        
        # AI 抽出
        if args.method in ['ai', 'full']:
            print(f"\n🤖 AI抽出実行中 ({args.ai_extraction})...")
            
            # コンテンツを取得（basicから、または新規取得）
            if 'basic' in results and results['basic']['success']:
                content = results['basic']['content']
            else:
                # AI抽出のみの場合は基本スクレイピングを実行
                scraper = BeautifulSoupScraper()
                basic_result = scraper.scrape(args.url)
                content = basic_result.get('content', '')
                scraper.close()
                
                if not content:
                    print("❌ コンテンツ取得失敗")
                    return
            
            # Gemini抽出実行
            try:
                extractor = GeminiExtractor()
                ai_result = extractor.extract(content, args.ai_extraction)
                results['ai'] = ai_result
                
                if args.verbose and ai_result.get('success'):
                    print(f"   抽出タイプ: {ai_result.get('extraction_type')}")
                    if 'summary' in ai_result:
                        print(f"   要約: {ai_result['summary'][:100]}...")
                    
            except Exception as e:
                print(f"❌ AI抽出エラー: {e}")
                results['ai'] = {
                    'success': False,
                    'error': str(e)
                }
        
        # 結果表示
        print("\n📋 実行結果:")
        
        if 'basic' in results:
            status = "✅ 成功" if results['basic']['success'] else "❌ 失敗"
            print(f"   基本スクレイピング: {status}")
        
        if 'ai' in results:
            status = "✅ 成功" if results['ai']['success'] else "❌ 失敗"
            print(f"   AI抽出: {status}")
        
        # ファイル出力
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            print(f"💾 結果を保存: {args.output}")
        
        # 簡易表示
        if not args.output and not args.verbose:
            if 'basic' in results and results['basic']['success']:
                print(f"\n📄 タイトル: {results['basic']['title']}")
                print(f"📝 要約: {results['basic']['content'][:200]}...")
            
            if 'ai' in results and results['ai']['success']:
                if 'summary' in results['ai']:
                    print(f"🤖 AI要約: {results['ai']['summary'][:200]}...")
        
        print("\n✅ 処理完了")
        
    except KeyboardInterrupt:
        print("\n⚠️ ユーザーによる中断")
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()