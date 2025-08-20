#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Setup Guide - 完全セットアップガイド
"""
from datetime import datetime

def main():
    """完全セットアップガイドを表示"""
    print("🎯 Enhanced AI News System - Complete Setup Guide")
    print("=" * 60)
    print(f"現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    print("📊 現在の状況:")
    print("✅ Enhanced AI News System開発完了")
    print("✅ GitHub Actions ワークフロー修正済み")
    print("✅ デプロイメント設定修正済み")
    print("⚠️ リモート同期が必要")
    print()
    
    print("🔄 STEP 1: リモート同期")
    print("実行: sync_and_push.bat")
    print("または手動で:")
    print("  git pull origin main")
    print("  git push origin main")
    print()
    
    print("🔧 STEP 2: GitHub Secrets 設定")
    print()
    print("📍 daily-ai-news (source repo) Settings → Secrets:")
    print("   Name: GEMINI_API_KEY")
    print("   Value: AIzaSyDf_VZIxpLvLZSrhPYH-0SqF7PwE2E5Cyo")
    print()
    print("   Name: PERSONAL_TOKEN")
    print("   Value: (GitHub Personal Access Token with repo permissions)")
    print("   作成: https://github.com/settings/tokens")
    print()
    
    print("⚙️ STEP 3: daily-ai-news-pages (public repo) Settings:")
    print("   Pages → Source: Deploy from a branch")
    print("   Pages → Branch: main")
    print("   Pages → Folder: / (root)")
    print()
    
    print("🚀 STEP 4: テスト実行")
    print("1. daily-ai-news の GitHub Actions でワークフロー実行")
    print("2. 'Enhanced Daily AI News (Gemini URL Context)' を選択")
    print("3. 'Run workflow' をクリック")
    print("4. ビルド完了後、Deploy workflow が自動実行されるか確認")
    print()
    
    print("🌐 STEP 5: サイト確認")
    print("URL: https://awano27.github.io/daily-ai-news-pages/")
    print("確認ポイント:")
    print("  - ページが表示される")
    print("  - X投稿の重複がない")
    print("  - 要約が300文字以内")
    print("  - Gemini強化マークがある")
    print()
    
    print("🕐 自動実行スケジュール:")
    print("  - 毎日 07:00 JST (22:00 UTC)")
    print("  - 毎日 19:00 JST (10:00 UTC)")
    print()
    
    print("🔍 トラブルシューティング:")
    print()
    print("❌ Build fails:")
    print("   → GEMINI_API_KEY がSecrets に設定されているか確認")
    print()
    print("❌ Deploy fails:")
    print("   → PERSONAL_TOKEN がSecrets に設定されているか確認")
    print("   → Token に repo permissions があるか確認")
    print()
    print("❌ Site not updating:")
    print("   → daily-ai-news-pages の Pages設定確認")
    print("   → main branch に設定されているか確認")
    print()
    print("❌ X posts not working:")
    print("   → Google Sheets CSV URL アクセス確認")
    print("   → CSV構造の変更確認")
    print()
    
    print("=" * 60)
    print("🎉 すべて設定完了後の動作:")
    print("1. 毎日自動でAIニュースサイトが更新")
    print("2. X投稿の重複除去とGemini強化要約")
    print("3. 300文字以内の読みやすい要約")
    print("4. 重要度による優先表示")
    print("5. 完全自動のメンテナンスフリー運用")
    
    print(f"\n🤖 Enhanced AI News System v2.0")
    print("Powered by Gemini URL Context API")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")