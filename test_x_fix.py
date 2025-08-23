#!/usr/bin/env python3
"""
Test the fixed X posts functionality
"""
import os
import subprocess
import sys

# 環境変数設定
os.environ['TRANSLATE_TO_JA'] = '1'
os.environ['TRANSLATE_ENGINE'] = 'google' 
os.environ['HOURS_LOOKBACK'] = '48'
os.environ['MAX_ITEMS_PER_CATEGORY'] = '25'
os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'

def run_build():
    """サイトを再ビルドしてXポストをテスト"""
    print("🔨 サイトを再ビルド中...")
    
    try:
        # build_simple_ranking.pyを実行
        result = subprocess.run([
            sys.executable, 'build_simple_ranking.py'
        ], capture_output=True, text=True, timeout=300)
        
        print("STDOUT:")
        print(result.stdout)
        print("\nSTDERR:")
        print(result.stderr)
        
        if result.returncode == 0:
            print("✅ ビルド成功!")
            
            # index.htmlでXポストをチェック
            if os.path.exists('index.html'):
                with open('index.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if 'X (Twitter)' in content or 'twitter.com' in content or '@' in content:
                    print("✅ Xポストがindex.htmlに含まれています")
                    
                    # Xポストの数をカウント
                    x_count = content.count('X (Twitter)')
                    twitter_count = content.count('twitter.com')
                    print(f"X (Twitter) mentions: {x_count}")
                    print(f"twitter.com links: {twitter_count}")
                    
                else:
                    print("⚠️ index.htmlにXポストが見つかりません")
            else:
                print("❌ index.htmlが生成されませんでした")
        else:
            print(f"❌ ビルド失敗: {result.returncode}")
            
    except subprocess.TimeoutExpired:
        print("❌ ビルドがタイムアウトしました")
    except Exception as e:
        print(f"❌ エラー: {e}")

if __name__ == "__main__":
    print("🧪 Xポスト修正テスト開始")
    print("=" * 50)
    run_build()
    print("=" * 50)
    print("🏁 テスト完了")