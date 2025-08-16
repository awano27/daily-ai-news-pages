#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Manual execution of auto_update_all.py components"""

import os
import sys
from datetime import datetime, timezone, timedelta

def main():
    print("=" * 60)
    print("🤖 Daily AI News 完全自動更新システム（手動実行）")
    print("=" * 60)
    
    # 環境設定
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    print("🔧 環境設定中...")
    print(f"📅 実行時刻: {now.strftime('%Y-%m-%d %H:%M JST')}")
    
    # 基本設定
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '20'
    
    # Google SheetsのCSV URL（X/Twitter投稿）
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    print("✅ 環境変数設定完了")
    print(f"  • 翻訳: 日本語")
    print(f"  • 取得期間: 過去24時間")
    print(f"  • 表示件数: 各カテゴリ20件")
    print(f"  • X投稿ソース: Google Sheets")
    
    try:
        print("\n📰 詳細ニュースページを更新中...")
        import build
        # Execute build process
        print("✅ build.py インポート成功")
        
        print("\n📊 ダッシュボードを更新中...")
        import generate_comprehensive_dashboard
        print("✅ generate_comprehensive_dashboard.py インポート成功")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        
    print("\n✅ 手動実行完了")

if __name__ == "__main__":
    main()