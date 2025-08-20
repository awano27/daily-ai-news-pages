#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deploy Enhanced System to GitHub - GitHubに強化版システムをデプロイ
"""
import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """コマンドを実行して結果を表示"""
    print(f"🔄 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
        if result.returncode == 0:
            print(f"✅ {description} - 成功")
            if result.stdout.strip():
                print(f"   出力: {result.stdout.strip()}")
            return True
        else:
            print(f"❌ {description} - 失敗")
            if result.stderr:
                print(f"   エラー: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - 例外: {e}")
        return False

def check_required_files():
    """必要なファイルが存在するかチェック"""
    required_files = [
        'enhanced_x_processor.py',
        'gemini_url_context.py', 
        'final_production_test.py',
        'build.py',
        'requirements.txt',
        '.github/workflows/enhanced-daily-build.yml',
        'GITHUB_SETUP.md'
    ]
    
    print("📋 必要ファイルの存在確認:")
    all_present = True
    
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - 見つかりません")
            all_present = False
    
    return all_present

def main():
    """メインデプロイ処理"""
    print("🚀 Enhanced AI News System - GitHub Deployment")
    print("=" * 60)
    
    # 必要ファイルのチェック
    if not check_required_files():
        print("❌ 必要なファイルが不足しています")
        return False
    
    # Git設定確認
    print("\n🔧 Git設定確認:")
    run_command("git config --get user.name", "ユーザー名確認")
    run_command("git config --get user.email", "メールアドレス確認")
    
    # Git status確認
    print("\n📊 Git状態確認:")
    run_command("git status --porcelain", "変更ファイル確認")
    
    # ファイルをステージング
    print("\n📁 ファイルをステージング:")
    files_to_add = [
        "enhanced_x_processor.py",
        "gemini_url_context.py", 
        "final_production_test.py",
        "build.py",
        "requirements.txt",
        ".github/workflows/enhanced-daily-build.yml",
        ".github/workflows/build.yml",
        "GITHUB_SETUP.md",
        ".env.example"
    ]
    
    for file_path in files_to_add:
        if Path(file_path).exists():
            success = run_command(f"git add {file_path}", f"{file_path} をステージング")
            if not success:
                print(f"⚠️ {file_path} のステージングに失敗")
    
    # .envファイルは除外（機密情報のため）
    run_command("git rm --cached .env", ".envファイルをキャッシュから除外")
    
    # コミット作成
    print("\n📝 変更をコミット:")
    commit_message = """🚀 Enhanced AI News System with Gemini URL Context

✨ 新機能:
- 🧠 Gemini URL contextによるX投稿強化
- ❌ 高度な重複除去システム
- 📝 300文字以内の要約制限
- ⭐ AI判定による重要度ランキング
- 🔄 自動カテゴリ分類

🤖 GitHub Actions:
- 毎日07:00 JST自動実行
- 毎日19:00 JST追加実行
- 手動実行サポート

📊 技術仕様:
- Gemini 2.5 Flash model
- CSV構造修正対応
- エラーハンドリング強化
- 詳細ログ出力

[Enhanced AI News System v2.0]"""
    
    success = run_command(f'git commit -m "{commit_message}"', "変更をコミット")
    if not success:
        print("⚠️ コミットに失敗または変更がありません")
    
    # プッシュ実行
    print("\n🌐 GitHubにプッシュ:")
    success = run_command("git push origin main", "変更をGitHubにプッシュ")
    if success:
        print("\n🎉 GitHub デプロイ完了!")
        print("\n📋 次のステップ:")
        print("1. GitHubリポジトリでGEMINI_API_KEYシークレットを設定")
        print("2. GitHub Pagesを有効化")
        print("3. ワークフロー権限を設定")
        print("4. GITHUB_SETUP.md を参照して詳細設定")
        print("\n🌐 設定完了後のサイトURL:")
        print("https://awano27.github.io/daily-ai-news-pages/")
        return True
    else:
        print("❌ プッシュに失敗しました")
        return False

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("\n✅ デプロイが正常に完了しました")
        else:
            print("\n❌ デプロイに問題がありました")
    except KeyboardInterrupt:
        print("\n⚠️ ユーザーによって中断されました")
    except Exception as e:
        print(f"\n❌ 予期しないエラー: {e}")
        import traceback
        traceback.print_exc()