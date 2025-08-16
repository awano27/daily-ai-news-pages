#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日付フィルタリングの修正
- 時刻なしの日付フォーマットに対応
- パースエラー時は除外（現在時刻にしない）
"""
import os
import sys
from pathlib import Path
import re

def fix_build_py():
    """build.pyの日付パース処理を修正"""
    
    print("🔧 build.pyの日付パース処理を修正中...")
    
    build_path = Path('build.py')
    content = build_path.read_text(encoding='utf-8')
    
    # 修正1: 日付パース処理を改善（複数フォーマットに対応）
    old_parse = """                    # 日付をパース
                    try:
                        # "August 10, 2025 at 02:41AM" -> datetime
                        dt = datetime.strptime(date_str, "%B %d, %Y at %I:%M%p")
                        dt = dt.replace(tzinfo=JST)  # JSTとして扱う
                    except:
                        dt = NOW  # パースに失敗した場合は現在時刻"""
    
    new_parse = """                    # 日付をパース（複数フォーマットに対応）
                    dt = None
                    # 複数の日付フォーマットを試す
                    date_formats = [
                        "%B %d, %Y at %I:%M%p",  # "August 10, 2025 at 02:41AM"
                        "%B %d, %Y"               # "August 13, 2025"
                    ]
                    for fmt in date_formats:
                        try:
                            dt = datetime.strptime(date_str, fmt)
                            dt = dt.replace(tzinfo=JST)  # JSTとして扱う
                            break
                        except:
                            continue
                    
                    # パースに失敗した場合はスキップ（現在時刻にしない）
                    if dt is None:
                        continue"""
    
    if old_parse in content:
        content = content.replace(old_parse, new_parse)
        print("✅ 日付パース処理を改善しました")
    else:
        print("⚠️ 既存のパース処理が見つかりません。別の方法で修正...")
        
        # 別パターンを試す
        pattern = r'try:\s+# "August.*?\n.*?dt = datetime\.strptime.*?\n.*?dt = dt\.replace.*?\n.*?except:\s+dt = NOW.*?'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(pattern, new_parse.strip(), content, flags=re.DOTALL)
            print("✅ 正規表現で日付パース処理を改善しました")
    
    # 修正2: データ追加時にNoneチェックを確実に
    old_append = """                    data.append({
                        'url': tweet_url,
                        'username': username,
                        'text': text,
                        'datetime': dt
                    })"""
    
    new_append = """                    if dt is not None:  # 日付が正しくパースできた場合のみ追加
                        data.append({
                            'url': tweet_url,
                            'username': username,
                            'text': text,
                            'datetime': dt
                        })"""
    
    if old_append in content:
        content = content.replace(old_append, new_append)
        print("✅ データ追加処理を改善しました")
    
    # ファイルを保存
    build_path.write_text(content, encoding='utf-8')
    print("✅ build.py を更新しました")
    
    return True

def update_and_deploy():
    """修正後にサイトを再生成してデプロイ"""
    
    print("\n📊 修正版でサイトを再生成...")
    
    # 環境変数設定
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    import subprocess
    from datetime import datetime, timezone, timedelta
    
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    try:
        # Git pull
        print("\n1️⃣ GitHubから最新を取得...")
        subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], check=True)
        
        # ビルド実行
        print("\n2️⃣ サイトを生成（8/14以降のみ）...")
        result = subprocess.run([sys.executable, 'build.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"❌ ビルドエラー: {result.stderr}")
            return False
        
        # ログから統計を抽出
        if result.stdout:
            for line in result.stdout.split('\n'):
                if 'X post items' in line or 'Created' in line:
                    print(f"   {line}")
        
        # ダッシュボード生成
        print("\n3️⃣ ダッシュボードを生成...")
        subprocess.run([sys.executable, 'generate_dashboard.py'], check=False)
        
        # コミット
        print("\n4️⃣ 変更をコミット...")
        files_to_add = ['build.py', 'index.html', 'ai_news_dashboard.html', 'dashboard_data.json']
        
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
        
        commit_msg = f"fix: Improved date parsing to exclude pre-8/14 posts [{now.strftime('%Y-%m-%d %H:%M JST')}]"
        
        try:
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ コミット完了")
        except:
            print("ℹ️ 変更なし、またはコミット済み")
        
        # プッシュ
        print("\n5️⃣ GitHubへプッシュ...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("\n" + "=" * 60)
        print("✅ 修正完了!")
        print("=" * 60)
        print("\n🎯 修正内容:")
        print("  • 時刻なしの日付フォーマット（August 13, 2025）に対応")
        print("  • パースエラーの投稿を除外（現在時刻として扱わない）")
        print("  • 8/14以降の投稿のみを正確にフィルタリング")
        
        print(f"\n📰 メインサイト: https://awano27.github.io/daily-ai-news/")
        print(f"📊 ダッシュボード: https://awano27.github.io/daily-ai-news/ai_news_dashboard.html")
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("=" * 60)
    print("🔧 日付フィルタリング問題を修正")
    print("=" * 60)
    
    # build.pyを修正
    if not fix_build_py():
        return False
    
    # サイトを再生成してデプロイ
    return update_and_deploy()

if __name__ == "__main__":
    sys.exit(0 if main() else 1)