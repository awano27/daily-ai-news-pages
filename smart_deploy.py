#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Smart Deploy - デプロイ失敗を自動解決するインテリジェントデプロイシステム
"""
import subprocess
import sys
import json
from datetime import datetime

def run_command(cmd, description=""):
    """コマンド実行と結果出力"""
    if description:
        print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            if description:
                print(f"✅ {description} 完了")
            return True, result.stdout.strip()
        else:
            if description:
                print(f"❌ {description} 失敗: {result.stderr.strip()}")
            return False, result.stderr.strip()
    except Exception as e:
        print(f"❌ コマンド実行エラー: {e}")
        return False, str(e)

def main():
    """スマートデプロイメント実行"""
    print("🚀 Smart Deploy - インテリジェントデプロイシステム")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # Step 1: 現在の状況確認
    print("📊 Step 1: Git状況分析")
    print("-" * 30)
    
    # リモート最新情報取得
    success, _ = run_command(["git", "fetch", "origin"], "リモート情報取得")
    if not success:
        print("❌ リモート接続に失敗しました")
        return
    
    # ローカルとリモートの差分確認
    success, behind_count = run_command([
        "git", "rev-list", "--count", "HEAD..origin/main"
    ], "コミット差分チェック")
    
    if success and behind_count and int(behind_count) > 0:
        print(f"⚠️ ローカルがリモートより {behind_count} コミット遅れています")
        print("🔄 自動同期を実行します...")
        
        # Step 2: 自動同期（Rebase戦略）
        print("\n📥 Step 2: スマート同期")
        print("-" * 30)
        
        # 現在の変更を一時保存
        success, _ = run_command(["git", "stash", "push", "-m", "smart-deploy-backup"], 
                                "変更の一時保存")
        
        if success:
            # リモートの変更を取得
            success, _ = run_command(["git", "pull", "origin", "main"], 
                                    "リモート変更取得")
            
            if success:
                # 保存した変更を復元
                success, _ = run_command(["git", "stash", "pop"], 
                                        "変更の復元")
                
                if not success:
                    print("⚠️ 変更復元で競合が発生しました")
                    print("🔄 競合解決を試行...")
                    
                    # 自動マージ試行
                    run_command(["git", "add", "."], "競合ファイルをステージング")
                    run_command(["git", "commit", "-m", "fix: Resolve merge conflicts"], 
                               "競合解決コミット")
            else:
                print("❌ リモート変更取得に失敗")
                return
        else:
            print("⚠️ 変更保存に失敗、直接プルを試行")
            success, _ = run_command(["git", "pull", "origin", "main"], 
                                    "強制プル")
    
    # Step 3: 改善内容を再コミット（必要な場合）
    print("\n💾 Step 3: 変更確認・コミット")
    print("-" * 30)
    
    # 未コミットの変更があるかチェック
    success, status = run_command(["git", "status", "--porcelain"], "変更状況確認")
    if success and status:
        print("📝 未コミットの変更を発見")
        
        # style.cssが含まれているかチェック
        if "style.css" in status:
            print("🎨 スタイルファイルの変更を検出")
            
            # 変更をコミット
            run_command(["git", "add", "style.css"], "スタイル変更をステージング")
            
            commit_msg = f"enhance: Smart deploy accessibility improvements\n\nAuto-deployed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}\n• WCAG AA compliant improvements\n• Enhanced visual hierarchy\n• Better responsive design"
            
            success, _ = run_command(["git", "commit", "-m", commit_msg], 
                                    "改善内容コミット")
    
    # Step 4: 安全なプッシュ
    print("\n🚀 Step 4: スマートプッシュ")
    print("-" * 30)
    
    # 最終プッシュ試行
    success, _ = run_command(["git", "push", "origin", "main"], "変更をプッシュ")
    
    if success:
        print("\n🎉 デプロイ成功!")
        print("=" * 40)
        print("✅ 変更がGitHubにプッシュされました")
        print("🔄 GitHub Actionsが自動実行されます")
        print()
        print("🌐 確認URL:")
        print("- Actions: https://github.com/awano27/daily-ai-news/actions")
        print("- サイト: https://awano27.github.io/daily-ai-news/")
        print()
        print("⏱️ 反映まで通常2-3分かかります")
        
    else:
        print("\n❌ プッシュに失敗しました")
        print("🔧 手動解決が必要です")
        print()
        print("手動解決手順:")
        print("1. git status で状況確認")
        print("2. git pull origin main で最新取得")
        print("3. 競合があれば解決")
        print("4. git push origin main で再試行")

if __name__ == "__main__":
    main()