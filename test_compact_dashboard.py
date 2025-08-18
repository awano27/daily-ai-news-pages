#!/usr/bin/env python3
"""
コンパクトダッシュボードテスト
"""

import sys
import os
sys.path.append(os.getcwd())

def test_compact_dashboard():
    """コンパクトダッシュボードをテスト"""
    try:
        # ファイルを直接インポートしてテスト
        from generate_compact_full_dashboard import create_compact_full_dashboard
        
        print("🧪 コンパクトダッシュボードテスト開始")
        
        # ダッシュボード生成
        html_content, articles_count, posts_count = create_compact_full_dashboard()
        
        if html_content:
            # テスト用ファイル名
            test_filename = "test_compact_dashboard.html"
            
            with open(test_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            print(f"✅ テスト成功: {test_filename}")
            print(f"📊 検証済み記事: {articles_count}件")
            print(f"📱 厳選投稿: {posts_count}件")
            
            return True
        else:
            print("❌ HTMLコンテンツが生成されませんでした")
            return False
            
    except Exception as e:
        print(f"❌ テストエラー: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_compact_dashboard()