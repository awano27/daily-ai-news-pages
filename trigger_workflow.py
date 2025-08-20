#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trigger GitHub Workflow - Enhanced AI News更新
"""
import requests
import json
import subprocess
import sys
from datetime import datetime

def trigger_via_api():
    """GitHub API経由でワークフロー実行"""
    print("🚀 GitHub API経由でEnhanced Daily Buildを実行...")
    
    # まずGitHubにプッシュして最新状態にする
    print("\n📤 現在の変更をGitHubにプッシュ...")
    
    try:
        # Git設定
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], capture_output=True)
        subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], capture_output=True)
        
        # ダミーファイル作成してコミット
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        trigger_file = f"trigger_{timestamp}.txt"
        
        with open(trigger_file, 'w') as f:
            f.write(f"Workflow trigger at {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n")
            f.write("Purpose: Update Enhanced AI News with latest content\n")
        
        subprocess.run(['git', 'add', trigger_file], capture_output=True)
        
        commit_msg = f"🔄 Trigger Enhanced Daily Build - {datetime.now().strftime('%Y-%m-%d %H:%M JST')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True)
        
        # プッシュ
        result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ プッシュ成功 - ワークフローがトリガーされます")
            
            # トリガーファイル削除（次回のため）
            import os
            os.remove(trigger_file)
            subprocess.run(['git', 'rm', trigger_file], capture_output=True)
            subprocess.run(['git', 'commit', '-m', f'cleanup: Remove trigger file {trigger_file}'], capture_output=True)
            subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True)
            
            return True
        else:
            print(f"❌ プッシュ失敗: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def check_workflow_status():
    """ワークフロー状態確認"""
    print("\n📊 ワークフロー状態確認...")
    
    try:
        result = subprocess.run(
            ['gh', 'run', 'list', '--workflow=enhanced-daily-build.yml', '--limit=1'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0 and result.stdout:
            print("最新のワークフロー実行:")
            print(result.stdout)
        else:
            print("GitHub CLI未インストールまたはエラー")
            
    except:
        pass

def main():
    """メイン処理"""
    print("=" * 60)
    print("🤖 Enhanced AI News - GitHub Actions経由更新")
    print("=" * 60)
    print(f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # ワークフロートリガー
    if trigger_via_api():
        print("\n" + "=" * 60)
        print("✅ ワークフロートリガー成功！")
        print("=" * 60)
        
        print("\n📋 次のステップ:")
        print("1. GitHub Actionsページで実行状況を確認")
        print("   https://github.com/awano27/daily-ai-news/actions")
        print()
        print("2. 約3-5分後にサイトが更新されます")
        print("   https://awano27.github.io/daily-ai-news-pages/")
        print()
        print("3. Enhanced Daily Buildワークフローが:")
        print("   - 最新48時間のAIニュース収集")
        print("   - Gemini URL Contextで要約生成")
        print("   - X投稿の重複排除と300字要約")
        print("   - HTMLファイル生成とデプロイ")
        
        # 状態確認
        check_workflow_status()
        
    else:
        print("\n❌ ワークフロートリガー失敗")
        print("手動でGitHub Actionsから実行してください:")
        print("1. https://github.com/awano27/daily-ai-news/actions")
        print("2. 'Enhanced Daily AI News'ワークフロー選択")
        print("3. 'Run workflow'ボタンクリック")

if __name__ == "__main__":
    main()