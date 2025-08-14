#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
サイトを本日08:00時点の情報でアップデート
Google SheetsからSNS/X最新情報を取得
"""
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

def main():
    print("=" * 60)
    print("🌅 AIニュースサイトを本日08:00の情報でアップデート")
    print("=" * 60)
    
    # 環境変数設定
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    # 本日08:00 JSTを基準に24時間以内の記事を取得
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    
    # Google SheetsのURLを設定（最新のX投稿データ）
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    print(f"\n📅 現在時刻: {now.strftime('%Y-%m-%d %H:%M JST')}")
    print(f"📊 取得期間: 過去24時間以内の記事")
    print(f"🔗 Google Sheets: {GOOGLE_SHEETS_URL[:60]}...")
    
    try:
        # Step 1: リモートの最新を取得
        print("\n1️⃣ GitHubから最新を取得...")
        subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], check=True)
        print("✅ 最新の変更を取得しました")
        
        # Step 2: サイト生成
        print("\n2️⃣ サイトを生成中...")
        print("   - RSS フィードから記事を取得")
        print("   - Google Sheetsから最新のX投稿を取得")
        print("   - 日本語に翻訳")
        print("   - HTMLを生成")
        
        result = subprocess.run([sys.executable, 'build.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"❌ ビルドエラー: {result.stderr}")
            return False
            
        # 出力を表示
        if result.stdout:
            for line in result.stdout.split('\n')[:20]:  # 最初の20行を表示
                if line.strip():
                    print(f"   {line}")
        
        # Step 3: index.htmlが生成されたか確認
        if not Path('index.html').exists():
            print("❌ index.html が生成されませんでした")
            return False
        
        # ファイルサイズチェック
        file_size = Path('index.html').stat().st_size
        print(f"\n✅ index.html 生成完了 ({file_size:,} bytes)")
        
        # Step 4: 更新時刻を確認
        with open('index.html', 'r', encoding='utf-8') as f:
            content = f.read()
            if '最終更新:' in content:
                import re
                match = re.search(r'最終更新: ([^<]+)', content)
                if match:
                    print(f"📝 最終更新時刻: {match.group(1)}")
        
        # Step 5: Git に追加してコミット
        print("\n3️⃣ 変更をGitにコミット...")
        
        # Add files
        subprocess.run(['git', 'add', 'index.html'], check=True)
        
        # コミットメッセージ
        commit_msg = f"chore: update index.html for {now.strftime('%Y-%m-%d %H:%M JST')} [skip ci]"
        
        # Commit
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        print("✅ コミット完了")
        
        # Step 6: GitHubにプッシュ
        print("\n4️⃣ GitHubへプッシュ中...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("\n" + "=" * 60)
        print("✅ アップデート完了!")
        print("=" * 60)
        
        print(f"\n📰 AIニュースサイトが更新されました:")
        print(f"   https://awano27.github.io/daily-ai-news/")
        print(f"\n📊 ダッシュボード:")
        print(f"   https://awano27.github.io/daily-ai-news/ai_news_dashboard.html")
        print(f"\n⏰ 更新基準時刻: 本日 08:00 JST")
        print(f"📡 Google Sheetsから最新のX投稿を取得済み")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ エラーが発生しました: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)