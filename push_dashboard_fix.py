#!/usr/bin/env python3
import subprocess
import os

os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

def run_git_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        print(f"{'✅' if result.returncode == 0 else '⚠️'} {cmd[:40]}...")
        if result.stdout:
            print(f"  {result.stdout.strip()[:100]}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {cmd[:40]}... - {e}")
        return False

print("🚀 総合ダッシュボードの「注目の投稿」修正をプッシュ中...")

commands = [
    "git fetch origin",
    "git pull origin main --no-edit", 
    "git add generate_comprehensive_dashboard.py",
    'git commit -m "fix: Resolve featured posts not found issue - Add fallback processing when Gemini API fails - Lower quality threshold for better post selection"',
    "git push origin main"
]

success = 0
for cmd in commands:
    if run_git_command(cmd):
        success += 1

if success >= 4:
    print("\n✅ 「注目の投稿が見つかりませんでした」の修正が完了しました！")
    print("📋 次のGitHub Actions実行で注目の投稿が表示されます")
else:
    print(f"\n⚠️ 一部の操作が失敗しました ({success}/{len(commands)})")

input("Press Enter to exit...")