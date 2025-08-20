#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Run Manual Workflow - 手動でGitHub Actionsワークフローを実行
"""
import webbrowser
from datetime import datetime

def main():
    """手動ワークフロー実行ガイド"""
    print("🚀 GitHub Actions Manual Workflow Execution Guide")
    print("=" * 60)
    print(f"実行時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    print("✅ YAML構文エラー修正完了!")
    print("   - enhanced-daily-build.yml: Fixed ✓")
    print("   - minimal-build.yml: Fixed ✓")
    print()
    
    print("📋 手動実行の手順:")
    print()
    print("1. GitHub Actions ページを開く")
    actions_url = "https://github.com/awano27/daily-ai-news-pages/actions"
    print(f"   🔗 {actions_url}")
    
    print("\n2. ワークフローを選択")
    print("   - 'Enhanced Daily AI News (Full Pipeline)' をクリック")
    
    print("\n3. 手動実行")
    print("   - 右上の 'Run workflow' ボタンをクリック")
    print("   - Branch: main を選択")
    print("   - 'Run workflow' をクリック")
    
    print("\n4. 実行状況を確認")
    print("   - リアルタイムでログを確認")
    print("   - 約5-10分で完了")
    
    print("\n5. サイト更新を確認")
    site_url = "https://awano27.github.io/daily-ai-news-pages/"
    print(f"   🌐 {site_url}")
    
    print("\n" + "=" * 60)
    print("🔍 確認ポイント:")
    print("   ✅ ワークフローが緑色のチェックマークで完了")
    print("   ✅ サイトが更新される")
    print("   ✅ X投稿の重複が除去される")
    print("   ✅ 要約が300文字以内になる")
    
    print("\n💡 トラブルシューティング:")
    print("   - エラーが出た場合: ログの詳細を確認")
    print("   - GEMINI_API_KEY エラー: Settings > Secrets で設定確認")
    print("   - Permission エラー: Settings > Actions > Workflow permissions 確認")
    
    print("\n🕐 自動実行スケジュール:")
    print("   - 毎日 07:00 JST (22:00 UTC)")
    print("   - 毎日 19:00 JST (10:00 UTC)")
    
    # ブラウザで開くか確認
    answer = input("\n🌐 GitHub Actions をブラウザで開きますか? (y/n): ")
    if answer.lower() == 'y':
        webbrowser.open(actions_url)
        print("✅ ブラウザでGitHub Actionsを開きました")
    
    print("\n🎯 次のアクション:")
    print("1. GitHub Actionsで手動実行")
    print("2. 実行完了を待つ（5-10分）")
    print("3. サイト更新を確認")
    print("4. 成功したら定期実行を待つ")

if __name__ == "__main__":
    main()
    input("\nPress Enter to exit...")