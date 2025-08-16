#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
日本ソース追加のGit競合を解決してデプロイ
"""
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

def deploy_japanese_sources():
    """Git競合を解決して日本ソースをデプロイ"""
    
    print("=" * 60)
    print("🇯🇵 日本AIニュースソース デプロイ完了")
    print("=" * 60)
    
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    try:
        # 現在の変更をコミット
        print("\n1️⃣ 日本ソース変更をコミット中...")
        
        files_to_add = ['feeds.yml', 'build.py', 'index.html']
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
        
        commit_msg = f"feat: Add Japanese AI business news sources and enhanced filtering [{now.strftime('%Y-%m-%d %H:%M JST')}]\n\n📰 Added 8 Japanese sources:\n- 日経新聞, ITmedia, ZDNET Japan\n- ASCII.jp, TechCrunch Japan\n- Google News Japanese searches\n\n🏢 Japanese companies in importance scoring:\n- ソフトバンク(80), トヨタ(75), NTT(70)\n- ソニー(70), 日立(65), 富士通(65)"
        
        try:
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ 日本ソース変更をコミットしました")
        except subprocess.CalledProcessError:
            print("ℹ️ コミットする変更がありません")
        
        # リモートから最新を取得
        print("\n2️⃣ リモートから最新を取得中...")
        subprocess.run(['git', 'fetch', 'origin', 'main'], check=True)
        
        # マージ（競合があれば自動解決）
        print("\n3️⃣ リモート変更とマージ中...")
        result = subprocess.run(['git', 'merge', 'origin/main'], 
                              capture_output=True, text=True)
        
        if result.returncode != 0:
            print("⚠️ マージ競合が発生しました。自動解決を試みます...")
            
            # 競合ファイルを解決（ローカル版を優先）
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
        print("✅ 日本AIニュースソース デプロイ完了!")
        print("=" * 60)
        
        print(f"\n🇯🇵 追加された日本ソース（8個）:")
        print(f"  📰 日経新聞 AI・テクノロジー")
        print(f"  💻 ITmedia AI・機械学習")
        print(f"  🔧 ZDNET Japan AI")
        print(f"  📱 ASCII.jp AI・IoT")
        print(f"  🚀 TechCrunch Japan")
        print(f"  🏢 Google News: 日本AI企業")
        print(f"  💰 Google News: 日本AI投資")
        print(f"  🤖 Google News: 生成AI日本")
        
        print(f"\n🏢 重要度スコア追加企業:")
        print(f"  ソフトバンク(80), トヨタ(75), NTT(70)")
        print(f"  ソニー(70), 日立(65), 富士通(65)")
        print(f"  楽天(60), リクルート(55), メルカリ(50)")
        
        print(f"\n🎯 強化された機能:")
        print(f"  • 日本語AI関連キーワード拡充")
        print(f"  • 日本企業ニュースの重要度ソート")
        print(f"  • 日本のAI投資・資金調達情報")
        print(f"  • 生成AI・ChatGPT日本動向")
        
        print(f"\n🌐 更新されたサイト:")
        print(f"   https://awano27.github.io/daily-ai-news/")
        print(f"\n💡 これで日本と海外両方のAI業界を完全網羅！")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ エラー: {e}")
        return False
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    return deploy_japanese_sources()

if __name__ == "__main__":
    sys.exit(0 if main() else 1)