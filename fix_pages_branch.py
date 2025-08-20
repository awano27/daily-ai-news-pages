#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix Pages Branch - daily-ai-news-pages リポジトリのブランチ問題を解決
"""
import webbrowser
from datetime import datetime

def main():
    """Pages ブランチ問題の解決ガイド"""
    print("🔧 GitHub Pages Branch Fix Guide")
    print("=" * 50)
    print(f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    print("🔍 問題の確認:")
    print("❌ daily-ai-news-pages リポジトリに main ブランチが存在しない")
    print("❌ GitHub Pages の Source で main を選択できない")
    print()
    
    print("💡 解決方法（2つのオプション）:")
    print()
    
    print("=" * 50)
    print("🎯 オプション 1: gh-pages ブランチを使用（推奨・簡単）")
    print("=" * 50)
    
    print("1. daily-ai-news-pages の Pages設定を開く")
    pages_url = "https://github.com/awano27/daily-ai-news-pages/settings/pages"
    print(f"   🔗 {pages_url}")
    print()
    
    print("2. Source設定を以下に変更:")
    print("   - Source: Deploy from a branch")
    print("   - Branch: gh-pages (こちらを選択)")
    print("   - Folder: / (root)")
    print("   - 'Save' をクリック")
    print()
    
    print("3. deploy-to-public.yml を gh-pages に戻す")
    print("   (元の設定が正しかった)")
    print()
    
    print("=" * 50)
    print("🎯 オプション 2: main ブランチを作成")
    print("=" * 50)
    
    print("1. daily-ai-news-pages リポジトリを開く")
    repo_url = "https://github.com/awano27/daily-ai-news-pages"
    print(f"   🔗 {repo_url}")
    print()
    
    print("2. 'Create a new file' をクリック")
    print("3. ファイル名: README.md")
    print("4. 内容:")
    print("""   # Enhanced Daily AI News
   
   AI業界の最新ニュースを自動収集・分析するサイトです。
   
   - 🧠 Gemini URL Context による高品質要約
   - ❌ X投稿の重複除去
   - 📝 300文字以内の読みやすい要約
   - ⭐ 重要度による優先表示
   
   毎日 07:00, 19:00 JST に自動更新されます。""")
    print()
    print("5. 'Commit new file' をクリック")
    print("6. これで main ブランチが作成される")
    print()
    
    print("=" * 50)
    print("🚀 推奨アクション:")
    print("=" * 50)
    
    print("**オプション 1 を推奨します（より簡単で確実）**")
    print()
    print("理由:")
    print("✅ 既存の deploy-to-public.yml が gh-pages 前提で設計されている")
    print("✅ GitHub Pages の一般的な慣例に従っている")
    print("✅ 設定変更が最小限")
    print()
    
    print("修正が必要なファイル:")
    print("📝 .github/workflows/deploy-to-public.yml")
    print("   Line 73: publish_branch: main → publish_branch: gh-pages")
    print()
    
    # ブラウザで開くか確認
    answer = input("🌐 GitHub Pages 設定ページを開きますか? (y/n): ")
    if answer.lower() == 'y':
        webbrowser.open(pages_url)
        print("✅ GitHub Pages 設定ページを開きました")
        print("💡 Branch を 'gh-pages' に設定してください")
    
    print("\n📋 設定後の確認手順:")
    print("1. Pages設定で gh-pages を選択")
    print("2. deploy-to-public.yml を gh-pages に修正")
    print("3. Enhanced ワークフローを手動実行")
    print("4. サイト更新を確認")
    
    print(f"\n🌐 最終確認URL: https://awano27.github.io/daily-ai-news-pages/")

if __name__ == "__main__":
    main()