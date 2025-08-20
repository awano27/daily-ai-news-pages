#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
X投稿取得のデバッグテスト
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

# build.pyをインポート
import build

def test_x_posts_gathering():
    """X投稿取得のテスト"""
    print("🔍 X投稿取得のデバッグテストを開始...")
    print("=" * 60)
    
    try:
        # X投稿を取得
        print(f"📱 X投稿CSV URL: {build.X_POSTS_CSV}")
        x_posts = build.gather_x_posts(build.X_POSTS_CSV)
        
        print(f"✅ X投稿取得結果: {len(x_posts)}件")
        
        if x_posts:
            print("\n📝 取得したX投稿の詳細:")
            for i, post in enumerate(x_posts[:10], 1):  # 最初の10件
                title = post.get('title', 'N/A')
                link = post.get('link', 'N/A')
                summary = post.get('_summary', 'N/A')[:100]
                source = post.get('_source', 'N/A')
                dt = post.get('_dt', 'N/A')
                
                print(f"\n  {i}. タイトル: {title}")
                print(f"     リンク: {link[:80]}...")
                print(f"     要約: {summary}...")
                print(f"     ソース: {source}")
                print(f"     日時: {dt}")
        else:
            print("⚠️ X投稿が取得されませんでした")
            
        return x_posts
        
    except Exception as e:
        print(f"❌ X投稿取得でエラー: {e}")
        import traceback
        traceback.print_exc()
        return []

def test_fallback_analysis(x_posts):
    """フォールバック分析のテスト"""
    if not x_posts:
        print("⚠️ X投稿がないためフォールバック分析をスキップ")
        return
        
    print("\n" + "=" * 60)
    print("🧪 フォールバック分析のテスト")
    
    try:
        # generate_comprehensive_dashboard.pyから関数をインポート
        from generate_comprehensive_dashboard import fallback_x_post_analysis
        
        # フォールバック分析を実行
        result = fallback_x_post_analysis(x_posts)
        
        print(f"✅ フォールバック分析結果:")
        print(f"   注目投稿: {len(result['influencer_posts'])}件")
        print(f"   技術ディスカッション: {len(result['tech_discussions'])}件")
        
        if result['influencer_posts']:
            print("\n📢 注目の投稿:")
            for i, post in enumerate(result['influencer_posts'], 1):
                print(f"   {i}. {post.get('username', 'N/A')} - 品質:{post.get('quality_score', 0)}")
                print(f"      内容: {post.get('summary', '')[:60]}...")
        else:
            print("⚠️ 注目の投稿が選別されませんでした")
            
        if result['tech_discussions']:
            print("\n💬 技術ディスカッション:")
            for i, post in enumerate(result['tech_discussions'], 1):
                print(f"   {i}. {post.get('username', 'N/A')} - 品質:{post.get('quality_score', 0)}")
                print(f"      内容: {post.get('summary', '')[:60]}...")
        else:
            print("⚠️ 技術ディスカッションが選別されませんでした")
            
        return result
        
    except Exception as e:
        print(f"❌ フォールバック分析でエラー: {e}")
        import traceback
        traceback.print_exc()
        return None

def test_csv_raw_access():
    """Google SheetsのCSV生データをテスト"""
    print("\n" + "=" * 60)
    print("🌐 Google Sheets CSVの直接アクセステスト")
    
    try:
        import requests
        
        url = build.X_POSTS_CSV
        print(f"📡 アクセス中: {url}")
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        content = response.text
        lines = content.strip().split('\n')
        
        print(f"✅ CSV取得成功: {len(lines)}行")
        print(f"📊 最初の3行:")
        for i, line in enumerate(lines[:3], 1):
            print(f"   {i}. {line[:100]}...")
            
        # 各行の列数チェック
        import csv
        import io
        reader = csv.reader(io.StringIO(content))
        row_count = 0
        valid_rows = 0
        
        for row in reader:
            row_count += 1
            if row_count == 1:  # ヘッダー
                print(f"📋 ヘッダー({len(row)}列): {row}")
                continue
            if len(row) >= 3:
                valid_rows += 1
                if valid_rows <= 3:  # 最初の3行のデータ
                    print(f"   データ行{valid_rows}({len(row)}列): {[col[:30] for col in row[:5]]}")
        
        print(f"📈 有効データ行: {valid_rows}行")
        
    except Exception as e:
        print(f"❌ CSV直接アクセスでエラー: {e}")
        import traceback
        traceback.print_exc()

def main():
    """メインテスト"""
    print("🚀 X投稿取得の総合デバッグテスト")
    
    # 1. CSV直接アクセステスト
    test_csv_raw_access()
    
    # 2. X投稿取得テスト  
    x_posts = test_x_posts_gathering()
    
    # 3. フォールバック分析テスト
    analysis_result = test_fallback_analysis(x_posts)
    
    print("\n" + "=" * 60)
    print("📋 テスト結果サマリー:")
    print(f"   X投稿取得: {'✅' if x_posts else '❌'} {len(x_posts) if x_posts else 0}件")
    if analysis_result:
        print(f"   注目投稿: {'✅' if analysis_result['influencer_posts'] else '❌'} {len(analysis_result['influencer_posts'])}件")
        print(f"   技術投稿: {'✅' if analysis_result['tech_discussions'] else '❌'} {len(analysis_result['tech_discussions'])}件")
    
    print("\n🎯 結論:")
    if analysis_result and analysis_result['influencer_posts']:
        print("✅ 注目の投稿が正常に取得・分析されました")
    else:
        print("❌ 注目の投稿の取得・分析に問題があります")
        print("💡 可能な原因:")
        print("   - Google SheetsのCSVデータが空/不正")
        print("   - 日付フィルターが厳しすぎる") 
        print("   - インフルエンサー判定が厳しすぎる")

if __name__ == "__main__":
    main()
    input("Press Enter to exit...")