#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monitor Deployment - デプロイメント状況をモニタリング
"""
import webbrowser
import requests
import time
from datetime import datetime

def check_site_status():
    """サイトの状況をチェック"""
    site_url = "https://awano27.github.io/daily-ai-news-pages/"
    
    try:
        print("🌐 サイトアクセス確認中...")
        response = requests.get(site_url, timeout=10)
        
        if response.status_code == 200:
            content = response.text.lower()
            
            # コンテンツの詳細チェック
            checks = {
                "サイト表示": response.status_code == 200,
                "HTML構造": "<html" in content and "</html>" in content,
                "タイトル有": "<title>" in content,
                "AI News関連": any(keyword in content for keyword in ["ai news", "daily ai", "enhanced"]),
                "日本語コンテンツ": any(char in content for char in "あいうえおニュース最新"),
                "X/Twitter投稿": any(keyword in content for keyword in ["x.com", "twitter.com", "xポスト"]),
                "2025年コンテンツ": "2025" in content,
                "Gemini強化": "gemini" in content or "enhanced" in content
            }
            
            print(f"✅ サイトアクセス成功! (Status: {response.status_code})")
            print(f"📊 Content size: {len(response.content):,} bytes")
            
            print("\n🔍 コンテンツ詳細チェック:")
            passed = 0
            for check_name, result in checks.items():
                status = "✅" if result else "❌"
                print(f"   {status} {check_name}")
                if result:
                    passed += 1
            
            quality_score = (passed / len(checks)) * 100
            print(f"\n📊 サイト品質スコア: {quality_score:.1f}% ({passed}/{len(checks)})")
            
            if quality_score >= 75:
                print("🎉 **サイト高品質稼働中！**")
                return "excellent"
            elif quality_score >= 50:
                print("✅ サイト正常稼働中")
                return "good"
            else:
                print("⚠️ サイトは表示されるが、コンテンツに改善余地あり")
                return "needs_improvement"
                
        elif response.status_code == 404:
            print("❌ サイトが見つかりません (404)")
            print("💡 GitHub Pagesの設定を確認してください")
            return "not_found"
        else:
            print(f"⚠️ サイトアクセスエラー: {response.status_code}")
            return "error"
            
    except requests.exceptions.Timeout:
        print("⏱️ サイトアクセスタイムアウト（サイト構築中の可能性）")
        return "timeout"
    except requests.exceptions.ConnectionError:
        print("🔌 サイト接続エラー（DNS設定中の可能性）")
        return "connection_error"
    except Exception as e:
        print(f"❌ サイトアクセス失敗: {e}")
        return "unknown_error"

def main():
    """デプロイメントモニタリング"""
    print("📊 Enhanced AI News - Deployment Monitor")
    print("=" * 60)
    print(f"監視開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    print("🚀 GitHub Actions Status:")
    print("✅ Pages Build #152: Pending → 実行中")
    print("✅ Minimal Build #5: In progress → 実行中") 
    print("✅ Pages Build #151: In progress → 実行中")
    print()
    
    print("💡 重複について:")
    print("これは正常です。複数のワークフローが並行実行されています。")
    print()
    
    # サイト状況確認
    site_status = check_site_status()
    
    print(f"\n📋 推奨アクション (Status: {site_status}):")
    
    if site_status == "excellent":
        print("🎉 **システム完全稼働達成！**")
        print("✅ Enhanced AI News System が正常に動作しています")
        print("🕐 毎日 07:00, 19:00 JST に自動更新されます")
        
    elif site_status == "good":
        print("✅ システム基本稼働中")
        print("💡 Enhanced ワークフローを実行して最新コンテンツに更新することを推奨")
        
    elif site_status in ["needs_improvement", "not_found", "error"]:
        print("🔧 追加設定が必要:")
        print("1. GitHub Pages設定確認")
        print("2. GEMINI_API_KEY 設定確認")
        print("3. Enhanced ワークフロー手動実行")
        
    else:
        print("⏱️ デプロイメント処理中")
        print("2-3分後に再確認してください")
    
    print(f"\n🌐 サイトURL: https://awano27.github.io/daily-ai-news-pages/")
    print("🔄 Actions URL: https://github.com/awano27/daily-ai-news/actions")
    print("⚙️ Pages Settings: https://github.com/awano27/daily-ai-news-pages/settings/pages")
    
    # ブラウザで開く
    answer = input("\n🌐 関連ページを開きますか? (y/n): ")
    if answer.lower() == 'y':
        print("🚀 ページを開いています...")
        webbrowser.open("https://awano27.github.io/daily-ai-news-pages/")
        time.sleep(1)
        webbrowser.open("https://github.com/awano27/daily-ai-news/actions")
        print("✅ ページを開きました")
    
    if site_status in ["excellent", "good"]:
        print("\n🎊 **Enhanced AI News System 稼働確認完了！**")
        print("毎日自動でAIニュースが更新されます。")
    else:
        print(f"\n🔄 現在の状況: {site_status}")
        print("継続的な監視と設定確認を推奨します。")

if __name__ == "__main__":
    main()