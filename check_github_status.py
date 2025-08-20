#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check GitHub Status - GitHub Actions と Pages の状況確認
"""
import subprocess
import os
from datetime import datetime

def run_command(cmd, description):
    """コマンドを実行して結果を表示"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        print(f"📊 結果 ({result.returncode}):")
        if result.stdout.strip():
            print(f"   出力: {result.stdout.strip()}")
        if result.stderr.strip():
            print(f"   エラー: {result.stderr.strip()}")
        return result.returncode == 0, result.stdout
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False, ""

def check_github_cli():
    """GitHub CLIが利用可能かチェック"""
    print("🔧 GitHub CLI 確認:")
    success, output = run_command("gh --version", "GitHub CLI バージョン確認")
    if success:
        print("✅ GitHub CLI が利用可能です")
        return True
    else:
        print("❌ GitHub CLI が見つかりません")
        print("💡 GitHub CLI をインストールしてください: https://cli.github.com/")
        return False

def check_workflow_status():
    """ワークフロー実行状況をチェック"""
    print("\n📊 GitHub Actions ワークフロー状況:")
    
    success, output = run_command("gh workflow list", "ワークフロー一覧取得")
    if success:
        print("✅ ワークフロー一覧取得成功")
    
    success, output = run_command("gh run list --limit 5", "最近の実行履歴")
    if success:
        print("✅ 実行履歴取得成功")
    
    print("\n🔄 手動でワークフローを実行してみます...")
    success, output = run_command("gh workflow run \"Enhanced Daily AI News (Full Pipeline)\"", "手動ワークフロー実行")
    if success:
        print("✅ ワークフロー実行開始")
    else:
        print("❌ ワークフロー実行失敗")

def check_pages_status():
    """GitHub Pages の状況確認"""
    print("\n🌐 GitHub Pages 状況確認:")
    success, output = run_command("gh api repos/{owner}/{repo}/pages", "Pages設定確認")
    if success:
        print("✅ GitHub Pages 設定確認")
    else:
        print("❌ GitHub Pages 設定に問題があります")

def create_immediate_build():
    """即座にビルドを実行するワークフロー作成"""
    print("\n🚀 即座にビルドを実行...")
    
    # 現在の時刻でビルド実行
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')
    
    workflow_content = f"""name: Immediate Build Test
on:
  workflow_dispatch:
    
jobs:
  immediate-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - name: Install dependencies
        run: |
          pip install feedparser pyyaml deep-translator==1.11.4 google-genai python-dotenv requests
      - name: Quick build test
        env:
          GEMINI_API_KEY: ${{{{ secrets.GEMINI_API_KEY }}}}
        run: |
          echo "🧪 Quick build test - {timestamp}"
          echo "GEMINI_API_KEY=${{{{ secrets.GEMINI_API_KEY }}}}" > .env
          echo "GEMINI_MODEL=gemini-2.5-flash" >> .env
          
          # Simple build test
          timeout 300 python build.py || echo "Build timeout"
          
          # Check results  
          ls -la *.html
          
      - name: Commit results
        run: |
          git config user.name "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          git add *.html || true
          git commit -m "🧪 Immediate build test - {timestamp} [skip ci]" || echo "No changes"
          git push
"""
    
    # ワークフローファイルを作成
    workflow_path = ".github/workflows/immediate-build.yml"
    try:
        with open(workflow_path, 'w', encoding='utf-8') as f:
            f.write(workflow_content)
        print(f"✅ 即座ビルドワークフロー作成: {workflow_path}")
        
        # Gitに追加してプッシュ
        run_command(f"git add {workflow_path}", "ワークフローファイルをステージング")
        run_command("git commit -m \"feat: Add immediate build workflow for testing\"", "ワークフローをコミット")
        run_command("git push", "ワークフローをプッシュ")
        
        print("🔄 ワークフローを手動実行中...")
        run_command("gh workflow run \"Immediate Build Test\"", "即座ビルド実行")
        
    except Exception as e:
        print(f"❌ ワークフロー作成エラー: {e}")

def main():
    """メイン診断処理"""
    print("🔍 GitHub Status Check - サイト更新問題の診断")
    print("=" * 60)
    
    print(f"📅 現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🌐 対象サイト: https://awano27.github.io/daily-ai-news-pages/")
    print()
    
    # GitHub CLI確認
    if not check_github_cli():
        print("\n❌ GitHub CLI なしでは詳細診断ができません")
        print("💡 代替手順:")
        print("1. GitHubのリポジトリページにアクセス")
        print("2. Actions タブでワークフローを確認") 
        print("3. Settings > Pages でGitHub Pages設定を確認")
        print("4. Settings > Secrets でGEMINI_API_KEY設定を確認")
        return
    
    # ワークフロー状況確認
    check_workflow_status()
    
    # Pages状況確認  
    check_pages_status()
    
    # 即座ビルド実行
    create_immediate_build()
    
    print("\n" + "=" * 60)
    print("📋 診断完了 - 次の手順:")
    print("1. GitHub Actions タブでワークフロー実行を確認")
    print("2. エラーがあればログを確認")
    print("3. Settings > Secrets でGEMINI_API_KEYを確認")
    print("4. Settings > Pages でソース設定を確認")
    print("5. 数分後にサイトの更新を再確認")
    
    print(f"\n🌐 サイト確認: https://awano27.github.io/daily-ai-news-pages/")
    print("🔄 ワークフロー確認: GitHub Actions タブ")

if __name__ == "__main__":
    main()