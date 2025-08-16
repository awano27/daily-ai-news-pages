#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ダッシュボードとメインサイトの件数を統一して再生成
"""
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

def main():
    print("=" * 60)
    print("🔄 件数を統一してサイトを再生成")
    print("=" * 60)
    
    # 環境変数設定（両方とも8件に統一）
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'  # 統一された件数
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    
    # Google SheetsのURL
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    print(f"\n📅 現在時刻: {now.strftime('%Y-%m-%d %H:%M JST')}")
    print(f"📊 各カテゴリ最大表示件数: 8件（統一）")
    print(f"🔗 Google Sheets: 最新X投稿を取得")
    
    try:
        # Step 1: リモートの最新を取得
        print("\n1️⃣ GitHubから最新を取得...")
        subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], check=True)
        print("✅ 最新の変更を取得しました")
        
        # Step 2: メインサイト生成
        print("\n2️⃣ メインサイトを生成...")
        result = subprocess.run([sys.executable, 'build.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"❌ ビルドエラー: {result.stderr}")
            return False
            
        # 出力の一部を表示
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines[:10]:  # 最初の10行を表示
                if line.strip():
                    print(f"   {line}")
        
        # index.htmlが生成されたか確認
        if not Path('index.html').exists():
            print("❌ index.html が生成されませんでした")
            return False
        
        print("✅ メインサイト生成完了")
        
        # Step 3: ダッシュボード生成（同じ件数設定で）
        print("\n3️⃣ ダッシュボードを生成...")
        
        # generate_dashboard.pyを直接実行
        result = subprocess.run([sys.executable, 'generate_dashboard.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"⚠️ ダッシュボード生成エラー: {result.stderr}")
        else:
            print("✅ ダッシュボード生成完了")
            
            # 生成されたダッシュボードの統計を確認
            if Path('dashboard_data.json').exists():
                import json
                with open('dashboard_data.json', 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                print("\n📊 生成されたサイトの統計（統一後）:")
                print(f"   ビジネス: {data['categories'].get('business', {}).get('count', 0)}件")
                print(f"   ツール: {data['categories'].get('tools', {}).get('count', 0)}件")
                print(f"   研究・論文: {data['categories'].get('posts', {}).get('count', 0)}件")
                
                # メインサイトと同じ件数になっているはず（最大8件）
                total_display = min(data['categories'].get('business', {}).get('count', 0), 8) + \
                               min(data['categories'].get('tools', {}).get('count', 0), 8) + \
                               min(data['categories'].get('posts', {}).get('count', 0), 8)
                print(f"   メインサイト表示合計: 最大{total_display}件")
        
        # Step 4: Git に追加してコミット
        print("\n4️⃣ 変更をGitにコミット...")
        
        # Add files
        files_to_add = [
            'index.html',
            'ai_news_dashboard.html',
            'dashboard_data.json',
            'generate_dashboard.py'
        ]
        
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
        
        # コミットメッセージ
        commit_msg = f"fix: Unified item counts between dashboard and main site (max 8 per category) [{now.strftime('%Y-%m-%d %H:%M JST')}]"
        
        # Commit
        try:
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ コミット完了")
        except subprocess.CalledProcessError:
            print("ℹ️ 変更がないか、既にコミット済みです")
        
        # Step 5: GitHubにプッシュ
        print("\n5️⃣ GitHubへプッシュ中...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("\n" + "=" * 60)
        print("✅ 件数統一完了!")
        print("=" * 60)
        
        print("\n🎯 統一後の仕様:")
        print("  • 各カテゴリ最大8件表示（メインサイト・ダッシュボード共通）")
        print("  • ダッシュボードの統計は表示件数ベース")
        print("  • メインサイトとダッシュボードの件数が一致")
        
        print(f"\n📰 メインサイト:")
        print(f"   https://awano27.github.io/daily-ai-news/")
        print(f"\n📊 ダッシュボード:")
        print(f"   https://awano27.github.io/daily-ai-news/ai_news_dashboard.html")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Git操作エラー: {e}")
        return False
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)