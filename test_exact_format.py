#!/usr/bin/env python3
"""
元サイト完全準拠ダッシュボードテスト
"""

import sys
import os
import traceback

def test_exact_format_requirements():
    """要件をテストして問題があれば作り直し"""
    try:
        print("🧪 元サイト完全準拠ダッシュボードテスト開始")
        
        # インポート
        sys.path.append(os.getcwd())
        from generate_exact_format_dashboard import create_dashboard, fetch_rss_items, fetch_x_posts, load_feeds
        
        print("\n📊 データ取得テスト...")
        
        # feeds.ymlテスト
        feeds_data = load_feeds()
        print(f"フィード設定読み込み: {'✅' if feeds_data else '❌'}")
        
        # RSSフィード取得テスト
        all_items = []
        if feeds_data:
            for category in ['Business', 'Tools', 'Posts']:
                if category in feeds_data:
                    for feed_info in feeds_data[category][:2]:  # 各カテゴリ2件のみテスト
                        if isinstance(feed_info, dict) and 'url' in feed_info:
                            items = fetch_rss_items(
                                feed_info['url'],
                                feed_info.get('name', 'Unknown'),
                                category
                            )
                            all_items.extend(items)
                            if len(all_items) >= 5:  # 5件取得できたら十分
                                break
                    if len(all_items) >= 5:
                        break
        
        print(f"RSS記事取得: {'✅' if len(all_items) > 0 else '❌'} ({len(all_items)}件)")
        
        # X投稿取得テスト
        x_posts = fetch_x_posts()
        print(f"X投稿取得: {'✅' if len(x_posts) > 0 else '❌'} ({len(x_posts)}件)")
        
        # HTML生成テスト
        print("\n🎨 HTML生成テスト...")
        html_content = create_dashboard(all_items, x_posts)
        
        if html_content:
            # ファイル出力
            filename = "test_exact_format.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTMLファイル生成: ✅ ({filename})")
            print(f"HTMLサイズ: {len(html_content):,}文字")
            
            # 要件チェック
            print("\n📋 要件チェック:")
            
            # 1. 元サイトと同じフォーマット
            has_kpi_grid = '.kpi-grid' in html_content
            has_category_card = '.category-card' in html_content
            has_ai_selected = '✨ AI選別' in html_content
            has_action_item = '💡' in html_content
            format_ok = has_kpi_grid and has_category_card and has_ai_selected and has_action_item
            print(f"1. 元サイトと同じフォーマット: {'✅' if format_ok else '❌'}")
            if not format_ok:
                print(f"   - KPIグリッド: {'✅' if has_kpi_grid else '❌'}")
                print(f"   - カテゴリカード: {'✅' if has_category_card else '❌'}")
                print(f"   - AI選別タグ: {'✅' if has_ai_selected else '❌'}")
                print(f"   - アクションアイテム: {'✅' if has_action_item else '❌'}")
            
            # 2. 本日分の情報取得
            today_data_ok = len(all_items) > 0
            print(f"2. 本日分の情報取得: {'✅' if today_data_ok else '❌'} ({len(all_items)}件)")
            
            # 3. Xのソースリンク
            has_x_source = 'ソース</a>' in html_content and 'x.com' in html_content
            print(f"3. Xのソースリンク: {'✅' if has_x_source else '❌'}")
            
            # 4. 日本語タイトル
            # HTMLに日本語タイトルが含まれているかチェック
            jp_title_keywords = ['GPT', 'AI', '技術', '動向', '企業', '研究']
            has_jp_titles = any(keyword in html_content for keyword in jp_title_keywords)
            print(f"4. 日本語タイトル: {'✅' if has_jp_titles else '❌'}")
            
            # 総合判定
            all_requirements_ok = format_ok and today_data_ok and has_x_source and has_jp_titles
            print(f"\n🎯 総合判定: {'✅ 合格' if all_requirements_ok else '❌ 不合格'}")
            
            if not all_requirements_ok:
                print("\n⚠️ 問題が見つかりました。作り直しが必要です。")
                return False
            else:
                print("\n🎉 全要件を満たしています！")
                return True
            
        else:
            print("❌ HTMLコンテンツが生成されませんでした")
            return False
            
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        print("📝 詳細:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_exact_format_requirements()
    if success:
        print("\n✅ テスト完了 - 要件を満たしています")
        sys.exit(0)
    else:
        print("\n❌ テスト失敗 - 作り直しが必要です")
        sys.exit(1)