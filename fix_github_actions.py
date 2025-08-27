#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Actions の修正スクリプト
"""
import os
import subprocess

def fix_github_actions():
    """GitHub Actionsの問題を修正"""
    print("🔧 GitHub Actions修正開始")
    print("=" * 40)
    
    try:
        # 現在のブランチを確認
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True)
        current_branch = result.stdout.strip()
        print(f"現在のブランチ: {current_branch}")
        
        # リモートリポジトリを確認
        result = subprocess.run(['git', 'remote', '-v'], 
                              capture_output=True, text=True)
        remotes = result.stdout.strip()
        print(f"リモートリポジトリ:\n{remotes}")
        
        # GitHub Actionsワークフローを修正
        workflow_file = '.github/workflows/enhanced-daily-build.yml'
        if os.path.exists(workflow_file):
            with open(workflow_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # mainブランチへのプッシュを現在のブランチに修正
            if current_branch != 'main':
                print(f"⚠️ ブランチ名を 'main' から '{current_branch}' に修正中...")
                content = content.replace('git push origin main', f'git push origin {current_branch}')
                content = content.replace('branches: [ main ]', f'branches: [ {current_branch} ]')
                
                with open(workflow_file, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"✅ ワークフロー修正完了")
        
        # より安全なGitHub Pagesデプロイ用のワークフローを作成
        safe_workflow = '''name: Safe GitHub Pages Deploy
on:
  push:
    branches: [ main, master, gh-pages ]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: true

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    
    steps:
      - name: Checkout
        uses: actions/checkout@v4
        
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"
          
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          
      - name: Build site
        env:
          TRANSLATE_TO_JA: "1"
          TRANSLATE_ENGINE: "google" 
          HOURS_LOOKBACK: "24"
          MAX_ITEMS_PER_CATEGORY: "8"
        run: |
          python build.py
          
      - name: Setup Pages
        uses: actions/configure-pages@v4
        
      - name: Upload artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
          
      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
'''
        
        # 安全なワークフローファイルを作成
        with open('.github/workflows/safe-pages-deploy.yml', 'w', encoding='utf-8') as f:
            f.write(safe_workflow)
        print("✅ 安全なデプロイワークフローを作成")
        
        # 変更をコミット
        subprocess.run(['git', 'add', '.github/workflows/'], check=True)
        subprocess.run(['git', 'commit', '-m', 'fix: Update GitHub Actions workflows for proper deployment'], check=True)
        subprocess.run(['git', 'push'], check=True)
        
        print("🎉 GitHub Actions修正完了！")
        print("\n次のステップ:")
        print("1. GitHubのActionsタブで新しいワークフローを確認")
        print("2. 手動で 'Safe GitHub Pages Deploy' を実行")
        print("3. 数分後にサイトが更新されることを確認")
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_github_actions()