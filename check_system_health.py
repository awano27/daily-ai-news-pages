#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
システムヘルスチェック - 毎日の更新前に実行
"""

import os
import sys
import requests
from datetime import datetime, timezone, timedelta
import subprocess
import yaml

def check_environment():
    """環境変数とAPI設定をチェック"""
    print("🔍 環境設定チェック...")
    
    # .env ファイル存在確認
    env_exists = os.path.exists('.env')
    print(f"  .env ファイル: {'✅' if env_exists else '❌'}")
    
    # Gemini API キー確認
    gemini_key = os.getenv('GEMINI_API_KEY')
    gemini_ok = bool(gemini_key and len(gemini_key) > 10)
    print(f"  Gemini API キー: {'✅' if gemini_ok else '❌'}")
    
    # feeds.yml 確認
    feeds_exists = os.path.exists('feeds.yml')
    print(f"  feeds.yml: {'✅' if feeds_exists else '❌'}")
    
    return env_exists and gemini_ok and feeds_exists

def check_dependencies():
    """必要なライブラリがインストールされているかチェック"""
    print("📦 依存関係チェック...")
    
    required_packages = [
        'feedparser',
        'pyyaml', 
        'requests',
        'google.generativeai',
        'dotenv'
    ]
    
    all_ok = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_').replace('.', '_'))
            print(f"  {package}: ✅")
        except ImportError:
            print(f"  {package}: ❌ (pip install {package})")
            all_ok = False
    
    return all_ok

def check_github_actions():
    """GitHub Actions の最新実行状況をチェック"""
    print("🔄 GitHub Actions チェック...")
    
    try:
        # GitHub API で最新のワークフロー実行を確認
        api_url = "https://api.github.com/repos/awano27/daily-ai-news/actions/runs?per_page=3"
        response = requests.get(api_url, timeout=10)
        
        if response.status_code == 200:
            runs = response.json().get('workflow_runs', [])
            if runs:
                latest_run = runs[0]
                status = latest_run.get('status')
                conclusion = latest_run.get('conclusion')
                updated_at = latest_run.get('updated_at')
                
                print(f"  最新実行: {status} ({conclusion})")
                print(f"  実行時刻: {updated_at}")
                
                return conclusion == 'success'
            else:
                print("  実行履歴なし: ❌")
                return False
        else:
            print(f"  API エラー: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  チェックエラー: {e}")
        return False

def check_live_site():
    """ライブサイトの更新状況をチェック"""
    print("🌐 ライブサイトチェック...")
    
    try:
        response = requests.get("https://awano27.github.io/daily-ai-news/", timeout=15)
        
        if response.status_code == 200:
            content = response.text
            
            # 今日の日付チェック
            today = datetime.now(timezone(timedelta(hours=9))).strftime('%Y-%m-%d')
            has_today_date = today in content
            
            # 記事数チェック
            article_count = content.count('article-item')
            
            # X投稿チェック  
            has_x_posts = 'x-item' in content or '注目のX投稿' in content
            
            print(f"  サイトアクセス: ✅")
            print(f"  今日の日付 ({today}): {'✅' if has_today_date else '❌'}")
            print(f"  記事数: {article_count} {'✅' if article_count >= 10 else '❌'}")
            print(f"  X投稿: {'✅' if has_x_posts else '❌'}")
            
            return has_today_date and article_count >= 10 and has_x_posts
        else:
            print(f"  アクセスエラー: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  サイトチェックエラー: {e}")
        return False

def check_google_sheets():
    """Google Sheets データ取得をチェック"""
    print("📊 Google Sheets チェック...")
    
    try:
        sheets_url = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
        response = requests.get(sheets_url, timeout=10)
        
        if response.status_code == 200:
            lines = response.text.split('\n')
            data_rows = len([line for line in lines if line.strip()])
            
            print(f"  アクセス: ✅")
            print(f"  データ行数: {data_rows} {'✅' if data_rows >= 10 else '❌'}")
            
            return data_rows >= 10
        else:
            print(f"  アクセスエラー: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"  Sheets チェックエラー: {e}")
        return False

def run_local_test():
    """ローカルでの生成テストを実行"""
    print("🧪 ローカル生成テスト...")
    
    try:
        # テスト実行
        result = subprocess.run([
            sys.executable, 
            'generate_reference_format_dashboard.py'
        ], capture_output=True, text=True, timeout=300)
        
        if result.returncode == 0:
            print("  生成テスト: ✅")
            
            # 生成されたファイルの確認
            html_files = [f for f in os.listdir('.') if f.startswith('reference_format_dashboard_') and f.endswith('.html')]
            if html_files:
                latest_file = max(html_files, key=lambda x: os.path.getmtime(x))
                file_size = os.path.getsize(latest_file)
                print(f"  生成ファイル: {latest_file} ({file_size:,} bytes)")
                
                # ファイル内容の簡単チェック
                with open(latest_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                has_content = len(content) > 50000
                has_articles = 'article-item' in content
                has_x_posts = 'x-item' in content
                
                print(f"  内容充実: {'✅' if has_content else '❌'}")
                print(f"  記事存在: {'✅' if has_articles else '❌'}")
                print(f"  X投稿存在: {'✅' if has_x_posts else '❌'}")
                
                return has_content and has_articles and has_x_posts
            else:
                print("  生成ファイルなし: ❌")
                return False
        else:
            print("  生成エラー: ❌")
            print(f"  エラー内容: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"  テストエラー: {e}")
        return False

def main():
    """メインチェック処理"""
    print("🏥 システムヘルスチェック開始")
    print("=" * 50)
    
    checks = [
        ("環境設定", check_environment),
        ("依存関係", check_dependencies), 
        ("GitHub Actions", check_github_actions),
        ("ライブサイト", check_live_site),
        ("Google Sheets", check_google_sheets),
        ("ローカル生成", run_local_test)
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n{name}:")
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"  予期しないエラー: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📋 チェック結果サマリー:")
    
    all_passed = True
    for name, result in results:
        status = "✅ 正常" if result else "❌ 要対応"
        print(f"  {name}: {status}")
        if not result:
            all_passed = False
    
    print(f"\n🎯 総合結果: {'✅ 全て正常' if all_passed else '❌ 問題あり'}")
    
    if not all_passed:
        print("\n🔧 対応方法:")
        print("  1. DAILY_UPDATE_GUIDE.md を参照")
        print("  2. 問題のある項目を個別に修正")
        print("  3. 必要に応じて手動更新を実行")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)