#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
実際のCSVデータでXポストを含むサイトを再構築
"""
import os
import subprocess

def rebuild_site_with_real_x_posts():
    """実際のCSVデータを使ってサイトを再構築"""
    print("🔄 実際のXポストでサイト再構築開始")
    print("=" * 50)
    
    # 環境変数を設定
    env_vars = {
        'TRANSLATE_TO_JA': '1',
        'TRANSLATE_ENGINE': 'google',
        'HOURS_LOOKBACK': '48',  # 48時間分のデータ
        'MAX_ITEMS_PER_CATEGORY': '8',
        'X_POSTS_CSV': 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
    }
    
    for key, value in env_vars.items():
        os.environ[key] = value
        print(f"✓ {key}={value}")
    
    try:
        # 現在のindex.htmlをバックアップ
        print("\n📁 現在のHTMLをバックアップ中...")
        if os.path.exists('index.html'):
            subprocess.run(['copy', 'index.html', 'index_backup.html'], shell=True)
        
        # build.pyを実行してサイトを再生成
        print("\n🔧 build.pyでサイト再生成中...")
        result = subprocess.run(['python', 'build.py'], 
                              capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("✅ build.py実行成功")
            print("--- ビルドログ（最後の20行）---")
            print('\n'.join(result.stdout.split('\n')[-20:]))
        else:
            print(f"❌ build.py実行エラー: {result.stderr}")
            
        # 新しいHTMLにXポストが含まれているかチェック
        if os.path.exists('index.html'):
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Xポストの存在確認
            x_post_indicators = [
                'X / SNS',
                'Xポスト',
                'x.com/',
                'twitter.com/'
            ]
            
            found_x_posts = []
            for indicator in x_post_indicators:
                count = content.count(indicator)
                if count > 0:
                    found_x_posts.append(f"{indicator}: {count}回")
            
            print(f"\n📊 Xポスト確認結果:")
            if found_x_posts:
                print("✅ Xポストが検出されました:")
                for found in found_x_posts:
                    print(f"   - {found}")
            else:
                print("❌ Xポストが検出されませんでした")
            
            # 実際のXポストURLを抽出
            import re
            x_urls = re.findall(r'href="(https://(?:x\.com|twitter\.com)/[^"]+)"', content)
            if x_urls:
                print(f"\n🔗 検出されたXポストURL（最初の3つ）:")
                for i, url in enumerate(x_urls[:3], 1):
                    print(f"   {i}. {url}")
            
        # Gitに変更をコミット
        print(f"\n📤 変更をGitにコミット中...")
        git_commands = [
            ['git', 'add', 'index.html'],
            ['git', 'commit', '-m', 'rebuild: Generate site with actual X posts from CSV'],
            ['git', 'push', 'origin', 'main']
        ]
        
        for cmd in git_commands:
            try:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                if result.returncode == 0:
                    print(f"✅ {' '.join(cmd)} 成功")
                else:
                    print(f"⚠️ {' '.join(cmd)} エラー: {result.stderr.strip()}")
            except subprocess.TimeoutExpired:
                print(f"⏰ {' '.join(cmd)} タイムアウト")
                
        print(f"\n🎉 サイト再構築完了！")
        print(f"📍 数分後に以下で確認:")
        print(f"   https://awano27.github.io/daily-ai-news/")
        print(f"   Postsタブで実際のCSVからのXポストが表示されます")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    rebuild_site_with_real_x_posts()