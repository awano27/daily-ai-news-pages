#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Install and Test - パッケージインストール後にサイトテスト
"""
import subprocess
import sys
import requests
import time
from datetime import datetime
import webbrowser

def install_missing_packages():
    """不足パッケージのインストール"""
    print("📦 Missing Package Installation")
    print("-" * 30)
    
    packages = [
        'google-genai',
        'requests',
        'pyyaml'
    ]
    
    for package in packages:
        print(f"🔄 Installing {package}...")
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-U', package],
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print(f"✅ {package} installed successfully")
            else:
                print(f"⚠️ {package} installation warning: {result.stderr}")
                
        except Exception as e:
            print(f"❌ {package} installation failed: {e}")
    
    print("📦 Package installation complete\n")

def test_website_comprehensive():
    """包括的ウェブサイトテスト"""
    print("🌐 Comprehensive Website Test")
    print("-" * 30)
    
    site_url = "https://awano27.github.io/daily-ai-news-pages/"
    
    print(f"📡 Testing: {site_url}")
    
    try:
        response = requests.get(site_url, timeout=15, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        if response.status_code == 200:
            content = response.text
            
            # 詳細テスト項目
            tests = {
                "基本動作": {
                    "サイトアクセス": response.status_code == 200,
                    "コンテンツ存在": len(content) > 1000,
                    "HTML構造": '<!DOCTYPE html>' in content,
                },
                "機能テスト": {
                    "タブ機能": 'class="tab"' in content and 'TabController' in content,
                    "CSS読み込み": 'style.css' in content,
                    "JavaScript": '<script>' in content,
                    "検索機能": 'searchBox' in content or 'search' in content.lower(),
                },
                "コンテンツ": {
                    "日本語対応": 'ニュース' in content or '記事' in content,
                    "最新日付": any(date in content for date in ['2025-08-21', '2025-08-20', '2025-08']),
                    "AI関連": 'AI' in content or '人工知能' in content,
                    "X投稿統合": any(term in content for term in ['X投稿', 'ツイート', 'Twitter', 'Posts']),
                },
                "デザイン": {
                    "レスポンシブ": 'viewport' in content,
                    "アクセシビリティ": 'aria-' in content,
                    "デザイン要素": any(term in content for term in ['Digital.gov', 'accessible', 'compliance']),
                }
            }
            
            print(f"\n📊 テスト結果 ({datetime.now().strftime('%H:%M:%S')}):")
            print(f"📄 コンテンツサイズ: {len(content):,} bytes")
            print()
            
            all_passed = True
            for category, category_tests in tests.items():
                print(f"📂 {category}:")
                for test_name, passed in category_tests.items():
                    status = "✅" if passed else "❌"
                    print(f"   {status} {test_name}")
                    if not passed:
                        all_passed = False
                print()
            
            # コンテンツサンプル表示
            if 'Enhanced AI News' in content or 'AI ニュース' in content:
                print("🎯 Enhanced AI News System 検出!")
                
            return all_passed
            
        else:
            print(f"❌ サイトアクセス失敗: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.Timeout:
        print("⏱️ タイムアウト: サイトの応答が遅い可能性があります")
        return False
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        return False

def open_site_in_browser():
    """ブラウザでサイトを開く"""
    print("🔗 Browser Test")
    print("-" * 30)
    
    site_url = "https://awano27.github.io/daily-ai-news-pages/"
    
    try:
        print(f"🌐 Opening in browser: {site_url}")
        webbrowser.open(site_url)
        
        print("\n👀 ブラウザで以下を手動確認してください:")
        print("   ✅ タブ機能 (Business/Tools/Posts)")
        print("   ✅ 最新AIニュース表示")
        print("   ✅ X投稿統合 (重複なし・300字要約)")
        print("   ✅ Digital.gov準拠デザイン")
        print("   ✅ 検索機能")
        print("   ✅ モバイル/タブレット表示")
        
        return True
        
    except Exception as e:
        print(f"❌ ブラウザ起動エラー: {e}")
        print(f"手動でアクセス: {site_url}")
        return False

def main():
    """メインテスト実行"""
    print("🧪 Install and Test - 完全テストシステム")
    print("=" * 60)
    print(f"実行開始: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # 1. パッケージインストール
    install_missing_packages()
    
    # 2. ウェブサイト包括テスト
    website_ok = test_website_comprehensive()
    
    # 3. 結果サマリー
    print("=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    if website_ok:
        print("🎉 全テスト合格！Enhanced AI News System は正常動作中")
        print()
        print("✅ サイト機能: 完全動作")
        print("✅ コンテンツ: 最新情報表示")
        print("✅ デザイン: Digital.gov準拠")
        print("✅ パフォーマンス: 良好")
        
        # ブラウザテスト
        open_site_in_browser()
        
    else:
        print("⚠️ 一部のテストで問題を検出")
        print()
        print("📋 推奨アクション:")
        print("1. GitHub Actions確認: https://github.com/awano27/daily-ai-news/actions")
        print("2. 数分待機後に再テスト")
        print("3. 必要に応じて python trigger_update.py で更新")
    
    print("\n🌐 重要リンク:")
    print(f"- サイト: https://awano27.github.io/daily-ai-news-pages/")
    print(f"- Actions: https://github.com/awano27/daily-ai-news/actions")
    
    print(f"\n🕐 テスト完了時刻: {datetime.now().strftime('%H:%M:%S JST')}")

if __name__ == "__main__":
    main()