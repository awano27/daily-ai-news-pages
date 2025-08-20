#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Trigger Website Update - Enhanced AI News最新化
"""
import subprocess
import os
import sys
from datetime import datetime
from pathlib import Path

def set_environment():
    """環境変数設定"""
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '48'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '30'
    os.environ['X_POSTS_CSV'] = 'https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0'
    
    print("✅ 環境設定完了")
    print(f"   - 過去{os.environ['HOURS_LOOKBACK']}時間のニュース")
    print(f"   - カテゴリあたり最大{os.environ['MAX_ITEMS_PER_CATEGORY']}記事")

def run_build():
    """build.py実行"""
    print("\n🚀 Enhanced Build実行中...")
    print("   Gemini URL Context統合により高品質コンテンツ生成")
    
    try:
        # build.py実行
        result = subprocess.run(
            [sys.executable, 'build.py'],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            print("✅ ビルド成功！")
            
            # 生成ファイル確認
            if Path('news_detail.html').exists():
                print("✅ news_detail.html 生成完了")
                
                # index.htmlにコピー
                import shutil
                shutil.copy('news_detail.html', 'index.html')
                print("✅ index.html 更新完了")
                
                return True
            else:
                print("❌ news_detail.html が生成されませんでした")
                return False
        else:
            print(f"❌ ビルドエラー: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ ビルドタイムアウト（5分超過）")
        return False
    except Exception as e:
        print(f"❌ 実行エラー: {e}")
        return False

def commit_and_push():
    """GitHubへコミット&プッシュ"""
    print("\n📤 GitHubへの更新プッシュ...")
    
    try:
        # Git設定
        subprocess.run(['git', 'config', 'user.name', 'github-actions[bot]'], check=True)
        subprocess.run(['git', 'config', 'user.email', '41898282+github-actions[bot]@users.noreply.github.com'], check=True)
        
        # ファイル追加
        subprocess.run(['git', 'add', '*.html'], check=True)
        subprocess.run(['git', 'add', 'style.css'], check=True)
        subprocess.run(['git', 'add', '_cache/'], check=False)  # キャッシュは失敗OK
        
        # コミット
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M JST')
        commit_msg = f"🤖 Enhanced AI News Update - {timestamp} [skip ci]"
        
        result = subprocess.run(['git', 'commit', '-m', commit_msg], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ コミット成功")
            
            # プッシュ
            push_result = subprocess.run(['git', 'push', 'origin', 'main'], capture_output=True, text=True)
            
            if push_result.returncode == 0:
                print("✅ プッシュ成功！")
                return True
            else:
                print(f"❌ プッシュ失敗: {push_result.stderr}")
                return False
        else:
            print("⚠️ 変更がないか、コミット失敗")
            return False
            
    except Exception as e:
        print(f"❌ Git操作エラー: {e}")
        return False

def trigger_github_action():
    """GitHub Action手動トリガー"""
    print("\n🔄 GitHub Action手動実行トリガー...")
    
    try:
        result = subprocess.run(
            ['gh', 'workflow', 'run', 'enhanced-daily-build.yml'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ GitHub Action トリガー成功")
            print("   ワークフローが開始されました")
            return True
        else:
            print(f"⚠️ GitHub CLIエラー: {result.stderr}")
            print("   直接プッシュで更新を試みます")
            return False
            
    except FileNotFoundError:
        print("⚠️ GitHub CLI未インストール")
        print("   直接プッシュで更新します")
        return False

def main():
    """メイン処理"""
    print("=" * 60)
    print("🚀 Enhanced AI News - サイト更新")
    print("=" * 60)
    print(f"開始時刻: {datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')}")
    
    # 1. 環境設定
    set_environment()
    
    # 2. ビルド実行
    if run_build():
        # 3. GitHubへプッシュ
        if commit_and_push():
            print("\n" + "=" * 60)
            print("🎉 サイト更新成功！")
            print("=" * 60)
            print("\n📊 更新内容:")
            print("- 最新48時間のAIニュース収集")
            print("- Gemini URL Context による高品質要約")
            print("- X投稿の重複排除と300字要約")
            print("- Digital.gov準拠のアクセシブルデザイン")
            
            print("\n🌐 確認URL:")
            print("メインサイト: https://awano27.github.io/daily-ai-news-pages/")
            print("GitHub Actions: https://github.com/awano27/daily-ai-news/actions")
            
            print("\n⏰ 反映時間:")
            print("約1-2分後にサイトに反映されます")
            
            # 4. GitHub Action追加トリガー（オプション）
            trigger_github_action()
            
        else:
            print("\n❌ GitHubプッシュ失敗")
            print("手動でgit pushを実行してください")
    else:
        print("\n❌ ビルド失敗")
        print("エラーログを確認してください")

if __name__ == "__main__":
    main()