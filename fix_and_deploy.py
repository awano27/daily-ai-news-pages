#!/usr/bin/env python3
"""
Git同期問題を解決してデプロイ
"""
import subprocess
import os

def fix_and_deploy():
    os.chdir(r"C:\Users\yoshitaka\daily-ai-news")
    
    print("🔧 Git同期問題を解決してデプロイ中...")
    
    try:
        # Pull with merge
        print("📥 リモートの変更をプル...")
        subprocess.run(["git", "pull", "origin", "main", "--no-rebase"], check=True)
        
        # Check if there are changes to commit
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        
        if result.stdout.strip():
            print("📝 変更をコミット...")
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", "fix: Gemini Web Fetcher 403 error resolution"], check=True)
        
        # Push
        print("📤 GitHubにプッシュ...")
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("✅ GitHub Pagesにデプロイ完了!")
        print("🔗 https://awano27.github.io/daily-ai-news/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ エラー: {e}")
        print("\n🔧 手動解決:")
        print("git pull origin main --no-rebase")
        print("git push origin main")
        return False
    
    return True

if __name__ == "__main__":
    fix_and_deploy()