#!/usr/bin/env python3
"""
改良版コンパクトダッシュボードテスト
"""

import sys
import os
import traceback

def test_improved_dashboard():
    """改良版コンパクトダッシュボードをテスト実行"""
    try:
        print("🧪 改良版ダッシュボードテスト開始")
        
        # インポート
        sys.path.append(os.getcwd())
        from generate_compact_full_dashboard import (
            extract_articles_from_analysis,
            fetch_x_posts_from_sheets, 
            create_compact_full_dashboard
        )
        
        # 各コンポーネントをテスト
        print("\n📰 記事抽出テスト...")
        articles = extract_articles_from_analysis()
        print(f"記事抽出結果: {len(articles)}件")
        
        print("\n📱 X投稿取得テスト...")
        x_posts = fetch_x_posts_from_sheets()
        print(f"X投稿取得結果: {len(x_posts)}件")
        
        print("\n🚀 フルダッシュボード生成テスト...")
        html_content, articles_count, posts_count = create_compact_full_dashboard()
        
        if html_content:
            # ファイル出力
            filename = "test_improved_dashboard.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n✅ テスト成功！")
            print(f"📂 ファイル: {filename}")
            print(f"📊 検証済み記事: {articles_count}件")
            print(f"📱 厳選投稿: {posts_count}件")
            print(f"📏 HTMLサイズ: {len(html_content):,}文字")
            
            # 品質チェック
            if articles_count >= 5:
                print("✅ 記事数OK")
            else:
                print("⚠️ 記事数少なめ")
                
            if posts_count >= 3:
                print("✅ 投稿数OK")
            else:
                print("⚠️ 投稿数少なめ")
            
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
    test_improved_dashboard()