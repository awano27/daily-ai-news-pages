#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Manual Enhanced Test - Enhanced AI News Systemの手動テスト実行
"""
import os
import subprocess
import sys
from datetime import datetime

def main():
    """Enhanced AI News Systemの手動テスト"""
    print("🚀 Enhanced AI News System - Manual Test")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # 環境変数設定
    os.environ["HOURS_LOOKBACK"] = "24"
    os.environ["MAX_ITEMS_PER_CATEGORY"] = "8"
    os.environ["TRANSLATE_TO_JA"] = "1"
    os.environ["TRANSLATE_ENGINE"] = "google"
    os.environ["X_POSTS_CSV"] = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    
    print("🔧 環境変数設定完了")
    print(f"  HOURS_LOOKBACK: {os.environ.get('HOURS_LOOKBACK')}")
    print(f"  MAX_ITEMS_PER_CATEGORY: {os.environ.get('MAX_ITEMS_PER_CATEGORY')}")
    print(f"  TRANSLATE_TO_JA: {os.environ.get('TRANSLATE_TO_JA')}")
    print()
    
    try:
        print("📰 Enhanced AI News Build 実行中...")
        result = subprocess.run([
            sys.executable, "build.py"
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ Build 成功!")
            print(f"📊 出力: {result.stdout[-200:]}")  # 最後の200文字
        else:
            print("❌ Build 失敗")
            print(f"Error: {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏱️ Build タイムアウト (5分)")
        
    except Exception as e:
        print(f"❌ Build エラー: {e}")
    
    # 生成されたファイルを確認
    print("\n📁 生成ファイル確認:")
    files_to_check = [
        "index.html",
        "news_detail.html", 
        "ai_news_dashboard.html"
    ]
    
    for filename in files_to_check:
        if os.path.exists(filename):
            size = os.path.getsize(filename)
            print(f"  ✅ {filename}: {size:,} bytes")
            
            # 最新の内容かチェック
            if "2025-08-20" in open(filename, 'r', encoding='utf-8').read():
                print(f"    🎯 {filename}: 最新コンテンツ確認")
            else:
                print(f"    ⚠️ {filename}: 古いコンテンツの可能性")
        else:
            print(f"  ❌ {filename}: 見つかりません")
    
    print("\n🌐 次のステップ:")
    print("1. 生成されたHTMLファイルを確認")
    print("2. GitHub Actions で deploy-to-public ワークフローを手動実行")
    print("3. https://awano27.github.io/daily-ai-news-pages/ で結果確認")
    print()
    print("🔗 GitHub Actions URL:")
    print("  https://github.com/awano27/daily-ai-news/actions")

if __name__ == "__main__":
    main()