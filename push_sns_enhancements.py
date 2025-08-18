#!/usr/bin/env python3
"""
SNS強化ダッシュボードをGitHubにプッシュ
"""
import subprocess
import os

os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

def run_cmd(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        print(f"{'✅' if result.returncode == 0 else '⚠️'} {cmd[:50]}...")
        if result.stdout:
            print(f"  {result.stdout.strip()[:100]}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {cmd[:50]}... - {e}")
        return False

print("🚀 SNS強化ダッシュボードをGitHubにプッシュ中...")

# Git操作
commands = [
    "git fetch origin",
    "git pull origin main --no-edit",
    "git add generate_sns_enhanced_dashboard.py run_sns_enhanced.bat fetch_x_posts.py",
    'git commit -m "feat: Add SNS enhanced dashboard with Google Sheets integration"',
    "git push origin main"
]

success_count = sum(1 for cmd in commands if run_cmd(cmd))

if success_count >= 4:
    print(f"\n✅ SNS強化ダッシュボードがGitHubにプッシュされました！")
    print("📊 Google Sheets連携によるX投稿データ取得機能が追加されました")
else:
    print(f"\n⚠️ 一部の操作が失敗しました ({success_count}/{len(commands)})")

input("Press Enter to exit...")