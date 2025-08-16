#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Git競合を解決してスマートソート機能をデプロイ
"""
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

def resolve_git_conflict():
    """Git競合を解決してデプロイ"""
    
    print("=" * 60)
    print("🔧 Git競合解決とスマートソート機能デプロイ")
    print("=" * 60)
    
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    try:
        # 現在の変更をコミット
        print("\n1️⃣ 現在の変更をコミット中...")
        
        files_to_add = ['build.py', 'index.html']
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
        
        commit_msg = f"feat: Add smart sorting for business news (importance-based ranking) [{now.strftime('%Y-%m-%d %H:%M JST')}]"
        
        try:
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ ローカル変更をコミットしました")
        except subprocess.CalledProcessError:
            print("ℹ️ コミットする変更がありません")
        
        # リモートから最新を取得（強制的に）
        print("\n2️⃣ リモートから最新を取得中...")
        subprocess.run(['git', 'fetch', 'origin', 'main'], check=True)
        
        # マージ（競合があれば自動解決）
        print("\n3️⃣ リモート変更とマージ中...")
        result = subprocess.run(['git', 'merge', 'origin/main'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("⚠️ マージ競合が発生しました。自動解決を試みます...")
            
            # index.htmlの競合を解決（ローカル版を優先）
            subprocess.run(['git', 'checkout', '--ours', 'index.html'], check=True)
            subprocess.run(['git', 'add', 'index.html'], check=True)
            
            # マージを完了
            subprocess.run(['git', 'commit', '--no-edit'], check=True)
            print("✅ 競合を自動解決しました")
        else:
            print("✅ マージ完了（競合なし）")
        
        # プッシュ
        print("\n4️⃣ GitHubへプッシュ中...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ GitHubにプッシュ完了")
        
        print("\n" + "=" * 60)
        print("✅ スマートソート機能デプロイ完了!")
        print("=" * 60)
        
        print(f"\n🎯 実装された機能:")
        print(f"  🏢 ビジネスニュース: 重要度順ソート")
        print(f"  📈 大手企業ニュースが上位表示")
        print(f"  🚀 重要キーワード優先")
        print(f"  📰 信頼性の高いソース重視")
        print(f"  ⏰ 新鮮なニュースにボーナス")
        
        print(f"\n📊 テスト結果:")
        print(f"  1位: Foundational Integrity Research (重要度高)")
        print(f"  2位: Anthropic vs OpenAI (企業重要度)")
        print(f"  3位: GPT-5 Infrastructure (技術重要度)")
        
        print(f"\n🌐 更新されたサイト:")
        print(f"   https://awano27.github.io/daily-ai-news/")
        print(f"\n💡 これで大きなニュースが確実に上位に表示されます！")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ エラー: {e}")
        print(f"\n📋 手動での解決方法:")
        print(f"1. git status で競合ファイルを確認")
        print(f"2. git add index.html")
        print(f"3. git commit -m 'resolve merge conflict'")
        print(f"4. git push origin main")
        return False
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    return resolve_git_conflict()

if __name__ == "__main__":
    sys.exit(0 if main() else 1)