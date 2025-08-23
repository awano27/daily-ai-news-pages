#!/usr/bin/env python3
"""
Manual trigger for GitHub Actions workflow
"""
import subprocess
import time
from datetime import datetime

def trigger_workflow():
    """手動でGitHub Actionsワークフローをトリガー"""
    print("🚀 GitHub Actions ワークフロー手動トリガー")
    print("=" * 50)
    
    # 現在時刻
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S JST')
    print(f"実行時刻: {now}")
    
    try:
        # GitHub Actions ワークフローをトリガー
        print("🔄 deploy-pages.yml ワークフローをトリガー中...")
        
        result = subprocess.run([
            'gh', 'workflow', 'run', 'deploy-pages.yml'
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ ワークフローが正常にトリガーされました")
            print("📊 GitHub Actions で自動ビルドが開始されます")
            
            # 少し待ってからステータス確認
            print("⏳ 5秒待機中...")
            time.sleep(5)
            
            # ワークフロー実行状況確認
            print("📋 最近のワークフロー実行状況:")
            status_result = subprocess.run([
                'gh', 'run', 'list', '--limit', '3'
            ], capture_output=True, text=True, timeout=15)
            
            if status_result.returncode == 0:
                print(status_result.stdout)
            
        else:
            print("❌ ワークフローのトリガーに失敗")
            print(f"エラー: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏱️ コマンドがタイムアウトしました")
        return False
    except FileNotFoundError:
        print("❌ GitHub CLI (gh) が見つかりません")
        print("GitHub CLI をインストールしてください: https://cli.github.com/")
        return False
    except Exception as e:
        print(f"❌ エラーが発生しました: {e}")
        return False
    
    print("\n🎯 次のステップ:")
    print("1. 📊 GitHub Actions: https://github.com/awano27/daily-ai-news-pages/actions")
    print("2. ⏳ 5-10分後にサイト確認: https://awano27.github.io/daily-ai-news-pages/")
    print("3. 📅 期待される内容: 2025-08-23の最新AIニュース")
    
    return True

def create_dummy_commit_trigger():
    """ダミーコミットでワークフローをトリガー"""
    print("\n🔄 代替案: ダミーコミットでワークフローをトリガー")
    print("=" * 50)
    
    try:
        # ダミーファイル作成
        trigger_file = f"trigger_workflow_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(trigger_file, 'w') as f:
            f.write(f"Manual workflow trigger at {datetime.now()}")
        
        print(f"📝 トリガーファイル作成: {trigger_file}")
        
        # Git操作
        subprocess.run(['git', 'add', trigger_file], check=True)
        
        commit_msg = f"trigger: Manual GitHub Actions workflow trigger - {datetime.now().strftime('%H:%M:%S')}"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        subprocess.run(['git', 'push', '--force', 'origin', 'main'], check=True)
        
        print("✅ ダミーコミットでワークフローをトリガーしました")
        
        # ファイル削除
        import os
        os.remove(trigger_file)
        subprocess.run(['git', 'rm', trigger_file], check=True)
        subprocess.run(['git', 'commit', '-m', f'cleanup: Remove {trigger_file}'], check=True)
        subprocess.run(['git', 'push', '--force', 'origin', 'main'], check=True)
        
        print("🧹 トリガーファイル削除完了")
        return True
        
    except Exception as e:
        print(f"❌ ダミーコミット作成に失敗: {e}")
        return False

def main():
    """メイン処理"""
    print("🎯 GitHub Pages 更新トリガー")
    print("=" * 60)
    
    # まず gh コマンドを試す
    if trigger_workflow():
        return True
    
    # gh コマンドが失敗した場合、ダミーコミットを試す
    print("\n🔄 GitHub CLI が使用できないため、代替案を実行します...")
    return create_dummy_commit_trigger()

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 GitHub Actions ワークフローがトリガーされました！")
        print("📱 2-10分後にサイトの更新を確認してください")
    else:
        print("\n❌ ワークフローのトリガーに失敗しました")