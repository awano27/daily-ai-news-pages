#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GitHub Secrets Setup Guide - GitHub Secrets設定ガイド
"""
import webbrowser
from datetime import datetime

def main():
    """GitHub Secrets設定ガイド"""
    print("🔐 GitHub Secrets Setup Guide")
    print("=" * 60)
    print(f"現在時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    print("🚨 CRITICAL: 以下の設定が完了するまでシステムは動作しません")
    print()
    
    print("📍 STEP 1: PERSONAL_TOKEN作成")
    print("1. GitHub Personal Access Token作成ページを開く")
    token_url = "https://github.com/settings/tokens/new"
    print(f"   🔗 {token_url}")
    print()
    print("2. Token設定:")
    print("   - Note: daily-ai-news deployment")
    print("   - Expiration: No expiration (推奨)")
    print("   - Scopes: ✅ repo (Full control of private repositories)")
    print("   - その他はすべて未チェックでOK")
    print()
    print("3. 'Generate token' をクリック")
    print("4. 生成されたToken文字列をコピー（重要: 1回しか表示されません）")
    print()
    
    print("📍 STEP 2: daily-ai-news Secrets設定")
    secrets_url = "https://github.com/awano27/daily-ai-news/settings/secrets/actions"
    print(f"1. 🔗 {secrets_url} を開く")
    print()
    print("2. 'New repository secret' をクリックして以下を追加:")
    print()
    print("   Secret 1:")
    print("   - Name: GEMINI_API_KEY")
    print("   - Value: AIzaSyDf_VZIxpLvLZSrhPYH-0SqF7PwE2E5Cyo")
    print()
    print("   Secret 2:")
    print("   - Name: PERSONAL_TOKEN")
    print("   - Value: (STEP 1で作成したToken文字列)")
    print()
    
    print("📍 STEP 3: daily-ai-news-pages Pages設定")
    pages_url = "https://github.com/awano27/daily-ai-news-pages/settings/pages"
    print(f"1. 🔗 {pages_url} を開く")
    print()
    print("2. Source設定:")
    print("   - Source: Deploy from a branch")
    print("   - Branch: main")
    print("   - Folder: / (root)")
    print()
    print("3. 'Save' をクリック")
    print()
    
    print("🧪 STEP 4: テスト実行")
    actions_url = "https://github.com/awano27/daily-ai-news/actions"
    print(f"1. 🔗 {actions_url} を開く")
    print()
    print("2. 'Enhanced Daily AI News Build (Gemini URL Context)' を選択")
    print("3. 'Run workflow' をクリック")
    print("4. Branch: main を選択 → 'Run workflow'")
    print("5. ビルド完了を待つ（約5-10分）")
    print("6. 成功したら Deploy workflow が自動実行される")
    print()
    
    print("🌐 STEP 5: サイト確認")
    site_url = "https://awano27.github.io/daily-ai-news-pages/"
    print(f"🔗 {site_url}")
    print()
    print("確認ポイント:")
    print("✅ Enhanced AI News ページが表示される")
    print("✅ X投稿の重複がない")
    print("✅ 要約が300文字以内")
    print("✅ 🧠 Gemini強化マークがある")
    print()
    
    print("=" * 60)
    print("⚠️ 注意事項:")
    print("- PERSONAL_TOKEN は機密情報です。他人に共有しないでください")
    print("- Token は1回しか表示されません。必ずコピーしてください")
    print("- 設定完了後、約15分でシステムが完全稼働します")
    print()
    
    print("🕐 設定完了後の自動実行スケジュール:")
    print("- 毎日 07:00 JST: メインビルド")
    print("- 毎日 19:00 JST: 追加ビルド")
    print()
    
    # ブラウザで開くか確認
    answer = input("🌐 必要なページをブラウザで順次開きますか? (y/n): ")
    if answer.lower() == 'y':
        print("\n🚀 ブラウザでページを開いています...")
        webbrowser.open(token_url)
        input("PERSONAL_TOKEN作成完了後、Enterを押してください...")
        webbrowser.open(secrets_url)
        input("Secrets設定完了後、Enterを押してください...")
        webbrowser.open(pages_url)
        input("Pages設定完了後、Enterを押してください...")
        webbrowser.open(actions_url)
        print("✅ すべてのページを開きました。設定を完了してください。")
    
    print(f"\n🎉 設定完了後の確認URL: {site_url}")

if __name__ == "__main__":
    main()