#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Comprehensive Test - Enhanced AI News System
"""
import os
import sys
import json
import requests
from datetime import datetime, timedelta
from pathlib import Path

def test_environment():
    """環境設定テスト"""
    print("🔧 環境設定テスト")
    print("-" * 30)
    
    # .env ファイル確認
    env_path = Path('.env')
    if env_path.exists():
        print("✅ .env ファイル存在")
        with open(env_path, 'r', encoding='utf-8') as f:
            env_content = f.read()
            if 'GEMINI_API_KEY' in env_content:
                print("✅ GEMINI_API_KEY 設定済み")
            else:
                print("❌ GEMINI_API_KEY 未設定")
    else:
        print("❌ .env ファイル未存在")
    
    # 必要ファイル確認
    required_files = [
        'build.py',
        'enhanced_x_processor.py', 
        'gemini_url_context.py',
        'feeds.yml',
        'style.css'
    ]
    
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file} 存在")
        else:
            print(f"❌ {file} 未存在")
    
    print()

def test_website_functionality():
    """ウェブサイト機能テスト"""
    print("🌐 ウェブサイト機能テスト")
    print("-" * 30)
    
    # メインサイト確認
    try:
        response = requests.get('https://awano27.github.io/daily-ai-news-pages/', timeout=10)
        if response.status_code == 200:
            content = response.text
            
            # 基本機能確認
            checks = {
                'タブ機能': 'class="tab"' in content,
                'CSS読み込み': 'style.css' in content,
                'JavaScript': 'TabController' in content,
                '検索機能': 'searchBox' in content,
                '日本語コンテンツ': 'ニュース' in content or '記事' in content,
                'X投稿統合': 'X投稿' in content or 'ツイート' in content
            }
            
            for check_name, passed in checks.items():
                status = "✅" if passed else "❌"
                print(f"{status} {check_name}: {'正常' if passed else '問題あり'}")
            
            # サイト情報表示
            print(f"\n📊 サイト情報:")
            print(f"   ステータス: {response.status_code}")
            print(f"   サイズ: {len(content):,} bytes")
            
            # 最新更新確認
            if '2025-08' in content:
                print("✅ 2025年8月コンテンツを確認")
            
        else:
            print(f"❌ サイトアクセス失敗: ステータス {response.status_code}")
            
    except Exception as e:
        print(f"❌ サイトテストエラー: {e}")
    
    print()

def test_github_actions():
    """GitHub Actions テスト"""
    print("⚙️ GitHub Actions 設定テスト")
    print("-" * 30)
    
    # ワークフローファイル確認
    workflows_dir = Path('.github/workflows')
    if workflows_dir.exists():
        workflow_files = list(workflows_dir.glob('*.yml'))
        print(f"✅ ワークフローファイル: {len(workflow_files)}個")
        
        for workflow in workflow_files:
            print(f"   - {workflow.name}")
            
            # 内容確認
            try:
                with open(workflow, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # 重要設定確認
                if 'cron:' in content:
                    print(f"     ✅ 定期実行設定あり")
                if 'GEMINI_API_KEY' in content:
                    print(f"     ✅ Gemini API設定あり")
                if 'enhanced' in workflow.name.lower():
                    print(f"     🚀 Enhanced workflow")
                    
            except Exception as e:
                print(f"     ❌ ファイル読み込みエラー: {e}")
                
    else:
        print("❌ .github/workflows ディレクトリ未存在")
    
    print()

def test_content_quality():
    """コンテンツ品質テスト"""
    print("📝 コンテンツ品質テスト") 
    print("-" * 30)
    
    # サンプルHTML確認
    html_files = ['index.html', 'news_detail.html']
    
    for html_file in html_files:
        if Path(html_file).exists():
            print(f"✅ {html_file} 存在")
            
            with open(html_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 品質チェック
            quality_checks = {
                'HTML5構造': '<!DOCTYPE html>' in content,
                'Meta情報': '<meta' in content,
                'CSS統合': 'style.css' in content,
                'JavaScript': '<script>' in content,
                'アクセシビリティ': 'aria-' in content,
                '日本語対応': 'lang="ja"' in content or 'charset="utf-8"' in content
            }
            
            for check, passed in quality_checks.items():
                status = "✅" if passed else "⚠️"
                print(f"   {status} {check}")
                
            print(f"   📊 ファイルサイズ: {len(content):,} bytes")
            
        else:
            print(f"❌ {html_file} 未存在")
    
    print()

def test_data_processing():
    """データ処理テスト"""
    print("📊 データ処理テスト")
    print("-" * 30)
    
    # キャッシュディレクトリ確認
    cache_dir = Path('_cache')
    if cache_dir.exists():
        print("✅ キャッシュディレクトリ存在")
        
        cache_files = list(cache_dir.glob('*'))
        print(f"   キャッシュファイル: {len(cache_files)}個")
        
        for cache_file in cache_files:
            print(f"   - {cache_file.name}")
            
            # 翻訳キャッシュ特別確認
            if cache_file.name == 'translations.json':
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        translations = json.load(f)
                    print(f"     翻訳キャッシュ: {len(translations)}件")
                except Exception as e:
                    print(f"     ❌ 翻訳キャッシュ読み込みエラー: {e}")
    else:
        print("⚠️ キャッシュディレクトリ未存在")
    
    # feeds.yml確認
    if Path('feeds.yml').exists():
        print("✅ feeds.yml 設定ファイル存在")
        
        try:
            import yaml
            with open('feeds.yml', 'r', encoding='utf-8') as f:
                feeds = yaml.safe_load(f)
            
            total_feeds = sum(len(category) for category in feeds.values())
            print(f"   設定済みフィード: {total_feeds}個")
            
            for category, feed_list in feeds.items():
                print(f"   - {category}: {len(feed_list)}個")
                
        except Exception as e:
            print(f"   ❌ feeds.yml解析エラー: {e}")
    
    print()

def main():
    """総合テスト実行"""
    print("🧪 Enhanced AI News System - 総合テスト")
    print("=" * 60)
    print(f"実行日時: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # 各テスト実行
    test_environment()
    test_website_functionality()
    test_github_actions()
    test_content_quality()
    test_data_processing()
    
    print("=" * 60)
    print("📋 **テスト完了**")
    print()
    print("✅ 正常項目: システムは正常に動作")
    print("⚠️ 警告項目: 動作するが改善の余地あり")
    print("❌ 問題項目: 修正が必要")
    print()
    print("🔗 確認URL:")
    print("- サイト: https://awano27.github.io/daily-ai-news-pages/")
    print("- Actions: https://github.com/awano27/daily-ai-news/actions")
    print()
    print("📈 次のステップ:")
    print("1. 問題項目の修正")
    print("2. パフォーマンス最適化")
    print("3. コンテンツ品質向上")

if __name__ == "__main__":
    main()