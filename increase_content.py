#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
表示件数を増やしてより多くの情報を掲載
"""
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

def update_display_limits():
    """表示件数を増やす設定に変更"""
    
    print("=" * 60)
    print("📈 表示件数を増加してより多くの情報を掲載")
    print("=" * 60)
    
    # 環境変数設定（大幅に増加）
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    # より多くの情報を表示
    os.environ['HOURS_LOOKBACK'] = '48'  # 48時間に拡張
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '20'  # 各カテゴリ20件に増加
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    
    # Google SheetsのURL
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    print(f"\n📅 現在時刻: {now.strftime('%Y-%m-%d %H:%M JST')}")
    print(f"📊 新しい設定:")
    print(f"   取得期間: 過去48時間（2日間）")
    print(f"   各カテゴリ最大表示: 20件")
    print(f"   予想合計表示: 最大60件")
    
    # generate_dashboard.pyも同じ設定に更新
    print(f"\n🔧 ダッシュボード設定も同期...")
    
    dashboard_path = Path('generate_dashboard.py')
    if dashboard_path.exists():
        content = dashboard_path.read_text(encoding='utf-8')
        
        # MAX_ITEMS_PER_CATEGORYを20に変更
        if "os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'" in content:
            content = content.replace(
                "os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'  # メインサイトと同じ件数に統一",
                "os.environ['MAX_ITEMS_PER_CATEGORY'] = '20'  # より多くの情報を分析"
            )
            dashboard_path.write_text(content, encoding='utf-8')
            print("✅ ダッシュボード設定を20件に更新")
    
    return True

def generate_expanded_site():
    """拡張設定でサイトを生成"""
    
    print(f"\n🚀 拡張設定でサイトを生成中...")
    
    try:
        # Git pull
        print("\n1️⃣ GitHubから最新を取得...")
        subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], check=True)
        
        # メインサイト生成
        print("\n2️⃣ メインサイトを生成（48時間、各20件）...")
        result = subprocess.run([sys.executable, 'build.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"❌ ビルドエラー: {result.stderr}")
            return False
        
        # 生成されたサイトの統計を表示
        if result.stdout:
            lines = result.stdout.split('\n')
            for line in lines:
                if any(keyword in line for keyword in ['items found', 'Found', 'Adding', 'Total items']):
                    print(f"   {line}")
        
        # index.htmlサイズ確認
        index_path = Path('index.html')
        if index_path.exists():
            size = index_path.stat().st_size
            print(f"\n📄 index.html サイズ: {size:,} bytes")
            
            # 内容確認
            with open(index_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            import re
            business_match = re.search(r'<div class="kpi-value">(\d+)件</div>\s*<div class="kpi-label">ビジネスニュース</div>', content)
            tools_match = re.search(r'<div class="kpi-value">(\d+)件</div>\s*<div class="kpi-label">ツールニュース</div>', content)
            posts_match = re.search(r'<div class="kpi-value">(\d+)件</div>\s*<div class="kpi-label">SNS/論文ポスト</div>', content)
            
            if business_match and tools_match and posts_match:
                business_count = int(business_match.group(1))
                tools_count = int(tools_match.group(1))
                posts_count = int(posts_match.group(1))
                total_count = business_count + tools_count + posts_count
                
                print(f"\n📊 生成されたコンテンツ:")
                print(f"   🏢 ビジネスニュース: {business_count}件")
                print(f"   ⚡ ツールニュース: {tools_count}件")
                print(f"   🧪 SNS/論文ポスト: {posts_count}件")
                print(f"   📈 合計表示: {total_count}件")
                
                if total_count > 24:  # 元の8*3=24件より多い場合
                    print(f"   ✅ 成功！{total_count - 24}件追加で表示されています")
        
        # ダッシュボード生成
        print("\n3️⃣ ダッシュボードを生成（拡張データ）...")
        subprocess.run([sys.executable, 'generate_dashboard.py'], check=False)
        
        return True
        
    except Exception as e:
        print(f"❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

def deploy_expanded_site():
    """拡張サイトをデプロイ"""
    
    print(f"\n📤 拡張サイトをGitHubにデプロイ...")
    
    try:
        JST = timezone(timedelta(hours=9))
        now = datetime.now(JST)
        
        # ファイルを追加
        files_to_add = [
            'index.html',
            'ai_news_dashboard.html', 
            'dashboard_data.json',
            'generate_dashboard.py'
        ]
        
        for file in files_to_add:
            if Path(file).exists():
                subprocess.run(['git', 'add', file], check=True)
        
        # コミット
        commit_msg = f"feat: Increase content display to 20 items per category (48h lookback) [{now.strftime('%Y-%m-%d %H:%M JST')}]"
        
        try:
            subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
            print("✅ 変更をコミットしました")
        except:
            print("ℹ️ 変更なし、またはコミット済み")
        
        # プッシュ
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        print("✅ GitHubにプッシュ完了")
        
        return True
        
    except Exception as e:
        print(f"❌ デプロイエラー: {e}")
        return False

def main():
    print("🚀 Daily AI News - コンテンツ拡張")
    
    # Step 1: 設定変更
    if not update_display_limits():
        return False
    
    # Step 2: サイト生成
    if not generate_expanded_site():
        return False
    
    # Step 3: デプロイ
    if not deploy_expanded_site():
        return False
    
    print("\n" + "=" * 60)
    print("✅ コンテンツ拡張完了!")
    print("=" * 60)
    
    print(f"\n🎉 新しい仕様:")
    print(f"  📊 取得期間: 過去48時間（2日間）")
    print(f"  📈 各カテゴリ: 最大20件表示")
    print(f"  📰 合計: 最大60件の記事")
    print(f"  💭 SNS投稿: より多くのX投稿を含む")
    
    print(f"\n🌐 サイトURL:")
    print(f"   メインサイト: https://awano27.github.io/daily-ai-news/")
    print(f"   ダッシュボード: https://awano27.github.io/daily-ai-news/ai_news_dashboard.html")
    
    print(f"\n💡 これでより豊富なAI情報をお楽しみいただけます！")
    
    return True

if __name__ == "__main__":
    sys.exit(0 if main() else 1)