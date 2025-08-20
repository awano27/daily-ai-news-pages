#!/usr/bin/env python3
import subprocess
import os

os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

def run_git_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=60)
        print(f"{'✅' if result.returncode == 0 else '⚠️'} {cmd[:50]}...")
        if result.stdout:
            print(f"  {result.stdout.strip()[:100]}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ {cmd[:50]}... - {e}")
        return False

print("🚀 GitHub Pages分離デプロイワークフローをプッシュ中...")

commands = [
    "git fetch origin",
    "git pull origin main --no-edit", 
    "git add .github/workflows/deploy-to-public.yml setup-public-repo.md",
    'git commit -m "feat: Add workflow to deploy to public GitHub Pages repository"',
    "git push origin main"
]

success = 0
for cmd in commands:
    if run_git_command(cmd):
        success += 1

if success >= 4:
    print("\n✅ デプロイワークフローがGitHubにプッシュされました！")
    print("\n📝 次のステップ:")
    print("1. GitHubでPersonal Access Tokenを作成")
    print("   https://github.com/settings/tokens")
    print("2. daily-ai-newsリポジトリのSecretsにPERSONAL_TOKENを追加")
    print("3. daily-ai-news-pagesという新しいPublicリポジトリを作成")
    print("4. 詳細はsetup-public-repo.mdを参照")
else:
    print(f"\n⚠️ 一部の操作が失敗しました ({success}/{len(commands)})")

input("Press Enter to exit...")