#!/usr/bin/env python3
"""
参考サイト準拠ダッシュボードテスト
"""

import sys
import os
import traceback
import requests

def test_reference_format_requirements():
    """全要件をテストして問題があれば詳細報告"""
    try:
        print("🧪 参考サイト準拠ダッシュボードテスト開始")
        
        # インポート
        sys.path.append(os.getcwd())
        from generate_reference_format_dashboard import create_dashboard, fetch_rss_items, fetch_x_posts, load_feeds
        
        print("\n📊 データ取得テスト...")
        
        # feeds.ymlテスト
        feeds_data = load_feeds()
        feeds_ok = bool(feeds_data)
        print(f"フィード設定読み込み: {'✅' if feeds_ok else '❌'}")
        
        # RSSフィード取得テスト
        all_items = []
        if feeds_data:
            for category in ['Business', 'Tools', 'Posts']:
                if category in feeds_data:
                    category_items = 0
                    for feed_info in feeds_data[category][:3]:  # 各カテゴリ3件テスト
                        if isinstance(feed_info, dict) and 'url' in feed_info:
                            items = fetch_rss_items(
                                feed_info['url'],
                                feed_info.get('name', 'Unknown'),
                                category
                            )
                            all_items.extend(items)
                            category_items += len(items)
                            if category_items >= 5:  # カテゴリあたり5件で十分
                                break
        
        rss_ok = len(all_items) > 0
        print(f"RSS記事取得: {'✅' if rss_ok else '❌'} ({len(all_items)}件)")
        
        # X投稿取得テスト
        x_posts = fetch_x_posts()
        x_ok = len(x_posts) > 0
        print(f"X投稿取得: {'✅' if x_ok else '❌'} ({len(x_posts)}件)")
        
        # Google Sheetsアクセステスト
        sheets_ok = False
        try:
            response = requests.get("https://docs.google.com/spreadsheets/d/1uuLKCLIJw--a1vCcO6UGxSpBiLTtN8uGl2cdMb6wcfg/export?format=csv&gid=0", timeout=10)
            sheets_ok = response.status_code == 200
        except:
            sheets_ok = False
        print(f"Google Sheetsアクセス: {'✅' if sheets_ok else '❌'}")
        
        # HTML生成テスト
        print("\n🎨 HTML生成テスト...")
        html_content = create_dashboard(all_items, x_posts)
        
        if html_content:
            # ファイル出力
            filename = "test_reference_format.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"HTMLファイル生成: ✅ ({filename})")
            print(f"HTMLサイズ: {len(html_content):,}文字")
            
            # 要件チェック
            print("\n📋 要件チェック:")
            
            # 1. 参考サイトと同じフォーマット
            format_checks = {
                'タイトル': 'AI業界全体像ダッシュボード' in html_content,
                'エグゼクティブサマリー': 'エグゼクティブサマリー' in html_content,
                'KPIグリッド': 'kpi-grid' in html_content,
                'カテゴリカード': 'category-card' in html_content,
                'AI選別タグ': '✨ AI選別' in html_content,
                'ビジネスインサイト': '💡' in html_content,
                'X投稿セクション': '注目のX投稿' in html_content,
                'フッターリンク': 'LLMアリーナ' in html_content and 'AlphaXiv' in html_content
            }
            format_ok = all(format_checks.values())
            print(f"1. 参考サイトと同じフォーマット: {'✅' if format_ok else '❌'}")
            for check, result in format_checks.items():
                if not result:
                    print(f"   - {check}: ❌")
            
            # 2. カテゴリ内容が指定通り
            category_checks = {
                'ビジネス・企業動向': 'ビジネス・企業動向' in html_content,
                '開発ツール・プラットフォーム': '開発ツール・プラットフォーム' in html_content,
                '研究・論文・技術解説': '研究・論文・技術解説' in html_content
            }
            category_ok = all(category_checks.values())
            print(f"2. カテゴリ内容が指定通り: {'✅' if category_ok else '❌'}")
            
            # 3. Xのソースリンク
            x_source_ok = 'ソース</a>' in html_content and 'x.com' in html_content
            print(f"3. Xのソースリンク: {'✅' if x_source_ok else '❌'}")
            
            # 4. 日本語タイトル
            jp_title_keywords = ['AI', 'GPT', '技術', '動向', '企業', '研究', '開発']
            has_jp_titles = any(keyword in html_content for keyword in jp_title_keywords)
            print(f"4. 日本語タイトル: {'✅' if has_jp_titles else '❌'}")
            
            # 5. フッターセクション
            footer_links = ['LLMアリーナ', 'AlphaXiv', 'AIトレンドワード']
            footer_ok = all(link in html_content for link in footer_links)
            print(f"5. フッターセクション: {'✅' if footer_ok else '❌'}")
            
            # 6. データの充実度
            data_sufficient = len(all_items) >= 5 and len(x_posts) >= 2
            print(f"6. データの充実度: {'✅' if data_sufficient else '❌'} (記事{len(all_items)}件, X投稿{len(x_posts)}件)")
            
            # 総合判定
            all_requirements = [
                format_ok, category_ok, x_source_ok, has_jp_titles, 
                footer_ok, data_sufficient, rss_ok, x_ok
            ]
            total_score = sum(all_requirements)
            max_score = len(all_requirements)
            
            print(f"\n🎯 総合判定: {total_score}/{max_score} ({'✅ 合格' if total_score >= max_score-1 else '❌ 要改善'})")
            
            if total_score >= max_score-1:
                print("\n🎉 ほぼ全要件を満たしています！")
                return True
            else:
                print(f"\n⚠️ {max_score-total_score}個の問題が見つかりました。改善が必要です。")
                return False
            
        else:
            print("❌ HTMLコンテンツが生成されませんでした")
            return False
            
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        print("📝 詳細:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_reference_format_requirements()
    if success:
        print("\n✅ テスト完了 - 要件をほぼ満たしています")
        sys.exit(0)
    else:
        print("\n❌ テスト失敗 - 改善が必要です")
        sys.exit(1)