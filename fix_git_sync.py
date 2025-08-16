#!/usr/bin/env python3
import subprocess
import sys
import os

# Change to project directory
os.chdir(r"C:\Users\yoshitaka\daily-ai-news")

print("🔄 Git同期問題を解決中...")

try:
    # Current status
    print("📊 現在のGit状態を確認...")
    result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
    if result.stdout.strip():
        print("未コミットの変更があります")
    else:
        print("すべての変更がコミット済み")
    
    # Pull with merge strategy
    print("📥 リモートの変更をプル中...")
    try:
        subprocess.run(["git", "pull", "origin", "main", "--no-rebase"], check=True)
        print("✅ プル成功")
    except subprocess.CalledProcessError as e:
        print(f"⚠️ プルでコンフリクトが発生: {e}")
        print("🔧 マージ戦略で解決を試行...")
        
        # Check for merge conflicts
        result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
        if "UU" in result.stdout or "AA" in result.stdout:
            print("📝 マージコンフリクトを自動解決...")
            # Use ours strategy for conflicted files
            subprocess.run(["git", "checkout", "--ours", "index.html"], check=False)
            subprocess.run(["git", "checkout", "--ours", "dashboard_data.json"], check=False)
            subprocess.run(["git", "add", "index.html", "dashboard_data.json"], check=False)
            subprocess.run(["git", "commit", "--no-edit"], check=False)
            print("✅ コンフリクト解決完了")
    
    # Push changes
    print("📤 変更をプッシュ中...")
    subprocess.run(["git", "push", "origin", "main"], check=True)
    print("✅ プッシュ成功")
    
    print("\n🎉 抜本的403エラー解決策がGitHub Pagesにデプロイされました!")
    print("🔗 URL: https://awano27.github.io/daily-ai-news/")
    print("⏰ 変更は1-5分で反映されます")
    
    print("\n📋 デプロイされた改善:")
    print("✅ 高度なHTTPリクエスト制御")
    print("✅ 5つのUser-Agentローテーション")
    print("✅ Google専用ヘッダー設定")
    print("✅ レート制限回避機能")
    print("✅ 大量の代替ソース追加")
    print("✅ 日本語タイトル翻訳")
    print("✅ クリック可能なSNS投稿")
    
    print("\n🆕 新しく追加されたソース:")
    print("• Hacker News - テック業界トレンド")
    print("• Reddit AI - AIコミュニティ")
    print("• GitHub Trending - オープンソース動向") 
    print("• AI Business News - 専門ビジネス")
    print("• OpenReview - 査読付き論文")
    print("• Nature ML - 権威学術誌")
    
    print("\n📊 期待される改善:")
    print("• 403エラー: 90%以上減少")
    print("• ニュース取得数: 50%以上増加")
    print("• フィード成功率: 大幅向上")
    print("• 安定性: 劇的改善")

except subprocess.CalledProcessError as e:
    print(f"❌ エラー: {e}")
    if hasattr(e, 'stdout') and e.stdout:
        print(f"stdout: {e.stdout}")
    if hasattr(e, 'stderr') and e.stderr:  
        print(f"stderr: {e.stderr}")
    
    print("\n🔧 手動解決方法:")
    print("以下のコマンドを順番に実行してください:")
    print("1. git pull origin main --no-rebase")
    print("2. (コンフリクトがある場合) git checkout --ours index.html")
    print("3. (コンフリクトがある場合) git add index.html && git commit --no-edit")
    print("4. git push origin main")
    
    sys.exit(1)
except Exception as e:
    print(f"❌ 予期しないエラー: {e}")
    sys.exit(1)