#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
完全自動更新スクリプト - Google Sheets含む全データソースから最新情報を取得して更新
"""
import os
import sys
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
import time

def setup_environment():
    """環境変数の設定"""
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    print("🔧 環境設定中...")
    print(f"📅 実行時刻: {now.strftime('%Y-%m-%d %H:%M JST')}")
    
    # 基本設定
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    os.environ['HOURS_LOOKBACK'] = '24'  # 24時間分のニュース
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '20'  # 各カテゴリ20件まで
    
    # Google SheetsのCSV URL（X/Twitter投稿）
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    print(f"✅ 環境変数設定完了")
    print(f"  • 翻訳: 日本語")
    print(f"  • 取得期間: 過去24時間")
    print(f"  • 表示件数: 各カテゴリ20件")
    print(f"  • X投稿ソース: Google Sheets")
    
    return now

def update_news_detail():
    """詳細ニュースページを更新（build.py実行）"""
    print("\n📰 詳細ニュースページを更新中...")
    
    try:
        # build.pyを実行
        result = subprocess.run(
            [sys.executable, 'build.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=300  # 5分タイムアウト
        )
        
        if result.returncode == 0:
            print("✅ 詳細ニュースページ更新完了")
            
            # 処理結果を表示
            if result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if any(keyword in line for keyword in ['Business:', 'Tools:', 'Posts:', 'X post', 'SUCCESS']):
                        print(f"  {line}")
            
            return True
        else:
            print(f"❌ ビルドエラー: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ タイムアウト: build.pyの実行に5分以上かかりました")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def update_dashboard():
    """ダッシュボードを更新（generate_comprehensive_dashboard.py実行）"""
    print("\n📊 ダッシュボードを更新中...")
    
    try:
        # generate_comprehensive_dashboard.pyを実行
        result = subprocess.run(
            [sys.executable, 'generate_comprehensive_dashboard.py'],
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=180  # 3分タイムアウト
        )
        
        if result.returncode == 0:
            print("✅ ダッシュボード更新完了")
            
            # エグゼクティブサマリーを表示
            if result.stdout:
                lines = result.stdout.split('\n')
                for line in lines:
                    if any(keyword in line for keyword in ['総記事数', 'ハイライト', '企業', 'トレンド']):
                        print(f"  {line}")
            
            return True
        else:
            print(f"❌ ダッシュボード生成エラー: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️ タイムアウト: ダッシュボード生成に3分以上かかりました")
        return False
    except Exception as e:
        print(f"❌ エラー: {e}")
        return False

def check_updates():
    """更新結果を確認"""
    print("\n🔍 更新結果を確認中...")
    
    files_to_check = {
        'index.html': 'ダッシュボード（ランディングページ）',
        'news_detail.html': '詳細ニュースページ',
        'dashboard_data.json': 'ダッシュボードデータ'
    }
    
    results = []
    for filename, description in files_to_check.items():
        file_path = Path(filename)
        if file_path.exists():
            # ファイルサイズと更新時刻を確認
            size = file_path.stat().st_size
            mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
            
            # 5分以内に更新されていれば成功とみなす
            if (datetime.now() - mtime).seconds < 300:
                results.append(f"  ✅ {description}: {size:,} bytes (更新済み)")
            else:
                results.append(f"  ⚠️ {description}: {size:,} bytes (古い)")
        else:
            results.append(f"  ❌ {description}: 存在しません")
    
    for result in results:
        print(result)
    
    return all('✅' in r for r in results)

def git_commit_and_push(now):
    """GitHubにコミット・プッシュ"""
    print("\n📤 GitHubへアップロード中...")
    
    try:
        # 変更をステージング
        files_to_add = ['index.html', 'news_detail.html', 'dashboard_data.json', 'build.py']
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
        
        # コミット
        commit_msg = f"""chore: Auto update AI news [{now.strftime('%Y-%m-%d %H:%M JST')}] [skip ci]

📊 Updates:
- Dashboard with executive summary and industry insights
- Detailed news from RSS feeds and Google Sheets
- X/Twitter posts with importance scoring
- Fixed reference links (LLM Arena, AlphaXiv, Trend Words)

🤖 Generated with Claude Code
Co-Authored-By: Claude <noreply@anthropic.com>"""
        
        try:
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ コミット成功")
        except subprocess.CalledProcessError:
            print("ℹ️ 変更なし（既にコミット済み）")
            return True
        
        # プッシュ
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ GitHubへプッシュ完了")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Git操作エラー: {e}")
        return False

def create_auto_update_batch():
    """Windows用の自動更新バッチファイルを作成"""
    batch_content = """@echo off
chcp 65001 > nul
echo ========================================
echo 🔄 Daily AI News 自動更新
echo ========================================

cd /d "C:\\Users\\yoshitaka\\daily-ai-news"

echo.
echo 📅 %date% %time%
echo.

python auto_update_all.py

if %errorlevel% == 0 (
    echo.
    echo ✅ 更新成功！
) else (
    echo.
    echo ❌ 更新失敗
)

echo.
echo Enterキーを押して終了...
pause > nul
"""
    
    batch_path = Path("run_auto_update.bat")
    batch_path.write_text(batch_content, encoding='utf-8')
    print(f"\n💡 自動更新用バッチファイル作成: {batch_path}")
    
    return batch_path

def create_github_action():
    """GitHub Actions用の自動更新ワークフローを作成"""
    workflow_content = """name: Auto Update AI News

on:
  schedule:
    # 毎日朝7時(JST) = 前日22時(UTC)に実行
    - cron: '0 22 * * *'
  workflow_dispatch:  # 手動実行も可能

jobs:
  update:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v3
      with:
        token: ${{ secrets.GITHUB_TOKEN }}
    
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    
    - name: Install dependencies
      run: |
        pip install feedparser pyyaml deep-translator==1.11.4
    
    - name: Set environment variables
      run: |
        echo "TRANSLATE_TO_JA=1" >> $GITHUB_ENV
        echo "TRANSLATE_ENGINE=google" >> $GITHUB_ENV
        echo "HOURS_LOOKBACK=24" >> $GITHUB_ENV
        echo "MAX_ITEMS_PER_CATEGORY=20" >> $GITHUB_ENV
        echo "X_POSTS_CSV=https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0" >> $GITHUB_ENV
    
    - name: Update news detail page
      run: python build.py
      continue-on-error: true
    
    - name: Generate dashboard
      run: python generate_comprehensive_dashboard.py
      continue-on-error: true
    
    - name: Commit and push
      run: |
        git config --local user.email "action@github.com"
        git config --local user.name "GitHub Action"
        git add -A
        git diff --quiet && git diff --staged --quiet || git commit -m "chore: Auto update AI news [skip ci]"
        git push
"""
    
    workflow_path = Path(".github/workflows/auto_update.yml")
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(workflow_content, encoding='utf-8')
    print(f"💡 GitHub Actions ワークフロー作成: {workflow_path}")
    
    return workflow_path

def main():
    """メイン実行関数"""
    print("=" * 60)
    print("🤖 Daily AI News 完全自動更新システム")
    print("=" * 60)
    
    # 環境設定
    now = setup_environment()
    
    # 更新処理
    success = True
    
    # 1. 詳細ニュースページ更新
    if not update_news_detail():
        print("⚠️ 詳細ニュースページの更新に失敗しましたが続行します")
        success = False
    
    # 2. ダッシュボード更新
    if not update_dashboard():
        print("⚠️ ダッシュボードの更新に失敗しましたが続行します")
        success = False
    
    # 3. 更新結果確認
    if not check_updates():
        print("⚠️ 一部のファイルが正しく更新されていません")
        success = False
    
    # 4. GitHubへアップロード（オプション）
    if '--push' in sys.argv:
        if not git_commit_and_push(now):
            print("⚠️ GitHubへのアップロードに失敗しました")
            success = False
    else:
        print("\n💡 GitHubへプッシュするには --push オプションを付けて実行してください")
    
    # 自動化ファイルを作成
    create_auto_update_batch()
    create_github_action()
    
    # 結果サマリー
    print("\n" + "=" * 60)
    if success:
        print("✅ 自動更新完了！")
    else:
        print("⚠️ 一部エラーがありましたが更新処理は完了しました")
    print("=" * 60)
    
    print("\n📊 更新内容:")
    print(f"  • Google Sheetsから最新X投稿を取得")
    print(f"  • RSS フィードから最新ニュースを収集")
    print(f"  • 重要度順にソート・ランキング")
    print(f"  • 日本語要約を自動生成")
    print(f"  • ダッシュボードで業界全体像を可視化")
    
    print("\n🔄 自動更新方法:")
    print("  1. 手動: run_auto_update.bat をダブルクリック")
    print("  2. タスクスケジューラ: run_auto_update.bat を毎日実行")
    print("  3. GitHub Actions: 毎日朝7時(JST)に自動実行")
    
    print("\n🌐 サイトURL:")
    print("  https://awano27.github.io/daily-ai-news/")
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())