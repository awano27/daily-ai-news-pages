#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Workflow Error - GitHub Actions YAML構文エラー修正
"""
import subprocess
from datetime import datetime

def run_command(cmd, description):
    """コマンドを実行"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {description} - 成功")
            if result.stdout.strip():
                print(f"   {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - 失敗: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - エラー: {e}")
        return False

def main():
    """ワークフローエラー修正"""
    print("🔧 GitHub Actions Workflow Error Fix")
    print("=" * 50)
    print(f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    print("📝 修正内容:")
    print("- enhanced-daily-build.yml のYAML構文エラー修正")
    print("- 複数行コミットメッセージを単一行に変更")
    print()
    
    # Gitコマンド実行
    commands = [
        ("git add .github/workflows/enhanced-daily-build.yml", "修正済みワークフローをステージング"),
        ("git commit -m \"fix: GitHub Actions YAML syntax error on line 151\"", "修正をコミット"),
        ("git push origin main", "修正をプッシュ")
    ]
    
    for cmd, desc in commands:
        if not run_command(cmd, desc):
            print(f"⚠️ {desc} に失敗しましたが、続行します")
    
    print("\n" + "=" * 50)
    print("✅ ワークフローエラー修正完了!")
    print()
    print("📋 確認手順:")
    print("1. GitHub Actions タブでワークフローエラーが解消されたか確認")
    print("2. 手動でワークフローを実行してテスト")
    print("3. エラーがなければ定期実行を待つ")
    print()
    print("🌐 GitHub Actions: https://github.com/awano27/daily-ai-news-pages/actions")
    print("🔄 手動実行: Actions → Enhanced Daily AI News → Run workflow")

if __name__ == "__main__":
    main()