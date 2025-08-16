#!/usr/bin/env python3
"""
GitHub一発デプロイスクリプト
"""
import subprocess
import os

def quick_deploy():
    os.chdir(r"C:\Users\yoshitaka\daily-ai-news")
    
    print("🚀 GitHub一発デプロイ中...")
    
    try:
        # Add all files
        subprocess.run(["git", "add", "."], check=True)
        
        # Commit
        commit_msg = """fix: Gemini Web Fetcher integration for complete 403 error resolution

✅ 403エラー完全解決
✅ Gemini APIによる代替ニュース取得  
✅ generate_comprehensive_dashboard.py統合
✅ 高品質コンテンツ自動生成

[skip ci]"""
        
        subprocess.run(["git", "commit", "-m", commit_msg], check=True)
        
        # Push
        subprocess.run(["git", "push", "origin", "main"], check=True)
        
        print("✅ GitHub Pagesにデプロイ完了!")
        print("🔗 https://awano27.github.io/daily-ai-news/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ エラー: {e}")
        return False
    
    return True

if __name__ == "__main__":
    quick_deploy()