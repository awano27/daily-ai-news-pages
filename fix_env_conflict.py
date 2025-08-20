#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix .env Conflict - 環境ファイル競合の自動解決
"""
import os
import subprocess
import shutil
from datetime import datetime

def run_command(cmd, description=""):
    """コマンド実行"""
    if description:
        print(f"🔄 {description}...")
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
        if result.returncode == 0:
            if description:
                print(f"✅ {description} 完了")
            return True, result.stdout.strip()
        else:
            if description:
                print(f"❌ {description} 失敗: {result.stderr.strip()}")
            return False, result.stderr.strip()
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False, str(e)

def main():
    """環境ファイル競合解決とデプロイ"""
    print("🔧 Fix .env Conflict - 環境ファイル競合解決")
    print("=" * 50)
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    print()
    
    # Step 1: .envファイルをバックアップ
    env_path = ".env"
    if os.path.exists(env_path):
        backup_name = f".env.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        print(f"💾 .envファイルをバックアップ: {backup_name}")
        shutil.copy2(env_path, backup_name)
        
        # .envを一時的に移動
        temp_name = ".env.temp"
        os.rename(env_path, temp_name)
        print(f"📦 .envを一時移動: {temp_name}")
    else:
        temp_name = None
        print("ℹ️ .envファイルが見つかりません")
    
    # Step 2: リモートの変更を取得
    print("\n📥 リモート同期実行")
    print("-" * 30)
    
    success, _ = run_command(["git", "pull", "origin", "main"], "リモート変更取得")
    
    if success:
        print("✅ リモート同期成功!")
        
        # .envファイルを復元
        if temp_name and os.path.exists(temp_name):
            if os.path.exists(env_path):
                print("⚠️ リモートにも.envが存在します")
                print("📝 ローカル設定を優先して復元...")
                os.remove(env_path)  # リモートの.envを削除
            
            os.rename(temp_name, env_path)
            print("🔄 ローカル.envを復元完了")
            
            # .envをgitignoreに追加
            gitignore_path = ".gitignore"
            if os.path.exists(gitignore_path):
                with open(gitignore_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if '.env' not in content:
                    with open(gitignore_path, 'a', encoding='utf-8') as f:
                        f.write('\n# Environment files\n.env\n.env.*\n')
                    print("📝 .gitignoreに.envを追加")
        
        # Step 3: アクセシビリティ改善をコミット
        print("\n🎨 アクセシビリティ改善デプロイ")
        print("-" * 30)
        
        # 変更をステージング（.envは除外）
        run_command(["git", "add", "style.css"], "スタイル改善をステージング")
        run_command(["git", "add", ".gitignore"], "gitignore更新をステージング")
        
        # コミット
        commit_msg = """enhance: Deploy accessibility improvements with conflict resolution

• WCAG AA compliant color contrast improvements
• Enhanced visual hierarchy and spacing  
• Better KPI area design and prominence
• Accessible tab navigation with focus indicators
• Improved chip design with visual indicators
• Mobile-first responsive optimizations
• Enhanced touch targets (44px minimum)

🔧 Fixed .env file conflict during deployment"""

        success, _ = run_command(["git", "commit", "-m", commit_msg], "改善内容コミット")
        
        if success:
            # プッシュ
            success, _ = run_command(["git", "push", "origin", "main"], "GitHubにプッシュ")
            
            if success:
                print("\n🎉 デプロイ成功!")
                print("=" * 40)
                print("✅ アクセシビリティ改善がデプロイされました")
                print("🔧 .env競合問題も解決しました")
                print()
                print("🌐 確認URL:")
                print("- GitHub Actions: https://github.com/awano27/daily-ai-news/actions")
                print("- 改善サイト: https://awano27.github.io/daily-ai-news/")
                print()
                print("⏱️ 反映まで2-3分かかります")
            else:
                print("❌ プッシュに失敗しました")
        else:
            print("❌ コミットに失敗しました")
    
    else:
        print("❌ リモート同期に失敗しました")
        
        # 失敗した場合は.envを復元
        if temp_name and os.path.exists(temp_name):
            os.rename(temp_name, env_path)
            print("🔄 .envファイルを復元しました")

if __name__ == "__main__":
    main()