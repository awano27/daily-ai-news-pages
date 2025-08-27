#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Pagesを強制更新するスクリプト
"""
import subprocess
import os
from datetime import datetime

def force_github_pages_update():
    """GitHub Pagesを強制的に更新"""
    print("🚀 GitHub Pages強制更新開始")
    print("=" * 50)
    
    try:
        # 現在の状況を確認
        print("📊 現在の状況確認:")
        
        # Gitブランチ確認
        result = subprocess.run(['git', 'branch', '-a'], capture_output=True, text=True)
        print(f"ブランチ一覧:\n{result.stdout}")
        
        # リモート確認
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        print(f"リモートリポジトリ:\n{result.stdout}")
        
        # 現在のブランチ
        result = subprocess.run(['git', 'branch', '--show-current'], capture_output=True, text=True)
        current_branch = result.stdout.strip()
        print(f"現在のブランチ: {current_branch}")
        
        # HTMLファイルの存在確認
        if os.path.exists('index.html'):
            with open('index.html', 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Xポスト確認
            if 'X / SNS (CSV実データ)' in content:
                print("✅ 更新されたXポストを確認")
            else:
                print("❌ Xポストが見つかりません")
            
            print(f"HTMLファイルサイズ: {len(content)} 文字")
        
        # 1. 現在のブランチに全てコミット
        print("\n📝 変更をコミット中...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"force: Update site with real X posts - {timestamp}"
        
        result = subprocess.run(['git', 'commit', '-m', commit_msg], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ コミット成功")
        else:
            print(f"⚠️ コミット: {result.stderr}")
        
        # 2. 現在のブランチにプッシュ
        print("📤 現在のブランチにプッシュ中...")
        result = subprocess.run(['git', 'push', 'origin', current_branch], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ プッシュ成功")
        else:
            print(f"❌ プッシュエラー: {result.stderr}")
        
        # 3. gh-pagesブランチが存在するかチェック
        print("\n🔍 gh-pagesブランチ確認中...")
        result = subprocess.run(['git', 'show-branch', 'origin/gh-pages'], 
                              capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ gh-pagesブランチ存在")
            
            # gh-pagesブランチに切り替えてマージ
            print("🔄 gh-pagesブランチに更新を反映...")
            subprocess.run(['git', 'checkout', 'gh-pages'], check=True)
            subprocess.run(['git', 'merge', current_branch], check=True)
            subprocess.run(['git', 'push', 'origin', 'gh-pages'], check=True)
            subprocess.run(['git', 'checkout', current_branch], check=True)
            print("✅ gh-pagesブランチ更新完了")
        else:
            print("⚠️ gh-pagesブランチが存在しません")
        
        # 4. 空のコミットでGitHub Actionsをトリガー
        print("\n⚡ GitHub Actionsトリガー用空コミット...")
        empty_commit_msg = f"trigger: Force GitHub Actions - {timestamp}"
        subprocess.run(['git', 'commit', '--allow-empty', '-m', empty_commit_msg], check=True)
        subprocess.run(['git', 'push', 'origin', current_branch], check=True)
        print("✅ GitHub Actionsトリガー完了")
        
        print("\n🎉 GitHub Pages強制更新完了！")
        print("📍 確認手順:")
        print("1. GitHub.com → リポジトリ → Actions タブで実行状況確認")
        print("2. Settings → Pages でデプロイ設定確認")
        print("3. 5-10分後にサイトをハードリフレッシュ (Ctrl+Shift+R)")
        print("4. https://awano27.github.io/daily-ai-news/")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    force_github_pages_update()