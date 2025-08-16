#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ビルドプロセスをテストして問題を診断
"""
import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path

def test_build():
    """ビルドプロセスをテストして詳細ログを出力"""
    
    print("=" * 60)
    print("🔧 メインサイトビルドプロセステスト")
    print("=" * 60)
    
    # 環境変数設定
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    print(f"📅 現在時刻: {now.strftime('%Y-%m-%d %H:%M JST')}")
    print(f"🔗 Google Sheets: {GOOGLE_SHEETS_URL}")
    print(f"🔧 環境変数:")
    print(f"   HOURS_LOOKBACK: {os.environ['HOURS_LOOKBACK']}")
    print(f"   MAX_ITEMS_PER_CATEGORY: {os.environ['MAX_ITEMS_PER_CATEGORY']}")
    print(f"   TRANSLATE_TO_JA: {os.environ['TRANSLATE_TO_JA']}")
    
    # 既存のindex.htmlの情報
    index_path = Path('index.html')
    if index_path.exists():
        stat = index_path.stat()
        mod_time = datetime.fromtimestamp(stat.st_mtime)
        print(f"\n📄 既存のindex.html:")
        print(f"   サイズ: {stat.st_size:,} bytes")
        print(f"   更新日時: {mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
    else:
        print(f"\n❌ index.html が存在しません")
    
    try:
        # build.pyを実行
        print(f"\n🚀 build.py を実行中...")
        result = subprocess.run([sys.executable, 'build.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        print(f"\n📊 実行結果:")
        print(f"   終了コード: {result.returncode}")
        
        if result.stdout:
            print(f"\n✅ 標準出力:")
            for line in result.stdout.split('\n'):
                if line.strip():
                    print(f"   {line}")
        
        if result.stderr:
            print(f"\n❌ エラー出力:")
            for line in result.stderr.split('\n'):
                if line.strip():
                    print(f"   {line}")
        
        # 新しいindex.htmlを確認
        if index_path.exists():
            new_stat = index_path.stat()
            new_mod_time = datetime.fromtimestamp(new_stat.st_mtime)
            print(f"\n📄 更新後のindex.html:")
            print(f"   サイズ: {new_stat.st_size:,} bytes")
            print(f"   更新日時: {new_mod_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # ファイル内容の一部を確認
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # 最終更新時刻を抽出
            import re
            match = re.search(r'最終更新：([^<]+)', content)
            if match:
                print(f"   HTML内の最終更新: {match.group(1)}")
            
            # カテゴリ別件数を抽出
            business_match = re.search(r'<div class="kpi-value">(\d+)件</div>\s*<div class="kpi-label">ビジネスニュース</div>', content)
            tools_match = re.search(r'<div class="kpi-value">(\d+)件</div>\s*<div class="kpi-label">ツールニュース</div>', content)
            posts_match = re.search(r'<div class="kpi-value">(\d+)件</div>\s*<div class="kpi-label">SNS/論文ポスト</div>', content)
            
            if business_match and tools_match and posts_match:
                print(f"   カテゴリ別件数:")
                print(f"     ビジネス: {business_match.group(1)}件")
                print(f"     ツール: {tools_match.group(1)}件")
                print(f"     SNS/論文: {posts_match.group(1)}件")
        
        # X投稿の処理状況を確認
        x_post_lines = [line for line in result.stdout.split('\n') if 'X post' in line or 'posts from CSV' in line]
        if x_post_lines:
            print(f"\n📱 X投稿処理:")
            for line in x_post_lines:
                print(f"   {line}")
        
        if result.returncode == 0:
            print(f"\n✅ ビルド成功!")
            return True
        else:
            print(f"\n❌ ビルド失敗 (終了コード: {result.returncode})")
            return False
            
    except Exception as e:
        print(f"\n❌ 実行エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    return test_build()

if __name__ == "__main__":
    sys.exit(0 if main() else 1)