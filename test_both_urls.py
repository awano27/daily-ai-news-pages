#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Both URLs - 両方のURLをテスト
"""
import requests
import time
from datetime import datetime

def test_url(url):
    """URLをテスト"""
    print(f"\n📡 Testing: {url}")
    print("-" * 40)
    
    try:
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            content = response.text
            
            print(f"✅ Status: {response.status_code}")
            print(f"📄 Size: {len(content):,} bytes")
            
            # 重要な要素をチェック
            checks = {
                "DOCTYPE": '<!DOCTYPE' in content,
                "TabController": 'TabController' in content,
                "Digital.gov": 'Digital.gov' in content or 'compliance' in content,
                "タブ機能HTML": 'class="tab"' in content,
                "更新タイムスタンプ": '2025-08-21' in content,
                "Enhanced": 'Enhanced' in content
            }
            
            print("\n📊 要素チェック:")
            for name, found in checks.items():
                status = "✅" if found else "❌"
                print(f"   {status} {name}")
            
            # 最初の100文字を表示
            print(f"\n📝 最初の100文字:")
            print(f"   {content[:100]}...")
            
            return response.status_code == 200 and checks["DOCTYPE"]
            
        else:
            print(f"❌ Status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    """メイン処理"""
    print("🧪 Test Both URLs - サイトURL確認")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    
    urls = [
        "https://awano27.github.io/daily-ai-news/",
        "https://awano27.github.io/daily-ai-news-pages/"
    ]
    
    results = {}
    for url in urls:
        results[url] = test_url(url)
        time.sleep(1)  # 少し待機
    
    print("\n" + "=" * 60)
    print("📋 SUMMARY")
    print("=" * 60)
    
    for url, success in results.items():
        status = "✅ WORKING" if success else "❌ NOT WORKING"
        print(f"{status}: {url}")
    
    # 正しいURLを特定
    working_url = None
    for url, success in results.items():
        if success:
            working_url = url
            break
    
    if working_url:
        print(f"\n🎯 使用すべきURL: {working_url}")
        print("\n📋 次のステップ:")
        print("1. ブラウザで確認:")
        print(f"   {working_url}")
        print("2. タブ機能をテスト")
        print("3. 検索機能をテスト")
    else:
        print("\n⏳ まだ更新中の可能性があります")
        print("2-3分待ってから再実行してください")

if __name__ == "__main__":
    main()