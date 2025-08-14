#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
統合アップデート：ダッシュボードとメインサイトを連携
8/14以降のSNS投稿のみフィルタリング
"""
import os
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path
import re

def update_build_py_date_filter():
    """build.pyの日付フィルタリングを8/14以降に修正"""
    print("\n📅 日付フィルタリングを8/14以降に設定...")
    
    build_path = Path('build.py')
    content = build_path.read_text(encoding='utf-8')
    
    # 8/14 00:00 JSTを基準日時として設定
    aug14_check = """            # 8/14以降の投稿のみ含める
            aug14_jst = datetime(2025, 8, 14, 0, 0, 0, tzinfo=JST)
            if post_date >= aug14_jst and (NOW - post_date) <= timedelta(hours=HOURS_LOOKBACK):"""
    
    # 既存の日付チェックを置換
    pattern = r'# 24時間以内の投稿のみ含める.*?\n\s+if \(NOW - post_date\) <= timedelta\(hours=HOURS_LOOKBACK\):'
    
    if re.search(pattern, content, re.DOTALL):
        content = re.sub(pattern, aug14_check, content, flags=re.DOTALL)
        build_path.write_text(content, encoding='utf-8')
        print("✅ 日付フィルタリングを8/14以降に更新しました")
    else:
        # 別の方法で探す
        if '            if (NOW - post_date) <= timedelta(hours=HOURS_LOOKBACK):' in content:
            content = content.replace(
                '            # 24時間以内の投稿のみ含める（他のニュースと同じフィルタリング）\n            if (NOW - post_date) <= timedelta(hours=HOURS_LOOKBACK):',
                aug14_check
            )
            build_path.write_text(content, encoding='utf-8')
            print("✅ 日付フィルタリングを8/14以降に更新しました")

def add_navigation_to_main_site():
    """メインサイトにダッシュボードへのナビゲーションを追加"""
    print("\n🔗 メインサイトにナビゲーションを追加...")
    
    build_path = Path('build.py')
    content = build_path.read_text(encoding='utf-8')
    
    # ヘッダーにナビゲーションを追加
    nav_html = """  <header class="site-header">
    <div class="brand">📰 Daily AI News</div>
    <nav class="nav-links">
      <a href="ai_news_dashboard.html" class="nav-link">📊 ダッシュボード</a>
    </nav>
    <div class="updated">最終更新：{updated_full}</div>
  </header>"""
    
    if '<nav class="nav-links">' not in content:
        content = content.replace(
            """  <header class="site-header">
    <div class="brand">📰 Daily AI News</div>
    <div class="updated">最終更新：{updated_full}</div>
  </header>""",
            nav_html
        )
        build_path.write_text(content, encoding='utf-8')
        print("✅ メインサイトにナビゲーション追加")

def add_navigation_to_dashboard():
    """ダッシュボードにメインサイトへのナビゲーションを追加"""
    print("\n🔗 ダッシュボードにナビゲーションを追加...")
    
    dashboard_path = Path('generate_dashboard.py')
    content = dashboard_path.read_text(encoding='utf-8')
    
    # ヘッダーHTMLを更新
    new_header = """        <header>
            <div class="header-content">
                <h1>📊 AIニュース ダッシュボード</h1>
                <nav style="display: flex; gap: 15px; align-items: center;">
                    <a href="index.html" style="color: white; text-decoration: none; padding: 8px 16px; background: rgba(255,255,255,0.2); border-radius: 8px; transition: background 0.3s;">
                        📰 メインサイトへ
                    </a>
                    <span style="color: #e2e8f0;">{date}</span>
                </nav>
            </div>
        </header>"""
    
    # 既存のヘッダーを置換
    if '<a href="index.html"' not in content:
        pattern = r'<header>.*?</header>'
        replacement = new_header
        content = re.sub(pattern, replacement, content, flags=re.DOTALL)
        dashboard_path.write_text(content, encoding='utf-8')
        print("✅ ダッシュボードにナビゲーション追加")

def update_styles():
    """style.cssにナビゲーションスタイルを追加"""
    print("\n🎨 スタイルシートを更新...")
    
    style_path = Path('style.css')
    if not style_path.exists():
        return
    
    content = style_path.read_text(encoding='utf-8')
    
    nav_styles = """
/* Navigation */
.nav-links {
  display: flex;
  gap: 15px;
  align-items: center;
}
.nav-link {
  color: white;
  text-decoration: none;
  padding: 8px 16px;
  background: rgba(255,255,255,0.1);
  border-radius: 8px;
  transition: all 0.3s;
}
.nav-link:hover {
  background: rgba(255,255,255,0.2);
  transform: translateY(-2px);
}
.site-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 15px;
}
"""
    
    if '.nav-links' not in content:
        content += nav_styles
        style_path.write_text(content, encoding='utf-8')
        print("✅ スタイルシート更新完了")

def main():
    print("=" * 60)
    print("🚀 統合アップデート開始")
    print("=" * 60)
    
    # 環境変数設定
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    
    os.environ['HOURS_LOOKBACK'] = '24'
    os.environ['MAX_ITEMS_PER_CATEGORY'] = '8'
    os.environ['TRANSLATE_TO_JA'] = '1'
    os.environ['TRANSLATE_ENGINE'] = 'google'
    
    # Google SheetsのURL
    GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0"
    os.environ['X_POSTS_CSV'] = GOOGLE_SHEETS_URL
    
    print(f"\n📅 現在時刻: {now.strftime('%Y-%m-%d %H:%M JST')}")
    print(f"📊 8/14以降のSNS投稿のみ表示")
    
    try:
        # Step 1: 最新を取得
        print("\n1️⃣ GitHubから最新を取得...")
        subprocess.run(['git', 'pull', 'origin', 'main', '--no-edit'], check=True)
        
        # Step 2: 日付フィルタリングを修正
        update_build_py_date_filter()
        
        # Step 3: ナビゲーションを追加
        add_navigation_to_main_site()
        add_navigation_to_dashboard()
        update_styles()
        
        # Step 4: メインサイト生成
        print("\n2️⃣ メインサイトを生成...")
        result = subprocess.run([sys.executable, 'build.py'], 
                              capture_output=True, text=True, encoding='utf-8')
        
        if result.returncode != 0:
            print(f"❌ ビルドエラー: {result.stderr}")
            return False
        
        # Step 5: ダッシュボード生成
        print("\n3️⃣ ダッシュボードを生成...")
        subprocess.run([sys.executable, 'run_dashboard_direct.py'], check=False)
        
        # Step 6: Git コミット
        print("\n4️⃣ 変更をコミット...")
        subprocess.run(['git', 'add', '.'], check=True)
        
        commit_msg = f"feat: Integrated dashboard with navigation, filtered SNS to Aug 14+ [{now.strftime('%Y-%m-%d %H:%M JST')}]"
        subprocess.run(['git', 'commit', '-m', commit_msg], check=True)
        
        # Step 7: プッシュ
        print("\n5️⃣ GitHubへプッシュ...")
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        
        print("\n" + "=" * 60)
        print("✅ 統合アップデート完了!")
        print("=" * 60)
        
        print("\n🎉 更新内容:")
        print("  ✓ ダッシュボードとメインサイトを相互リンクで接続")
        print("  ✓ SNS投稿を8/14以降のみに限定")
        print("  ✓ ナビゲーションメニューを追加")
        
        print(f"\n📰 メインサイト:")
        print(f"   https://awano27.github.io/daily-ai-news/")
        print(f"\n📊 ダッシュボード:")
        print(f"   https://awano27.github.io/daily-ai-news/ai_news_dashboard.html")
        
        return True
        
    except Exception as e:
        print(f"\n❌ エラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    sys.exit(0 if main() else 1)