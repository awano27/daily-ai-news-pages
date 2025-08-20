#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix CSS Deployment - style.css 404問題を緊急修正
"""
import subprocess
import sys
from datetime import datetime

def run_command(cmd, description=""):
    """コマンド実行"""
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
        print(f"❌ エラー: {e}")
        return False, str(e)

def main():
    """CSS 404問題の緊急修正"""
    print("🚨 Fix CSS Deployment - style.css 404問題修正")
    print("=" * 60)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    print("🔍 問題分析:")
    print("- style.cssファイルは存在する")
    print("- GitHub ActionsがCSSファイルをコミットに含めていない")
    print("- HTMLはstyle.cssを参照しているが404エラー")
    print()
    
    print("🛠️ 修正内容:")
    print("- GitHub Actionsワークフローを更新")
    print("- style.cssを明示的にコミットに含める")
    print("- Digital.gov準拠デザインを正しくデプロイ")
    print()
    
    # ワークフロー修正をコミット
    print("📝 ワークフロー修正をコミット")
    print("-" * 30)
    
    success, _ = run_command([
        "git", "add", ".github/workflows/enhanced-daily-build.yml"
    ], "ワークフロー修正をステージング")
    
    if not success:
        print("❌ ステージングに失敗しました")
        return
    
    # コミット
    commit_msg = """fix: Include style.css in GitHub Actions deployment

🚨 URGENT CSS FIX:
- Added style.css to git add command in workflow
- Fixed 404 error preventing Digital.gov design from loading
- Ensures complete deployment of HTML + CSS + cache

🎯 Result: Digital.gov compliant design will now deploy correctly
📱 Restores beautiful, accessible UI/UX

Previous issue: GitHub Actions only committed *.html files
Solution: Explicitly include style.css in deployment"""

    success, _ = run_command([
        "git", "commit", "-m", commit_msg
    ], "CSS修正をコミット")
    
    if not success:
        print("❌ コミットに失敗しました")
        return
    
    # プッシュ
    success, _ = run_command([
        "git", "push", "origin", "main"
    ], "修正をプッシュ")
    
    if success:
        print("\n🎉 CSS 404問題修正完了!")
        print("=" * 40)
        print("✅ GitHub Actionsワークフローを修正")
        print("✅ style.cssが正しくデプロイされるように設定")
        print("✅ 次回の自動ビルドでデザインが復元")
        print()
        
        print("📋 次のステップ:")
        print("1. GitHub Actionsで手動実行または自動実行を待つ")
        print("2. https://awano27.github.io/daily-ai-news/ でデザイン復元を確認")
        print("3. Digital.gov準拠の美しいUIが表示されることを確認")
        print()
        
        print("🌐 確認URL:")
        print("- Actions: https://github.com/awano27/daily-ai-news/actions")
        print("- サイト: https://awano27.github.io/daily-ai-news/")
        print()
        
        print("⏱️ 修正反映:")
        print("- 次回のGitHub Actions実行時（自動または手動）")
        print("- または Enhanced workflow を手動実行")
        
    else:
        print("❌ プッシュに失敗しました")

if __name__ == "__main__":
    main()