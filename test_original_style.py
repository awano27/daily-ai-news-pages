#!/usr/bin/env python3
"""
元サイトスタイルダッシュボードテスト
"""

import sys
import os
import traceback

def test_original_style_dashboard():
    """元サイトスタイルダッシュボードをテスト実行"""
    try:
        print("🧪 元サイトスタイルダッシュボードテスト開始")
        
        # インポート
        sys.path.append(os.getcwd())
        from generate_original_style_dashboard import create_original_style_dashboard
        
        print("\n🎨 元サイトスタイルダッシュボード生成テスト...")
        html_content, articles_count, posts_count = create_original_style_dashboard()
        
        if html_content:
            # ファイル出力
            filename = "test_original_style_dashboard.html"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"\n✅ テスト成功！")
            print(f"📂 ファイル: {filename}")
            print(f"📊 掲載記事: {articles_count}件")
            print(f"📱 SNS投稿: {posts_count}件")
            print(f"📏 HTMLサイズ: {len(html_content):,}文字")
            
            # デザイン要素チェック
            design_checks = [
                ('KPIグリッド', '.kpi-grid' in html_content),
                ('カテゴリカード', '.category-card' in html_content),
                ('青基調デザイン', '#3b82f6' in html_content),
                ('エグゼクティブサマリー', 'エグゼクティブサマリー' in html_content),
                ('レスポンシブ', '@media' in html_content)
            ]
            
            print("\n🎨 デザイン要素チェック:")
            for name, check in design_checks:
                status = "✅" if check else "❌"
                print(f"  {status} {name}")
            
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
    test_original_style_dashboard()